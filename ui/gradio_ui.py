import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from agents import build_agent
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the agent
agent = build_agent()

def chat_with_agent(user_input):
    """Send user message to agent and extract only the final AI reply."""
    response = agent.invoke({"messages": [HumanMessage(content=user_input)]} ,   {"configurable": {"thread_id": "1"}})

    # Extract final AI message content
    if isinstance(response, dict) and "messages" in response:
        for msg in reversed(response["messages"]):
            if isinstance(msg, AIMessage) and msg.content.strip():
                return msg.content.strip()

    # Fallbacks
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response)


def respond(message, history):
    """Handle Gradio chat interaction."""
    bot_reply = chat_with_agent(message)
    history = history + [[message, bot_reply]]
    return "", history


with gr.Blocks() as demo:
    gr.Markdown("# 🏨 Hotel Booking Agent (LangGraph + Tavily Web Search)")
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(placeholder="Ask about hotels, e.g. 'Find 4-star hotels in Paris'")
    send_btn = gr.Button("Send")

    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

# 🚀 Launch the app
if __name__ == "__main__":
    demo.launch()
