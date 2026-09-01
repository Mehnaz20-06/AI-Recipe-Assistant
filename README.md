# 🍳 AI Recipe Assistant

> A memory-powered AI chatbot that learns your food preferences, allergies, and dietary restrictions to provide personalized recipe recommendations.

Built with **Python, Google Gemini, Mem0, Qdrant, and Streamlit**.
## 🌐 Live Demo

🚀 **[Try the AI Recipe Assistant](https://ai-recipe-assistant-qezhzqhe3tvuhz79s9jeat.streamlit.app/)**

---

## ✨ Features

-  **Long-term memory** — Remembers preferences across sessions
-  **Personalized recipes** — Tailors recipes using stored memories
-  **Diet-aware suggestions** — Considers allergies and dietary restrictions
-  **Natural conversation** — Chat naturally with the AI
-  **Secure configuration** — API keys stored securely
-  **Cloud-ready** — Uses Qdrant Cloud for persistent memory
-  **Streamlit UI** — Simple and interactive web interface

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   Streamlit UI   │
                    │      app.py      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Recipe Agent   │
                    │   Gemini AI      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Memory Manager  │
                    │      Mem0        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Qdrant Cloud   │
                    │  Vector Memory   │
                    └──────────────────┘
