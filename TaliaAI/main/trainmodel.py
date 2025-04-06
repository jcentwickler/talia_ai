import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from utils import nltk_tokenizer

conn = sqlite3.connect('knowledgebase.db')
cursor = conn.cursor()
cursor.execute("SELECT sentence, intent FROM user_intents")
rows = cursor.fetchall()

texts = [row[0] for row in rows]
labels = [row[1] for row in rows]

conn.close()

model = Pipeline([
    ("tfidf", TfidfVectorizer(tokenizer=nltk_tokenizer))
])

model.fit(texts, labels)

joblib.dump(model, "talia_ai_model.pkl")

print("Modelo entrenado exitosamente")
