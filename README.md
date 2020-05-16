# Implementación del modelo Markowitz

## 1. Índice

+ Descripcion del problema
+ Consideraciones metodológicas:
  + Portafolio de activos y sus rendimiento,
  + Solver basado en multiplicadores de Lagrage,
  + Solver basado en método de Newton,
+ Estructura del repositorio,
+ Instrucciones para AWS y Docker
+ Reporte de Resultados
+ Reportes de Equipos:
  + Programación
  + Revisión


[WIP: Añadir índice al repositorios y referencias cruzadas]


## 2. Descripción del problema

En el contexto de finanzas, un problema relevante es definir estrategias que permitan a los inversionista diversificar sus inversiones con el objetivo de minimizar el riesgo de su capital. Típicamente, esto corresponde con que un inversionista tiene interés en un conjunto definido de activos, denominado *portafolio*, sobre el que debe tomar una decisión sobre como adquirir o vender acciones con la idea obtener un determinado rendimiento ![r > 0](https://render.githubusercontent.com/render/math?math=r%20%3E%200). Sin embargo, es deseable que la elección considere reducir el riesgo inherente al mercado de inversiones.

En términos matemáticos y considerando la consabida teoría financiera, lo anterior equivale a una formulación denominada *Modelo de Markowitz*, propuesta por el economista Harry Markowitz, a través de la cual se trata de minimizar la norma inducida por la matriz de covarianza ![\Sigma](https://render.githubusercontent.com/render/math?math=%5CSigma) de los activos con referencia a los propociones de como se debe elegir las acciones que integranun portafolio específico (pesos), sujeto a que se obtenga un rendimiento acorde a la expectativa del inversionista. A estas proporciones las denotaremos **![w_i](https://render.githubusercontent.com/render/math?math=w_i)**, que finalmente es un vector de tamaño ![n \times 1](https://render.githubusercontent.com/render/math?math=n%20%5Ctimes%201), donde ![n \times 1](https://render.githubusercontent.com/render/math?math=n%20%5Ctimes%201) es el número de acciones a analizar.

Ello constituye  un **problema de optimización sujeto a restricciones (lineales) de igualdad**, que se puede expresar en los términos siguientes:

![\min_{w} \frac{1}{2}w^T\Sigma w](https://render.githubusercontent.com/render/math?math=%5Cmin_%7Bw%7D%20%5Cfrac%7B1%7D%7B2%7Dw%5ET%5CSigma%20w)

Sujeto a las restricciones lineales:
- El inversionista el rendimiento que vislumbra: <img src="https://render.githubusercontent.com/render/math?math=w^T\mu=r">
- Los pesos de los activos se encuentran distribuidos congruentemente sobre el portafolio; <img src="https://render.githubusercontent.com/render/math?math=w^T1_{n}=1">


Resolver este problema nos permite encontrar como se integra el portafolio que dado un rendimiento ![r > 0](https://render.githubusercontent.com/render/math?math=r%20%3E%200) esperado el inversionista, tenga varianza **mínima varianza** , el cual corresponde con el perfil de los inversionistas que son aversos al riesgo.  Es decir, nos permite conocer los pesos de un portafolio que, de acuerdo a una frontera de posibilidades de alocación y un rendimiento esperado, se localiza en frontera superior de entre todos los portafolios de inversión según su varianza, tal como se aprecia en la curva de la imagen:

![alt-text](https://github.com/czammar/MNO_finalproject/blob/master/images/frontera_eficiente.png)

Es así que  propósito de este proyecto será desarrollar estrategias que permitan resolver el modelo de Markowitz empleando herramientas de optimización y cómputo distribuido, particularmente aprovechando la disponibilidad de tarjetas GPU, así como el framework Cupy de Python para este tipo de  hardware. En adición, en este proyecto se busca echar mano de herramientas de computo en la nube y ambientes de virtualización, concretamente AWS y Docker.

A continuación se describen la estructura del presente repositorio, así como los algoritmos planteados para dar solución al modelo en cuestión.


## 3. Consideraciones metodológicas

### 3.1 Portafolio de activos, sus rendimientos y pesos.

* Tras analizar las fuentes de datos disponibles, se estableció considerar precios históricos de las 50 empresas, que destacan en sus correspondientes industria,  seleccionándose las que tienen mayor participación en el mercado (al momento de realizar este proyecto). En concreto, se consideraron  las empresas:

[WIP: Añadir tabla de nombre de empresas junto con sus acrónimos]

* Para considerar el comportamiento histórico de las acciones de dichas empresas, se consideró la información financiera de los últimos 5 años para hacer el análisis (esto es, desde el 1 de enero de 2015 al 30 de abril de 2020). Dicha información se obtuvo del API de Python que permite obtener datos desde Yahoo Finance, considerándose como valores de referencia de los activos a los precios diarios **Closed Price** (es decir, los precios al cierre de la bolsa).

* En complemento, para el cálculo de los rendimientos esperados de cada una de las empresas, se estímó pertinente evaluarlo a través de los precios de cierre diarios a partir de la fórmula del *rendimiento instantáneo* en escala logarítimica:

![r=log\tfrac{P_t}{P_{t-1}}](https://render.githubusercontent.com/render/math?math=R%3Dlog%5Ctfrac%7BPt%7D%7BPt-1%7D)<br />

Ello para evitar problemas numéricos debidos a la escala de los rendimientos.

* En lo tocante a como se debe determinar el vector de pesos asociado al portafolio de activos![$W$](https://render.githubusercontent.com/render/math?math=%24W%24), se consideró relevante pensarlos como una proporción, lo que equivale a que la suma de la entradas sea igual a 1.

* Por otro lado, el rendimiento esperado del portafolio se obtiene haciendo el producto punto del vector de rendimientos medios de los activos en el periodo en cuestión y los pesos del portafolio elegido, cumpliendo los portafolios factibles la restricción ![r=w^t \mu](https://render.githubusercontent.com/render/math?math=r%3Dw%5Et%20%5Cmu)

* Finalmente, la matriz de varianzas y covarianzas de los portafolios se calcula como las correspondientes matrices de varianzas y covarianzas rendimientos de las acciones en el periodo de los últimos 5 años para hacer el análisis (1 de enero de 2015 al 30 de abril de 2020).


### 3.2 Fase 1:
En este caso, el problema de minimización se aborda calculando la solución analítica del problema de optimización recién descrito, empleando la expresión del Lagrangiano del
problema de optimización considerando las respectivas restricciones, aprovechando que la matriz de covarianzas es simétrica y definida positiva.

**Solución:** Aplicar el método de multiplicadores de Lagrange al problema de optimización convexa (minimización) sujeto a restricciones lineales

- Definimos el Lagrangiano del problema:

![L(w,\lambda_{1}, \lambda_{2}) = \frac{1}{2}w^T\Sigma w +  \lambda_{1}(r-w^T\mu) + \lambda_{2}(1-w^T1_{n})](https://render.githubusercontent.com/render/math?math=L(w%2C%5Clambda_%7B1%7D%2C%20%5Clambda_%7B2%7D)%20%3D%20%5Cfrac%7B1%7D%7B2%7Dw%5ET%5CSigma%20w%20%2B%20%20%5Clambda_%7B1%7D(r-w%5ET%5Cmu)%20%2B%20%5Clambda_%7B2%7D(1-w%5ET1_%7Bn%7D))

- Derivar las condiciones de primer orden, que debe satisfacer el punto factible del problema:

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





## Pasos a seguir


1) Obtener base de datos de precios históricos de 50 empresas que coticen en bolsa, se obtendrá un conjunto de empresas por cada industria en el mercado y se seleccionaran las que tengan mayor participación en el mercado. Esta información la obtendremos de Yahoo Finance y los precios serán diarios **Closed Price**(al cierre de la bolsa)de los últimos 5 años para hacer el análisis. Se realizará un proceso de extracción de la base de datos definida en la etapa 1 del diagrama de flujo.

2) Se calcularán los rendimientos esperados de cada una de las empresas con los precios de acuerdo a la siguiente fórmula:
![r=log\tfrac{P_t}{P_{t-1}}](https://render.githubusercontent.com/render/math?math=R%3Dlog%5Ctfrac%7BPt%7D%7BPt-1%7D)<br />

3) Determinar el vector de pesos ![$W$](https://render.githubusercontent.com/render/math?math=%24W%24), se puede asignar aleatoriamente entre ![$(0,1)$](https://render.githubusercontent.com/render/math?math=%24(0%2C1)%24) con la condición de que la suma de la entradas sea igual a 1.<br />
4) Obtener el rendimiento esperado del portafolio ![r=w^t \mu](https://render.githubusercontent.com/render/math?math=r%3Dw%5Et%20%5Cmu)

5) Obtener la matriz de varianzas y covarianzas de los rendimientos de las acciones ![\Sigma](https://render.githubusercontent.com/render/math?math=%5CSigma)<br />

6) Para

Definir la función a optimizar  ![w^{*}=w_{0}\cdot (\Sigma^{-1}\cdot \mu)+w_{1}\cdot (\Sigma^{-1}\cdot 1)](https://render.githubusercontent.com/render/math?math=w%5E%7B*%7D%3Dw_%7B0%7D%5Ccdot%20(%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu)%2Bw_%7B1%7D%5Ccdot%20(%5CSigma%5E%7B-1%7D%5Ccdot%201))<br />
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

## Resultados de la optimización Markowitz

Una vez aplicado el algoritmo que resuelve el sistema de minimización para obtener el portafolio de *mínima varianza*, que en otras palabras significa obtener el portafolio de menor riesgo para inversionistas aversos al riesgo, se espera obtener las ponderaciones o proporciones que el inversionista debe invertir en las acciones evaluadas en un vector de todo el conjunto de acciones. Estos pesos pueden ser negativos porque asumimos que pueden existir Ventas en corto(*short sale*), lo cual implica que los inversores podrían tener una ganancia si tienen algún contrato de préstamo de titulos accionarios, los cuales deben devolver a una fecha futura y podrían devolverlos a un precio menor.

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

### Fase 2

## Método de Newton con reestricciones de igualdad

Consideraciones:

1) El punto inicial debe ser factible, es decir: <img src="https://render.githubusercontent.com/render/math?math=w\in domf"> , <img src="https://render.githubusercontent.com/render/math?math=w^T\mu = r"> y <img src="https://render.githubusercontent.com/render/math?math=w^T1_{n} = 1">

2) El paso de Newton <img src="https://render.githubusercontent.com/render/math?math=\Delta w">, debe modificarse de modo que satisfaga las reestricciones.


### Aproximación de segundo orden
Supongase que w es un punto factible del problema y desarrollese vía el teorema de Taylor la aproximación de segundo orden con centro en el punto w para f

<img src="https://render.githubusercontent.com/render/math?math=f: \hat{f}(w \oplus + v) = f(w) \oplus \Delta f(w)^Tv \oplus \frac{1}{2}v^T\Delta^2f(w)v">

Entonces el problema que se resolvera es:
min <img src="https://render.githubusercontent.com/render/math?math=\hat{f}(w\oplus v)">

Sujeto a:
- <img src="https://render.githubusercontent.com/render/math?math=(w\oplus v)^T\mu=r">
- <img src="https://render.githubusercontent.com/render/math?math=(w\oplus v)^T1_{n}=1">

con variable  <img src="https://render.githubusercontent.com/render/math?math=v \in R^n">, el cual como f es convexa es un problema convexo de minimización cuadrática con reestricciones de igualdad.

## Organización del equipo

Para el desarrollo del proyecto, los integrantes se dividieron principalmente en dos grupos; el **Grupo de programación** encargado de la implementación de los métodos y algoritmos; y el **Grupo de revisión** encargado de probar y reportar los métodos del primer grupo. Ambos grupos fueron coordinados por el **Project Manager** con ayuda de un **Asistente**.

La división anterior se puede resumir mediante la siguiente tabla:

**Fase 1: Implementación empleando método de Lagrange**

| #    | Rol                                   | Persona      |
| ---- | --------------------------------------| ------------ |
| 1    | Grupo de programación                 | Bruno        |
| 2    | Grupo de programación                 | Itzel        |
| 3    | Grupo de programación                 | César        |
| 4    | Grupo de revisión                     | León         |
| 5    | Grupo de revisión/Asistente de PM     | Danahi       |
| 6    | Project Manager                       | Yalidt       |

**Fase 2: Implementación usando método de Newton**

| #    | Rol                                        | Persona      |
| ---- | -------------------------------------------| ------------ |
| 1    | Grupo de programación                      | Bruno        |
| 2    | Grupo de programación                      | Itzel        |
| 3    | Grupo de programación                      | César        |
| 4    | Grupo de revisión/ Ayudante de programación| León         |
| 5    | Grupo de revisión/ Contexto Teórico        | Yalidt       |
| 6    | Project Manager                            | Danahi       |


## Referencias

Bodie, Z., Kane, A., & Marcus, A. J. (2011). Investments. New York: McGraw-Hill/Irwin.<br />
https://www.niceideas.ch/airxcell_doc/doc/userGuide/portfolio_optimTheory.html<br />
