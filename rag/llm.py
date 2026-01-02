# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",  
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

