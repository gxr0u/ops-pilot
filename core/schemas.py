from pydantic import BaseModel, Field
from typing import List


class ActionItem(BaseModel):
    task: str = Field(..., description="Action to be taken")
    owner: str = Field(..., description="Responsible person or team")
    priority: str = Field(..., description="HIGH | MEDIUM | LOW")


class OpsOutput(BaseModel):
    summary: str

    decisions: List[str]

    action_items: List[ActionItem]

    risks: List[str]

    assumptions: List[str]

    open_questions: List[str]

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence in extracted information"
    )
