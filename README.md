# OpsPilot – AI Ops Assistant

OpsPilot is a **local-first, cost-aware AI Ops Assistant** that converts unstructured operational data  
(meeting notes, internal docs, Slack exports) into **structured decisions, action items, and risks**.

It is designed as a **production-style LLM orchestration system**, not a chatbot — emphasizing
deterministic outputs, strict validation, and selective use of large models.

---

## 🚀 Why OpsPilot?

Teams often rely on:
- messy meeting notes
- undocumented decisions
- manual follow-ups

OpsPilot turns raw operational text into **clear, structured, and actionable outputs** that teams can
immediately use.

Unlike generic chatbots, OpsPilot focuses on:
- reliability
- cost-awareness
- schema enforcement
- real-world deployment patterns

---

## ✨ Key Features

- 🏠 **Local-first** (Ollama supported)
- 💰 **Cost-aware model routing**
- 🔁 **Two-pass LLM orchestration**
- 📐 **Strict schema validation (Pydantic)**
- 🧪 **Confidence scoring & fallback reasoning**
- 🖥️ **Gradio UI for fast demos**

---
## 🧠 How It Works

OpsPilot uses a **multi-stage pipeline** where large language models are used **only when necessary**.

```text
Unstructured Input  
↓  
Extraction Pass (Cheap / Local LLM)  
↓  
Normalization & Cleanup  
↓  
Confidence Scoring (Code)  
↓  
Conditional Reasoning (Stronger LLM)  
↓  
Schema Validation (Pydantic)  
↓  
Structured Ops Output (JSON)
```
---
## 🤖 Model Strategy

| Stage        | Model Used                          |
|--------------|-------------------------------------|
| Extraction   | Ollama (LLaMA 3.2 3B)               |
| Reasoning    | Groq / HuggingFace (Larger models)  |
| Validation   | Code (Pydantic)                     |

> **Enterprise / subscription deployments** can swap in GPT-4 or Claude at the routing layer  
> without changing the core architecture.
---
## 🏗️ Project Structure
```text
ops-pilot/
├── core/               # Shared infrastructure (model routing, schemas)
│   ├── confidence.py
│   ├── model_router.py
│   └── schemas.py
│
├── ops_assistant/      # Ops Assistant domain logic
│   ├── prompts/
│   │   ├── extractor.txt
│   │   └── reasoner.txt
│   ├── pipeline.py
│   └── service.py
│
├── ui/                 # Presentation layer
│   └── gradio_app.py
│
├── examples/           # Sample inputs & outputs
│
├── README.md
├── requirements.txt
└── .env.example
```
---
## 📂 Example

### Input (examples/meeting_notes.txt)

    We discussed the Q3 launch timeline.
    Decision was made to delay the launch by one week.
    Aditya will follow up with the frontend team.
    Risk identified around analytics vendor dependency.

### Output (examples/output.json)

    {
      "decisions": ["delay Q3 launch by one week"],
      "action_items": [
        {
          "task": "follow up with the frontend team",
          "owner": "Aditya",
          "priority": "HIGH"
        }
      ],
      "risks": ["analytics vendor dependency"]
    }
---
## ▶️ Running Locally

### 1. Install dependencies

    pip install -r requirements.txt

### 2. Start Ollama

    ollama run llama3.2:3b

### 3. Launch the Gradio UI

    python -m ui.gradio_app

Open in your browser:

    http://localhost:7860
---
## 🔐 Environment Variables

Create a `.env` file using `.env.example` as reference:

    GROQ_API_KEY=your_groq_api_key
    HF_API_KEY=your_huggingface_api_key
    OLLAMA_URL=http://localhost:11434

⚠️ Never commit your `.env` file.
---
