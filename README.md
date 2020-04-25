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
* 1)Obtener base de datos de precios históricos de 50 empresas que coticen en bolsa, se obtendrá un conjunto de empresas por cada industria en el mercado. Esta infromación la obtendremos de CapitalIQ y los precios serán diarios **Closed Price**, es decir al cierre de la bolsa.

* 2)Se calcularán los rendimientos esperados de cada una de las empresas con los precios de acuerdo a la siguiente fórmula [Pendiente incluir formula]:

* 3)Determinar el vector de pesos ![$W$](https://render.githubusercontent.com/render/math?math=%24W%24), se puede asignar aleatoriamente entre ![$(0,1)$](https://render.githubusercontent.com/render/math?math=%24(0%2C1)%24) con la condición de que la suma de la entradas sea igual a 1
* 4)Obtener la matriz de varianzas y covarianzas de los rendimientos obtenidos
* 5)Obtener el rendimiento esperado del portafolio ![$\mu=WR$](https://render.githubusercontent.com/render/math?math=%24%5Cmu%3DWR%24)
* 6)Obtener la matriz de varianzas y covarianzas de los rendimientos de las acciones ![$V$](https://render.githubusercontent.com/render/math?math=%24V%24),
* 7)Definir la función a optimizar  ![$minimo \; w^t V w$](https://render.githubusercontent.com/render/math?math=%24minimo%20%5C%3B%20w%5Et%20V%20w%24)
* 8)Establecer las restricciones del modelo
\[restricciones : w^t \mu=R\]<br />
                \[\forall i, wi\geq 0\]<br />
                \[W^te=1\]<br />

  * Donde \[e\] es un vector \[e=(1,1,1....1)^t\], \[V\] es la matriz de varianzas-covarianzas y \[\mu\]es el rendimiento esperado del portafolio.<br />
* 9) Solucionar el siguiente sistema  \[w=V^{-1}(\mu\cdot 1)A^{-1}\binom{R}{1}\]<br />
Donde A se define como

![$A=\begin{pmatrix} a &b \\ b& c \end{pmatrix} = \begin{pmatrix} \mu^{t}\cdot V^{-1}\cdot \mu & \mu^{t}\cdot V^{-1}\cdot1 \\ \mu^{t}\cdot V^{-1}\cdot 1 & 1^{t}\cdot V^{-1}\cdot 1 \end{pmatrix}$](https://render.githubusercontent.com/render/math?math=%24A%3D%5Cbegin%7Bpmatrix%7D%20a%20%26b%20%5C%5C%20b%26%20c%20%5Cend%7Bpmatrix%7D%20%3D%20%5Cbegin%7Bpmatrix%7D%20%5Cmu%5E%7Bt%7D%5Ccdot%20V%5E%7B-1%7D%5Ccdot%20%5Cmu%20%26%20%5Cmu%5E%7Bt%7D%5Ccdot%20V%5E%7B-1%7D%5Ccdot1%20%5C%5C%20%5Cmu%5E%7Bt%7D%5Ccdot%20V%5E%7B-1%7D%5Ccdot%201%20%26%201%5E%7Bt%7D%5Ccdot%20V%5E%7B-1%7D%5Ccdot%201%20%5Cend%7Bpmatrix%7D%24)



