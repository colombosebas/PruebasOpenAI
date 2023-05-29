# Acá la idea es probar un caso de uso de un modelo entrenado con preguntas de POS
from langchain.llms import OpenAI
import os


def seteoRespuesta(textoIn):
    texto = textoIn.strip()
    if texto == "000":
        return 'Saludo'
    elif texto == "001":
        return 'Ubicación'
    elif texto == "002":
        return 'POS bloqueado'
    elif texto == "003":
        return 'Rollo'
    elif texto == "004":
        return 'Terminar contrato/devolver POS'
    elif texto == "005":
        return 'Imprimir'
    elif texto == "006":
        return 'Parametrización forzado'
    elif texto == "007":
        return 'Reiniciar/Apagar POS'
    elif texto == "008":
        return 'Contratar'
    elif texto == "009":
        return 'POS no llega'
    elif texto == "010":
        return 'Deuda'
    elif texto == "011":
        return 'Formas de pago'
    elif texto == "999":
        return 'La pregunta no corresponde'

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
print(OpenAI.api_key)

llm = OpenAI()
llm = OpenAI(model_name="davinci:ft-geocom-uruguay:poscolombo-2023-05-25-16-10-54", temperature=0, max_tokens=2)
while True:
    Pregunta = input('Ingresa tu pregunta: ')
    if Pregunta == 'Exit':
        break
    PreguntaPreparada = Pregunta + '->'
    Respuesta = llm(PreguntaPreparada)
    print(f'Respuesta sin procesar: {Respuesta}')
    print(f'Respuesta procesada: {seteoRespuesta(Respuesta)}')