# 🏦 EVA — A Persona-Driven Banking Chatbot with Streamlit & OpenAI (Part 6)

Meet **Eva**, a professional banking assistant chatbot that lives entirely in the browser — built with Streamlit's native chat UI and OpenAI's `gpt-4o-mini`, scoped to banking queries only, and remembering the conversation across turns using `st.session_state`.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Chat%20UI-FF4B4B?logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-412991?logo=openai&logoColor=white)
![Series](https://img.shields.io/badge/GenAI%20Series-Part%206-blueviolet)

---
### 🔗 Live Demo → ... **[https://banking-assistant-openai-chatbot.onrender.com/](https://banking-assistant-openai-chatbot.onrender.com/)**

## 📌 Overview

Part 5 of this series taught Streamlit's rerun model with plain widgets. This project fuses that model with a real LLM: a **domain-scoped chatbot** using Streamlit's purpose-built chat components (`st.chat_message`, `st.chat_input`) instead of generic text boxes — the same UI pattern behind every production chat product.

Eva has one job: answer banking questions, politely decline everything else, and remember the conversation as it goes.

---

## ✨ What the App Does

1. Displays a title and an opening assistant greeting
2. Renders the **full chat history** on every rerun, so past messages never disappear
3. Captures new input via `st.chat_input()` — a chat-style input bar pinned to the bottom
4. Displays the user's message instantly
5. Sends the **full conversation** to `gpt-4o-mini`, wrapped in a system prompt that defines Eva's persona and domain scope
6. Displays Eva's response in an assistant chat bubble

---

## 🔍 The Code, Section by Section

### 1️⃣ Persistent Chat History via Session State
```python
if "messages" not in st.session_state:
    st.session_state["messages"] = []
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])
```
Streamlit reruns the **entire script** on every interaction — without this redraw loop, the chat window would reset to blank after each message. `st.session_state` is Streamlit's answer to the "widgets forget everything" problem this series hit back in Part 4's memory demo, now solved the Streamlit-native way.

### 2️⃣ Native Chat Widgets
```python
user_input = st.chat_input()
```
`st.chat_input()` and `st.chat_message()` are Streamlit's dedicated chat components — rendering message bubbles with role-appropriate avatars, distinct from the generic `st.text_input()` used in Part 5.

### 3️⃣ The Persona System Prompt
```python
"content": """You are a professional Banker whose name is 'Eva'.
If someone asks your name, tell them that your name is 'EVA ChatBot'.
You can give answers about Banking related query and in case anyone asking
apart from Bank, please politely tell them that you are an expert in Banking..."""
```
A single paragraph does three jobs: **identity** (who the bot is), **scope** (what it will answer), and **refusal behaviour** (how it declines off-topic questions) — the same guardrail-through-instruction pattern from Part 4, now protecting a domain-specific assistant.

### 4️⃣ Calling the Model with Full History
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[system_message] + st.session_state['messages'])
```
The system prompt is prepended fresh on every call, followed by the accumulated conversation — so Eva always knows both her role and everything said so far.

---

## ⚠️ A Bug Worth Knowing About

Look closely at the message-saving logic:

```python
st.session_state["messages"].append({"role":"user","content":user_input})
response = client.chat.completions.create(...)
st.chat_message("assistant").write({response.choices[0].message.content})
# st.session_state["messages"].append({"role":"assistant", ...})   ← commented out!
```

**Eva's own replies are never saved back into `session_state`.** Only user messages accumulate; the assistant's side of the conversation is displayed but not remembered. Practically, this means Eva can see growing user context but has no memory of what *she* previously said — a subtle but real bug, and a good lesson in why testing multi-turn conversations (not just single exchanges) matters before shipping a chatbot.

---

## 🗂️ Folder Contents

```
06-eva-banking-chatbot-streamlit/
├── GenAI_05_Bot_Openai.py       # The application
├── requirements.txt             # Dependencies
├── README.md                    # This documentation
└── Project_Explanation.docx     # 250-word project summary
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation & Run

```bash
git clone https://github.com/Kailaswadje/genai-learning-series.git
cd genai-learning-series/06-eva-banking-chatbot-streamlit
pip install -r requirements.txt
streamlit run GenAI_05_Bot_Openai.py
```

> ⚠️ Set your API key via an environment variable or `getpass`-style prompt before running publicly — never hardcode or commit it. The original script reads from a local file path; replace this before deploying.

---

## 🧠 Key Takeaways

- **`st.session_state` is Streamlit's persistence layer** — the fix for the rerun model's biggest gotcha: everything resets unless you explicitly store it
- **Native chat widgets (`st.chat_input`, `st.chat_message`) beat generic inputs** for anything conversational — purpose-built UI, minimal code
- **A persona prompt is identity + scope + refusal, in one paragraph** — the pattern scales from teaching assistants to bankers to any domain expert
- **Multi-turn testing catches what single-message testing can't** — the assistant-memory bug here only shows up after 2+ exchanges, a real-world reminder to test conversations, not just messages
- This is the direct architectural ancestor of my deployed [LangChain-OpenAI Chatbot](https://github.com/Kailaswadje/Langchain-Openai-Chatbot)

---

## 📚 GenAI Series Navigation

| Part | Project | Focus |
|---|---|---|
| 01 | OpenAI API Hands-On | SDK fundamentals: chat, embeddings, images |
| 02 | Prompt Engineering with OpenAI | Zero-shot, few-shot, CoT, real tasks |
| 03 | Prompt Engineering with Gemini | Portability, grounding, hallucination probes |
| 04 | Conversational Chatbots | Memory, LangChain, flipped interaction |
| 05 | First Streamlit App | Frontend fundamentals, the rerun model |
| **06 (this folder)** | EVA Banking Chatbot | Session state, native chat UI, persona scoping |

---

## 🔮 Possible Extensions

- [ ] Fix the assistant-memory bug by uncommenting the append line
- [ ] Add a "New Conversation" button that clears `session_state`
- [ ] Add streaming responses for a real-time typing effect
- [ ] Swap the raw OpenAI SDK for LangChain's `RunnableWithMessageHistory` (Part 4 pattern) for cleaner memory management
- [ ] Add input guardrails to block PII (account numbers, passwords) from being sent to the model

---

## 👤 Author

**Kailas Wadje**
MSc Data Science & AI, University of Liverpool

- GitHub: [@Kailaswadje](https://github.com/Kailaswadje)
- LinkedIn: [linkedin.com/in/kwadaje](https://www.linkedin.com/in/kwadaje/)

---

## 🙏 Acknowledgements

Hands-on practice completed as part of the **Learnbay GenAI programme**.

---

⭐ If Eva helped you understand Streamlit chat apps, consider giving it a star!
