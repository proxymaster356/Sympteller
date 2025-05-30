
# 💊 Sympteller — Your AI Health Assistant

Sympteller is a hybrid AI-powered disease detection tool that intelligently analyzes user-provided symptoms using **Google Gemini (2 APIs)** and an **offline Mistral model** via **Ollama**. It works both **online and offline**, providing clean, confident diagnoses with no unnecessary disclaimers.

---

## ⚙️ How It Works

```mermaid
graph TD
    A[User Inputs Symptoms] --> B{Internet Available?}
    B -- Yes --> C[Gemini Agent 1 + Agent 2]
    C --> D{Both Succeed?}
    D -- Yes --> E[Ollama Mistral decides better answer]
    D -- One Fails --> F[Use available Gemini answer]
    D -- Both Fail --> G[Use Mistral for full fallback]
    B -- No --> H[Offline Mistral Diagnosis Only]

🧠 **Features**
✅ Dual Gemini 2.5 API calls for higher reliability
✅ Smart voting via Ollama (Mistral) adjudication
✅ 100% Offline fallback when no internet
✅ Flask backend + Beautiful animated HTML frontend
✅ Dark mode, glowing diagnosis cards, and responsive design


   
