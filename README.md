# Fundamentos de FastAPI

Este repositorio es la recopilación de la parte práctica del curso de Fundamentos de FastAPI realizado en Platzi
## 1. Cómo ejecutar en Windows
La actividad en principio la desarrollé en Windows utilizando la PowerShell para la instalación, actualización y activación del entorno virtual.
### Instalar PIP
Lo primero que se debe tener en cuenta es tener **pip** instalado ( y preferiblemente actualizado), yo lo hice siguiendo una [guía](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/ ) (en inglés) para instalar pip en windows.

Pero para hacerlo "corto" son estos dos comandos:

<pre>curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py</pre>

Luego tener PIP instalado, debemos crear el entorno virtual, lo que nos permitirá descargar los módulos necesarios para ejecutar este repositorio

<pre>
python -m venv &ltnombre&gt
</pre>

Luego se se activa el entorno virtual
<pre>
.\&ltnombre&gt\Scripts\activate
</pre>

Y para desactivar simplemente se hace uso del comando `deactivate`

## 2. Cómo ejecutar en Linux/Ubuntu

Ubuntu no fue donde lo probé en principio, pero es Linux, en general instalar cosas es mas "Fácil" la mayoría veces

### Instalar pip
## Primera forma
Se repite el mismo paso de Windows para traer el módulo de pip y luego se instala.

<pre>curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
pyton3 get-pip.py</pre>

## Segunda forma
Se debe tener actualizado el sistema, en el caso que lo hice con Ubuntu
<pre>sudo apt-get update && sudo apt-get update</pre>

Luego de tener pip, se debe instalar el complemento para generar el entorno virtual

<pre> sudo apt install python3.10-venv </pre>

Luego se utiliza el mismo comando, con un pequeño detalle para crear el espacio virtual:
<pre>python3 -m venv &ltnombre&gt
</pre>

Luego para activarlo se utiliza el comando 
<pre>source &ltnombre-venv&gt/bin/activate</pre>

Y para salir igual solo se necesita `deactivate`

Con el entorno virtual activo, se ejecuta el comando

<pre>pip install -r requirements.txt</pre>

Ya que en el archivo se incluye el listado de módulos y sus versiones necesarias para ejecutar bien.

# Contenido
En el archivo [main](main.py) está todo el nucleo de la aplicación (no estádel todo organizado es posible que si esté engorroso de leer). Allí se ve el CRUD básico con lo métodos GET, POST, PUT y DELETE.

Luego en el archivo [jwtmanager](jwtmanager.py) está la información para la creación y validación del token,

# Ejecución
Para ejecutar el archivo main, no se realizaría una ejecución digamos... "normal".
Se debe correr el comando
<pre>uvicorn main:app --reload </pre>
Y ya podremos acceder al [localhost](http://localhost:8000/docs) para visualizar la documentación de la api.

## Tener en cuenta
Tiene la depedencia para consumir el token, por lo tanto no permitirá consumir los métodos sin ingresar el JWT.

> Agradezco que hallas leído hasta este punto.