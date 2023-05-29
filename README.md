# PruebasOpenAI

Son pruebas muy básicas que estoy haciendo para conocer las herramientas.

## ProbadoChatGPT
**Pruebas directas sobre OpenAI** 

Acá pruebo el modelo whisper de audio y también el consumo normal de la api de chatgpt. Funciona bien.

## Entrenando Modelo
**Pruebas directas sobre OpenAI**

Acá entro un modelo con datos POS (POS.jsonl), solo pido una respuesta de dos token, ya que las respuestas las tengo almacenadas.
El problema es que no me dice nunca: no sé.

## ProbandoLangChain
**Pruebas con LangChain**

Acá hago varias pruebas, pero la última es usar un agente con dos tool, una creada por mi y otra que ya existe para buscar en google. Funciona bien.

## ProbandoLangChainUCPOS
**Pruebas con LangChain**

Acá uso langchain sobre el modelo que entré anteriormente en EntrenandoModelo (que devuelve dos token).
Como solo devuelve dos token langchain no sabe que hacer con la respuesta y no funciona bien.


## ProbandoLangChainUCMaldo
**Pruebas con LangChain**

Acá uso una tool Apify que viene con langchain para hacer scrapping de la página de Maldonado. Solo tengo 5 doláres, así que el scrapping lo hace por la mitad y dura más de 5 horas.
Al agente le paso dos tool, una con el documento resultado del scrapping y otra para que me consulta la deuda.
Las preguntas sobre el scrapping diríamos que funcionan un 6 de 10. Lo que no conseguí aún resolver es que el agente se pare y le pida al usuario el padrón. Y que no continue hasta que el usuario le pase el padron
Tuve que modificar el archivo output_parser.py, sino el agente chat conversacional no entendía la salida.
Acá también hace el embedding cada vez que inicializa, eso es carísimo. Tengo que revisar como guardarlo en un archivo el índice y no hacerlo cada vez.


## ProbandoMasSalud
**Pruebas directas sobre OpenAI**
Scrapping de la página massalud.com.uy, tomando el ejemplo de: https://github.com/openai/openai-cookbook/tree/main/apps/web-crawl-q-and-a