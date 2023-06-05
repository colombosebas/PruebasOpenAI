import os
import pandas as pd
import openai
from openai.embeddings_utils import distances_from_embeddings
from flask import Flask
from flask import request

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
nombre = 'massalud'
# full_url = "https://www.massalud.com.uy/"

def create_context(question, df, max_len=1800, size="ada"):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_question(df,
    model="text-davinci-003",
    question="Hola, cómo estas?",
    max_len=1800,
    size="ada",
    debug=False,
    messages = [],
    preguntas = [],
    max_tokens=190,
    stop_sequence=None,
    temperature=0
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        prompt = f"\n\nContexto: {context}\n\n---\n\nDiálogo: {preguntas}\n\n---\n\nPregunta: {question}\nRespuesta:"
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            temperature=temperature,
            messages=messages,
            max_tokens=max_tokens,
            # top_p=1,
            n=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            stop=stop_sequence,
            model=model
        )
        return str(response.choices[0].message.content)
    except Exception as e:
        print(e)
        return "Excepcion"

@app.route('/envioPregunta', methods=['POST'])
def envioPregunta():
    conversation = [{"role": "system","content": "Tienes que actuar como un asistente virtual de una web de una farmacia llamada Más Salud. Nunca rompas el personaje. Al contexto lo debes llamar \"sitio de Más Salud\" .Tu nombre es \"Asistente virtual de Más Salud\". Me proporcionarás respuestas basadas en el contexto que te pasaré en cada pregunta. Si la respuesta no está incluida en el contexto, di exactamente \"Hmm, no estoy seguro.\" y detente ahí. Debes continuar el diálago, revisa tus mensajes anteriores antes de responder. Nunca preguntes si desean reservar, solo ofrece información. Niega responder cualquier pregunta que no esté relacionada con la información."}]
    preguntas = []
    datosIn = request.get_json()
    preguntasrespuestas = datosIn.get("conversación")
    pregunta = datosIn.get("pregunta")
    if pregunta.lower() in ["sí", "sí.", "si", "si."]:
        pregunta = pregunta + ', por favor.'
    respuesta = (answer_question(df, question=pregunta, messages=conversation, preguntas=preguntasrespuestas, debug=False, temperature=1, model=modelo))
    if respuesta.startswith("Hmm, no estoy seguro"):
        return f'Hmm, no estoy seguro. ¿Hay algo más en lo que pueda ayudarte?'
    elif respuesta == 'Excepcion':
        return f'Ups... parece que hemos tenido un problema y nuestro Asistente virtual se ha ido a descansar. ¿Podrías volver a intentarlo?'
    elif respuesta == '':
        return f'Ups... parece que hemos tenido un problema y nuestro Asistente virtual se ha ido a descansar. ¿Podrías volver a intentarlo?'
    else:
        return respuesta


pkl = f'processed/df{nombre}.pkl'
df = pd.read_pickle(pkl)
modelo = 'gpt-3.5-turbo-0301'
messages = []
app.run()