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
1) Obtener base de datos de precios históricos de 55 empresas que coticen en bolsa, se obtendrá un conjunto de empresas por cada industria en el mercado. Esta infromación la obtendremos de CapitalIQ y los precios serán diarios **Closed Price**, es decir al cierre de la bolsa. Debido a que es una plataforma privada no se puede extraer la información directamente, por lo que en nuestro proyecto no hay un proceso de EL.

2) Se calcularán los rendimientos esperados de cada una de las empresas con los precios de acuerdo a la siguiente fórmula:
![r=log\tfrac{P_t}{P_{t-1}}](https://render.githubusercontent.com/render/math?math=R%3Dlog%5Ctfrac%7BPt%7D%7BPt-1%7D)<br />

3) Determinar el vector de pesos ![$W$](https://render.githubusercontent.com/render/math?math=%24W%24), se puede asignar aleatoriamente entre ![$(0,1)$](https://render.githubusercontent.com/render/math?math=%24(0%2C1)%24) con la condición de que la suma de la entradas sea igual a 1.<br />
4) Obtener el rendimiento esperado del portafolio ![$\mu=WR$](https://render.githubusercontent.com/render/math?math=%24%5Cmu%3DWR%24)<br />

5) Obtener la matriz de varianzas y covarianzas de los rendimientos de las acciones ![\Sigma](https://render.githubusercontent.com/render/math?math=%5CSigma)<br />

6) Definir la función a optimizar  ![minimizar:   w^*=\mu\cdot w_{0}^{*}+w_{1}^{*}](https://render.githubusercontent.com/render/math?math=minimizar%3A%20%20%20w%5E*%3D%5Cmu%5Ccdot%20w_%7B0%7D%5E%7B*%7D%2Bw_%7B1%7D%5E%7B*%7D)<br />
7) Establecer las restricciones del modelo<br />
![restricciones : w^t \mu=r](https://render.githubusercontent.com/render/math?math=restricciones%20%3A%20w%5Et%20%5Cmu%3DR)<br />
![\forall i, wi\geq 0](https://render.githubusercontent.com/render/math?math=%5Cforall%20i%2C%20wi%5Cgeq%200)<br />
![W^te=1](https://render.githubusercontent.com/render/math?math=W%5Ete%3D1)<br />

* Donde los vectores auxiliares son los siguientes:<br />
![w_{0}^{*}=\frac{1}{\Delta}\cdot (B\cdot \Sigma^{-1}\cdot \mu-C\cdot \Sigma^{-1}\cdot 1)](https://render.githubusercontent.com/render/math?math=w_%7B0%7D%5E%7B*%7D%3D%5Cfrac%7B1%7D%7B%5CDelta%7D%5Ccdot%20(B%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu-C%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%201))<br />
![w_{1}^{*}=\frac{1}{\Delta}\cdot (C\cdot \Sigma^{-1}\cdot \mu-A\cdot \Sigma^{-1}\cdot 1)](https://render.githubusercontent.com/render/math?math=w_%7B1%7D%5E%7B*%7D%3D%5Cfrac%7B1%7D%7B%5CDelta%7D%5Ccdot%20(C%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%20%5Cmu-A%5Ccdot%20%5CSigma%5E%7B-1%7D%5Ccdot%201))<br />
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

El proceso en comento, se resumen a continuación:



![Diagrama de flujo](./images/diagrama_flujo.jpeg)


## Referencias 

Bodie, Z., Kane, A., & Marcus, A. J. (2011). Investments. New York: McGraw-Hill/Irwin.<br />
https://www.niceideas.ch/airxcell_doc/doc/userGuide/portfolio_optimTheory.html<br />




