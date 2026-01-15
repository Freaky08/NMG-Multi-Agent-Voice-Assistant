# 🚗 Auto Dealership Voice Assistant

A multi-agent, voice-enabled assistant for booking test drives at an auto dealership.

## ✨ Features
- Voice-based interaction (STT + TTS)
- Multi-agent architecture using LangGraph
- Knowledge-based car discovery
- Test drive booking with dummy database
- Automatic voice responses (no play button)
- Streamlit web UI

## 🧠 Architecture
Agents involved:
- Conversational Agent – intent & slot extraction
- Knowledge Agent – fetches car models from JSON
- Booking Agent – stores bookings in a dummy DB

## 🛠️ Tech Stack
- Python
- Streamlit
- LangGraph / LangChain
- OpenAI (LLM only)
- Whisper (transformers)
- gTTS

## 🚀 How to Run

### 1. Clone the repo

git clone https://github.com/<your-username>/Auto-Dealership-Voice-Assistant.git
cd Auto-Dealership-Voice-Assistant

### 2. Create virtual environment

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### 3. Install dependencies


pip install -r requirements.txt

### 4. Set environment variables

Create a .env file:
OPENAI_API_KEY=your_api_key_here

### 5. Run the app

streamlit run streamlit_app.py

📁 Data
cars.json – car models & features

bookings.json – stores test drive bookings

📌 Notes
Audio autoplay requires user interaction (browser restriction)
.env file is ignored for security
