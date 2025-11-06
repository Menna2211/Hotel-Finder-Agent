from langchain_openai import ChatOpenAI
import os
from langchain_ollama import ChatOllama

def get_openrouter_api_key():
    """Get OpenRouter API key from environment with fallback"""
    return os.getenv("OPENROUTER_API_KEY")

def get_openrouter_llm():
    """Get OpenRouter LLM instance"""
    openrouter_api_key = get_openrouter_api_key()
    base_url = "https://openrouter.ai/api/v1"
    model_name = "nvidia/nemotron-nano-12b-v2-vl:free"
    
    if not openrouter_api_key:
        raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable.")
    
    return ChatOpenAI(
        model=model_name,
        temperature=0.3,
        openai_api_key=openrouter_api_key,
        openai_api_base=base_url,
        max_tokens=2048,
    )
    
def get_ollama_llm():
    """Get Ollama LLM instance using the new ChatOllama"""
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.3,
        base_url="http://localhost:11434",
    )

def get_llm_with_fallback():
    """Get LLM with fallback from OpenRouter to Ollama"""
    try:
        return get_openrouter_llm()
    except Exception as e:
        print(f"OpenRouter failed: {e}. Falling back to Ollama...")
        return get_ollama_llm()