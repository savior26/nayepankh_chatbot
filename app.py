from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# Initialize the Gemini Client
# Make sure your system environment variable GOOGLE_API_KEY is configured
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")
client = genai.Client(api_key=GOOGLE_API_KEY)

# Global dictionary acting as session memory tracking
SESSION_MEMORY = {}

SYSTEM_PROMPT = """
You are the official conversational digital representative for NayePankh Foundation, 
a leading youth-led NGO registered in Uttar Pradesh (12A & 80G certified), dedicated to uplifting underprivileged communities through impactful initiatives.
Core focus areas: Food distribution (underprivileged families & stray animals), Menstrual hygiene drives (sanitary pads), and youth education.
Operational areas: Kanpur, Ghaziabad.

COMMUNICATION PROTOCOLS:
1. Accept and respond fluently in English, Hindi, or Hinglish based on how the user speaks to you.
2. If a user expresses an interest to donate, explicitly mention our 50% tax exemption benefits under Section 80G.
3. Be incredibly polite, warm, community-focused, and supportive. Keep responses crisp and conversational.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id', 'default_user')
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "Empty message string"}), 400

    # Initialize historical track for new sessions
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = []

    # Map previous items to formal Gemini Content objects
    contents = []
    for msg in SESSION_MEMORY[session_id]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["text"])])
        )
    
    # Append the newest input message
    contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
            )
        )
        
        
        reply_text = response.text

        # Record exchange to preserve system memory context
        SESSION_MEMORY[session_id].append({"role": "user", "text": user_message})
        SESSION_MEMORY[session_id].append({"role": "model", "text": reply_text})

        return jsonify({
            "reply": reply_text,
            "history_length": len(SESSION_MEMORY[session_id])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)