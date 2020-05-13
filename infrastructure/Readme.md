
 # Manual AWS 
 
 En este documento se explican los pasos a seguir para levantar una instancia en AWS donde se pueden ejecutar los códigos desarrollados para la implementación del modelo Markowitz en paralelo.
 
 Para poder seguir estos pasos, es necesario tener habilitados los permisos para levantar instancias con GPU's en AWS.
 
 1. Levantamos una instancia en AWS en una máquina que tenga la opción p2.xlarge como tipo de instancia, en este caso elegimos la máquina **Deep Learning AMI (Ubuntu 18.04) Version 28.1** pues tiene una tarjeta gráfica NVIDIA. Elegimos **p2.xlarge** como tipo de instancia con 4 vCPUs y continuamos con la configuración de la instancia, eligiendo una Network, IAM Role y Security Group adecuados.


 2. En la sección *Advanced Details* agregamos la siguiente configuración:
```
#!/bin/bash
region=<aquí colocar región en la que se lanzarán las instancias>
name_instance=mi-nodo
apt-get update
apt-get install -y git curl python3-pip && pip3 install --upgrade pip&& pip3 install awscli --upgrade
##etiquetar instancia
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
aws ec2 create-tags --resources $INSTANCE_ID --tag Key=Name,Value=$name_instance-$PUBLIC_IP --region=$region
```

Esto se basa en el [wiki](https://github.com/ITAM-DS/analisis-numerico-computo-cientifico/wiki/1.2.Instalaci%C3%B3n-de-herramientas-%C3%BAtiles-en-AWS) del repositorio de la materia de Metódos Numéricos y Optimización. Se puede notar que no añadimos la instalación de Docker en esta configuración, pues la máquina ya tiene Docker instalado.

 3. Una vez levantada la instancia, se crea un Dockerfile para construir una imagen de Docker con CuPy, la configuración se basa en el Dockerfile [jupyterlab_nvidia_cupy:1.1.0_10.1](https://github.com/palmoreck/dockerfiles/blob/master/jupyterlab/nvidia/cupy/1.1.0_10.1/Dockerfile), este archivo se crea en una ruta específica:
 
```
mkdir /home/ubuntu/jupyter
cd /home/ubuntu/jupyter
nano Dockerfile
```
En el [Dockerfile](https://github.com/czammar/MNO_finalproject/blob/master/infrastructure/Dockerfile) agregamos la configuración:

```
FROM nvidia/cuda:10.1-devel-ubuntu18.04

ENV JUPYTERLAB_VERSION 1.1.0
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && echo "America/Mexico_City" > /etc/timezone && apt-get install -y tzdata

RUN apt-get update && apt-get install -y \
            sudo \
            nano \
            less \
            git \
            wget \
            curl \
            python3-dev \
            python3-pip \
            python3-setuptools \
            nodejs && pip3 install --upgrade pip && \
            pip3 install --upgrade setuptools 

RUN pip3 install pandas yfinance matplotlib seaborn numpy datetime

RUN groupadd miuser
RUN useradd miuser -g miuser -m -s /bin/bash
RUN echo 'miuser ALL=(ALL:ALL) NOPASSWD:ALL' | (EDITOR='tee -a' visudo)
RUN echo 'miuser:qwerty' | chpasswd
RUN pip3.6 install jupyter jupyterlab==$JUPYTERLAB_VERSION --upgrade
USER miuser


RUN pip3 install --user cupy-cuda101 awscli

RUN jupyter notebook --generate-config && sed -i "s/#c.NotebookApp.password = .*/c.NotebookApp.password = u'sha1:115e429a919f:21911277af52f3e7a8b59380804140d9ef3e2380'/" /home/miuser/.jupyter/jupyter_notebook_config.py

ENTRYPOINT ["/usr/local/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]
```

Esta configuración es la necesaria para poder ejecutar nuestro [desarrollo](https://github.com/czammar/MNO_finalproject/blob/master/infrastructure/Solver_AWS.ipynb) del modelo Markowitz.

 4. Se crean variables de ambiente auxiliares y se construye la imagen:
```
nombre_imagen=jupyter_image
nombre_contenedor=jupyter_contenedor
docker build . -t $nombre_imagen		
```

 5. Creamos una carpeta que vincularemos con el contenedor al levantarlo:
```
cd
mkdir mi_carpeta
```

 6. Finalmente levantamos un contenedor de la imagen que acabamos de construir:
```
docker run --gpus all --rm -v /home/ubuntu/mi_carpeta:/datos --name $nombre_contenedor -p 8888:8888 -d $nombre_imagen
```

 7. En el navegador vamos a 
```
<dns ipv4 instancia>:8888
```

Y de esta forma ingresamos a *jupyterlab* donde tenemos CuPy.
 
