## utils.py
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from googletrans import Translator

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("spanish"))

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
    return [lemmatizer.lemmatize(w) for w in tokens if w.isalpha() and w not in stop_words]

def extract_text_to_translate(user_input):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [w for w in tokens if w not in SUPPORTED_LANGUAGES.keys() and w not in ["traduce", "traducir", "a", "en", "cómo", "se", "dice"]]
    return " ".join(filtered_tokens)

def extract_target_language(user_input):
    user_input_lower = user_input.lower()
    for name, code in SUPPORTED_LANGUAGES.items():
        if name in user_input_lower:
            return code
    return None

def translate_text(text, target_language="es"):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text
