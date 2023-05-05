import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

messages=[]

while True:
    Pregunta = input('Ingresa tu pregunta: ')
    if Pregunta == 'Exit':
        break
    messages.append({"role": "user", "content": Pregunta})
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0301",
      messages=messages
    )
    messages.append({"role": completion.choices[0].message.role, "content": str(completion.choices[0].message.content)})
    print(str(completion.choices[0].message.content))

# import os
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
#
# audio_file= open("C:\Seba\PruebasOpenAI\Jaime2.mp3", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# texto = str(transcript)
# texto = texto.encode('utf-8').decode('unicode_escape')
# print(transcript)
# print(texto)