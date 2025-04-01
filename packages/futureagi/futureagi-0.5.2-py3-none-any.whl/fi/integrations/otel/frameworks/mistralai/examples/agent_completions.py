import os

from mistralai import Mistral

from fi.integrations.otel import MistralAIInstrumentor, register
from fi.integrations.otel.types import (
    EvalName,
    EvalSpanKind,
    EvalTag,
    EvalTagType,
    ProjectType,
)

# Configure trace provider with custom evaluation tags
eval_tags = [
    EvalTag(
        eval_name=EvalName.DETERMINISTIC_EVALS,
        value=EvalSpanKind.TOOL,
        type=EvalTagType.OBSERVATION_SPAN,
        config={
            "multi_choice": False,
            "choices": ["Yes", "No"],
            "rule_prompt": "Evaluate if the response is correct",
        },
    )
]

# Configure trace provider with custom evaluation tags
trace_provider = register(
    project_type=ProjectType.EXPERIMENT,
    eval_tags=eval_tags,
    project_name="FUTURE_AGI",
    project_version_name="v1",
)

# Initialize the Mistral AI instrumentor
MistralAIInstrumentor().instrument(tracer_provider=trace_provider)

if __name__ == "__main__":
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    response = client.agents.complete(
        agent_id="agent_id",
        messages=[
            {"role": "user", "content": "plan a vacation for me in Tbilisi"},
        ],
    )
    print(response)
