import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the agent with caching - include API key in cache key
@st.cache_resource
def load_agent(api_key):
    """Load agent with the provided API key"""
    return build_agent(api_key)

def test_openrouter_connection(api_key):
    """Test OpenRouter connection directly"""
    try:
        from model_config import get_openrouter_llm
        llm = get_openrouter_llm(api_key)
        
        # Test with a simple message
        response = llm.invoke("Say 'Hello' in 2 words")
        return True, f"Connection successful! Response: {response.content}"
    except Exception as e:
        return False, str(e)

def chat_with_agent(user_input):
    """Send user message to agent and extract only the final AI reply."""
    try:
        if 'agent' not in st.session_state or st.session_state.agent is None:
            return "Agent not initialized. Please initialize the agent first."
            
        response = st.session_state.agent.invoke(
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
        help="Get your API key from https://openrouter.ai/keys",
        key="api_key_input"
    )
    
    # Store API key in session state when entered
    if openrouter_key:
        st.session_state.openrouter_key = openrouter_key
        st.success("✅ API Key saved!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Test Connection button
        if st.button("Test Connection"):
            if openrouter_key:
                with st.spinner("Testing connection..."):
                    success, message = test_openrouter_connection(openrouter_key)
                    if success:
                        st.success("✅ " + message)
                        st.session_state.connection_tested = True
                    else:
                        st.error(f"❌ {message}")
                        st.session_state.connection_tested = False
            else:
                st.warning("⚠️ Please enter an API key first")
    
    with col2:
        # Initialize Agent button
        if st.button("Initialize Agent"):
            if openrouter_key:
                with st.spinner("Initializing agent..."):
                    try:
                        # Clear cache and load new agent with API key
                        load_agent.clear()
                        agent_instance = load_agent(openrouter_key)
                        st.session_state.agent = agent_instance
                        st.session_state.agent_initialized = True
                        st.success("✅ Agent initialized successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to initialize agent: {str(e)}")
                        st.session_state.agent_initialized = False
            else:
                st.warning("⚠️ Please enter an API key first")
    
    st.markdown("---")
    st.header("Chat Controls")
    
    if st.button("Clear Chat History"):
        if "messages" in st.session_state:
            st.session_state.messages = []
        st.rerun()
    
    if st.button("Reset Everything"):
        keys_to_remove = ['openrouter_key', 'agent_initialized', 'connection_tested', 'messages', 'agent']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        load_agent.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("Current Status")
    if "openrouter_key" in st.session_state:
        st.code(f"API Key: {st.session_state.openrouter_key[:10]}...")
    else:
        st.code("API Key: Not set")
        
    if "connection_tested" in st.session_state:
        st.code(f"Connection: {'✅ Tested' if st.session_state.connection_tested else '❌ Failed'}")
    else:
        st.code("Connection: Not tested")
        
    if "agent_initialized" in st.session_state:
        st.code(f"Agent: {'✅ Initialized' if st.session_state.agent_initialized else '❌ Not initialized'}")
    else:
        st.code("Agent: Not initialized")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input only if agent is ready
if st.session_state.get("agent_initialized") and st.session_state.agent:
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
    st.chat_input("Configure and initialize agent to start chatting", disabled=True)
    
    # Help messages
    if not st.session_state.get("openrouter_key"):
        st.info("🔑 **Step 1:** Enter your OpenRouter API key in the sidebar")
    elif not st.session_state.get("agent_initialized"):
        st.info("🚀 **Step 2:** Click 'Initialize Agent' to start chatting")