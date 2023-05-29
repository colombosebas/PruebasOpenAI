import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

#En terminal
#openai tools fine_tunes.prepare_data -f POS.jsonl
#Esto lo que hace es analizar el archivo POS y en base a aceptar sus sugerencias se crea el archivo POS_prepared

#En terminal
# openai api fine_tunes.create -t POS.jsonl -m ada --suffix POS1Colombo
#Aquí le pedimos que entrene un modelo ada con el archivo POS_prepared
#Modelo devuelto: ft-Nhn3VWYE0RrV9nK47k0yKdTp
#Nombre del modelo: davinci:ft-geocom-uruguay:poscolombo-2023-05-25-16-10-54

#En terminal
#openai api fine_tunes.list
#le pedimos que nos liste los modelos creados y nos dice si ya están pronto o aún no. Demora bastante el que esté pronto un modelo, y eso que probé con uno mínúsculo

def seteoRespuesta(texto):
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

modelo = 'ada:ft-personal-2023-05-09-14-28-18'
while True:
    Pregunta = input('Ingresa tu pregunta (escribe exit para salir): ')
    if Pregunta == 'exit':
        break
    completion = openai.Completion.create(
      model=modelo,
      prompt=Pregunta + "->",
      max_tokens=2,
      temperature=0.1,
      top_p=0.1,
      n=1,
      logprobs=2
    )
    numero = str(completion['choices'][0]['text']).strip()
    print(f'{numero} {seteoRespuesta(numero)}')
    token_completions = completion['choices'][0]['logprobs']['token_logprobs']
    token_probs = [10 ** p for p in token_completions]
    max_prob = max(token_probs)
    confianza = max_prob / sum(token_probs)
    print(f'Confianza: {confianza}')
    print('************************************')
    # print(completion)
