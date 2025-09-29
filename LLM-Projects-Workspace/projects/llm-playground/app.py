import streamlit as st
import sys
import os
from pathlib import Path

from api_config import APIConfig
import openai
import google.generativeai as genai
from groq import Groq

# Initialize API configuration
api_config = APIConfig()

def get_openai_response(user_input, messages, model):
    """Get response from OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_config.get_openai_key())
        
        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_anthropic_response(user_input, messages, model):
    """Get response from Anthropic API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_config.get_anthropic_key())
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = client.messages.create(
            model=model,
            messages=anthropic_messages,
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens,
        )
        
        return response.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def get_google_response(user_input, messages, model):
    """Get response from Google Gemini API"""
    try:
        genai.configure(api_key=api_config.get_gemini_key())
        model_instance = genai.GenerativeModel(model)
        
        # Convert messages to Google format
        chat_history = []
        for msg in messages[:-1]:  # Exclude the last message (current user input)
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        chat = model_instance.start_chat(history=chat_history)
        response = chat.send_message(user_input)
        
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def get_groq_response(user_input, messages, model):
    """Get response from Groq API"""
    try:
        client = Groq(api_key=api_config.get_groq_key())
        
        # Convert messages to Groq format
        groq_messages = []
        for msg in messages:
            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = client.chat.completions.create(
            model=model,
            messages=groq_messages,
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit page configuration
st.set_page_config(
    page_title="Venkat's LLM Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like interface
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin-top: 0px;
    }
    
    /* ChatGPT-style conversation layout */
    .chat-container {
        max-width: 768px;
        margin: 0 auto;
        padding: 20px;
        overflow-y: auto;
        scroll-behavior: smooth;
        padding-bottom: 40px;
    }
    
    .user-message {
        background-color: #f7f7f8;
        padding: 16px 20px;
        border-radius: 18px;
        margin: 16px 0;
        margin-left: 20%;
        position: relative;
        display: block !important;
        width: auto !important;
        animation: fadeInUp 0.3s ease-out;
        font-size: 15px;
        line-height: 1.5;
    }
    
    .assistant-message {
        background-color: transparent;
        padding: 16px 0;
        margin: 16px 0;
        position: relative;
        display: block !important;
        width: auto !important;
        animation: fadeInUp 0.3s ease-out;
        border-bottom: 1px solid #f0f0f0;
        font-size: 15px;
        line-height: 1.6;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-avatar, .assistant-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        position: absolute;
        top: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
    }
    
    .user-avatar {
        right: 15px;
        background-color: #19c37d;
        color: white;
    }
    
    .assistant-avatar {
        left: 15px;
        background-color: #ab68ff;
        color: white;
    }
    
    /* Override Streamlit's default styling */
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    
    .stMarkdown > div {
        background-color: transparent !important;
    }
    
    /* Custom scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Basic form styling without positioning conflicts */
    .stTextInput > div > div > input {
        padding: 12px 16px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #e5e5e5 !important;
    }

    .stButton > button {
        background: #19c37d !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background: #17b374 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = "Google"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemini-2.5-flash"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1000

# Sidebar for model selection and settings
with st.sidebar:
    st.title("🤖 Venkat's LLM Playground")
    
    # Provider selection
    provider = st.selectbox(
        "Select Provider",
        ["OpenAI", "Anthropic", "Google", "Groq"],
        index=["OpenAI", "Anthropic", "Google", "Groq"].index(st.session_state.selected_provider)
    )
    st.session_state.selected_provider = provider
    
    # Model selection based on provider
    if provider == "OpenAI":
        models = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
    elif provider == "Anthropic":
        models = ["claude-opus-4-1-20250805", "claude-opus-4-20250514", "claude-sonnet-4-20250514", "claude-3-7-sonnet-20250219", "claude-3-5-haiku-20241022"]
    elif provider == "Google":
        models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    elif provider == "Groq":
        models = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma-7b-it"]
    else:
        models = ["gemini-2.5-flash"]
    
    model = st.selectbox("Select Model", models)
    st.session_state.selected_model = model
    
    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 2.0, st.session_state.temperature, 0.1)
    st.session_state.temperature = temperature
    
    # Max tokens slider
    max_tokens = st.slider("Max Tokens", 100, 4000, st.session_state.max_tokens, 100)
    st.session_state.max_tokens = max_tokens
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="user-avatar">U</div>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="assistant-avatar">AI</div>
                <div style="margin-left: 50px;">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #8e8ea0;">
        <h3>Welcome to Venkat's LLM Playground! 👋</h3>
        <p>Start a conversation by typing a message below.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input form - Basic Streamlit implementation
st.markdown("---")
st.markdown("### 💬 Chat with AI")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Type your message here...", key="user_input")
    submitted = st.form_submit_button("Send Message", type="primary")

    if submitted and user_input:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response based on selected provider
        try:
            if st.session_state.selected_provider == "OpenAI":
                response = get_openai_response(user_input, st.session_state.messages, st.session_state.selected_model)
            elif st.session_state.selected_provider == "Anthropic":
                response = get_anthropic_response(user_input, st.session_state.messages, st.session_state.selected_model)
            elif st.session_state.selected_provider == "Google":
                response = get_google_response(user_input, st.session_state.messages, st.session_state.selected_model)
            elif st.session_state.selected_provider == "Groq":
                response = get_groq_response(user_input, st.session_state.messages, st.session_state.selected_model)
            else:
                response = "Provider not configured."
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
        
        # Rerun to update the display
        st.rerun()