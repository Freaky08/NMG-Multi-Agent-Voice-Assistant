from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Imports

from app.graph import build_graph
from app.voice.stt import STTAgent
from app.voice.tts import speak
from app.agents.conversational_agent import generate_speech


# Streamlit Config
st.set_page_config(
    page_title="Auto Dealership Voice Assistant",
    layout="centered"
)

st.title("🚗 Auto Dealership Voice Assistant")



# Helpers: Audio autoplay

def autoplay_audio(audio_path: str):
    if not audio_path or not os.path.exists(audio_path):
        return

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        encoded = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{encoded}" type="audio/mp3">
        </audio>
    """
    components.html(audio_html, height=0)


def speak_once(state: dict):
    """
    Speak response automatically only once per new response.
    """
    response = state.get("response")
    if response and state.get("_spoken") != response:
        audio_path = speak(response)
        autoplay_audio(audio_path)
        state["_spoken"] = response



# Initialize LangGraph
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()


# Initialize STT Agent
if "stt_agent" not in st.session_state:
    st.session_state.stt_agent = STTAgent()

# Initialize Agent State

if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "user_input": None,
        "intent": None,
        "car_type": None,
        "model": None,
        "date": None,
        "time": None,
        "available_models": None,
        "booking_details": None,
        "response": None,
        "_spoken": None
    }



if "ready_to_listen" not in st.session_state:
    st.session_state.ready_to_listen = False



# Voice Input Controls

st.markdown("### 🎙️ Speak to the Assistant")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Start Recording"):

        
        #GREETING ONLY
        
        if (
            st.session_state.agent_state["user_input"] is None
            and not st.session_state.ready_to_listen
        ):
            st.session_state.agent_state = st.session_state.graph.invoke(
                st.session_state.agent_state
            )

            st.success(st.session_state.agent_state["response"])
            speak_once(st.session_state.agent_state)


            st.session_state.ready_to_listen = True


        # START LISTENING
    
        else:
            st.session_state.stt_agent.start_recording()
            st.info("Listening... Speak now")

with col2:
    if st.button("⏹ Stop & Transcribe"):
        with st.spinner("Transcribing..."):
            user_text = st.session_state.stt_agent.stop_and_transcribe()

        if user_text:
            st.write("**You said:**", user_text)

            st.session_state.agent_state["user_input"] = user_text
            st.session_state.agent_state = st.session_state.graph.invoke(
                st.session_state.agent_state
            )
        else:
            st.warning("No speech detected.")




if (
    st.session_state.agent_state.get("available_models")
    and not st.session_state.agent_state.get("model")
    and not st.session_state.agent_state.get("booking_details")
):
    st.session_state.agent_state = generate_speech(
        st.session_state.agent_state
    )
    st.info(st.session_state.agent_state["response"])
    speak_once(st.session_state.agent_state)



#Booking Confirmation

if st.session_state.agent_state.get("booking_details"):
    st.session_state.agent_state = generate_speech(
        st.session_state.agent_state
    )
    st.success(st.session_state.agent_state["response"])
    speak_once(st.session_state.agent_state)
