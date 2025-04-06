# Instalación

**Requerimientos**
- Python<=[3.11.11](https://www.python.org/downloads/release/python-31111)
- [git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop/) (Opcional)
  
Sigue estos pasos para configurar y ejecutar el proyecto:

1. **Clonar el repositorio**

   Ejecuta el siguiente comando en el terminal para clonar el codigo del repositorio de GitHub.
     ```
     git clone https://github.com/jcentwickler/talia_ai.git
     ```

3. **Crear el archivo `.env`**

   Crea un archivo`.env` en el directorio raiz y agrega la siguiente entrada:
     ```
     TELEGRAM_API_TOKEN=<TOKEN>
     ```

5. **Instalar las dependencias**

   Ejecuta el siguiente comando en el directorio raiz para instalar las dependencias de python:
     ```bash
     pip install -r requirements.txt
     ```

7. **Crear la base de conocimientos en SQLite**
     ```bash
     python ./source/createdb.py
     ```

8. **Entrenar el modelo de Machine Learning**
     ```bash
     python ./source/trainmodel.py
     ```

9. **Ejecutar el bot**
     ```bash
     python ./source/telegrambot.py
     ```
# Instalación en Docker

1. **Seguir los 2 primeros pasos de la seccion anterior**

2. **Construir y descargar las imagenes necesarias**

   Ejecuta el siguiente comando en el directorio raiz para descargar y construir las imagenes necesarias para el proyecto
     ```
     docker compose build
     ```  
4. **Ejecutar el bot**
     ```
     docker compose up -d
     ```
# Librerias
- googletrans==4.0.0-rc1
- scikit_learn==1.6.1
- pyTelegramBotAPI==4.26.0
- python-dotenv==1.1.0

Usuario en telegram: @TaliaAI_bot

![Screenshot](https://i.imgur.com/p5zt0Dm.jpeg)
