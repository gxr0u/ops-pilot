import json
from core.model_router import call_ollama, call_groq
from core.confidence import compute_confidence
from core.schemas import OpsOutput
from pathlib import Path


PROMPTS = Path(__file__).parent / "prompts"


def derive_summary(extracted: dict) -> str:
    parts = []

    if extracted.get("decisions"):
        parts.append(f"Decisions: {', '.join(extracted['decisions'])}.")

    if extracted.get("action_items"):
        owners = {item["owner"] for item in extracted["action_items"]}
        parts.append(f"Action items assigned to {', '.join(owners)}.")

    if extracted.get("risks"):
        parts.append(f"Key risks include {', '.join(extracted['risks'])}.")

    return " ".join(parts) if parts else "No clear summary could be derived."


def load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text()


def normalize_action_items(action_items: list[dict]) -> list[dict]:
    normalized = []
    for item in action_items:
        normalized.append({
            "task": item.get("task", "").strip(),
            "owner": item.get("owner", "Unassigned"),
            "priority": item.get("priority", "MEDIUM")
        })
    return normalized



def run_ops_pipeline(input_text: str) -> OpsOutput:
    extractor_prompt = load_prompt("extractor.txt") + "\n\n" + input_text
    extracted_raw = call_ollama(extractor_prompt)

    extracted = json.loads(extracted_raw)

    # Normalize action items to satisfy schema
    if "action_items" in extracted:
        extracted["action_items"] = normalize_action_items(
            extracted.get("action_items", [])
        )

    # Remove non-schema fields (intermediate-only)
    extracted.pop("key_points", None)

    # Compute confidence AFTER normalization & cleanup
    confidence = compute_confidence(extracted)

    if confidence < 0.7:
        reasoner_prompt = (
            load_prompt("reasoner.txt")
            + "\n\nORIGINAL INPUT:\n"
            + input_text
            + "\n\nEXTRACTED DATA:\n"
            + json.dumps(extracted)
        )
        refined_raw = call_groq(reasoner_prompt)
        refined = json.loads(refined_raw)
    else:
        refined = {
            "summary": derive_summary(extracted),
            **extracted
        }


    refined["confidence_score"] = confidence
    return OpsOutput(**refined)

