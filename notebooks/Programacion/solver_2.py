import cupy as cp
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import time

def extraer_datos_yahoo(stocks):
  '''
  Funcion para extraer datos de los portafolios de yahoo finance de 2015-01-01 a 2020-04-30
  '''
  df_c = yf.download(stocks, start='2015-01-01', end='2020-04-30').Close
  base = df_c['AAPL'].dropna().to_frame()
  for i in range(0,50):
      base = base.join(df_c.iloc[:,i].to_frame(), lsuffix='_caller', rsuffix='_other')
  base = base.drop(columns=['AAPL_caller'])
  base = base.rename(columns={"AAPL_other": "AAPL"})
  base = base.fillna(method='ffill')
  base = base.fillna(method='bfill')
  return base


def calcular_rendimiento_vector(x):
  """
  Función para calcular el rendimiento esperado

  params:
      x     vector de precios
  
  return:
      r_est rendimiento esperado diario
  """

  # Definimos precios iniciales y finales como arreglo alojado en la gpu
  x_o = cp.asarray(x)
  x_f = x_o[1:]

  # Calculamos los rendimientos diarios
  r = cp.log(x_f/x_o[:-1])

  return r

def calcular_rendimiento(X):
  """
  Función para calcular el rendimiento esperado para un conjunto de acciones

  params:
      X      matriz mxn de precios, donde:
             m es el número de observaciones y
             n el número de acciones
  
  return:
      r_est rvector de rendimientos esperados
  """
  m,n = X.shape
  r_est = cp.zeros(n)
  X = cp.asarray(X)

  for i in range(n):
    r_est[i] = calcular_rendimiento_vector(X[:,i]).mean()

  return 264*r_est

def calcular_varianza(X):

  """
  Función para calcular el la matriz de varianzas y covarianzas para un conjunto de acciones

  params:
      X      matriz mxn de precios, donde:
             m es el número de observaciones y
               n el número de acciones
  
  return:
      S  matriz de varianzas y covarianzas
  """
  m,n=X.shape
  X = cp.asarray(X)

  X_m = cp.zeros((m-1,n))

  for i in range(n):
    X_m[:,i] = calcular_rendimiento_vector(X[:,i]) - calcular_rendimiento_vector(X[:,i]).mean()

  S = (cp.transpose(X_m)@X_m)/(m-2)

  return S


def formar_vectores(mu, Sigma):
  '''
  Calcula las cantidades u = \Sigma^{-1}  \mu y v := \Sigma^{-1} \cdot 1 del problema de Markowitz

  Args:
    mu (cupy array, vector): valores medios esperados de activos (dimension n)
    Sigma (cupy array, matriz): matriz de covarianzas asociada a activos (dimension n x n)

  Return:
    u (cupy array, escalar): vector dado por \cdot Sigma^-1 \cdot mu (dimension n)
    v (cupy array, escalar): vector dado por Sigma^-1 \cdot 1 (dimension n)
  '''

  # Vector auxiliar con entradas igual a 1
  n = Sigma.shape[0]
  ones_vector = cp.ones(n)

  # Formamos vector \cdot Sigma^-1 mu y Sigm^-1 1
  # Nota: 
  #   1) u= Sigma^-1 \cdot mu se obtiene resolviendo  Sigma u = mu
  #   2) v= Sigma^-1 \cdot 1 se obtiene resolviendo  Sigma v = 1

  # Obtiene vectores de interes
  u = cp.linalg.solve(Sigma, mu)
  u = u.transpose() # correcion de expresion de array
  v = cp.linalg.solve(Sigma, ones_vector)

  return u , v


