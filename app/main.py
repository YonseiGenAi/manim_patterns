# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.llm_pseudocode import call_llm_pseudocode_ir
from app.llm import call_llm_domain_ir, call_llm_attention_ir
from app.llm_domain import call_llm_detect_domain, build_sorting_trace_ir

from app.render_cnn_matrix import render_cnn_matrix
from app.render_sorting import render_sorting
from app.render_seq_attention import render_seq_attention

from app.patterns import PatternType
from app.schema import validate_attention_ir

from app.llm_anim_ir import call_llm_anim_ir
from app.llm_codegen import call_llm_codegen

import tempfile
import subprocess


class GenerateRequest(BaseModel):
    text: str


app = FastAPI()


@app.post("/generate")
async def generate_visualization(req: GenerateRequest):
    user_text = req.text

    # 1) pseudocode IR 생성
    pseudo_ir = call_llm_pseudocode_ir(user_text)

    # 2) domain 분류
    try:
        domain = call_llm_detect_domain(user_text)
    except Exception:
        domain = "generic"

    # 3) 패턴 LLM 추천
    from app.llm_pattern import call_llm_pattern
    llm_pattern = call_llm_pattern(user_text)

    # 4) 최종 패턴 결정 (domain 우선)
    from app.patterns import resolve_pattern
    final_pattern = resolve_pattern(domain, llm_pattern)

    # 5) 대표 도메인 처리 → 전용 렌더러 실행

    # --- CNN ---
    if domain == "cnn_param" and final_pattern == PatternType.GRID:
        cnn_ir = call_llm_domain_ir("cnn_param", user_text)
        cfg = cnn_ir.get("ir", {}).get("params", {})

        video_path = render_cnn_matrix(
            cfg,
            out_basename=cnn_ir.get("basename", "cnn_param_demo"),
            fmt=cnn_ir.get("out_format", "mp4"),
        )

        return {
            "domain": domain,
            "pattern": final_pattern.value,
            "cnn_ir": cnn_ir,
            "video_path": video_path,
        }

    # --- SORTING ---
    if domain == "sorting" and final_pattern == PatternType.SEQUENCE:
        sort_trace = build_sorting_trace_ir(user_text)
        video_path = render_sorting(sort_trace)
        return {
            "domain": domain,
            "pattern": final_pattern.value,
            "sorting_trace": sort_trace,
            "video_path": video_path,
        }

    # --- TRANSFORMER ---
    if domain == "transformer" and final_pattern == PatternType.SEQ_ATTENTION:
        attn_ir = call_llm_attention_ir(user_text)
        errors = validate_attention_ir(attn_ir)
        if errors:
            return {
                "domain": domain,
                "pattern": final_pattern.value,
                "errors": errors,
            }

        video_path = render_seq_attention(attn_ir, out_basename="attn_demo")
        return {
            "domain": domain,
            "pattern": final_pattern.value,
            "attention_ir": attn_ir,
            "video_path": video_path,
        }

    # 6) 비대표 도메인 → 패턴 기반 베이스 렌더러 (추후 확장)
    # 지금은 generic fallback만

    anim_ir = call_llm_anim_ir(pseudo_ir)
    manim_code = call_llm_codegen(anim_ir)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(manim_code)
        tmp_path = tmp.name

    subprocess.run(["manim", "-ql", tmp_path, "AlgorithmScene", "--format", "mp4"])

    return {
        "domain": domain,
        "pattern": final_pattern.value,
        "pseudocode_ir": pseudo_ir,
        "anim_ir": anim_ir,
        "message": "fallback generic visualization started",
    }

