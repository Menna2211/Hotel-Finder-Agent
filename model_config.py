from langchain_openai import ChatOpenAI
import os
from langchain_ollama import ChatOllama


def get_openrouter_llm(api_key=None):
    """Get OpenRouter LLM instance"""
    # Get API key from parameter, environment, or raise error
    openrouter_api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    base_url = "https://openrouter.ai/api/v1"
    model_name = "nvidia/nemotron-nano-12b-v2-vl:free"
    
    if not openrouter_api_key:
        raise ValueError("OpenRouter API key not found. Please provide an API key.")
    
    # Set both environment variables to be safe
    os.environ["OPENAI_API_KEY"] = openrouter_api_key
    os.environ["OPENROUTER_API_KEY"] = openrouter_api_key
    
    return ChatOpenAI(
        model=model_name,
        temperature=0.3,
        api_key=openrouter_api_key,  # Use api_key parameter
        base_url=base_url,
        max_tokens=2048,
    )
    
def get_ollama_llm():
    """Get Ollama LLM instance using the new ChatOllama"""
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.3,
        base_url="http://localhost:11434",
    )

def get_llm_with_fallback(api_key=None):
    """Get LLM with fallback from OpenRouter to Ollama"""
    try:
        return get_openrouter_llm(api_key)
    except Exception as e:
        print(f"OpenRouter failed: {e}. Falling back to Ollama...")
        return get_ollama_llm()