def formar_abc(mu, Sigma):
  '''
  Calcula las cantidades A, B y C del diagrama de flujo del problema de Markowitz

  Args:
    mu (cupy array, vector): valores medios esperados de activos (dimension n)
    Sigma (cupy array, matriz): matriz de covarianzas asociada a activos (dimension n x n)

  Return:
    A (cupy array, escalar): escalar dado por mu^t \cdot Sigma^-1 \cdot mu
    B (cupy array, escalar): escalar dado por 1^t \cdot Sigma^-1 \cdot 1
    C (cupy array, escalar): escalar dado por 1^t \cdot Sigma^-1 \cdot mu
  '''

  # Vector auxiliar con entradas igual a 1
  n = Sigma.shape[0]
  ones_vector = cp.ones(n)

  # Formamos vector \cdot Sigma^-1 mu y Sigm^-1 1
  # Nota: 
  #   1) u= Sigma^-1 \cdot mu se obtiene resolviendo  Sigma u = mu
  #   2) v= Sigma^-1 \cdot 1 se obtiene resolviendo  Sigma v = 1

  u, v = formar_vectores(mu, Sigma)

  # Obtiene escalares de interes
  A = mu.transpose()@u
  B = ones_vector.transpose()@v
  C = ones_vector.transpose()@u

  return A, B, C

def delta(A,B,C):
  '''
  Calcula las cantidad Delta = AB-C^2 del diagrama de flujo del problema de Markowitz

  Args:
    A (cupy array, escalar): escalar dado por mu^t \cdot Sigma^-1 \cdot mu
    B (cupy array, escalar): escalar dado por 1^t \cdot Sigma^-1 \cdot 1
    C (cupy array, escalar): escalar dado por 1^t \cdot Sigma^-1 \cdot mu

  Return:
    Delta (cupy array, escalar): escalar dado \mu^t \cdot \Sigma^{-1} \cdot \mu
  '''
  Delta = A*B-C**2

  return Delta

def formar_omegas(r, mu, Sigma):
  '''
  Calcula las cantidades w_o y w_ del problema de Markowitz

  Args:
    mu (cupy array, vector): valores medios esperados de activos (dimension n)
    Sigma (cupy array, matriz): matriz de covarianzas asociada a activos (dimension n x n)

  Return:
    w_0 (cupy array, matriz): matriz dada por 
          w_0 = \frac{1}{\Delta} (B \Sigma^{-1} \hat{\mu}- C\Sigma^{-1} 1) 
    w_1 (cupy array, vector): vector dado por 
         w_1 = \frac{1}{\Delta} (C \Sigma^{-1} \hat{\mu}- A\Sigma^{-1} 1)
  '''
  # Obtenemos u = Sigma^{-1} \hat{\mu}, v = \Sigma^{-1} 1
  u, v = formar_vectores(mu, Sigma)
  # Escalares relevantes
  A, B, C = formar_abc(mu, Sigma)
  Delta = delta(A,B,C)
  # Formamos w_0 y w_1
  w_0 = (1/Delta)*(r*B-C)
  w_1 = (1/Delta)*(A-C*r)

  return w_0, w_1


def markowitz(r, mu, Sigma):
  '''
  Calcula las cantidades w_o y w_ del problema de Markowitz

  Args:
    mu (cupy array, vector): valores medios esperados de activos (dimension n)
    Sigma (cupy array, matriz): matriz de covarianzas asociada a activos (dimension n x n)

  Return:
    w_0 (cupy array, matriz): matriz dada por 
          w_0 = \frac{1}{\Delta} (B \Sigma^{-1} \hat{\mu}- C\Sigma^{-1} 1) 
    w_1 (cupy array, vector): vector dado por 
         w_1 = \frac{1}{\Delta} (C \Sigma^{-1} \hat{\mu}- A\Sigma^{-1} 1)
  '''
  # Obtenemos u = Sigma^{-1} \hat{\mu}, v = \Sigma^{-1} 1
  u, v = formar_vectores(mu, Sigma)

  # Formamos w_0 y w_1
  w_0, w_1 = formar_omegas(r, mu, Sigma)

  return w_0*u+w_1*v

