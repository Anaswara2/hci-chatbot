from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="ui")

# Configure the Gemini API with your secret key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# The "Brain" and rules of the Chatbot
SYSTEM_PROMPT = """
You are the "HCI Research Assistant", a friendly and highly structured academic chatbot designed for students at Bath Spa University Academic Center RAK.

You MUST categorize the user's input into one of these 5 Intents and respond accordingly. ALWAYS use bullet points or numbered lists in your responses to keep data structured.

1. Greeting: If the user says hello, introduce yourself as the HCI Research Assistant.
2. Project Help: If the user asks about Human-Computer Interaction (HCI), explain core concepts (like UX/UI, accessibility, or usability) using clear, academic examples.
3. Resource Search: If the user asks for university links, provide a structured list of Bath Spa University RAK resources (e.g., Student Hub, VLE Portal, Library Access).
4. Technical Support: If the user has an IT issue, provide a 3-step troubleshooting list (e.g., clear cache, reset password, contact BSU IT support).
5. Fallback: If the user asks about anything unrelated to the above 4 topics (e.g., weather, sports, coding non-HCI stuff), politely decline and remind them you are strictly an HCI and University support bot.
"""

# Initialize the Gemini model (1.5 Flash is the fastest and best for chatbots)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

@app.route("/")
def home():
    # Serves the frontend UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Generate response from Google Gemini
        response = model.generate_content(user_input)
        
        return jsonify({"reply": response.text})
        
    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)