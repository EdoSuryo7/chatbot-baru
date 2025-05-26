#import libraries
import streamlit as st
import requests
import json
from datetime import datetime
import os

# Function to load chat history from file
def load_chat_history():
    chat_history_file = "chat_history.json"
    if os.path.exists(chat_history_file):
        try:
            with open(chat_history_file, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading chat history: {str(e)}")
            return []
    return []

# Function to save chat history to file
def save_chat_history(chat_history):
    chat_history_file = "chat_history.json"
    try:
        with open(chat_history_file, "w", encoding='utf-8') as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving chat history: {str(e)}")

# Set page config to wide mode and remove default menu
st.set_page_config(
    page_title="AI Chatbot Kasultanan Bulakan",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat bubbles and fixed header
st.markdown("""
<style>
/* Fixed Header Styles */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #8B0000;
    background-image: linear-gradient(45deg, #8B0000 25%, #A00000 25%, #A00000 50%, #8B0000 50%, #8B0000 75%, #A00000 75%, #A00000 100%);
    background-size: 56.57px 56.57px;
    color: white;
    padding: 0.8rem 1.5rem;
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    height: 90px;
    border-bottom: 2px solid #FFD700;
}

.header-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
    padding: 5px 0;
    line-height: 1.4;
}

.header-subtitle {
    font-size: 0.9rem;
    opacity: 0.85;
    margin: 0;
    padding: 3px 0;
    line-height: 1.2;
}

/* Container for header text */
.header-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
    padding: 10px 0;
}

/* Content padding to account for new header height */
.content {
    margin-top: 100px;
    padding: 10px;
    margin-bottom: 70px; /* Add space for input box */
    background-color: #f5f1e6;
    background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23a17f1a' fill-opacity='0.05'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    min-height: calc(100vh - 170px);
}

body {
    background-color: #f5f1e6 !important;
}

/* Chat container styles */
.chat-container {
    display: flex;
    align-items: flex-start;
    margin: 10px 0;
    flex-direction: row;
    max-width: 100%;
}

.chat-container.user {
    flex-direction: row-reverse;
}

/* Avatar styles */
.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    margin: 0 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: white;
    flex-shrink: 0;
}

.user-avatar {
    background-color: #128C7E;
}

.assistant-avatar {
    background-color: #9575CD;
}

/* Chat bubble styles */
.user-bubble {
    background-color: #E8F3FF;
    border-radius: 15px 0 15px 15px;
    padding: 10px 15px;
    margin: 0;
    max-width: 100%;
    position: relative;
    word-wrap: break-word;
    overflow-wrap: break-word;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(173, 216, 230, 0.5);
}

.assistant-bubble {
    background-color: #FFF5F5;
    border-radius: 0 15px 15px 15px;
    padding: 10px 15px;
    margin: 0;
    max-width: 100%;
    position: relative;
    word-wrap: break-word;
    overflow-wrap: break-word;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 182, 193, 0.5);
}

/* Message group styles */
.message-group {
    display: flex;
    flex-direction: column;
    max-width: 70%;
}

.user-group {
    align-items: flex-end;
}

.assistant-group {
    align-items: flex-start;
}

.timestamp {
    font-size: 0.7em;
    color: #666;
    margin-top: 3px;
    text-align: right;
    padding-right: 5px;
}

/* Make sure messages don't overflow */
div[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0 !important;
    overflow: hidden;
    max-width: 100%;
}

/* Streamlit container adjustments */
.stMarkdown {
    background: transparent !important;
    max-width: 100% !important;
}

.element-container {
    max-width: 100% !important;
}

/* Ensure proper spacing around chat elements */
.stChatMessage {
    margin: 0 !important;
    padding: 0 !important;
}

/* Additional improvements for mobile responsiveness */
@media (max-width: 768px) {
    .message-group {
        max-width: 85%;
    }
    
    .avatar {
        width: 30px;
        height: 30px;
        font-size: 14px;
    }
}

/* Hide default Streamlit header */
header[data-testid="stHeader"] {
    display: none;
}

/* Style for main content area */
section[data-testid="stSidebar"] > div {
    padding-top: 0rem;
}

section.main > div {
    padding-top: 0rem;
}

/* Adjust input box position */
.stChatInputContainer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    padding: 1rem;
    z-index: 1000;
}
</style>

<div class="header">
    <h1 class="header-title">🧠 AI Chatbot Kasultanan Bulakan</h1>
    <p class="header-subtitle">Powered by {MODEL} via OpenRouter 🤖</p>
</div>
<div class="content">
""", unsafe_allow_html=True)

#API Configuration
OPENROUTER_API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3-0324"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://chatbot-baru.streamlit.app/",
    "X-Title": "AI Chatbot Streamlit",
    "Content-Type": "application/json"
}
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        bubble_class = "user-bubble" if chat["role"] == "user" else "assistant-bubble"
        container_class = "user" if chat["role"] == "user" else "assistant"
        group_class = "user-group" if chat["role"] == "user" else "assistant-group"
        avatar_class = "user-avatar" if chat["role"] == "user" else "assistant-avatar"
        avatar_text = "👤" if chat["role"] == "user" else "🤖"
        
        st.markdown(f"""
            <div class="chat-container {container_class}">
                <div class="avatar {avatar_class}">{avatar_text}</div>
                <div class="message-group {group_class}">
                    <div class="{bubble_class}">
                        {chat["content"]}
                        <div class="timestamp">{chat.get('timestamp', '')}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Add closing div for content
st.markdown("</div>", unsafe_allow_html=True)

# Get user input
user_input = st.chat_input("Tulis pesan di sini...")

# Handle message submission
if user_input:
    # Get current timestamp
    current_time = datetime.now().strftime("%H:%M")
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"""
            <div class="chat-container user">
                <div class="avatar user-avatar">👤</div>
                <div class="message-group user-group">
                    <div class="user-bubble">
                        {user_input}
                        <div class="timestamp">{current_time}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Save to session state and persistent storage
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input,
        "timestamp": current_time
    })
    save_chat_history(st.session_state.chat_history)

    # Make API call
    with st.spinner("Sultan Menjawab..."):
        # Prepare messages including full chat history
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history])
        
        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            # Send request to API
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json=payload,
                timeout=30
            )
            
            # Handle response
            if response.status_code == 200:
                try:
                    bot_reply = response.json()['choices'][0]['message']['content']
                except (KeyError, IndexError, json.JSONDecodeError) as e:
                    st.error(f"Error parsing API response: {str(e)}")
                    bot_reply = "⚠️ Maaf, terjadi kesalahan dalam memproses respons."
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                bot_reply = f"⚠️ Maaf, gagal mengambil respons dari OpenRouter. Status: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            bot_reply = "⚠️ Maaf, terjadi masalah koneksi ke server."
        
        # Get current timestamp for bot response
        current_time = datetime.now().strftime("%H:%M")
        
        # Display bot response with timestamp
        with st.chat_message("assistant"):
            st.markdown(f"""
                <div class="chat-container assistant">
                    <div class="avatar assistant-avatar">🤖</div>
                    <div class="message-group assistant-group">
                        <div class="assistant-bubble">
                            {bot_reply}
                            <div class="timestamp">{current_time}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # Save bot response to session state and persistent storage
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": bot_reply,
            "timestamp": current_time
        })
        save_chat_history(st.session_state.chat_history)
        
#end of code
