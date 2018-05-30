===========================================================================================================================
Requisitos previos de desarrollo, basodo en Python 2.7 para entorno  windows:
===========================================================================================================================

 Paso 1:

     python -m pip install --upgrade pip wheel setuptools

     Microsoft Visual C++ Compiler for Python 2.7

       descargar en  https://www.microsoft.com/en-us/download/details.aspx?id=44266

 Paso 2:

     Los siguientes módulos de Python (disponibles vía pip):


        python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
        python -m pip install kivy
        python -m pip install Zope.Interface
        python -m pip install PyOpenSSL
        python -m pip install Twisted

     O simplemente ejecutar:

        pip install -Ur directorio/requirements.txt

 Paso 3 (opcional)

    Para verificar la instalación, listando los package

        pip list

        ó de forma individual

        pip show package_name

Errores:

 Twisted, si durante la instalación da error verificar que se tiene instalado  Microsoft Visual C++ Compiler for Python 2.7
 del paso 1, y la version del sistema operativo debe ser de 64 bits dado que la version actual usada no esta disponible
 para 32 bits.

===========================================================================================================================
Pasos para la generación del binario de la aplicación (.exe) basado en la libreria pyinstaller:
============================================================================================================================
    paso 1:

        Instalarar la libreria pyinstaller desde la consola

            pip install --upgrade pyinstaller

    paso 2:

        En la consola de windows situarse en la raiz de la aplicación, Ejemplo cd C:\PycharmProjects\sportech37_sync_interface
        situada  la consola en la raiz ejecutar el siguiente comando:

            python -m PyInstaller sportech.spec

        Terminado el proceso de la consola se crearan dos carpetas "build" y "dist", la carpeta dist contendra los archivos
        copilados para la distribución de la aplicación.