import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from gpytranslate import SyncTranslator
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

nltk.download('stopwords')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

lemmatizer = WordNetLemmatizer()
stop_words_es = stopwords.words("spanish")

SUPPORTED_LANGUAGES = {
    "ingles": "en",
    "español": "es",
    "frances": "fr",
    "aleman": "de",
    "ruso": "ru",
    "italiano": "it",
    "portugues": "pt",
    "chino": "zh-cn",
    "japones": "ja",
    "arabe": "ar"
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

def extract_target_language(user_input):
    user_input_lower = user_input.lower()
    for name, code in SUPPORTED_LANGUAGES.items():
        if name in user_input_lower:
            return [name, code]
    return None

def translate_text(text, target_language):
    translator = SyncTranslator()
    translation = translator.translate(text, dest=target_language)    
    return translation.text
