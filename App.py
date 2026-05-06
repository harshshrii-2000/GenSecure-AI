from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Create Gemini client (NEW SDK)
client = genai.Client(api_key=API_KEY)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Explanation API
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic")
    level = data.get("level", "Beginner")

    if not topic:
        return jsonify({"result": "❌ Please enter a topic"})

    prompt = f"""
You are an AI Machine Learning Tutor.

Topic: {topic}
Level: {level}

Explain with:
1. Simple explanation
2. Real-life example
3. Key points
4. Short summary
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({"result": response.text})

# Quiz API
@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic")
    level = data.get("level", "Beginner")

    if not topic:
        return jsonify({"quiz": "❌ Please enter a topic"})

    prompt = f"""
Create 5 MCQs on this topic.

Topic: {topic}
Level: {level}

Format:
Q1: Question?
A) Option
B) Option
C) Option
D) Option
Answer: A
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({"quiz": response.text})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
