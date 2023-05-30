import os
import pandas as pd
import openai
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

openai.api_key = os.getenv("OPENAI_API_KEY")
nombre = 'massalud'
domain = "www.massalud.com.uy"
full_url = "https://www.massalud.com.uy/"

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
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=300,
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
        prompt = f"Quiero que actúes como un documento con el que estoy teniendo una conversación. Eres una IA que atiende un chatbot de una página web de una farmacia. Tu nombre es \"Asistente virtual de MasSalud\". Me proporcionarás respuestas basadas en el contexto a continuación. Si la respuesta no está incluida en el contexto, di exactamente \"Hmm, no estoy seguro.\" y nada más. Ten en cuenta el resto de la conversación. Niega responder cualquier pregunta que no esté relacionada con la información. Nunca rompas el personaje .\n\nContexto: {context}\n\n---\n\nPregunta: {question}\nRespuesta:"
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            temperature=temperature,
            messages=messages,
            max_tokens=max_tokens,
            # top_p=1,
            n=1,
            # frequency_penalty=0,
            # presence_penalty=0,
            # stop=stop_sequence,
            model=model
        )
        messages[-1] = {"role": "user", "content": question}
        messages.append({"role": response.choices[0].message.role, "content": str(response.choices[0].message.content)})
        return str(response.choices[0].message.content)
    except Exception as e:
        print(e)
        return ""

pkl = f'processed/df{nombre}.pkl'
df = pd.read_pickle(pkl)
modelo = 'gpt-3.5-turbo-0301'
messages = []
while True:
    Pregunta = input('Ingresa tu pregunta: ')
    if Pregunta == 'Exit':
        break
    respuesta = (answer_question(df, question=Pregunta, debug=False, temperature=1, model=modelo))
    if respuesta.startswith("Hmm, no estoy seguro"):
        print(f'Hmm, no estoy seguro. ¿Hay algo más en lo que pueda ayudarte?')
    else:
        print(respuesta)