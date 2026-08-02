import streamlit as st
from openai import OpenAI

# API Key is required
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

st.title("GENAI ChatBot 🤖 ")
st.chat_message("assistant").write("Hi, How may I help you?")

## below code checks for memory.. first time it would be empty , so it createa s empty list
# loop thru every message in memory and displays the mesg
# first time user msg and then assistant msg and so on
#Streamlit reruns the entire script every time the user sends a message.
#Without this loop:for msg in st.session_state["messages"]:
#all old messages would disappear.The loop redraws the entire chat history from memory every time.

if "messages" not in st.session_state:
            st.session_state["messages"] = []
for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
# taking user input 
user_input = st.chat_input()
# check if user entered something  
if user_input:
          # display user message immediately
        st.chat_message("user").write(user_input)
            # Store user message in memory for bot to remember 
        st.session_state["messages"].append({"role":"user","content":user_input})
        response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[ {"role":"system",
"content":"""
You are a professional Banker whose name is 'Eva'.
If someone asks your name, tell them that your name is 'EVA ChatBot'.
You can give answers about Banking related query and in case anyone asking apart from Bank,
please politely tell them that you are an expert in Banking and hence please ask banking related query only and don't give answer which is not relevant to Bank.
""" }] + st.session_state['messages'])
        assistant_reply = response.choices[0].message.content

        st.chat_message("assistant").write(assistant_reply)
        st.session_state["messages"].append({
                "role": "assistant",
                "content": assistant_reply
})
      # st.session_state["messages"].append({"role":"user","content":user_input})
      # st.session_state["messages"].append({"role":"assistant","content":response.choices[0].message.content})


# line 31 onwards above calls the LLM AND gives clear prompt-instructions  to the model and appends all chat history
# response from gpt is displayed as an assitant chat  and then append to memory
# so basically bot replied is stored for future context 
#One-line summary
#User types → display user message → save to memory → 
# send history to GPT → display response → save response to memory. 
