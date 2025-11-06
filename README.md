# Hotel Finder Agent 🏨

An intelligent AI-powered hotel finding assistant that helps users discover and book hotels based on their preferences and requirements. Built with LangChain for agent orchestration, featuring persistent memory through MemoryServer, intelligent web search via Tavily API, and flexible model selection with OpenRouter.

## Technologies Used

- 🔗 [LangChain](https://python.langchain.com/) - For building and managing the AI agent
- 🧠 MemoryServer - For persistent conversation memory
- 🔍 [Tavily API](https://tavily.com/) - For intelligent web search capabilities
- 🤖 [OpenRouter](https://openrouter.ai/) - For flexible AI model selection and routing

## LangChain Components

The project utilizes several LangChain components:
- Agents for task orchestration
- Memory for conversation persistence
- Tools for web search and information retrieval
- Chains for complex reasoning tasks
- Prompts for structured interactions

## Features

- 🤖 AI-powered hotel search and recommendations
- 🔍 Natural language understanding for processing user queries
- 🌐 Web search integration for real-time hotel information
- 📱 Multiple UI options (Gradio and Streamlit)
- 🎯 Contextual understanding of user preferences
- 💬 Interactive conversation-based search experience

## Project Structure

```
Hotel-Finder-Agent/
├── agents/                 # AI agent implementation
│   ├── __init__.py
│   └── agent_builder.py    # Agent construction and configuration
├── tools/                  # Agent tools and utilities
│   ├── __init__.py
│   └── web_search_tool.py # Web search integration
├── ui/                     # User interface implementations
│   ├── gradio_ui.py       # Gradio-based UI
│   └── streamlit_app.py   # Streamlit-based UI
├── main.py                # Application entry point
├── model_config.py        # AI model configuration
└── requirements.txt       # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Menna2211/Hotel-Finder-Agent.git
cd Hotel-Finder-Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys:
Create a `.env` file in the root directory with the following environment variables:
```env
TAVILY_API_KEY=your_tavily_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

### Streamlit Interface
To run the application with Streamlit UI:
```bash
streamlit run ui/streamlit_app.py
```

### Gradio Interface
To run the application with Gradio UI:
```bash
python ui/gradio_ui.py
```

## Configuration

The agent's behavior and model settings can be configured in `model_config.py`. Adjust parameters like:
- Model selection through OpenRouter (choose from various AI models)
- Memory configuration for MemoryServer integration
- Tavily API search parameters
- Temperature and other model settings
- Response formatting preferences
- Search result filtering and ranking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.


## Acknowledgments

- Thanks to all contributors and users of this project
- Built with Python, LangChain, and modern AI technologies
