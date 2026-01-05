import gradio as gr
import json
from ops_assistant.pipeline import run_ops_pipeline
from pydantic import ValidationError


def run_assistant(input_text: str):
    if not input_text or len(input_text.strip()) < 20:
        return (
            "⚠️ Input too short",
            [],
            [],
            [],
            [],
            [],
            "{}",
            0.0
        )

    try:
        result = run_ops_pipeline(input_text)

        return (
            result.summary,
            result.decisions,
            [
                f"{item.task} | Owner: {item.owner} | Priority: {item.priority}"
                for item in result.action_items
            ],
            result.risks,
            result.assumptions,
            result.open_questions,
            json.dumps(result.dict(), indent=2),
            result.confidence_score
        )

    except ValidationError as ve:
        return (
            "❌ Schema validation failed",
            [],
            [],
            [],
            [],
            [],
            str(ve),
            0.0
        )

    except Exception as e:
        return (
            "❌ Error running Ops Assistant",
            [],
            [],
            [],
            [],
            [],
            str(e),
            0.0
        )


with gr.Blocks(title="OpsPilot – AI Ops Assistant") as demo:
    gr.Markdown(
        """
        # 🧠 OpsPilot – AI Ops Assistant
        Convert unstructured operational data into **decisions, action items, and risks**.

        - Local-first (Ollama supported)
        - Cost-aware model routing
        - Deterministic structured outputs
        """
    )

    with gr.Row():
        input_text = gr.Textbox(
            label="Input (Meeting Notes / Docs / Slack Export)",
            placeholder="Paste raw operational text here...",
            lines=12
        )

    run_btn = gr.Button("Run Ops Assistant", variant="primary")

    with gr.Tabs():
        with gr.Tab("Summary"):
            summary = gr.Textbox(lines=4)

        with gr.Tab("Decisions"):
            decisions = gr.JSON()

        with gr.Tab("Action Items"):
            actions = gr.JSON()

        with gr.Tab("Risks"):
            risks = gr.JSON()

        with gr.Tab("Assumptions"):
            assumptions = gr.JSON()

        with gr.Tab("Open Questions"):
            open_questions = gr.JSON()

        with gr.Tab("Raw JSON"):
            raw_json = gr.Code(language="json")

    confidence = gr.Slider(
        minimum=0,
        maximum=1,
        value=0,
        label="Confidence Score",
        interactive=False
    )

    run_btn.click(
        run_assistant,
        inputs=input_text,
        outputs=[
            summary,
            decisions,
            actions,
            risks,
            assumptions,
            open_questions,
            raw_json,
            confidence
        ]
    )


if __name__ == "__main__":
    demo.launch()
