# Instalación

Sigue estos pasos para configurar y ejecutar el proyecto:

1. **Crear el archivo `.env`**
   - Dentro de la carpeta `main`, crea un archivo `.env` y agrega la siguiente entrada:
     ```
     TELEGRAM_API_TOKEN=<Token del API de Telegram>
     ```

2. **Instalar las dependencias**
   - Ejecuta el siguiente comando para instalar las dependencias de python:
     ```bash
     pip install -r requirements.txt
     ```

3. **Crear la base de conocimientos en SQLite**
     ```bash
     python createdb.py
     ```

4. **Entrenar el modelo de Machine Learning**
     ```bash
     python trainmodel.py
     ```

5. **Ejecutar el bot**
     ```bash
     python telegrambot.py
     ```

![Screenshot](https://i.imgur.com/p5zt0Dm.jpeg)
