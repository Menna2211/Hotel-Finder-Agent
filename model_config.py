from langchain_openai import ChatOpenAI
import os
from langchain_ollama import ChatOllama

openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
base_url = "https://openrouter.ai/api/v1"
model_name = "nvidia/nemotron-nano-12b-v2-vl:free"

def get_openrouter_llm():
    """Get OpenRouter LLM instance"""
    return ChatOpenAI(
        model=model_name,
        temperature=0.3,
        openai_api_key=openrouter_api_key,
        openai_api_base=base_url,
    )
    
def get_ollama_llm():
    """Get Ollama LLM instance using the new ChatOllama"""
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.3,
        base_url="http://localhost:11434",
    )
