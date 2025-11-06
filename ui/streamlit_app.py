# app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the agent
@st.cache_resource
def load_agent():
    return build_agent()

agent = load_agent()

def chat_with_agent(user_input):
    """Send user message to agent and extract only the final AI reply."""
    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            {"configurable": {"thread_id": "1"}}
        )

        # Extract final AI message content
        if isinstance(response, dict) and "messages" in response:
            for msg in reversed(response["messages"]):
                if isinstance(msg, AIMessage) and msg.content.strip():
                    return msg.content.strip()

        # Fallbacks
        if hasattr(response, "content"):
            return response.content.strip()
        return str(response)
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Hotel Finder Agent", page_icon="🏨")
st.title("🏨 Hotel Finder Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about hotels, e.g., 'Find 4-star hotels in Paris'"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    with st.spinner("Searching for hotels..."):
        response = chat_with_agent(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with additional controls
with st.sidebar:
    st.header("Chat Controls")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.subheader("About")
    st.markdown("""
    This chatbot can help you:
    - Find hotels by location and star rating
    - Compare hotel prices and amenities
    - Get recent reviews and availability
    - Book hotels based on your preferences
    """)
    
    st.markdown("---")
    st.markdown("💡 **Tips:**")
    st.markdown("- Be specific about location and dates")
    st.markdown("- Mention your budget and preferences")
    st.markdown("- Ask about amenities or special requirements")