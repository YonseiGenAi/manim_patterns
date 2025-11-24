# app/prompts.py

DOMAIN_PROMPTS = {
    "cnn_param": {
        "system": "You are a precise JSON generator for CNN visualization IRs. Output ONLY JSON.",
        "template": """
Generate a JSON object following the exact structure below.
Do NOT include explanations, comments, or additional text.

{{
  "ir": {{
    "metadata": {{"domain": "cnn_param"}},
    "params": {{
      "input_size": <integer>,
      "kernel_size": <integer>,
      "stride": <integer>,
      "padding": <integer>,
      "seed": 1
    }}
  }},
  "basename": "cnn_forward_param",
  "out_format": "mp4"
}}

Rules:
- "NxN 행렬" or "matrix" → input_size
- "kernel size", "filter", "커널" → kernel_size
- input_size는 padding을 포함하지 않는다.
- 절대 사용자의 수치를 변경하거나 추정하지 말라.
- JSON 외의 문장은 절대 포함하지 말라.

User text:
{text}
"""
    },

    "sorting_trace": {
        "system": """
You are a sorting algorithm visual trace generator.
Extract the array and generate a full bubble-sort-like trace.
Return ONLY JSON.
""",
        "template": """
Generate a bubble-sort trace for the user's request.

User request:
{text}

Output JSON with this structure:

{{
  "algorithm": "bubble_sort",
  "input": {{ "array": [5, 1, 4, 2, 8] }},
  "trace": [
    {{ "step": 1, "compare": [0,1], "swap": true,  "array": [1,5,4,2,8] }},
    {{ "step": 2, "compare": [1,2], "swap": true,  "array": [1,4,5,2,8] }}
  ]
}}
"""
    },



    "seq_attention": {
        "system": "You are a precise JSON generator for transformer self-attention & next-token visualization. Output ONLY JSON.",
        "template": """
You are given a USER REQUEST that may include:
- An example input sentence (often in English) that should be fed into a transformer.
- Surrounding Korean explanation such as "라는 문장의 next token prediction이 어떻게 동작해?" and other context.

From this USER REQUEST, do the following:

1. Extract the short **input sequence** that will be fed into the transformer.
   - Prefer the English part that looks like an example sentence, e.g. "I want to play".
   - If the user writes something like `I want to play라는 문장의 next token prediction이...`,
     then the input sequence MUST be exactly "I want to play".
   - If there are quotes, backticks, or text before '라는 문장', treat that as the candidate.
   - If multiple candidates exist, choose the simplest short phrase (3–10 tokens) that looks like a natural input.
   - If you truly cannot find any clear example, fall back to using the entire request text as raw_text.

2. Use ONLY that extracted input sequence as "raw_text" and "tokens".
   - Do NOT include the surrounding Korean question or explanation in "raw_text".
   - "tokens" must be a whitespace-based tokenization of raw_text.

Then produce a JSON object with the following structure:

{
  "pattern_type": "seq_attention",
  "raw_text": "<the extracted input sequence>",
  "tokens": ["...", "...", "..."],
  "weights": [w_0, w_1, ..., w_{N-1}],
  "query_index": <integer index of the token that acts as the query>,
  "next_token": {
    "candidates": ["...", "...", "..."],
    "probs": [p_0, p_1, p_2]
  }
}

Rules:
- "raw_text" MUST be exactly the extracted input sequence (e.g. "I want to play"), NOT the whole user request.
- "tokens" MUST be a simple whitespace-based split of raw_text.
- Let N = len(tokens). "weights" MUST be a 1D array of length N, representing attention from the query token to each token.
- "query_index" SHOULD normally be N-1 (the last token).
- "next_token.candidates" MUST be 2~6 plausible next tokens in English.
- "next_token.probs" MUST have the same length as "candidates" and sum to approximately 1.0.
- Do NOT output anything except the JSON object. No explanations, no comments.

USER REQUEST:
{text}
"""
    },

}


