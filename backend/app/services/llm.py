from langchain_huggingface import HuggingFaceEndpoint,HuggingFaceEmbeddings, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("HUGGINGFACEHUB_API_KEY")

llm=HuggingFaceEmbeddings(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=api_key,
    max_new_token=3000,
    temperature=0.4
)

model=ChatHuggingFace(llm=llm)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
