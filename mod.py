import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# point the SAME client at Groq instead of OpenAI
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

models = client.models.list()

for model in models.data:
    print(model.id)
