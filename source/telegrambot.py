import telebot
import joblib
import sqlite3
import random
import os
from utils import *
from dotenv import load_dotenv
load_dotenv()

user_states = {"neutral": True}

model = joblib.load("talia_ai_model.pkl")
replyModel = joblib.load("reply_classifier.pkl")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def define_word_without_context(message, word) -> None:
    bot.reply_to(message, f"\n{define_word(word)}")

def ask_define_word_without_context(message) -> None:
     word = user_states["definir_sin_contexto"][0]
     define_word_without_context(message, word)
     user_states["definir_sin_contexto"]=["", False]
     user_states["neutral"] = True

@bot.message_handler(commands=['start'])
def handle_welcome_command(message):
    bot.reply_to(message, "Hi")

@bot.message_handler(commands=['code'])
def handle_code_command(message):
    bot.reply_to(message, "https://github.com/jcentwickler/talia_ai/tree/main")

@bot.message_handler(func=lambda message: True)
def classify_message(message):
    if user_states["neutral"]:
        user_input = message.text
        predicted_label = model.predict([user_input])[0]
        full_language = None
        target_language = None

        if predicted_label == "translate":
            language = extract_target_language(user_input)
            if language and len(language) > 2:
                full_language = language[0]
                target_language = language[1]
            if target_language:
                text_to_translate = extract_text_to_translate(user_input)
                if text_to_translate:
                    print(f"'{target_language}'")
                    print(f"'{text_to_translate}'")
                    translated_text = translate_text(text_to_translate, target_language)
                    print(f"'{translated_text}'")
                    frase = random.choice(RESPUESTAS_TRADUCCION).format(full_language)
                    bot.reply_to(message, f"{frase} {translated_text}")
                else:
                    bot.reply_to(message, "No encontré texto para traducir. Por favor proporciona lo que deseas traducir.")
            else:
                bot.reply_to(message, "No pude identificar el idioma para traducir. Por favor especifícalo claramente.")
    
        elif predicted_label == "define":
            word_and_context = extract_word_to_define(user_input)
            length = len(word_and_context)

            if length > 1:
                word = word_and_context[0].lower().strip()
                context = word_and_context[1].lower().strip()
                print(f"Word: `{word}` \nContext: {context.split(' ')}")

                if word in context.split(' '):
                    definition = define_word_by_context(context, word)
                    bot.reply_to(message, f"Definición: {definition}")
                else:
                    bot.reply_to(message, "La palabra no fue encontrada en el contexto que proporcionaste. ¿Deseas definir la palabra sin contexto?")
                    user_states["neutral"]=False
                    user_states["definir_sin_contexto"]=[word, True]
            else:
                word = extract_word_to_define(user_input)[0]
                define_word_without_context(message, word)
        else:
            bot.reply_to(message, f"Intención: {predicted_label}")
    else:
        user_input = message.text
        predicted_reply = replyModel.predict([user_input])[0]
        if  predicted_reply == "affirmative":
            if user_states["definir_sin_contexto"][1]:
                ask_define_word_without_context(message) 
        elif  predicted_reply == "negative":
            bot.reply_to(message, "¡Esta bien!. 👍 Si necesitas algo mas no dudes en mencionarlo")
            user_states["neutral"] = True
        else: 
            bot.reply_to(message, "No entiendo tu respuesta, intentalo denuevo 😔")


print("Bot en ejecución...")
bot.infinity_polling()

