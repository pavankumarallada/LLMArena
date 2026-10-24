# pip install streamlit openai python-dotenv
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Both clients point to Groq (same as your Gradio code)
openai_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def ask(client, model, prompt):
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def battle(prompt):
    a = ask(openai_client, "openai/gpt-oss-120b", prompt)
    b = ask(groq_client, "openai/gpt-oss-20b", prompt)
    return a, b

# ---------- Streamlit UI ----------
st.set_page_config(page_title="LLM Arena", layout="wide")
st.title("🥊 LLM Arena — one prompt, two models")

# Session state for outputs + votes
if "out_a" not in st.session_state:
    st.session_state.out_a = ""
if "out_b" not in st.session_state:
    st.session_state.out_b = ""
if "verdict" not in st.session_state:
    st.session_state.verdict = ""

prompt = st.text_area("Ask both models the same thing", height=100)

if st.button("⚔️ Battle!", type="primary"):
    if prompt.strip():
        with st.spinner("Battling..."):
            a, b = battle(prompt)
            st.session_state.out_a = a
            st.session_state.out_b = b
            st.session_state.verdict = ""
    else:
        st.warning("Please enter a prompt first.")

# Two columns for the two models
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🤖 Model A")
    st.markdown(st.session_state.out_a or "_No response yet_")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("👍", key="up_a"):
            st.session_state.verdict = "🗳️ Thanks! You voted: **👍 Model A**"
    with b2:
        if st.button("👎", key="down_a"):
            st.session_state.verdict = "🗳️ Thanks! You voted: **👎 Model A**"

with col_b:
    st.subheader("🤖 Model B")
    st.markdown(st.session_state.out_b or "_No response yet_")
    b3, b4 = st.columns(2)
    with b3:
        if st.button("👍", key="up_b"):
            st.session_state.verdict = "🗳️ Thanks! You voted: **👍 Model B**"
    with b4:
        if st.button("👎", key="down_b"):
            st.session_state.verdict = "🗳️ Thanks! You voted: **👎 Model B**"

# Show the vote result
if st.session_state.verdict:
    st.markdown(st.session_state.verdict)