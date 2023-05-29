# Acá la idea es probar un caso de uso de un scraping a una web y hacer consultas de la misma con una tool de consulta de deuda
import json

from langchain.llms import OpenAIChat
import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import Tool
from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
from langchain.document_loaders import TextLoader


os.environ['SERPAPI_API_KEY'] = 'Poner clave'
# os.environ["APIFY_API_TOKEN"] = "Poner clave"
OpenAIChat.api_key = os.getenv("OPENAI_API_KEY")
# apify = ApifyWrapper()
print(OpenAIChat.api_key)

# loader = apify.call_actor(
#     actor_id="apify/website-content-crawler",
#     run_input={"startUrls": [{"url": "https://www.maldonado.gub.uy/"}]},
#     dataset_mapping_function=lambda item: Document(
#         page_content=item["text"] or "", metadata={"source": item["url"]}
#     ),
# )

#Definiendo funciones propias
def consultaDeuda(padron):
    ## Es necesario que el usuario indique su número de padron o CM para obtener la deuda.
    try:
        intpadron = int(padron)
        if intpadron <= 1000:
            return f'La consulta de deuda del padron {padron} es de $1500'
        elif intpadron >= 1001 and intpadron <= 3000:
            return f'La consulta de deuda del padron {padron} es de $4500'
        elif intpadron >= 3001 and intpadron <= 6000:
            return f'La consulta de deuda del padron {padron} es de $6500'
        else:
            return f'La consulta de deuda del padron {padron} es de $10500'
    except ValueError:
        return 'Debes solicitar al usuario humano que proporcione el [número de padrón], el cual es un entero.'

def consultaDocumento(query):
    result = index.query_with_sources(query)
    return (result["answer"])

tool_Deuda = Tool(
    name="Consulta de deuda",
    func=consultaDeuda,
    description="This tool is used to retrieve the debt value. Priority should be given to this tool over others. In order to use this tool, it is essential that you provide the [Número padrón]. If you don't have it, you must ask the user to provide it. This tool should only receive the enrollment number, which is an integer.",
    return_direct = False,
)

tool_ConsultaDocumento = Tool(
    name="Consulta en documento",
    func=consultaDocumento,
    description="In this tool, all queries should be performed here, unless they are debt-related queries. In that case, the tool should be consulted.",#"En esta tool se deben realizar todas las consultas, a no ser que sean consulta sobre deuda, en ese caso se debe consultar la tool tool_Deuda."
    return_direct = False,
)

loader = TextLoader('scrape.txt', encoding='utf8')
print(f'Comienza a crear el índice')
index = VectorstoreIndexCreator().from_loaders([loader])
print(f'Termina de crear el índice')

# while True:
#     Pregunta = input('Ingresa tu pregunta: ')
#     result = index.query_with_sources(Pregunta)
#     print(result["answer"])

llm = OpenAIChat(temperature=0)
tools = [tool_ConsultaDocumento, tool_Deuda]
conversational_memory = ConversationBufferWindowMemory(memory_key='chat_history', k=5,return_messages=True)
agent = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, max_iterations=3, memory=conversational_memory)
while True:
    Pregunta = input('Ingresa tu pregunta: ')
    if Pregunta == 'Exit':
        break
    agent.run(Pregunta)

