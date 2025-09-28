# 🤖 LLM Playground

A clean, intuitive web interface for interacting with multiple Large Language Models (LLMs) including OpenAI GPT, Google Gemini, and Groq models.

## ✨ Features

- **Multi-Provider Support**: Switch between OpenAI, Google Gemini, and Groq models
- **Clean ChatGPT-like Interface**: Modern, responsive design with chat bubbles
- **Multiple Chat Sessions**: Create and manage multiple conversation threads
- **Model Configuration**: Adjust temperature, max tokens, and other parameters
- **Real-time Responses**: Stream responses from your selected LLM
- **Chat History**: Keep track of all your conversations
- **Secure API Management**: Uses the workspace's centralized API key system

## 🚀 Quick Start

### Prerequisites

Make sure you have your API keys configured in the workspace `.env` file:
```bash
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
```

### Installation

1. **Navigate to the playground directory:**
   ```bash
   cd projects/llm-playground
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

## 🎯 Usage

### Getting Started
1. **Select a Provider**: Choose from OpenAI, Google Gemini, or Groq in the sidebar
2. **Pick a Model**: Select the specific model you want to use
3. **Adjust Settings**: Configure temperature and max tokens as needed
4. **Start Chatting**: Type your message and press Send or Enter

### Features Overview

#### 🔧 Model Settings
- **Provider Selection**: Switch between different AI providers
- **Model Selection**: Choose from available models for each provider
- **Temperature Control**: Adjust creativity/randomness (0.0 - 2.0)
- **Max Tokens**: Set response length limits

#### 💬 Chat Management
- **New Chat**: Start fresh conversations anytime
- **Chat History**: Access previous conversation sessions
- **Clear Chat**: Reset the current conversation
- **Session Switching**: Jump between different chat threads

#### 🎨 Interface Features
- **Responsive Design**: Works on desktop and mobile
- **Message Bubbles**: Clear distinction between user and AI messages
- **Real-time Updates**: Instant message display and responses
- **Loading Indicators**: Visual feedback during AI processing

## 🔧 Configuration

### Available Models

**OpenAI:**
- GPT-4
- GPT-4 Turbo
- GPT-3.5 Turbo

**Google Gemini:**
- Gemini Pro
- Gemini Pro Vision

**Groq:**
- Llama2 70B
- Mixtral 8x7B
- Gemma 7B

### Settings Explanation

- **Temperature**: Controls randomness in responses
  - `0.0`: Deterministic, focused responses
  - `1.0`: Balanced creativity and coherence
  - `2.0`: Maximum creativity and randomness

- **Max Tokens**: Limits response length
  - Lower values: Shorter, more concise responses
  - Higher values: Longer, more detailed responses

## 🛠️ Troubleshooting

### Common Issues

1. **"No API keys configured" error**
   - Check your `.env` file in the workspace root
   - Ensure API keys are properly formatted without quotes
   - Restart the application after updating keys

2. **Model not responding**
   - Verify your API key has sufficient credits/quota
   - Check your internet connection
   - Try switching to a different model or provider

3. **Import errors**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Ensure you're in the correct directory
   - Check Python version compatibility

### Performance Tips

- **Use GPT-3.5 Turbo** for faster responses and lower costs
- **Adjust max tokens** based on your needs (lower = faster)
- **Set temperature to 0.7** for balanced responses
- **Clear chat history** periodically to improve performance

## 🔒 Security

- API keys are managed through the workspace's secure `.env` system
- Keys are never exposed in the interface or logs
- All communications use HTTPS when deployed
- No conversation data is stored permanently

## 🎨 Customization

The interface can be customized by modifying the CSS in `app.py`:
- Change color schemes in the `<style>` section
- Adjust layout dimensions and spacing
- Modify chat bubble designs
- Update fonts and typography

## 📝 Development

### Project Structure
```
llm-playground/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

### Adding New Providers
1. Add client initialization in `get_api_clients()`
2. Update the provider selection list
3. Add model options for the new provider
4. Implement the API call logic in the response generation section

## 🤝 Contributing

Feel free to enhance the playground by:
- Adding new LLM providers
- Improving the UI/UX design
- Adding new features (file uploads, conversation export, etc.)
- Optimizing performance
- Adding more configuration options

## 📄 License

This project is part of the LLM-Projects-Workspace and follows the same licensing terms.

---

**Happy Chatting!** 🚀 Enjoy exploring different LLMs with this intuitive playground interface.