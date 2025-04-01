import asyncio

import litellm

from fi.integrations.otel import LiteLLMInstrumentor, register
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

async def run_examples():
    # Configure trace provider with custom evaluation tags
    trace_provider = register(
        project_type=ProjectType.EXPERIMENT,
        eval_tags=eval_tags,
        project_name="FUTURE_AGI",
        project_version_name="v1",
    )

    # Initialize the Lite LLM instrumentor
    LiteLLMInstrumentor().instrument(tracer_provider=trace_provider)

    # Simple single message completion call
    litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"content": "What's the capital of China?", "role": "user"}],
    )

    # Multiple message conversation completion call with added param
    litellm.completion(
        model="gpt-3.5-turbo",
        messages=[
            {"content": "Hello, I want to bake a cake", "role": "user"},
            {
                "content": "Hello, I can pull up some recipes for cakes.",
                "role": "assistant",
            },
            {"content": "No actually I want to make a pie", "role": "user"},
        ],
        temperature=0.7,
    )

    # Multiple message conversation acompletion call with added params
    await litellm.acompletion(
        model="gpt-3.5-turbo",
        messages=[
            {"content": "Hello, I want to bake a cake", "role": "user"},
            {
                "content": "Hello, I can pull up some recipes for cakes.",
                "role": "assistant",
            },
            {"content": "No actually I want to make a pie", "role": "user"},
        ],
        temperature=0.7,
        max_tokens=20,
    )

    # Completion with retries
    litellm.completion_with_retries(
        model="gpt-3.5-turbo",
        messages=[{"content": "What's the highest grossing film ever", "role": "user"}],
    )

    # Embedding call
    litellm.embedding(
        model="text-embedding-ada-002", input=["good morning from litellm"]
    )

    # Asynchronous embedding call
    await litellm.aembedding(
        model="text-embedding-ada-002", input=["good morning from litellm"]
    )

    # Image generation call
    litellm.image_generation(model="dall-e-2", prompt="cute baby otter")

    # Asynchronous image generation call
    await litellm.aimage_generation(model="dall-e-2", prompt="cute baby otter")


asyncio.run(run_examples())
