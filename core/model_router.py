import requests
import os


def call_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"]


def call_groq(prompt: str) -> str:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chat = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return chat.choices[0].message.content


def call_hf(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0}
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct",
        headers=headers,
        json=payload,
        timeout=60
    )
    response.raise_for_status()
    return response.json()[0]["generated_text"]
