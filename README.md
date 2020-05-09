# Implementación del modelo Markowitz a cómputo en paralelo



## Organización

Para el desarrollo del proyecto, los integrantes se dividieron principalmente en dos grupos; el **Grupo de programación** encargado de la implementación de los métodos y algoritmos; y el **Grupo de revisión** encargado de probar y reportar los métodos del primer grupo. Ambos grupos fueron coordinados por el **Project Manager** con ayuda de un **Asistente**.

La división anterior se puede resumir mediante la siguiente tabla:

| #    | Rol                                   | Persona      |
| ---- | --------------------------------------| ------------ |
| 1    | Grupo de programación                 | Bruno        |
| 2    | Grupo de programación                 | Itzel        |
| 3    | Grupo de programación                 | César        |
| 4    | Grupo de revisión                     | León         |
| 5    | Grupo de revisión/Asistente de PM     | Danahi       |
| 6    | Project Manager                       | Yalidt       |

## Descripción del problema

Se busca desallorar un algoritmo(en paralelo) para encontrar la proporción de dinero que cierto inversionista debe invertir en un conjunto de acciones. A estas proporciones las denotaremos **wi**, que finalmente es un vector de tamaño nx1, donde n es el número de acciones a analizar. Este algoritmo se basa en el modelo de Markovitz, que de acuerdo a una frontera de posibilidades de alocación se busca la parte superior de esa frontera, ya que justamente en esa parte los rendimientos son positivos.

![alt-text](https://github.com/czammar/MNO_finalproject/blob/master/images/frontera_eficiente.png)

La finalidad del algoritmo será encontrar el portafolio de **mínima varianza**, el cual es para aquellos inversionistas que son aversos al riesgo.

## Metodología
1) Obtener base de datos de precios históricos de 50 empresas que coticen en bolsa, se obtendrá un conjunto de empresas por cada industria en el mercado y se seleccionaran las que tengan mayor participación en el mercado. Esta información la obtendremos de Yahoo Finance y los precios serán diarios **Closed Price**(al cierre de la bolsa)de los últimos 5 años para hacer el análisis. Se realizará un proceso de extracción de la base de datos definida en la etapa 1 del diagrama de flujo.

