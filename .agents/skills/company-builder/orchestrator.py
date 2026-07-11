#!/usr/bin/env python3
"""
Company Builder Orchestrator
Runs the 9-phase company building process.
"""

import os
import sys
import json
import yaml
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from string import Template

# Add scripts to path
SKILL_ROOT = Path(__file__).parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_codex_agent import run_codex_agent, run_parallel_agents


@dataclass
class PhaseState:
    name: str
    status: str  # pending, running, completed, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    output_files: List[str] = None


def load_config() -> Dict:
    with open(SKILL_ROOT / "config.yaml") as f:
        return yaml.safe_load(f)


def load_state() -> Dict[str, PhaseState]:
    state_path = SKILL_ROOT / "state.json"
    if state_path.exists():
        with open(state_path) as f:
            data = json.load(f)
        return {k: PhaseState(**v) for k, v in data.items()}
    return {}


def save_state(state: Dict[str, PhaseState]):
    state_path = SKILL_ROOT / "state.json"
    with open(state_path, "w") as f:
        json.dump({k: asdict(v) for k, v in state.items()}, f, indent=2)


def read_prompt(name: str) -> str:
    path = SKILL_ROOT / "prompts" / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def render_prompt(template: str, **kwargs) -> str:
    return Template(template).safe_substitute(**kwargs)


def get_output_path(path_str: str) -> Path:
    """Get anchored output path for a relative path string."""
    return SKILL_ROOT / path_str


