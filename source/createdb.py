import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

import sqlite3
con = sqlite3.connect("knowledgebase.db")
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_intents';")
table_exists = cur.fetchone()

if not table_exists:
    cur.execute("""CREATE TABLE IF NOT EXISTS user_intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sentence TEXT NOT NULL,
    intent VARCHAR(50) NOT NULL)""")
    
    cur.execute("""INSERT INTO user_intents (sentence, intent) VALUES
    ('¿Puedes traducir esto al inglés?', 'translate'),
    ('Traduce esto al francés, por favor.', 'translate'),
    ('Necesito esta frase en italiano.', 'translate'),
    ('¿Cómo se dice "amor" en alemán?', 'translate'),
    ('Pon esta oración en portugués.', 'translate'),
    ('Quiero esta frase en japonés.', 'translate'),
    ('¿Me ayudas a traducir esto?', 'translate'),
    ('Tradúceme esto a chino.', 'translate'),
    ('Pásalo al árabe.', 'translate'),
    ('¿Cómo se traduce esta palabra?', 'translate'),
    ('Cambia esto al ruso.', 'translate'),
    ('Convierte esta frase al inglés.', 'translate'),
    ('¿Podrías traducir esto al coreano?', 'translate'),
    ('Hazme una traducción de esto.', 'translate'),
    ('Tradúcelo, por favor.', 'translate'),
    ('Pon esto en otro idioma.', 'translate'),
    ('Traducción al francés de esto, por favor.', 'translate'),
    ('Dime cómo decir esto en inglés.', 'translate'),
    ('¿Cuál es la traducción de esto al alemán?', 'translate'),
    ('Enséñame esto en japonés.', 'translate'),
    ('Tradúcelo al italiano.', 'translate'),
    ('Quiero saber cómo se dice esto en chino.', 'translate'),
    ('¿Cómo lo digo en árabe?', 'translate'),
    ('Convierte esto en portugués.', 'translate'),
    ('Dímelo en otro idioma.', 'translate'),
    ('Traduce esto a un idioma extranjero.', 'translate'),
    ('¿Me puedes decir esto en francés?', 'translate'),
    ('¿Qué significa esto en inglés?', 'translate'),
    ('¿Cuál es la palabra equivalente en japonés?', 'translate'),
    ('Escríbelo en ruso.', 'translate'),
    ('Necesito la versión inglesa.', 'translate'),
    ('Traduce la siguiente oración.', 'translate'),
    ('Tradúceme la siguiente frase.', 'translate'),
    ('Quiero saber la traducción.', 'translate'),
    ('¿Cómo lo traduzco?', 'translate'),
    ('¿Cómo se diría esto en alemán?', 'translate'),
    ('¿Cómo puedo decirlo en otro idioma?', 'translate'),
    ('Enséñame cómo se dice esto en coreano.', 'translate'),
    ('¿Me podrías traducir esto, por favor?', 'translate'),
    ('¿Podrías ponerlo en inglés?', 'translate'),
    ('Explícame esto en francés.', 'translate'),
    ('¿Puedes mostrarme la versión japonesa?', 'translate'),
    ('Traducime esto al portugués.', 'translate'),
    ('Pasalo a inglés.', 'translate'),
    ('¿Me das la traducción al chino?', 'translate'),
    ('¿Cuál sería la frase en ruso?', 'translate'),
    ('¿Cómo dirías esto en otro idioma?', 'translate'),
    ('Dime cómo se dice en inglés.', 'translate'),
    ('Transforma esta frase al árabe.', 'translate'),
    ('¿Podés traducirme esto?', 'translate'),
    ('¿Cómo se dice esta frase en inglés?', 'translate'),
    ('Traducí esta oración, por favor.', 'translate'),
    ('¿Puedes poner esto en francés?', 'translate'),
    ('¿Cuál es la traducción correcta de esto?', 'translate'),
    ('¿Esto cómo se dice en portugués?', 'translate'),
    ('Dame la traducción al italiano.', 'translate'),
    ('¿Podrías mostrarme cómo se dice esto en coreano?', 'translate'),
    ('Convierte esta palabra en inglés.', 'translate'),
    ('¿Esto cómo lo digo en chino?', 'translate'),
    ('Necesito que esto esté en otro idioma.', 'translate'),
    ('¿Puedes cambiar esto al ruso?', 'translate'),
    ('¿Me pasás la versión francesa?', 'translate'),
    ('Quisiera saber cómo se dice esto en alemán.', 'translate'),
    ('¿Cómo lo escribirías en japonés?', 'translate'),
    ('Decime esto en otro idioma.', 'translate'),
    ('Traducí esta palabra a inglés.', 'translate'),
    ('¿Cómo se traduce esta frase?', 'translate'),
    ('Pásame esto en inglés, por favor.', 'translate'),
    ('¿Cómo dirías esto en francés?', 'translate'),
    ('¿En qué idioma está esto? Traducímelo.', 'translate'),
    ('Dame esto traducido al español.', 'translate'),
    ('Tradúcelo al idioma que puedas.', 'translate'),
    ('¿Puedo ver esto en italiano?', 'translate'),
    ('¿Esto qué significa en inglés?', 'translate'),
    ('¿Cómo sonaría esto en portugués?', 'translate'),
    ('¿Cuál es el equivalente en alemán?', 'translate'),
    ('¿Puedo tener la traducción japonesa?', 'translate'),
    ('Traducílo, que no entiendo.', 'translate'),
    ('No entiendo esto, ¿lo traducís?', 'translate'),
    ('¿Podrías interpretarlo al inglés?', 'translate'),
    ('¿Cómo lo expresás en chino?', 'translate'),
    ('¿Qué dice esta frase en otro idioma?', 'translate'),
    ('¿Esto cómo lo leo en ruso?', 'translate'),
    ('¿Cómo suena esto en coreano?', 'translate'),
    ('¿Me lo escribís en inglés?', 'translate'),
    ('¿Puedes poner esta frase en japonés?', 'translate'),
    ('¿Cómo traduces esta palabra?', 'translate'),
    ('¿Cuál sería la versión portuguesa?', 'translate'),
    ('¿Esto está bien traducido?', 'translate'),
    ('¿Cuál es el significado en otro idioma?', 'translate'),
    ('Pásame la frase en otro idioma.', 'translate'),
    ('Traduce lo siguiente, por favor.', 'translate'),
    ('Escribilo en francés.', 'translate'),
    ('Necesito esto en alemán.', 'translate'),
    ('¿Cómo puedo traducir esto?', 'translate'),
    ('Quiero esto en otro idioma.', 'translate'),
    ('¿Cuál es la mejor traducción?', 'translate'),
    ('¿Me podés ayudar con la traducción?', 'translate'),
    ('Esto no lo entiendo, ¿me lo traducís?', 'translate'),
    ('Reescribí esto en inglés.', 'translate'),
    ('Escribime esto como si fuera francés.', 'translate');""")

    cur.execute("""INSERT INTO user_intents (sentence, intent) VALUES
    ('Lee esto en voz alta.', 'tts'),
    ('Por favor, pronuncia esto.', 'tts'),
    ('¿Puedes leerme esto?', 'tts'),
    ('Di esto en voz alta.', 'tts'),
    ('Lee la siguiente frase.', 'tts'),
    ('¿Puedes leer esto para mí?', 'tts'),
    ('Hazme la lectura de esto.', 'tts'),
    ('Por favor, pronuncia esta palabra.', 'tts'),
    ('¿Puedes hablarlo en voz alta?', 'tts'),
    ('Pronuncia esto por favor.', 'tts'),
    ('Dímelo en voz alta.', 'tts'),
    ('Lee esto en voz alta por favor.', 'tts'),
    ('¿Puedes decir esto en voz alta?', 'tts'),
    ('Quiero que leas esto en voz alta.', 'tts'),
    ('Lee esta frase para mí.', 'tts'),
    ('¿Puedes decirlo en voz alta?', 'tts'),
    ('Pronuncia esta oración.', 'tts'),
    ('Por favor, lee la siguiente frase en voz alta.', 'tts'),
    ('Pronuncia esto en voz alta.', 'tts'),
    ('¿Puedes decirme esto en voz alta?', 'tts'),
    ('Quiero que lo leas en voz alta.', 'tts'),
    ('Di en voz alta lo siguiente.', 'tts'),
    ('Lee en voz alta esta frase.', 'tts'),
    ('¿Puedes hacer que lea esto?', 'tts'),
    ('Quiero que pronuncies esta palabra.', 'tts'),
    ('Habla esto en voz alta.', 'tts'),
    ('Por favor, pronuncia esta frase.', 'tts'),
    ('¿Me lees esto en voz alta?', 'tts'),
    ('Dime esto en voz alta.', 'tts'),
    ('¿Puedes leerlo en voz alta?', 'tts'),
    ('Hazme la lectura de esta frase.', 'tts'),
    ('Lee esta palabra para mí.', 'tts'),
    ('Pronuncia la siguiente frase en voz alta.', 'tts'),
    ('¿Puedes leer la siguiente oración?', 'tts'),
    ('Habla esto por favor.', 'tts'),
    ('Quiero escuchar esto en voz alta.', 'tts'),
    ('¿Puedes decirme esta palabra en voz alta?', 'tts'),
    ('¿Me puedes leer esto?', 'tts'),
    ('Di esto para mí, por favor.', 'tts'),
    ('¿Podrías leer esto para mí?', 'tts'),
    ('Pronuncia lo siguiente en voz alta.', 'tts'),
    ('Dime cómo se escucha esto en voz alta.', 'tts'),
    ('¿Puedes leer esta frase en voz alta?', 'tts'),
    ('Quiero que me leas esta palabra.', 'tts'),
    ('¿Puedes pronunciar lo siguiente?', 'tts'),
    ('Haz que lea esto en voz alta.', 'tts'),
    ('¿Puedes pronunciar esta oración para mí?', 'tts'),
    ('¿Puedes leer esto en voz alta para mí?', 'tts'),
    ('Por favor, dilo en voz alta.', 'tts'),
    ('Quiero escuchar esto en voz alta.', 'tts'),
    ('¿Me puedes decir esto en voz alta?', 'tts'),
    ('Lee la siguiente oración en voz alta.', 'tts'),
    ('¿Puedes hablarlo por mí?', 'tts'),
    ('Pronuncia esta palabra para mí, por favor.', 'tts'),
    ('Dímelo fuerte y claro.', 'tts'),
    ('Di esto en voz alta, por favor.', 'tts'),
    ('¿Puedes leerlo en voz alta ahora?', 'tts'),
    ('Lee lo siguiente para mí.', 'tts'),
    ('¿Podrías pronunciar esto?', 'tts'),
    ('Habla en voz alta esto para mí.', 'tts'),
    ('Por favor, lee esto en voz alta.', 'tts'),
    ('Pronuncia lo siguiente en voz alta.', 'tts'),
    ('¿Puedes hacer que esto se lea en voz alta?', 'tts'),
    ('Di en voz alta lo que te pido.', 'tts'),
    ('¿Me podrías leer esto en voz alta?', 'tts'),
    ('¿Puedes leerlo de nuevo en voz alta?', 'tts'),
    ('Pronuncia esta frase de forma clara.', 'tts'),
    ('¿Puedes decir esta palabra claramente?', 'tts'),
    ('¿Te gustaría leer esto en voz alta?', 'tts'),
    ('Por favor, habla esto de forma clara.', 'tts'),
    ('¿Puedes pronunciar todo esto en voz alta?', 'tts'),
    ('Lee lo que acabo de escribir.', 'tts'),
    ('¿Puedes decirme esta frase en voz alta?', 'tts'),
    ('Por favor, repite esto en voz alta.', 'tts'),
    ('Hazme la lectura en voz alta.', 'tts'),
    ('¿Cómo suena esto en voz alta?', 'tts'),
    ('Lee esta palabra para mí en voz alta.', 'tts'),
    ('Di esto con claridad, por favor.', 'tts'),
    ('¿Puedes decir esta palabra en voz alta?', 'tts'),
    ('¿Podrías leer esto para mí en voz alta?', 'tts'),
    ('¿Puedes hablar en voz alta esta frase?', 'tts'),
    ('Quiero escuchar esto ahora, por favor.', 'tts'),
    ('Dímelo en voz alta, por favor.', 'tts'),
    ('¿Podrías pronunciar esta oración?', 'tts'),
    ('¿Cómo se oye esto en voz alta?', 'tts'),
    ('¿Puedes repetir esto en voz alta?', 'tts'),
    ('Por favor, pronuncia esta palabra clara y fuerte.', 'tts'),
    ('Haz que esto se lea en voz alta.', 'tts'),
    ('¿Podrías leer esto nuevamente en voz alta?', 'tts'),
    ('Lee esto con voz clara y alta.', 'tts'),
    ('Por favor, lee la frase completa.', 'tts'),
    ('Dime cómo se dice esto en voz alta.', 'tts'),
    ('¿Puedes repetirlo de nuevo en voz alta?', 'tts'),
    ('¿Podrías hablar esto en voz alta?', 'tts'),
    ('¿Puedes decir esta frase con claridad?', 'tts'),
    ('Quiero oír esto en voz alta.', 'tts'),
    ('Leeme esta palabra', 'tts'),
    ('Leeme esta texto', 'tts');""")


    cur.execute("""INSERT INTO user_intents (sentence, intent) VALUES
    ('¿Qué significa esta palabra?', 'define'),
    ('¿Puedes darme la definición de esto?', 'define'),
    ('¿Qué significa "amor" en español?', 'define'),
    ('Explícame el significado de esta palabra.', 'define'),
    ('¿Me puedes decir qué significa esto?', 'define'),
    ('¿Cuál es la definición de esta palabra?', 'define'),
    ('Dime el significado de esta palabra.', 'define'),
    ('¿Cómo se define esto?', 'define'),
    ('¿Qué quiere decir esta palabra?', 'define'),
    ('¿Cómo se interpreta esto?', 'define'),
    ('¿Qué significa "felicidad" en inglés?', 'define'),
    ('¿Puedes explicar qué significa esta palabra?', 'define'),
    ('¿Cómo se define "amistad"?', 'define'),
    ('Explícame qué significa esta frase.', 'define'),
    ('¿Qué significa "libertad" en este contexto?', 'define'),
    ('¿Puedes darme el significado de esta frase?', 'define'),
    ('¿Cuál es el significado de "familia"?', 'define'),
    ('¿Cómo puedo definir "cultura"?', 'define'),
    ('¿Qué significa "justicia"?', 'define'),
    ('Dime qué significa "equilibrio".', 'define'),
    ('¿Qué quiere decir "respeto"?', 'define'),
    ('¿Cómo puedo interpretar "honestidad"?', 'define'),
    ('¿Cuál es la definición de "valentía"?', 'define'),
    ('¿Qué significa "honradez"?', 'define'),
    ('¿Cómo se define "sabiduría"?', 'define'),
    ('¿Qué significa la palabra "amistad"?', 'define'),
    ('¿Me puedes decir qué significa "futuro"?', 'define'),
    ('¿Cómo se entiende "paz"?', 'define'),
    ('¿Puedes darme la definición de "esperanza"?', 'define'),
    ('¿Qué significa "responsabilidad"?', 'define'),
    ('¿Cómo se define "fuerza"?', 'define'),
    ('¿Qué significa la palabra "compasión"?', 'define'),
    ('¿Qué significa "sueño"?', 'define'),
    ('¿Cuál es la definición de "trabajo"?', 'define'),
    ('Dime qué significa "sabiduría" en este contexto.', 'define'),
    ('¿Qué significa "familia" para ti?', 'define'),
    ('Explícame qué es "amistad".', 'define'),
    ('¿Qué significa la palabra "alegría"?', 'define'),
    ('¿Cómo definirías "solidaridad"?', 'define'),
    ('¿Qué quiere decir "coraje"?', 'define'),
    ('¿Me puedes decir qué significa "confianza"?', 'define'),
    ('¿Cuál es el significado de "amor" en este contexto?', 'define'),
    ('¿Qué quiere decir "creatividad"?', 'define'),
    ('Dime la definición de "voluntad".', 'define'),
    ('¿Qué significa "conflicto"?', 'define'),
    ('¿Cómo se define "lucha"?', 'define'),
    ('¿Qué significa "honestidad" para ti?', 'define'),
    ('¿Qué quiere decir "lealtad"?', 'define'),
    ('¿Cómo se define "resiliencia"?', 'define'),
    ('¿Qué significa "responsabilidad" en este contexto?', 'define'),
    ('¿Cómo se define "emoción"?', 'define'),
    ('¿Qué significa la palabra "destino"?', 'define'),
    ('¿Qué quiere decir "innovación"?', 'define'),
    ('Dime el significado de "amistad" en este contexto.', 'define'),
    ('¿Cómo se entiende "poder"?', 'define'),
    ('¿Qué significa "dignidad"?', 'define'),
    ('Explícame qué significa "conciencia".', 'define'),
    ('¿Qué quiere decir "generosidad"?', 'define'),
    ('¿Cómo se define "trabajo en equipo"?', 'define'),
    ('¿Qué significa "compromiso"?', 'define'),
    ('¿Cuál es la definición de "intuición"?', 'define'),
    ('¿Qué significa "sabio"?', 'define'),
    ('¿Me puedes explicar el significado de "sentimiento"?', 'define'),
    ('¿Qué quiere decir "autonomía"?', 'define'),
    ('¿Cómo se define "perseverancia"?', 'define'),
    ('¿Qué significa "libertad de expresión"?', 'define'),
    ('Explícame qué es "honor".', 'define'),
    ('¿Qué significa "integridad"?', 'define'),
    ('¿Cómo definirías "compasión"?', 'define'),
    ('¿Qué significa "trabajo duro"?', 'define'),
    ('¿Qué quiere decir "respeto mutuo"?', 'define'),
    ('¿Qué significa "optimismo"?', 'define'),
    ('¿Cuál es la definición de "trabajo colaborativo"?', 'define'),
    ('¿Qué significa "solidaridad" en este contexto?', 'define'),
    ('¿Qué significa la palabra "reconocimiento"?', 'define'),
    ('¿Qué significa "mente abierta"?', 'define'),
    ('¿Qué quiere decir "empatía"?', 'define'),
    ('¿Cómo se entiende "esfuerzo"?', 'define'),
    ('¿Me puedes dar la definición de "confianza mutua"?', 'define'),
    ('¿Qué significa "crecimiento personal"?', 'define'),
    ('¿Qué significa "valentía" en este contexto?', 'define'),
    ('¿Cómo se define "madurez"?', 'define'),
    ('¿Qué significa "tolerancia"?', 'define'),
    ('¿Qué quiere decir "poder de decisión"?', 'define'),
    ('¿Cómo se define "sabiduría popular"?', 'define'),
    ('¿Qué significa "alegría" para ti?', 'define'),
    ('Explícame qué es "lucha por la justicia".', 'define'),
    ('¿Qué significa "paz interior"?', 'define'),
    ('¿Qué quiere decir "cooperación"?', 'define'),
    ('¿Cómo se define "responsabilidad social"?', 'define'),
    ('¿Qué significa "libertad individual"?', 'define'),
    ('¿Qué significa la palabra "fuerza de voluntad"?', 'define'),
    ('¿Cómo se entiende "superación personal"?', 'define'),
    ('¿Qué significa "empatía" en este contexto?', 'define'),
    ('¿Cuál es la definición de "creatividad" en este ámbito?', 'define'),
    ('Explícame qué significa "poder colectivo".', 'define'),
    ('¿Qué quiere decir "autodisciplina"?', 'define'),
    ('¿Qué significa "honestidad" para ti?', 'define'),
    ('¿Cómo se define "visión global"?', 'define');""")

    con.commit()
    
con.close()

print("Base de conocimientos creada")