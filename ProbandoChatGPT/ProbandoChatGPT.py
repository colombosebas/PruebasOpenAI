import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)
print(openai.Model.list())

#Prueba de conversación usando chatgpt
# messages=[]
#
# while True:
#     Pregunta = input('Ingresa tu pregunta: ')
#     if Pregunta == 'Exit':
#         break
#     messages.append({"role": "user", "content": Pregunta})
#     completion = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo-0301",
#       messages=messages,
#       n=1,
#       temperature=0.7
#     )
#     messages.append({"role": completion.choices[0].message.role, "content": str(completion.choices[0].message.content)})
#     print(str(completion.choices[0].message.content))

#prueba de transcripción de audio

# audio_file= open("C:\Seba\PruebasOpenAI\ProbandoChatGPT\Jaime.mp3", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# texto = str(transcript)
# texto = texto.encode('utf-8').decode('unicode_escape')
# print(transcript)
# print(texto)