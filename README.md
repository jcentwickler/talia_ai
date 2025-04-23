# Requerimientos
- Python [3.11.11](https://www.python.org/downloads/release/python-31111)
- [git](https://git-scm.com/downloads)
- Git Bash (Solo Windows) (Opcional)
- [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Solo Windows) (Recomendado) (Opcional)
- [pyenv](https://github.com/pyenv/pyenv) (Solo Linux) (Recomendado) (Opcional)
- [Docker](https://www.docker.com/products/docker-desktop/) (Opcional)

# Instalación
Sigue estos pasos para configurar y ejecutar el proyecto:

**Recomendacion para usuarios de Windows:** Usar el programa **git bash** para ejectuar los comandos, este viene incluido al instalar **git**. Si sabes lo que haces puede utilizar **Powershell** pero tendras que modificar los comandos antes ejectuarlos.

## 1. **Clonar el repositorio**
Ejecuta el siguiente comando en el terminal para clonar el codigo del repositorio de GitHub. 
```
git clone https://github.com/jcentwickler/talia_ai.git
```
     
## 2. **Navegar a la carpeta del proyecto**
```
cd talia_ai
```
     
## 3. **Crear el archivo `.env`**
Crea un archivo`.env` en el directorio source y agrega las siguientes entradas y luego reemplazar \<TOKEN> y \<KEY>.  
```
TELEGRAM_API_TOKEN=<TOKEN>
OPENAI_API_KEY=<KEY>
```
Tambien puedes crear el archivo con este comando y modificarlo directamente antes de ejectuarlo o mas luego con un editor de texto como VScode.  
```
echo -e "TELEGRAM_API_TOKEN=<TOKEN>\nOPENAI_API_KEY=<KEY>" > source/.env
```
## 4. **Verificar la version de python**
```
python --version
```
Verificar que la version sea 3.11.11 o verificar que el comando ```python3.11```funcione sino instalarlo y asegurarse que este en el PATH o ejecutar el comando ```pyenv local 3.11.11``` dentro de la carpeta (Si se instalo pyenv/pyenv-win)

## 5. **Acceder al entorno virtual de python**
   
**Windows**
```
source source/.venv/Scripts/activate
```
> [!WARNING]
> Si te sale el error ``` "No se pudo cargar el archivo source/.venv/Scripts/activate porque la ejecución de scripts esta deshabilitada en este sistema"``` entonces ejectuar este comando primero en Powershell antes de continuar.
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser ​
```

**Linux**
```
source source/.venv/bin/activate
```
   
## 6. **Configurar el bot**

- **Usar el script de configuración**

**Windows**
     
```
bash setup.sh
```
   
**Linux**
```
chmod +x setup.sh && bash setup.sh
```

- **Configurarlo manualmente**

**Windows o Linux**
```
pip install -r requirements.txt; python source/createdb.py; python source/creategamedb.py; python source/trainmodel.py
```

## 7. **Ejecutar el bot**
```
cd source
```
```
python telegrambot.py
```
     
# Instalación en Docker

## 1. **Seguir los 3 primeros pasos de la seccion anterior**
   
## 2. **Ejecutar el bot**
```
docker compose up -d --build
```
## Librerias
- nltk==3.9.1 -
- scikit_learn==1.6.1
- pyTelegramBotAPI==4.26.0
- python-dotenv==1.1.0
- gpytranslate==2.0.0
- openai==1.75.0
- pywsd==1.2.5 

Usuario en telegram: @TaliaAI_bot

https://t.me/TaliaAI_bot

![Screenshot](https://i.imgur.com/W5fGtvb.png)
