from agents.agent_builder import build_agent
from langchain_core.messages import HumanMessage, AIMessage

def main():
    print("🏨 Hotel Booking Agent (CLI Mode)")
    print("Type 'exit' or 'quit' to end.\n")

    # 1️⃣ Build the LangChain Agent
    agent = build_agent()

    # 2️⃣ Chat Loop
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            # ✅ Proper invoke structure
            response = agent.invoke({"messages": [HumanMessage(content=user_input)]} , {"configurable": {"thread_id": "1"}})

            # ✅ Extract only the final AI answer
            message = None
            if isinstance(response, dict) and "messages" in response:
                for msg in reversed(response["messages"]):
                    if isinstance(msg, AIMessage) and msg.content.strip():
                        message = msg.content.strip()
                        break

            # fallback
            if not message:
                message = str(response)

        except Exception as e:
            message = f"⚠️ Error: {e}"

        print(f"Agent: {message}\n")


if __name__ == "__main__":
    main()
