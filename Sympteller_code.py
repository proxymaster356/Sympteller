import requests
import json
import socket

# ==== CONFIGURATION ====
GEMINI_API_KEY_1 = 'AIzaSyB56uMJi1GGU8xWWZok4JvoD_ytunj5pUQ'
GEMINI_API_KEY_2 = 'AIzaSyBoffbTe27tuJoUm62KCiSJSAHL9uOOQjI'
GEMINI_MODEL_NAME = "gemini-2.5-flash-preview-04-17"  # Change model 
OLLAMA_BASE_URL = 'http://127.0.0.1:11434'
OLLAMA_MODEL = 'mistral'

# === Check for Internet ===
def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# === Gemini API Call ===
def query_gemini(prompt, api_key, model_name="gemini-pro"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"[Gemini Error] HTTP {response.status_code}: {response.text}"
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"[Gemini Error] Exception: {e}"

# === Ollama Mistral Call ===
def query_ollama_mistral(prompt):
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()['response']
    except Exception as e:
        return f"[Ollama Error] {e}"

# === Disease Detection Function ===
def detect_disease(symptoms):
    if is_connected():
        print("🌐✨ Internet detected. Analyzing symptoms for accurate diagnosis... 🩺🔍")

        gemini_prompt = f"""
You are a confident and concise medical assistant. Given the symptoms below, return only the most probable disease or condition name. 
Do NOT include any disclaimers, suggestions to consult a doctor, or statements about being an AI.
Just return the diagnosis in 1 sentence or less.

Symptoms: {symptoms}
Diagnosis:
"""

        ans1 = query_gemini(gemini_prompt, GEMINI_API_KEY_1, GEMINI_MODEL_NAME)
        print("Ai Agent 1 response:", ans1)
        ans2 = query_gemini(gemini_prompt, GEMINI_API_KEY_2, GEMINI_MODEL_NAME)
        print("Ai Agent 2 response:", ans2)

        ans1_is_error = ans1.startswith("[Ai Agent 1 Error]")
        ans2_is_error = ans2.startswith("[Ai Agent 2 Error]")

        if ans1_is_error and ans2_is_error:
            print("⚠️ Both Ai Agent calls failed. Falling back to Ollama only.")
            prompt = f"The patient has the following symptoms: {symptoms}. What is the most probable disease? Give a short and direct answer."
            print("Ollama fallback prompt:", prompt)
            response = query_ollama_mistral(prompt).strip()
            print("Ollama response:", response)
            return response

        elif ans1_is_error:
            print("⚠️ Ai Agent 1 failed, using Ai Agent 2 response:", ans2)
            return ans2.strip()

        elif ans2_is_error:
            print("⚠️ Ai Agent 2 failed, using Ai Agent 1 response:", ans1)
            return ans1.strip()

        else:
            verification_prompt = f"""Based on the symptoms below and two different diagnoses, choose the more accurate one and provide a clear, confident diagnosis in one sentence. Do not mention AI or adjudication,Don't tell to ask for a doctor.

Symptoms: {symptoms}
Ai Agent 1 Diagnosis: {ans1}
Ai Agent 2 Diagnosis: {ans2}
"""
            response = query_ollama_mistral(verification_prompt).strip()
            return response

    else:
        print("❌ No Internet. Using Main Boss only...")
        prompt = f"You are a medical assistant verifying two AI diagnoses. Given the symptoms and both answers, choose the more accurate one. Return the final diagnosis clearly in one sentence. Do NOT include disclaimers, AI mentions, or consult a doctor or healthcare professional or any other advice or tell to ask for a doctor or to consult"
        # print("Ollama offline prompt:", prompt)
        response = query_ollama_mistral(prompt).strip()
        # print("Ollama offline response:", response)
        return response

# === MAIN LOOP ===
if __name__ == "__main__":
    print("🩺✨ Welcome to Sympteller💊 — Your AI Health Assistant 🤖")

    while True:
        user_input = input("\n🩺 Enter symptoms (or 'exit'): ").strip()
        if user_input.lower() == 'exit':
            print("👋 Goodbye!")
            break
        if not user_input:
            print("⚠️ Please enter some symptoms.")
            continue
        diagnosis = detect_disease(user_input)
        print("✅ Diagnosis:", diagnosis)