2) Se calcularán los rendimientos esperados de cada una de las empresas con los precios de acuerdo a la siguiente fórmula:
![r=log\tfrac{P_t}{P_{t-1}}](https://render.githubusercontent.com/render/math?math=R%3Dlog%5Ctfrac%7BPt%7D%7BPt-1%7D)<br />

3) Determinar el vector de pesos ![$W$](https://render.githubusercontent.com/render/math?math=%24W%24), se puede asignar aleatoriamente entre ![$(0,1)$](https://render.githubusercontent.com/render/math?math=%24(0%2C1)%24) con la condición de que la suma de la entradas sea igual a 1.<br />
4) Obtener el rendimiento esperado del portafolio ![r=w^t \mu](https://render.githubusercontent.com/render/math?math=r%3Dw%5Et%20%5Cmu)

5) Obtener la matriz de varianzas y covarianzas de los rendimientos de las acciones ![\Sigma](https://render.githubusercontent.com/render/math?math=%5CSigma)<br />

6) Definir la función a optimizar  ![w^{*}=w_{0}\cdot (\Sigma^{-1}\cdot \mu)+w_{1}\cdot (\Sigma^{-1}\cdot 1)](https://render.githubusercontent.com/render/math?math=w%5E%7B*%7D%3Dw_%7B0%7D%5Ccdot%20(%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu)%2Bw_%7B1%7D%5Ccdot%20(%5CSigma%5E%7B-1%7D%5Ccdot%201))<br />
7) Establecer las restricciones del modelo<br />
![restricciones : w^t \mu=r](https://render.githubusercontent.com/render/math?math=restricciones%20%3A%20w%5Et%20%5Cmu%3DR)<br />
![W^te=1](https://render.githubusercontent.com/render/math?math=W%5Ete%3D1)<br />

* Donde los vectores auxiliares son los siguientes:<br />
![w_{0}=\frac{1}{\Delta }(\hat{r}\cdot B-C)](https://render.githubusercontent.com/render/math?math=w_%7B0%7D%3D%5Cfrac%7B1%7D%7B%5CDelta%20%7D(%5Chat%7Br%7D%5Ccdot%20B-C))<br />
![w_{1}=\frac{1}{\Delta }(A-C\cdot \hat{r})](https://render.githubusercontent.com/render/math?math=w_%7B1%7D%3D%5Cfrac%7B1%7D%7B%5CDelta%20%7D(A-C%5Ccdot%20%5Chat%7Br%7D))<br />
Donde :<br />
![\Delta =A\cdot B-C^2](https://render.githubusercontent.com/render/math?math=%5CDelta%20%3DA%5Ccdot%20B-C%5E2)<br />
![A=\mu^t\cdot \Sigma^{-1}\cdot \mu](https://render.githubusercontent.com/render/math?math=A%3D%5Cmu%5Et%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu)<br />
![B=\1^t\cdot \Sigma^{-1}\cdot \1](https://render.githubusercontent.com/render/math?math=B%3D%5C1%5Et%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%20%5C1)<br />
![C=\1^t\cdot \Sigma^{-1}\cdot \mu](https://render.githubusercontent.com/render/math?math=C%3D%5C1%5Et%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu)

## Diagrama de Flujo

En este sentido, para llevar a cambo la implementación descrito en la sección precedente, se propuso descomponer en una serie de etapas que facilitan la implementación colaborativa y el emsable del código.

* **Etapa I:** se refiere a la obtención de los datos de portafolios a analizar, junto con su limpieza y transformación para posteriores análisis,
* **Etapa II:** corresponde a la estimación de tres elementos base del modelo, a saber el retorno esperado de los activos, el valor medio esperado de los mismo junto con la matriz de covarianzas asociada.
* **Etapa III:** relativa a la aproximación de la composición de los pesos que permite integrar el portafolio de inversión que posee **mínima varianza**, el cual es para aquellos inversionistas que son aversos al riesgo.

El proceso comentado, se resumen a continuación:



![Diagrama de flujo](./images/diagrama_flujo.png)

## Desarrollo

Evaluar distintos portafolios, es decir distintos pesos **w**, usando la media y varianza del protafolio: <img src="https://render.githubusercontent.com/render/math?math=(\mu, \Sigma)"> para 
- Retornos esperados  <img src="https://render.githubusercontent.com/render/math?math=\mu"> más grandes 
- Varianza  <img src="https://render.githubusercontent.com/render/math?math=\Sigma"> más pequeña

**Problema:** Minimización del riesgo: Dado un objetivo de retorno **r**, elegir los pesos del portafolio **w** que:

Minimice <img src="https://render.githubusercontent.com/render/math?math=\frac{1}{2}w^T\Sigma w">

Sujeto a: 
- <img src="https://render.githubusercontent.com/render/math?math=w^T\mu=r">
- <img src="https://render.githubusercontent.com/render/math?math=w^T1_{n}=1">

**Solución:** Aplicar el método de multiplicadores de Lagrange al problema de optimización convexa (minimización) sujeto a restricciones lineales

- Definir Lagrangiano

<img src="https://render.githubusercontent.com/render/math?math=L(w,\lambda_{1}, \lambda_{2}) = \frac{1}{2}w^T\Sigma w + \lambda_{1}(r-w^T\mu) +\lambda_{2}(1-w^T1_{n})">

- Derivar las condiciones de primer orden

<img src="https://render.githubusercontent.com/render/math?math=\frac{\delta L}{\delta w} = 0_{n} = \Sigma w - \lambda_{1}\mu - \lambda_{2}1_{n}">

<img src="https://render.githubusercontent.com/render/math?math=\frac{\delta L}{\delta \lambda_{1}} = 0 = r -w^T\mu">

<img src="https://render.githubusercontent.com/render/math?math=\frac{\delta L}{\delta \lambda{2}} = 0 = 1 -w^T1_{n}">

- Resolver para **w** en terminos de <img src="https://render.githubusercontent.com/render/math?math=\lambda_{1}, \lambda_{2}">

<img src="https://render.githubusercontent.com/render/math?math=w_{0} = \lambda_{1}\Sigma^{-1}1_{n}">

- Resolver para <img src="https://render.githubusercontent.com/render/math?math=\lambda_{1}, \lambda_{2}"> sustituyendo para **w**
<img src="https://render.githubusercontent.com/render/math?math=r = w^T_{0}\mu = \lambda_{1}(\mu^T\Sigma^{-1}\mu) \oplus \lambda_{2}(\mu^T\Sigma^{-1}1_{n}))">

<img src="https://render.githubusercontent.com/render/math?math=1 = w^T 1_{n} = \lambda_{1}(\mu^T\Sigma^{-1}1_{n}) \oplus \lambda_{2}(1^T_{n}\Sigma^{-1}1_{n})">

<img src="https://render.githubusercontent.com/render/math?math=\Rightarrow">


![Matriz](./images/matriz.png)


<img src="https://render.githubusercontent.com/render/math?math=a =(\mu\Sigma^{-1}), b =(\mu\Sigma_{-1}1_{n}) , c = (1^T_{n}\Sigma^{-1}1_{n})">


## Referencias 

Bodie, Z., Kane, A., & Marcus, A. J. (2011). Investments. New York: McGraw-Hill/Irwin.<br />
https://www.niceideas.ch/airxcell_doc/doc/userGuide/portfolio_optimTheory.html<br />