def ensure_dir(path_str: str):
    """Ensure parent directory exists for an output path."""
    path = get_output_path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_output_files(file_paths: List[str]) -> str:
    """Read and concatenate output files for context passing."""
    parts = []
    for fp in file_paths:
        p = Path(fp)
        if p.exists():
            parts.append(f"=== {fp} ===\n{p.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def phase1_pain_hunt(config: Dict, state: Dict) -> List[str]:
    """Phase 1: Parallel pain hunting across sources."""
    phase_cfg = config["phases"]["pain_hunt"]
    sources = phase_cfg["sources"]
    n_researchers = min(phase_cfg["researchers"], len(sources))
    per_researcher = phase_cfg["problems_per_researcher"]
    max_parallel = phase_cfg["max_parallel"]
    timeout = config["codex"]["timeout_seconds"]
    
    template = read_prompt("phase1_pain_hunt")
    prompts = []
    
    for i in range(n_researchers):
        source = sources[i % len(sources)]
        prompt = render_prompt(template,
            researcher_id=i + 1,
            source=source,
            max_problems=per_researcher,
            timestamp=datetime.now().isoformat()
        )
        prompts.append(prompt)
    
    print(f"  Launching {len(prompts)} researchers (max {max_parallel} parallel)...")
    results = run_parallel_agents(prompts, max_parallel, timeout)
    
    # Aggregate
    raw_path = Path(phase_cfg["output"]["raw"])
    ensure_dir(raw_path)
    raw_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
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
    
    candidates_text = Path(config["phases"]["pain_hunt"]["output"]["candidates"]).read_text()
    
    # Round 1: 5 judges score all candidates
    template = read_prompt("phase2_judge")
    judges = phase_cfg["judges"]
    criteria = phase_cfg["criteria"]
    
    prompts = []
    for j in range(judges):
        prompt = render_prompt(template,
            judge_id=j + 1,
            candidates=candidates_text,
            criteria="\n".join(f"- {c}" for c in criteria),
            round="round1",
            top_k=phase_cfg["top_k"]
        )
        prompts.append(prompt)
    
    print(f"  Round 1: {judges} judges scoring...")
    scores = run_parallel_agents(prompts, min(judges, config["codex"]["max_parallel"]), timeout)
    
    scores_path = Path(phase_cfg["output"]["scores"])
    ensure_dir(scores_path)
    scores_path.write_text("\n\n---\n\n".join(scores), encoding="utf-8")
    
    # TODO: Parse scores, select top_k, run advocate/skeptic, final judges
    # For MVP: pick first candidate as winner
    winner_path = Path(phase_cfg["output"]["winner"])
    ensure_dir(winner_path)
    winner_path.write_text(f"# Winner (placeholder)\n\nBased on tournament:\n\n{candidates_text[:3000]}", encoding="utf-8")
    
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
    
    results = []
    for i in range(iterations):
        prompt = render_prompt(template,
            iteration=i + 1,
            max_iterations=iterations,
            business_plan=plan_text,
            previous_feedback="" if i == 0 else results[-1][-2000:]
        )
        print(f"  Brand iteration {i+1}/{iterations}...")
        result = run_codex_agent(prompt, timeout)
        results.append(result)
    
    guide_path = Path(phase_cfg["output"]["guide"])
    ensure_dir(guide_path)
    guide_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    logo_path = Path(phase_cfg["output"]["logo"])
    ensure_dir(logo_path)
    logo_path.write_text("<svg>Logo placeholder - feed prompt to image generator</svg>", encoding="utf-8")
    
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
    landing_text = Path(config["phases"]["landing_page"]["output"]["dir"]).joinpath("index.html").read_text()[:5000]
    
    template = read_prompt("phase6_launch_video")
    prompt = render_prompt(template,
        brand_guide=brand_text,
        business_plan=plan_text,
        landing_page_summary=landing_text
    )
    
    print("  Writing launch video script...")
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
    prompt = render_prompt(template,
        brand_guide=brand_text,
        business_plan=plan_text
    )
    
    print("  Writing founder video script...")
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
    landing_text = Path(config["phases"]["landing_page"]["output"]["dir"]).joinpath("index.html").read_text()[:5000]
    
    template = read_prompt("phase8_red_team")
    attack_vectors = phase_cfg["attack_vectors"]
    skeptics = min(phase_cfg["skeptics"], len(attack_vectors))
    
    prompts = []
    for i in range(skeptics):
        vector = attack_vectors[i % len(attack_vectors)]
        prompt = render_prompt(template,
            attack_vector=vector,
            business_plan=plan_text,
            brand_guide=brand_text,
            landing_page_summary=landing_text
        )
        prompts.append(prompt)
    
    print(f"  Red team: {skeptics} skeptics attacking...")
    results = run_parallel_agents(prompts, min(skeptics, config["codex"]["max_parallel"]), timeout)
    
    verdict_path = Path(phase_cfg["output"]["verdict"])
    ensure_dir(verdict_path)
    verdict_path.write_text("\n\n---\n\n".join(results), encoding="utf-8")
    
    # TODO: Parse verdicts, generate fixes
    fixes_path = Path(phase_cfg["output"]["fixes"])
    ensure_dir(fixes_path)
    fixes_path.write_text("# Fixes Applied\n\n[Auto-generated after parsing verdicts]", encoding="utf-8")
    
    return [str(verdict_path), str(fixes_path)]


def phase9_recap(config: Dict, state: Dict) -> List[str]:
    """Phase 9: Package recap."""
    phase_cfg = config["phases"]["recap"]
    timeout = config["codex"]["timeout_seconds"]
    
    # Collect all artifact paths
    artifacts = {}
    for phase_name, phase_cfg in config["phases"].items():
        if "output" in phase_cfg:
            out = phase_cfg["output"]
            if isinstance(out, dict):
                for k, v in out.items():
                    artifacts[f"{phase_name}.{k}"] = v
            else:
                artifacts[phase_name] = out
    
    template = read_prompt("phase9_recap")
    prompt = render_prompt(template,
        artifacts_json=json.dumps(artifacts, indent=2),
        company_name="CounterBrief",  # Would parse from winner
        timestamp=datetime.now().isoformat()
    )
    
    print("  Generating HTML recap...")
    result = run_codex_agent(prompt, timeout)
    
    html_path = Path(phase_cfg["output"]["html"])
    ensure_dir(html_path)
    html_path.write_text(result, encoding="utf-8")
    
    return [str(html_path)]


PHASES = {
    1: ("Pain Hunt", phase1_pain_hunt),
    2: ("Tournament", phase2_tournament),
    3: ("Business Design", phase3_business_design),
    4: ("Brand", phase4_brand),
    5: ("Landing Page", phase5_landing_page),
    6: ("Launch Video", phase6_launch_video),
    7: ("Founder Video", phase7_founder_video),
    8: ("Red Team", phase8_red_team),
    9: ("Recap", phase9_recap),
}


def run_phase(num: int, config: Dict, state: Dict) -> List[str]:
    name, fn = PHASES[num]
    phase_state = state.get(str(num))
    
    if phase_state and phase_state.status == "completed":
        print(f"Phase {num} ({name}): already completed, skipping")
        return phase_state.output_files or []
    
    # Update state: running
    state[str(num)] = PhaseState(name=name, status="running", started_at=datetime.now().isoformat())
    save_state(state)
    
    print(f"\n{'='*50}")
    print(f"PHASE {num}: {name}")
    print(f"{'='*50}")
    
    try:
        outputs = fn(config, state)
        
        # Update state: completed
        state[str(num)] = PhaseState(
            name=name,
            status="completed",
            started_at=state[str(num)].started_at,
            completed_at=datetime.now().isoformat(),
            output_files=outputs
        )
        save_state(state)
        print(f"[OK] Phase {num} completed. Outputs: {outputs}")
        return outputs
        
    except Exception as e:
        state[str(num)] = PhaseState(
            name=name,
            status="failed",
            started_at=state[str(num)].started_at,
            completed_at=datetime.now().isoformat(),
            error=str(e)
        )
        save_state(state)
        print(f"[FAIL] Phase {num} failed: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Company Builder Orchestrator")
    parser.add_argument("--phase", type=int, help="Run specific phase (1-9)")
    parser.add_argument("--resume", action="store_true", help="Resume from last completed phase")
    parser.add_argument("--reset", action="store_true", help="Reset state and start fresh")
    args = parser.parse_args()
    
    config = load_config()
    
    if args.reset:
        state = {}
        (SKILL_ROOT / "state.json").unlink(missing_ok=True)
        print("State reset.")
    else:
        state = load_state()
    
    if args.phase:
        phases_to_run = [args.phase]
    elif args.resume:
        # Find first incomplete phase
        phases_to_run = []
        for i in range(1, 10):
            s = state.get(str(i))
            if not s or s.status != "completed":
                phases_to_run = list(range(i, 10))
                break
        if not phases_to_run:
            print("All phases completed!")
            return
    else:
        phases_to_run = list(range(1, 10))
    
    print(f"Running phases: {phases_to_run}")
    print(f"Config: {config['codex']['max_parallel']} parallel, {config['codex']['timeout_seconds']}s timeout")
    
    for phase_num in phases_to_run:
        try:
            run_phase(phase_num, config, state)
        except Exception as e:
            print(f"\n[FAIL] Pipeline failed at phase {phase_num}: {e}")
            sys.exit(1)
    
    print("="*50)
    print("ALL PHASES COMPLETE!")
    print("="*50)
    recap_path = SKILL_ROOT / "output" / "recap" / "index.html"
    if recap_path.exists():
        print(f"\nOpen: {recap_path}")
        print(f"      file://{recap_path.absolute()}")


if __name__ == "__main__":
    main()