import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise RuntimeError("NVIDIA_API_KEY is not set")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

MODEL = os.getenv("NVIDIA_MODEL", "openai/gpt-oss-20b")


def ask_nvidia(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Bob, an investigative case-analysis assistant. "
                    "Use only the evidence provided to you. "
                    "Do not claim identity confirmation. "
                    "Do not change backend scores. "
                    "Clearly distinguish matching evidence, conflicting "
                    "evidence, uncertainty, and recommended next actions."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    return response.choices[0].message.content or ""