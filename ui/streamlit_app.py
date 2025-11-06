import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# Load agent with API key
@st.cache_resource
def load_agent(api_key: str):
    return build_agent(api_key)

# Chat with agent
def chat_with_agent(user_input):
    response = st.session_state.agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        {"configurable": {"thread_id": "1"}}
    )

    # Extract final AI message content
    if isinstance(response, dict) and "messages" in response:
        for msg in reversed(response["messages"]):
            if isinstance(msg, AIMessage) and msg.content.strip():
                return msg.content.strip()
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response)

# Streamlit UI
st.set_page_config(page_title="Hotel Finder Agent", page_icon="🏨")
st.title("🏨 Hotel Finder Agent")

# Sidebar: OpenRouter API key
with st.sidebar:
    st.header("🔑 API Key")
    api_key = st.text_input("Enter your OpenRouter API key:", type="password")
    
    if st.button("Initialize Agent") and api_key:
        try:
            st.session_state.agent = load_agent(api_key)
            st.success("✅ Agent initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize agent: {str(e)}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (only enabled if agent is initialized)
if st.session_state.get("agent"):
    if prompt := st.chat_input("Ask about hotels, e.g., 'Find 4-star hotels in Makkah'"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Searching for hotels..."):
            response = chat_with_agent(prompt)
        
        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.chat_input("Enter API key and initialize agent to start chatting.", disabled=True)
