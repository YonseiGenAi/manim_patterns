# app/llm_pattern.py
import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


PATTERN_SYSTEM_PROMPT = """
You are a pattern classifier.
Your task is to decide the VISUALIZATION PATTERN for a computational process.

Allowed patterns:
- "grid"          : 2D matrix, heatmap, convolution, attention matrix
- "sequence"      : step-by-step algorithm, sorting, iterative procedures
- "seq_attention" : tokens + attention weights, transformer-style
- "flow"          : pipeline, blocks, dataflow operation chains

Return ONLY JSON: {"pattern": "<one_of_above>"} 
"""


def call_llm_pattern(user_text: str) -> str:
    """Ask the LLM to *recommend* a pattern."""
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PATTERN_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Text:\n'''{user_text}'''\nReturn only JSON.",
            },
        ],
    )
    data = json.loads(resp.choices[0].message.content)
    return data.get("pattern", "flow")  # fallback to flow
# app/llm_pattern.py
import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


PATTERN_SYSTEM_PROMPT = """
You are a pattern classifier.
Your task is to decide the VISUALIZATION PATTERN for a computational process.

Allowed patterns:
- "grid"          : 2D matrix, heatmap, convolution, attention matrix
- "sequence"      : step-by-step algorithm, sorting, iterative procedures
- "seq_attention" : tokens + attention weights, transformer-style
- "flow"          : pipeline, blocks, dataflow operation chains

Return ONLY JSON: {"pattern": "<one_of_above>"} 
"""


def call_llm_pattern(user_text: str) -> str:
    """Ask the LLM to *recommend* a pattern."""
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PATTERN_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Text:\n'''{user_text}'''\nReturn only JSON.",
            },
        ],
    )
    data = json.loads(resp.choices[0].message.content)
    return data.get("pattern", "flow")  # fallback to flow
