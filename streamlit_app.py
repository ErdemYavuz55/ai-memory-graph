import streamlit as st
import requests
import datetime
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie
import json

# ========================
# Backend API URL
# ========================
BACKEND_URL = "https://ai-memory-graph.onrender.com"

# ========================
# Page Config
# ========================
st.set_page_config(page_title="AI Memory Graph", layout="wide", page_icon="🧠")

# ========================
# Header with Animation
# ========================
def load_lottieurl(url: str):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json")

col1, col2 = st.columns([4, 1])
with col1:
    st.title("🧠 AI Memory Graph")
    st.markdown("A visual way to extract and understand chat memories using NLP + Graphs.")
with col2:
    st_lottie(lottie_ai, height=100, key="ai")

add_vertical_space(2)

# ========================
# Chat Input
# ========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.container():
    st.subheader("💬 Add Chat Messages")
    sender = st.text_input("Sender")
    text = st.text_area("Message")
    if st.button("➕ Add Message"):
        if sender and text:
            st.session_state["messages"].append({
                "sender": sender,
                "text": text,
                "timestamp": datetime.datetime.utcnow().isoformat()
            })
            st.success("Message added!")

# ========================
# Show Current Messages
# ========================
if st.session_state["messages"]:
    st.write("### 📑 Current Messages")
    st.json(st.session_state["messages"])

    add_vertical_space(1)

    col1, col2, col3 = st.columns(3)

    # Extract Triplets
    with col1:
        if st.button("🔍 Extract Triplets"):
            resp = requests.post(f"{BACKEND_URL}/extract", json=st.session_state["messages"])
            if resp.status_code == 200:
                st.success("Triplets extracted!")
                st.json(resp.json())
            else:
                st.error(f"Error {resp.status_code}")

    # Memory Summary
    with col2:
        if st.button("📝 Memory Summary"):
            resp = requests.post(f"{BACKEND_URL}/memory-summary", json=st.session_state["messages"])
            if resp.status_code == 200:
                st.info("Summary:")
                st.json(resp.json())
            else:
                st.error(f"Error {resp.status_code}")

    # Graph
    with col3:
        if st.button("🌐 Show Graph"):
            resp = requests.post(f"{BACKEND_URL}/graph-html", json=st.session_state["messages"])
            if resp.status_code == 200:
                st.components.v1.html(resp.text, height=600, scrolling=True)
            else:
                st.error(f"Error {resp.status_code}")

