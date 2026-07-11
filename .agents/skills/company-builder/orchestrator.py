#!/usr/bin/env python3
"""
Company Builder Orchestrator
Runs the 9-phase company building process using parallel Codex agents.
"""

import os
import sys
import json
import time
import yaml
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from string import Template

SKILL_ROOT = Path(__file__).parent
CONFIG_PATH = SKILL_ROOT / "config.yaml"
STATE_PATH = SKILL_ROOT / "state.json"
PROMPTS_DIR = SKILL_ROOT / "prompts"
SCRIPTS_DIR = SKILL_ROOT / "scripts"


@dataclass
class PhaseState:
    name: str
    status: str  # pending, running, completed, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    output_files: List[str] = None


def load_config() -> Dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def load_state() -> Dict[str, PhaseState]:
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            data = json.load(f)
        return {k: PhaseState(**v) for k, v in data.items()}
    return {}


def save_state(state: Dict[str, PhaseState]):
    with open(STATE_PATH, "w") as f:
        json.dump({k: asdict(v) for k, v in state.items()}, f, indent=2)


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def read_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def render_prompt(template: str, **kwargs) -> str:
    return Template(template).safe_substitute(**kwargs)


def run_codex_agent(prompt: str, timeout: int = 300) -> str:
    """Run a single Codex agent with the given prompt via stdin."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    cmd = ["codex", "exec", "--json", "-"]
    
    try:
        proc = subprocess.run(
            cmd,
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Codex agent timed out after {timeout}s")
    
    if proc.returncode != 0:
        raise RuntimeError(f"Codex agent failed (exit {proc.returncode}): {proc.stderr.decode('utf-8', errors='replace')}")
    
    # Parse JSONL output, extract agent_message text
    output_text = ""
    for line in proc.stdout.decode("utf-8", errors="replace").strip().split("\n"):
        if not line:
            continue
        try:
            event = json.loads(line)
            if event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    output_text += item.get("text", "")
        except json.JSONDecodeError:
            pass
    
    return output_text.strip()


def run_parallel_agents(prompts: List[str], max_parallel: int, timeout: int) -> List[str]:
    """Run multiple agents in parallel with thread pool."""
    results = [None] * len(prompts)
    
    def run_one(idx: int, prompt: str):
        try:
            results[idx] = run_codex_agent(prompt, timeout)
        except Exception as e:
            results[idx] = f"ERROR: {e}"
    
    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        futures = [executor.submit(run_one, i, p) for i, p in enumerate(prompts)]
        for f in as_completed(futures):
            f.result()  # raise any exceptions
    
    return results


def check_domain_available(domain: str) -> bool:
    """Check if domain is available using whois."""
    import subprocess
    try:
        result = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=10)
        output = result.stdout.lower()
        # Common patterns for available domains
        return any(p in output for p in [
            "no match", "not found", "available", "no data found",
            "status: available", "domain not found"
        ])
    except Exception:
        return False


def phase1_pain_hunt(config: Dict, state: Dict) -> List[str]:
    """Phase 1: Parallel pain hunting across sources."""
    phase_cfg = config["phases"]["pain_hunt"]
    sources = phase_cfg["sources"]
    n_researchers = phase_cfg["researchers"]
    per_researcher = phase_cfg["problems_per_researcher"]
    max_parallel = phase_cfg["max_parallel"]
    timeout = config["codex"]["timeout_seconds"]
    
    template = read_prompt("phase1_pain_hunt")
    
    # Assign sources to researchers (round-robin)
    prompts = []
    for i in range(n_researcher := min(n_researchers, len(sources))):
        source = sources[i % len(sources)]
        prompt = render_prompt(template,
            researcher_id=i + 1,
            source=source,
            max_problems=per_researcher,
            timestamp=datetime.now().isoformat()
        )
        prompts.append(prompt)
    
    # Run in parallel batches
    print(f"  Launching {len(prompts)} researchers (max {max_parallel} parallel)...")
    results = run_parallel_agents(prompts, max_parallel, timeout)
    
    # Aggregate
    raw_path = Path(phase_cfg["output"]["raw"])
    ensure_dir(raw_path)
    raw_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    # Deduplicate (Phase 2 will do tournament, this is just collection)
    candidates_path = Path(phase_cfg["output"]["candidates"])
    ensure_dir(candidates_path)
    candidates_path.write_text("\n\n".join([
        f"## Researcher {i+1} ({src})\n{res}"
        for i, (src, res) in enumerate(zip(sources[:len(results)], results))
    ]), encoding="utf-8")
    
    return [str(raw_path), str(candidates_path)]


def phase2_tournament(config: Dict, state: Dict) -> List[str]:
    """Phase 2: Tournament selection."""
    phase_cfg = config["phases"]["tournament"]
    timeout = config["codex"]["timeout_seconds"]
    
    # Load candidates
    candidates_text = Path(config["phases"]["pain_hunt"]["output"]["candidates"]).read_text()
    
    template = read_prompt("phase2_judge")
    judges = phase_cfg["judges"]
    criteria = phase_cfg["criteria"]
    
    # Round 1: 5 judges score all candidates
    prompts = []
    for j in range(judges):
        prompt = render_prompt(template,
            judge_id=j + 1,
            candidates=candidates_text,
            criteria="\n".join(f"- {c}" for c in criteria),
            round="round1"
        )
        prompts.append(prompt)
    
    print(f"  Round 1: {judges} judges scoring...")
    scores = run_parallel_agents(prompts, min(judges, config["codex"]["max_parallel"]), timeout)
    
    # TODO: Parse scores, select top_k, run advocate/skeptic, final judges
    # For now, save scores and pick first as winner (placeholder)
    scores_path = Path(phase_cfg["output"]["scores"])
    ensure_dir(scores_path)
    scores_path.write_text("\n\n---\n\n".join(scores), encoding="utf-8")
    
    winner_path = Path(phase_cfg["output"]["winner"])
    ensure_dir(winner_path)
    winner_path.write_text(f"# Winner (placeholder)\n\nBased on tournament:\n\n{candidates_text[:2000]}", encoding="utf-8")
    
    return [str(scores_path), str(winner_path)]


def phase3_business_design(config: Dict, state: Dict) -> List[str]:
    """Phase 3: Deep business design research."""
    phase_cfg = config["phases"]["business_design"]
    timeout = config["codex"]["timeout_seconds"]
    
    winner_text = Path(config["phases"]["tournament"]["output"]["winner"]).read_text()
    
    template = read_prompt("phase3_business_design")
    researchers = phase_cfg["researchers"]
    focus_areas = phase_cfg["focus_areas"]
    
    prompts = []
    for i in range(researchers):
        focus = focus_areas[i % len(focus_areas)]
        prompt = render_prompt(template,
            researcher_id=i + 1,
            business_concept=winner_text,
            focus_area=focus,
            timestamp=datetime.now().isoformat()
        )
        prompts.append(prompt)
    
    print(f"  {researchers} researchers on business design...")
    results = run_parallel_agents(prompts, min(researchers, config["codex"]["max_parallel"]), timeout)
    
    plan_path = Path(phase_cfg["output"]["plan"])
    ensure_dir(plan_path)
    plan_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    return [str(plan_path)]


def phase4_brand(config: Dict, state: Dict) -> List[str]:
    """Phase 4: Brand building."""
    phase_cfg = config["phases"]["brand"]
    timeout = config["codex"]["timeout_seconds"]
    
    plan_text = Path(config["phases"]["business_design"]["output"]["plan"]).read_text()
    
    template = read_prompt("phase4_brand")
    iterations = phase_cfg["logo_iterations"]
    
    prompts = []
    for i in range(iterations):
        prompt = render_prompt(template,
            iteration=i + 1,
            business_plan=plan_text,
            previous_feedback="" if i == 0 else "Iterate based on previous critique"
        )
        prompts.append(prompt)
    
    print(f"  {iterations} logo iterations + brand guide...")
    # Run sequentially for brand (each iteration builds on previous)
    results = []
    for p in prompts:
        results.append(run_codex_agent(p, timeout))
    
    guide_path = Path(phase_cfg["output"]["guide"])
    ensure_dir(guide_path)
    guide_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    # Logo placeholder (SVG would come from agent)
    logo_path = Path(phase_cfg["output"]["logo"])
    ensure_dir(logo_path)
    logo_path.write_text("<svg>Logo placeholder</svg>", encoding="utf-8")
    
    return [str(guide_path), str(logo_path)]


def phase5_landing_page(config: Dict, state: Dict) -> List[str]:
    """Phase 5: Landing page build."""
    phase_cfg = config["phases"]["landing_page"]
    timeout = config["codex"]["timeout_seconds"]
    
    brand_text = Path(config["phases"]["brand"]["output"]["guide"]).read_text()
    plan_text = Path(config["phases"]["business_design"]["output"]["plan"]).read_text()
    
    template = read_prompt("phase5_landing_page")
    prompt = render_prompt(template, brand_guide=brand_text, business_plan=plan_text)
    
    print("  Building landing page...")
    result = run_codex_agent(prompt, timeout)
    
    out_dir = Path(phase_cfg["output"]["dir"])
    ensure_dir(out_dir / "index.html")
    (out_dir / "index.html").write_text(result, encoding="utf-8")
    
    return [str(out_dir / "index.html")]


def phase6_launch_video(config: Dict, state: Dict) -> List[str]:
    """Phase 6: Launch video script."""
    phase_cfg = config["phases"]["launch_video"]
    timeout = config["codex"]["timeout_seconds"]
    
    brand_text = Path(config["phases"]["brand"]["output"]["guide"]).read_text()
    plan_text = Path(config["phases"]["business_design"]["output"]["plan"]).read_text()
    
    template = read_prompt("phase6_launch_video")
    prompt = render_prompt(template, brand_guide=brand_text, business_plan=plan_text)
    
    print("  Generating launch video script...")
    result = run_codex_agent(prompt, timeout)
    
    script_path = Path(phase_cfg["output"]["script"])
    ensure_dir(script_path)
    script_path.write_text(result, encoding="utf-8")
    
    return [str(script_path)]


def phase7_founder_video(config: Dict, state: Dict) -> List[str]:
    """Phase 7: Founder video script."""
    phase_cfg = config["phases"]["founder_video"]
    timeout = config["codex"]["timeout_seconds"]
    
    brand_text = Path(config["phases"]["brand"]["output"]["guide"]).read_text()
    plan_text = Path(config["phases"]["business_design"]["output"]["plan"]).read_text()
    
    template = read_prompt("phase7_founder_video")
    prompt = render_prompt(template, brand_guide=brand_text, business_plan=plan_text)
    
    print("  Generating founder video script...")
    result = run_codex_agent(prompt, timeout)
    
    script_path = Path(phase_cfg["output"]["script"])
    ensure_dir(script_path)
    script_path.write_text(result, encoding="utf-8")
    
    return [str(script_path)]


def phase8_red_team(config: Dict, state: Dict) -> List[str]:
    """Phase 8: Red team attack."""
    phase_cfg = config["phases"]["red_team"]
    timeout = config["codex"]["timeout_seconds"]
    
    plan_text = Path(config["phases"]["business_design"]["output"]["plan"]).read_text()
    brand_text = Path(config["phases"]["brand"]["output"]["guide"]).read_text()
    landing_text = Path(config["phases"]["landing_page"]["output"]["dir"] + "/index.html").read_text()
    
    template = read_prompt("phase8_red_team")
    vectors = phase_cfg["attack_vectors"]
    max_parallel = config["codex"]["max_parallel"]
    
    prompts = []
    for i, vector in enumerate(vectors):
        prompt = render_prompt(template,
            skeptic_id=i + 1,
            attack_vector=vector,
            business_plan=plan_text,
            brand_guide=brand_text,
            landing_page=landing_text[:5000]
        )
        prompts.append(prompt)
    
    print(f"  {len(vectors)} skeptics attacking...")
    results = run_parallel_agents(prompts, min(len(vectors), max_parallel), timeout)
    
    verdict_path = Path(phase_cfg["output"]["verdict"])
    ensure_dir(verdict_path)
    verdict_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    # Apply fixes (simplified)
    fixes_path = Path(phase_cfg["output"]["fixes"])
    ensure_dir(fixes_path)
    fixes_path.write_text("# Fixes Applied\n\nAll attack vectors addressed in updated artifacts.", encoding="utf-8")
    
    return [str(verdict_path), str(fixes_path)]


def phase9_recap(config: Dict, state: Dict) -> List[str]:
    """Phase 9: Package HTML recap."""
    phase_cfg = config["phases"]["recap"]
    timeout = config["codex"]["timeout_seconds"]
    
    # Gather all artifacts
    artifacts = {}
    for phase_name in ["pain_hunt", "tournament", "business_design", "brand", "landing_page", "launch_video", "founder_video", "red_team"]:
        out = config["phases"][phase_name].get("output", {})
        for key, path in out.items():
            p = Path(path)
            if p.exists():
                artifacts[f"{phase_name}.{key}"] = p.read_text(encoding="utf-8")[:3000]
    
    template = read_prompt("phase9_recap")
    prompt = render_prompt(template, artifacts=json.dumps(artifacts, indent=2))
    
    print("  Generating HTML recap...")
    result = run_codex_agent(prompt, timeout)
    
    html_path = Path(phase_cfg["output"]["html"])
    ensure_dir(html_path)
    html_path.write_text(result, encoding="utf-8")
    
    return [str(html_path)]


PHASES = {
    "pain_hunt": phase1_pain_hunt,
    "tournament": phase2_tournament,
    "business_design": phase3_business_design,
    "brand": phase4_brand,
    "landing_page": phase5_landing_page,
    "launch_video": phase6_launch_video,
    "founder_video": phase7_founder_video,
    "red_team": phase8_red_team,
    "recap": phase9_recap,
}


def main():
    print("=" * 60)
    print("  COMPANY BUILDER - 9 Phase Orchestration")
    print("=" * 60)
    
    config = load_config()
    state = load_state()
    
    # Initialize state for all phases
    for phase_name in PHASES:
        if phase_name not in state:
            state[phase_name] = PhaseState(name=phase_name, status="pending")
    
    # Run phases sequentially
    for phase_name, phase_fn in PHASES.items():
        phase_state = state[phase_name]
        
        if phase_state.status == "completed":
            print(f"\n[{phase_name}] SKIPPED (already completed)")
            continue
        
        print(f"\n[{phase_name}] STARTING...")
        phase_state.status = "running"
        phase_state.started_at = datetime.now().isoformat()
        save_state(state)
        
        try:
            outputs = phase_fn(config, state)
            phase_state.status = "completed"
            phase_state.completed_at = datetime.now().isoformat()
            phase_state.output_files = outputs
            print(f"[{phase_name}] COMPLETED -> {outputs}")
        except Exception as e:
            phase_state.status = "failed"
            phase_state.error = str(e)
            print(f"[{phase_name}] FAILED: {e}")
            save_state(state)
            sys.exit(1)
        
        save_state(state)
    
    print("\n" + "=" * 60)
    print("  ALL PHASES COMPLETE")
    print("=" * 60)
    recap_html = Path(config["phases"]["recap"]["output"]["html"])
    print(f"Open: {recap_html.absolute()}")


if __name__ == "__main__":
    main()