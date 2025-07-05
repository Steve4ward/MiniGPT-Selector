# 🧠 MiniGPT — A Lightweight ChatGPT-like Web App

MiniGPT is a lightweight web-based chat interface built with **Streamlit** and powered by **OpenRouter’s API** (using models like Mistral). It mimics the conversational experience of ChatGPT and supports multi-session history management and local persistence.

---

## 🚀 Features

- 💬 Chat interface powered by OpenRouter AI (e.g. `mistralai/mistral-7b-instruct`)
- 📁 Multiple named chat sessions
- 💾 Persistent chat history (saved as JSON files)
- 🧹 Clear and restart sessions
- 📥 Download session history
- 🎨 Simple clean UI with timestamps

---

## 🔧 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenRouter API](https://openrouter.ai/)
- `.env` config via [python-dotenv](https://pypi.org/project/python-dotenv/)
- Local JSON file storage for session management

---

## 📦 Installation

```bash
git clone https://github.com/steve4ward/mini-chatgpt.git
cd mini-chatgpt
python -m venv venv
.\venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
```

Create a .env file with:

```env
OPENROUTER_API_KEY=your-api-key-here
```
Then run:

```bash
streamlit run app.py
```

---

## 📂 History System

All chats are saved in the history/ folder as sessionname.json. You can:
- Select a previous session
- Start a new named session
- Download sessions via the sidebar

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙋‍♂️ Author

Made by Stefanos Forward
