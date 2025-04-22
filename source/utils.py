import nltk
import os
import requests
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from gpytranslate import SyncTranslator
from openai import OpenAI
from dotenv import load_dotenv
from pywsd.lesk import adapted_lesk
from nltk.corpus import wordnet as wn
from nltk import pos_tag

load_dotenv()

nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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

def define_word(word):
    top_n=3
    number=1
    synsets = wn.synsets(word)
    definitions = []

    if len(synsets) > 0:
        for syn in synsets[:top_n]:
            definitions.append(f"Definición {number}: {syn.definition()}\n")
            number+=1
        return "\n".join(definitions)
    else:
        request = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if request.status_code == 200:
            data = request.json()

            max_definitions = min(3, len(data[0]['meanings'][0]['definitions']))

            for n in range(max_definitions):
                definitions.append(f"Definición {number}: {data[0]['meanings'][0]['definitions'][n]['definition']}\n")
                number += 1

    return "\n".join(definitions)


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
