import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the agent with caching
@st.cache_resource
def load_agent(openrouter_key=None):
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
    return build_agent()

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

# Sidebar configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # OpenRouter API Key input
    st.subheader("OpenRouter API Key")
    openrouter_key = st.text_input(
        "Enter your OpenRouter API Key:",
        type="password",
        placeholder="sk-or-v1-...",
        help="Get your API key from https://openrouter.ai/keys"
    )
    
    # Store API key in session state
    if openrouter_key:
        st.session_state.openrouter_key = openrouter_key
        st.success("✅ API Key saved!")
    elif "openrouter_key" in st.session_state:
        openrouter_key = st.session_state.openrouter_key
    else:
        st.warning("⚠️ Please enter your OpenRouter API key to start chatting")
    
    st.markdown("---")
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
    
    # Display current configuration
    st.markdown("---")
    st.subheader("Current Settings")
    if "openrouter_key" in st.session_state:
        st.code(f"API Key: {st.session_state.openrouter_key[:10]}...")
    else:
        st.code("API Key: Not set")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent only if API key is provided
if "openrouter_key" in st.session_state and st.session_state.openrouter_key:
    try:
        agent = load_agent(st.session_state.openrouter_key)
        agent_ready = True
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {str(e)}")
        agent_ready = False
else:
    agent_ready = False
    st.info("🔑 Please enter your OpenRouter API key in the sidebar to start chatting")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input only if agent is ready
if agent_ready:
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
else:
    st.chat_input("Enter your OpenRouter API key in the sidebar to enable chatting", disabled=True)