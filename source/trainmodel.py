import sqlite3
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from utils import nltk_tokenizer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

conn = sqlite3.connect('knowledgebase.db')
cursor: cursor = conn.cursor()
cursor.execute("SELECT sentence, intent FROM user_intents")
rows: list[str] = cursor.fetchall()

texts: list[str] = [row[0] for row in rows]
labels: list[str] = [row[1] for row in rows]

conn.close()

stop_words_es = stopwords.words("spanish")

model = Pipeline([
    ("tfidf", TfidfVectorizer(tokenizer=nltk_tokenizer, stop_words=stop_words_es)),
    ('clf', LogisticRegression(max_iter=10000))
])

model.fit(texts, labels)

joblib.dump(model, "talia_ai_model.pkl")

print("Modelo entrenado exitosamente")
