## telegrambot.py
#!/usr/bin/python
import telebot
import joblib
import sqlite3
from utils import *
import random
from utils import RESPUESTAS_TRADUCCION
import os
from dotenv import load_dotenv
load_dotenv()

model = joblib.load("talia_ai_model.pkl")

conn = sqlite3.connect('knowledgebase.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT intent FROM user_intents")
labels = [row[0] for row in cursor.fetchall()]
conn.close()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def classify_message(message):
    user_input = message.text
    predicted_label = model.predict([user_input])[0]

    if predicted_label == "translate":
        target_language = extract_target_language(user_input)
        if target_language:
            text_to_translate = extract_text_to_translate(user_input)
            if text_to_translate:
                translated_text = translate_text(text_to_translate, target_language=target_language)
                frase = random.choice(RESPUESTAS_TRADUCCION).format(target_language)
                bot.reply_to(message, f"{frase} {translated_text}")
            else:
                bot.reply_to(message, "No encontré texto para traducir. Por favor proporciona lo que deseas traducir.")
        else:
            bot.reply_to(message, "No pude identificar el idioma para traducir. Por favor especifícalo claramente.")
    else:
        bot.reply_to(message, f"Intención: {predicted_label}")

print("Bot en ejecución...")
bot.infinity_polling()
