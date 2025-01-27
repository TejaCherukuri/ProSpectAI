from langchain_groq import ChatGroq
import os

class ChatModel:
    def __init__(self,):
        self.groq = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model="deepseek-r1-distill-llama-70b")