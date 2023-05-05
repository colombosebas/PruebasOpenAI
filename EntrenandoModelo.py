import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

faq_data = open('FAQs.txt', encoding="utf-8")
listafaqs = faq_data.read()
faq_data.close()

openai.Model.create(
    id="modelo_pruebas_inac",
    training_data=listafaqs,
    model="gpt-3.5-turbo-0301",
    prompt_language="es",
    max_tokens=50,
    n_epochs=1,
    batch_size=4
)
