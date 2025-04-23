import sqlite3
import random
import telebot
import openai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

user_sessions = {}

system_prompt = """Eres un chatbot diseñado para evaluar traducciones del ingles a español y vice-versa basadas en reglas específicas. Cuando un usuario envíe una traducción, debes evaluar su precisión comparándola con la traducción de referencia. Proporciona una puntuación del 1 al 10 y explica por qué el usuario obtuvo esa puntuación. La evaluación debe seguir estas reglas:

### Reglas de Evaluación:
1. **Puntuación 10/10**: La traducción es 100% precisa y gramaticalmente correcta, sin errores. Mantiene el significado, el tono y la estructura de la oración original.
2. **Puntuación 9/10**: La traducción es muy cercana a la original, pero tiene pequeños errores o diferencias en la elección de palabras o en la redacción que no afectan significativamente el significado.
3. **Puntuación 7/10**: La traducción es comprensible pero contiene varios errores u omisiones que afectan el significado o la estructura de la oración.
4. **Puntuación 5/10**: La traducción transmite el significado general pero tiene errores evidentes que dificultan la comprensión o la claridad.
5. **Puntuación 3/10**: La traducción es mayormente incorrecta, pero algunas palabras o frases aún se entienden parcialmente.
6. **Puntuación 1/10**: La traducción es mayormente incorrecta, con pocos elementos reconocibles de la oración original.
7. **Puntuación 0/10**: La traducción es completamente incorrecta y no transmite ningún significado relacionado con la oración original.

### Formato de Salida:
Para cada traducción, sigue este formato:

"<b>[Oración Original]</b>\n"
    "<code>{original}</code>\n\n"
    "<b>[Traducción del Usuario]</b>\n"
    "<code>{user_translation}</code>\n\n"
    "<b>[Puntuación]</b>\n"
    "<b>{score}/10 puntos</b>\n\n"
    "<b>[Razonamiento]</b>\n"
    "{reasoning}\n\n"
    "<b>[Motivación]</b>\n"
    "<i>{motivation}</i>"

### Ejemplos de Salida:

#### Ejemplo 1 (Traducción Perfecta):
- **Oración Original**: "The quick brown fox jumps over the lazy dog."
- **Traducción del Usuario**: "El rápido zorro marrón salta sobre el perro perezoso."
- **Puntuación**: 10/10 puntos
- **Razonamiento**: Tu traducción es perfecta. Has mantenido el significado, el tono y la estructura de la oración original sin ningún error.
- **Motivación**: ¡Buen trabajo! Sigue practicando para mejorar aún más.

#### Ejemplo 2 (Errores Moderados):
- **Oración Original**: "The quick brown fox jumps over the lazy dog."
- **Traducción del Usuario**: "El zorro marrón rápido salta por el perro flojo."
- **Puntuación**: 6/10 puntos
- **Razonamiento**: La traducción tiene algunos errores moderados. Aunque el significado sigue siendo comprensible, se utilizó "por" en lugar de "sobre", lo cual cambia ligeramente la imagen que transmite la frase. Además, "flojo" no es una traducción precisa de "lazy" en este contexto; "perezoso" sería más adecuado.
- **Motivación**: ¡Sigue practicando! Los errores son parte del aprendizaje.

#### Ejemplo 3 (Traducción Incorrecta):
- **Oración Original**: "The quick brown fox jumps over the lazy dog."
- **Traducción del Usuario**: "El zorro come el perro perezoso."
- **Puntuación**: 3/10 puntos
- **Razonamiento**: La traducción es mayormente incorrecta. Aunque usaste algunas palabras clave correctas, como "zorro" y "perro perezoso", la estructura y el significado están muy alejados de la oración original. Además, "come" no tiene sentido en este contexto.
- **Motivación**: ¡No te des por vencido! Asegúrate de practicar más las traducciones y revisar el significado de las palabras.

### Instrucciones Adicionales:
- Proporciona comentarios que sean **constructivos** y **motivadores**. El objetivo es ayudar al usuario a aprender y mejorar sus habilidades de traducción.
- Las explicaciones deben ser **claras** y **concisas**.
- **Siempre** proporciona el feedback en **español**.
- Dale formato al texto utilizando HTML en cumplimiento con las especificaciones y etiquetas que soporta el API de telegram.
"""

def get_sentence(difficulty, language_pair):
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    
    if language_pair == "es-en":
        language = "spanish"
    elif language_pair == "en-es":
        language = "english"
    else:
        return None, None
    
    query = "SELECT sentence FROM sentences WHERE difficulty = ? AND language = ?"
    cursor.execute(query, (difficulty, language))
    sentences = cursor.fetchall()
    conn.close()

    if sentences:
        return random.choice(sentences)[0]
    else:
        return None

def evaluate_translation(sentence, user_translation):
    prompt = f"Oración Original: {sentence}\n" \
             f"Traducción del Usuario: {user_translation}\n"

    response = openai.chat.completions.create(
        model="gpt-4.1-nano", 
        max_tokens=300,
        temperature=0.5,
        store=True,
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    )

    result = response.choices[0].message.content.strip()
    return result

def register_handlers(bot):

    @bot.message_handler(commands=['play'])
    def play_game(message):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("Español a Inglés", callback_data="lang_es-en"),
            InlineKeyboardButton("Inglés a Español", callback_data="lang_en-es")
        )
        bot.send_message(message.chat.id, """
        <b>¡Bienvenido al juego de traducciones!</b>
Por favor, elige el modo de juego:
        
        
        """, reply_markup=markup, parse_mode="HTML")


    @bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
    def handle_language_selection(call):
        language_pair = call.data.replace('lang_', '')
        user_sessions[call.from_user.id] = {"lang": language_pair}

        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("Fácil", callback_data="diff_easy"),
            InlineKeyboardButton("Intermedio", callback_data="diff_intermediate"),
            InlineKeyboardButton("Difícil", callback_data="diff_hard")
        )

        bot.edit_message_text("Elige la dificultad:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data.startswith('diff_'))
    def handle_difficulty_selection(call):
        user_id = call.from_user.id
        if user_id not in user_sessions:
            bot.send_message(call.message.chat.id, "Sesión no encontrada. Usa /play para empezar de nuevo.")
            return

        difficulty = call.data.replace('diff_', '')
        language_pair = user_sessions[user_id]['lang']
        sentence = get_sentence(difficulty, language_pair)

        if sentence:
            user_sessions[user_id].update({"difficulty": difficulty, "sentence": sentence})
            bot.edit_message_text(f"Traduce esta oración:\n\n{sentence}",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, "Escribe tu traducción:")
        else:
            bot.send_message(call.message.chat.id, "No se encontró ninguna oración para esa dificultad.")


    @bot.message_handler(func=lambda message: message.from_user.id in user_sessions and 'sentence' in user_sessions[message.from_user.id])
    def handle_user_translation(message):
        user_id = message.from_user.id
        data = user_sessions[user_id]
        sentence = data['sentence']
        user_translation = message.text.strip()

        result = evaluate_translation(sentence, user_translation)
        bot.send_message(message.chat.id,
            f"{result}",
            parse_mode="HTML"
        )

        del user_sessions[user_id]
        bot.send_message(message.chat.id, "¡Gracias por jugar! Usa /play para intentarlo de nuevo.")