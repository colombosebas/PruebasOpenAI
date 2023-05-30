from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import os
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.human import HumanInputLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import Tool

os.environ['SERPAPI_API_KEY'] = 'cbef55ab87fe0a81be0f5611b82b23d390368031d6fdd14b836bd65238019aca'
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
print(OpenAI.api_key)


# llm = OpenAI()
# llm = OpenAI(model_name="text-davinci-003", n=1, best_of=1)
# text = "Cual sería un buen nombre para una compañia que hace una plataforma omnicanal de atención y donde se pueden configurar chatbots?"
# print(llm(text))
# llm_result = llm.generate(["Dime un chiste", "Dime un poema corto"]*2)
# print(llm_result)
# print(len(llm_result.generations))
# print(llm_result.llm_output)
# *******************************************************

# llmchat = ChatOpenAI()
# llmchat = ChatOpenAI(model_name="gpt-3.5-turbo-0301",temperature=0)
# text = "Cual sería un buen nombre para una compañia que hace una plataforma omnicanal de atención y donde se pueden configurar chatbots?"
# print(llmchat(text))
# *******************************************************
# tools = load_tools(["wikipedia"])
# llm = HumanInputLLM(prompt_func=lambda prompt: print(f"\n===PROMPT====\n{prompt}\n=====END OF PROMPT======"))
# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# agent.run("What is 'Bocchi the Rock!'?")


# *******************************************************
# prompt = PromptTemplate(
#     input_variables=["product"],
#     template="What is a good name for a company that makes {product}?",
# )
# print(prompt.format(product="colorful socks"))

# *******************************************************
# string_prompt = PromptTemplate.from_template("tell me a joke about {subject}")
# string_prompt_value = string_prompt.format_prompt(subject="soccer")
# string_prompt_value.to_string()
# string_prompt_value.to_messages()
# *******************************************************
# An example prompt with no input variables
# no_input_prompt = PromptTemplate(input_variables=[], template="Tell me a joke.")
# print(no_input_prompt.format())
# -> "Tell me a joke."

# An example prompt with one input variable
# one_input_prompt = PromptTemplate(input_variables=["adjective"], template="Tell me a {adjective} joke.")
# print(one_input_prompt.format(adjective="funny"))
# -> "Tell me a funny joke."

# An example prompt with multiple input variables
# multiple_input_prompt = PromptTemplate(
#     input_variables=["adjective", "content"],
#     template="Tell me a {adjective} joke about {content}."
# )
# print(multiple_input_prompt.format(adjective="funny", content="chickens"))
# -> "Tell me a funny joke about chickens."

#Uso básico de un agente
# llm = OpenAI(temperature=0)
# tools = load_tools(["serpapi", "llm-math"], llm=llm)
# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

#Definiendo una función propia
def edadSebastian(x):
    return '37'

tool_Edad = Tool(
    name="Edad de Sebastian",
    func=edadSebastian,
    description="Es útil para saber la edad de Sebastian Colombo Cabanas, siempre que se pregunté la edad de Sebastián Colombo se debe usar primero esta tool",
    return_direct = False,
)


llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
tools.append(tool_Edad)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.run("Podrías decirme la edad de Sebastián Colombo y si es mayor que Cristiano Ronaldo.")