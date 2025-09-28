from flask import Flask, request, jsonify, render_template_string
import os
import json

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Playground</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 20px;
        }
        
        .sidebar {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: fit-content;
        }
        
        .chat-area {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            height: 600px;
        }
        
        .messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            border-bottom: 1px solid #eee;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 80%;
        }
        
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
        }
        
        .assistant-message {
            background: #f1f3f4;
            color: #333;
        }
        
        .input-area {
            padding: 20px;
            display: flex;
            gap: 10px;
        }
        
        .input-area input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .input-area button {
            padding: 12px 24px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .input-area button:hover {
            background: #0056b3;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        .form-group select, .form-group input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .sidebar {
                order: 2;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 LLM Playground</h1>
            <p>Chat with multiple AI models in one place</p>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <div class="form-group">
                    <label for="provider">AI Provider:</label>
                    <select id="provider" onchange="updateModels()">
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="google">Google</option>
                        <option value="groq">Groq</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="model">Model:</label>
                    <select id="model">
                        <option value="gpt-4o">GPT-4o</option>
                        <option value="gpt-4o-mini">GPT-4o Mini</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="temperature">Temperature: <span id="temp-value">0.7</span></label>
                    <input type="range" id="temperature" min="0" max="2" step="0.1" value="0.7" oninput="updateTempValue()">
                </div>
                
                <div class="form-group">
                    <label for="max-tokens">Max Tokens:</label>
                    <input type="number" id="max-tokens" value="1000" min="1" max="4000">
                </div>
                
                <button onclick="clearChat()" style="width: 100%; padding: 10px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer;">
                    Clear Chat
                </button>
            </div>
            
            <div class="chat-area">
                <div class="messages" id="messages">
                    <div style="text-align: center; padding: 40px; color: #666;">
                        <h3>Welcome! 👋</h3>
                        <p>Start a conversation by typing a message below.</p>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <p>🤔 Thinking...</p>
                </div>
                
                <div class="input-area">
                    <input type="text" id="user-input" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const models = {
            openai: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'],
            anthropic: ['claude-opus-4-1-20250805', 'claude-opus-4-20250514', 'claude-sonnet-4-20250514', 'claude-3-7-sonnet-20250219', 'claude-3-5-haiku-20241022'],
            google: ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b'],
            groq: ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768', 'gemma-7b-it']
        };
        
        let messages = [];
        
        function updateModels() {
            const provider = document.getElementById('provider').value;
            const modelSelect = document.getElementById('model');
            modelSelect.innerHTML = '';
            
            models[provider].forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
        }
        
        function updateTempValue() {
            const temp = document.getElementById('temperature').value;
            document.getElementById('temp-value').textContent = temp;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            userInput.value = '';
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            
            // Get AI response
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        provider: document.getElementById('provider').value,
                        model: document.getElementById('model').value,
                        temperature: parseFloat(document.getElementById('temperature').value),
                        max_tokens: parseInt(document.getElementById('max-tokens').value),
                        messages: messages
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    addMessage(data.response, 'assistant');
                } else {
                    addMessage('Error: ' + data.error, 'assistant');
                }
            } catch (error) {
                addMessage('Error: Failed to get response', 'assistant');
            }
            
            // Hide loading
            document.getElementById('loading').style.display = 'none';
        }
        
        function addMessage(content, role) {
            messages.push({role, content});
            
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}-message`;
            messageDiv.textContent = content;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            // Remove welcome message if it exists
            const welcome = messagesDiv.querySelector('div[style*="text-align: center"]');
            if (welcome) welcome.remove();
        }
        
        function clearChat() {
            messages = [];
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <h3>Welcome! 👋</h3>
                    <p>Start a conversation by typing a message below.</p>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        provider = data.get('provider')
        model = data.get('model')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        messages = data.get('messages', [])
        
        # Add user message to conversation
        messages.append({"role": "user", "content": message})
        
        # Get response based on provider
        if provider == 'openai':
            response = get_openai_response(messages, model, temperature, max_tokens)
        elif provider == 'anthropic':
            response = get_anthropic_response(messages, model, temperature, max_tokens)
        elif provider == 'google':
            response = get_google_response(messages, model, temperature, max_tokens)
        elif provider == 'groq':
            response = get_groq_response(messages, model, temperature, max_tokens)
        else:
            return jsonify({"success": False, "error": "Invalid provider"})
        
        return jsonify({"success": True, "response": response})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_openai_response(messages, model, temperature, max_tokens):
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"

def get_anthropic_response(messages, model, temperature, max_tokens):
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Anthropic Error: {str(e)}"

def get_google_response(messages, model, temperature, max_tokens):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        model_instance = genai.GenerativeModel(model)
        
        # Convert messages to Google format
        conversation_text = ""
        for msg in messages:
            role = "Human" if msg["role"] == "user" else "Assistant"
            conversation_text += f"{role}: {msg['content']}\n"
        
        response = model_instance.generate_content(
            conversation_text,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        
        return response.text
    except Exception as e:
        return f"Google Error: {str(e)}"

def get_groq_response(messages, model, temperature, max_tokens):
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)