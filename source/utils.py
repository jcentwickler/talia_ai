import nltk
import os
import requests
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from gpytranslate import SyncTranslator
from openai import OpenAI
from dotenv import load_dotenv
from pywsd.lesk import adapted_lesk
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from pathlib import Path
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

lemmatizer = WordNetLemmatizer()
stop_words_es = stopwords.words("spanish")

SUPPORTED_LANGUAGES = {
    "ingles": "en",
    "español": "es",
}

RESPUESTAS_TRADUCCION = [
    "¡Por supuesto! Aquí tienes el texto en `{}`:",
    "Claro. Aquí está la traducción en `{}`:",
    "Sin problema, en `{}` sería:",
    "Esta es la versión en `{}`:",
    "Así se dice en `{}`:",
    "Aquí lo tienes en `{}`:",
    "En `{}` se dice así:",
    "La traducción al idioma `{}` es:",
    "Esto en `{}` sería:",
    "Perfecto, en `{}` se dice:",
    "En `{}` lo dirías así:",
    "Este es el equivalente en `{}`:",
    "Traducción en `{}`:",
]

def nltk_tokenizer(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(w) for w in tokens if w.isalpha() and w not in stop_words_es]

def extract_text_to_translate(user_input):
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=True,
        messages=[{"role": "user", "content": (f'Extrae únicamente el texto que el usuario desea traducir.\n'
        f'Devuelve **solo** la frase o palabra a traducir, **sin comillas, sin explicaciones y sin texto adicional, tal y como esta y sin traducir**.\n'
        f'Usuario: {user_input}')}
        ])
    return completion.choices[0].message.content

def extract_word_to_define(user_input):
        completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=True,
        messages = [{"role": "user", "content": (
        f'Extrae la palabra o el termino que el usuario desea definir y su contexto, solo si el usuario lo proporciona.\n'
        f'Debes devolver **solo** la palabra o termino **sin comillas, sin explicaciones y sin texto adicional**, tal como está escrito.\n'
        f'Si hay contexto, devuélvelo en una nueva línea. El contexto puede ser una oración, párrafo, extracto o bloque de texto proporcionado por el usuario, no implícito y sin modificación alguna\n'
        f'Usuario: {user_input}'
        )}]
)
        return completion.choices[0].message.content.splitlines()

def extract_text_to_read(user_input):
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",
        store=True,
        messages = [{
        "role": "user",
        "content": (
        f'Extrae únicamente el texto que el usuario desea que sea leído en voz alta o mediante TTS.\n'
        f'Devuelve exclusivamente esa frase, palabra o texto **sin comillas, sin explicaciones, sin etiquetas, y sin ningún añadido**.\n'
        f'Mantén el texto extraido exactamente como fue escrito por el usuario, incluyendo mayúsculas, puntuación y formato.\n'
        f'Usuario: {user_input}'
    )
}])
    return completion.choices[0].message.content

def define_word(word):
    top_n=3
    number=1
    synsets = wn.synsets(word)
    definitions = []
    message = f"¡Claro! Es posible que «{word}» tenga varios significados. Si quieres una definición más precisa, por favor proporciona el contexto en el que se usa.\n\n"

    if len(synsets) > 0:
        for syn in synsets[:top_n]:
            definitions.append(f"Definición [en] {number}: {syn.definition()}\n")
            number+=1
        return message + "\n".join(definitions)
    else:
        request = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if request.status_code == 200:
            data = request.json()

            max_definitions = min(3, len(data[0]['meanings'][0]['definitions']))

            for n in range(max_definitions):
                definitions.append(f"Definición {number}: {data[0]['meanings'][0]['definitions'][n]['definition']}\n")
                number += 1
            return message + "\n".join(definitions)
        else:
            return "No se encontró una definición para la palabra o termino. Asegúrate de que esté escrita en inglés y sin errores gramaticales."


def define_word_by_context(context, word):
    tokens = word_tokenize(context)
    pos_tags = pos_tag(tokens)

    def get_wordnet_pos(tag):
        if tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('V'):
            return wn.VERB
        elif tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('R'):
            return wn.ADV
        else:
            return None

    pos = None
    for w, t in pos_tags:
        if w.lower() == word.lower():
            pos = get_wordnet_pos(t)
            break

    sense = adapted_lesk(context, word, pos=pos)
    if sense:
        definition = sense.definition()
        print(f"Predicted synset: {sense.name()}")
        print(f"Definition: {definition}")
        print(f"Examples: {sense.examples()}")

        return definition
    else:
        print("No suitable sense found.")
        return f"""No se pudo encontrar una definicion para 
               Palabra: {word}
               Contexto: {context}"""
    


def extract_target_language(user_input):
    user_input_lower = user_input.lower()
    for name, code in SUPPORTED_LANGUAGES.items():
        if name in user_input_lower:
            return [name, code]
    return None

def translate_text(text, target_language):
    translator = SyncTranslator()
    translation = translator.translate(text, targetlang=target_language)    
    return translation.text

def text_to_speech(text, bot, message): 
    text_to_read = extract_text_to_read(text)

    speech_path = Path(f"TTS \"{datetime.today().strftime('%Y-%m-%d %H-%M-%S')}\"...")
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text_to_read,
        response_format="mp3"
    ) as response:
        response.stream_to_file(speech_path)

    with open(speech_path, "rb") as audio:
        bot.send_audio(message.chat.id, audio)
    os.remove(speech_path)

def escape_markdown_v2(text):
    markdown_special_chars = r'([_*\[\]()~`>#+\-=|{}.!])'
    return re.sub(markdown_special_chars, r'\\\1', text)