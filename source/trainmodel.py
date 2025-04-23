import sqlite3
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
import nltk

conn = sqlite3.connect('knowledgebase.db')
cursor: cursor = conn.cursor()
cursor.execute("SELECT sentence, intent FROM user_intents")
rows: list[str] = cursor.fetchall()

texts: list[str] = [row[0] for row in rows]
labels: list[str] = [row[1] for row in rows]

conn.close()

stop_words_es = stopwords.words("spanish")

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words=stop_words_es)),
    ('clf', LogisticRegression(max_iter=10000))
])

model.fit(texts, labels)

joblib.dump(model, "talia_ai_model.pkl")

X = [
    "sí", "si", "claro", "claro que sí", "vale", "va", "va dale", "ok", "okay", "okey", "perfecto", "de acuerdo", "obvio", 
    "seguro", "sí quiero", "sí, dale", "sí porfa", "por supuesto", "afirmativo", "sí señor", "sí señora", "así es", 
    "dale", "eso quiero", "quiero", "acepto", "venga", "simón", "de una", "me gusta", "eso está bien", "todo bien", 
    "excelente", "sí, gracias", "bueno", "me sirve", "sí, por qué no", "sí obvio", "sí jajaja", "dale pues", "si quiero",
    "se hace", "hágale", "ya pues", "yeah", "yes", "listo", "está bien", "se aprueba", "yes please", "me encanta",

    "no", "nop", "no gracias", "mejor no", "ni hablar", "no quiero", "rechazo", "negativo", "nunca", "no porfa", 
    "nah", "ni loco", "no gracias jajaja", "noup", "nel", "ni merda", "olvídalo", "nope", "nonono", "definitivamente no",
    "jamás", "ni cagando", "nunca en la vida", "no es necesario", "no hace falta", "no me interesa", "ni en pedo",
    "cero ganas", "para nada", "estoy bien así", "estoy bien, gracias", "paso", "no por ahora", "tal vez después", "me abstengo",
    "prefiero que no", "prefiero no hacerlo", "no, gracias", "no deseo", "nah bro", "ya fue", "siguiente", "rechazado",

    "te quiero", "naranja", "jajaja", "xd", "wtf", "quiero tacos", "hoy es lunes", "me duele la cabeza", "no sé", 
    "tal vez", "ni idea", "supongo", "quizá", "quién sabe", "perro", "taco", "lol", "qué?", "ni me acuerdo", "ayuda", 
    "eso qué", "super", "increíble", "dame más", "no importa", "ay si si", "qué dices", "uff", "shakira", "te amo", 
    "quién eres tú", "no entiendo", "mmm", "khe", "asdf", "hola", "buenas", "todo cool", "me da igual", "sin comentarios",
    "🥲", "😅", "🙃", "🐸", "✨", "no lo sé rick", "ok pero no", "puede ser", "quiero llorar", "uwu", "asdfgh", "lalala", "zzz", "123", "jeje", "💀"
]

y = [
    *["affirmative"] * 50,
    *["negative"] * 50,
    *["other"] * 50,
]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words=stop_words_es, ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=10000))
])

pipeline.fit(X, y)

joblib.dump(pipeline, "reply_classifier.pkl")

print("Modelos entrenados exitosamente")