import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime, UTC 

from pathlib import Path

HISTORY_DIR = Path("history")
HISTORY_DIR.mkdir(exist_ok=True)
DEFAULT_SESSION = "session_default"

def get_history_path():
    session = st.session_state.get("session_name", DEFAULT_SESSION)
    return HISTORY_DIR / f"{session}.json"

def save_chat_history():
    with open(get_history_path(), "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)

def load_chat_history():
    path = get_history_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            st.session_state.messages = json.load(f)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(
    page_title="Mini ChatGPT",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    """
    <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding-right: 10px;
            margin-bottom: 1rem;
            border: 1px solid #e6e6e6;
            border-radius: 8px;
            background-color: #f9f9f9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if "session_name" not in st.session_state:
    st.session_state.session_name = DEFAULT_SESSION
    load_chat_history()
    if "messages" not in st.session_state:
        st.session_state.messages = []

st.title("MiniGPT")
# st.markdown("## 🤖 Mini ChatGPT")
st.markdown("Chat with an assistant powered by OpenRouter.")

chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            timestamp = msg.get("timestamp")
            if timestamp:
                readable = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
                st.caption(f"🕒 {readable}")
            st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
    st.markdown('</div>', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    prompt = st.text_input("You:")
    submitted = st.form_submit_button("Send")

with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 💾 Session Controls")

    # Discover all session history files
    session_files = [f.stem for f in HISTORY_DIR.glob("*.json")]
    current_session = st.session_state.get("session_name", DEFAULT_SESSION)
    session_selected = st.selectbox("📂 Load Previous Session", session_files, index=session_files.index(current_session) if current_session in session_files else 0)

    with st.form(key="new_session_form"):
        new_session_name = st.text_input("🆕 New Session Name")
        create_clicked = st.form_submit_button("➕ Start New Session")

        if create_clicked and new_session_name.strip():
            st.session_state.session_name = new_session_name.strip()
            st.session_state.messages = []
            save_chat_history()
            st.rerun()

    if session_selected != st.session_state.get("session_name"):
        st.session_state.session_name = session_selected
        load_chat_history()
        st.rerun()
    
    
    path = get_history_path()
    with open(path, "rb") as f:
        st.download_button("📥 Download This Session", f, file_name=f"{st.session_state.session_name}.json")

if submitted and prompt:
    user_msg = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now(UTC).isoformat()
    }
    st.session_state.messages.append(user_msg)

    with st.spinner("Thinking..."):
        try:
            messages_for_openai = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=messages_for_openai
            )
            reply_content = response.choices[0].message.content

        except Exception as e:
            reply_content = f"⚠️ Error: {str(e)}"

    assistant_msg = {
        "role": "assistant",
        "content": reply_content,
        "timestamp": datetime.now(UTC).isoformat()
    }
    st.session_state.messages.append(assistant_msg)
    save_chat_history()

    st.rerun()
