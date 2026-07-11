#!/usr/bin/env python3
"""
Codex Agent Runner - Helper for running Codex CLI as subprocess.
Used by orchestrator.py for parallel agent execution.
"""

import subprocess
import json
import os
import sys
from typing import Optional


def run_codex_agent(prompt: str, timeout: int = 300, model: str = "sonnet") -> str:
    """
    Run a Codex agent with the given prompt.
    
    Args:
        prompt: The prompt to send to the agent
        timeout: Timeout in seconds (default 5 min)
        model: Model to use (sonnet, opus, etc.)
    
    Returns:
        The agent's response text
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Use exec with stdin for prompt
    # On Windows, codex is a .ps1 script, need to call via powershell
    if sys.platform == "win32":
        cmd = ["powershell", "-NoProfile", "-Command", "codex", "exec", "--json", "-"]
    else:
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
        raise RuntimeError(f"Agent timed out after {timeout}s")
    
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"Agent failed (exit {proc.returncode}): {stderr}")
    
    # Parse JSONL output for agent_message
    response_parts = []
    for line in proc.stdout.decode("utf-8", errors="replace").strip().split("\n"):
        if not line:
            continue
        try:
            event = json.loads(line)
            if event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    response_parts.append(item.get("text", ""))
        except json.JSONDecodeError:
            pass
    
    return "".join(response_parts).strip()


def run_parallel_agents(prompts: list, max_parallel: int, timeout: int) -> list:
    """
    Run multiple agents in parallel using thread pool.
    
    Args:
        prompts: List of prompts to run
        max_parallel: Maximum concurrent agents
        timeout: Timeout per agent in seconds
    
    Returns:
        List of results in same order as prompts
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    results = [None] * len(prompts)
    
    def run_one(idx: int, prompt: str):
        try:
            results[idx] = run_codex_agent(prompt, timeout)
        except Exception as e:
            results[idx] = f"ERROR: {e}"
    
    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        futures = [executor.submit(run_one, i, p) for i, p in enumerate(prompts)]
        for f in as_completed(futures):
            f.result()  # Raise any exceptions
    
    return results


# Alias for backward compatibility
run_agent = run_codex_agent


if __name__ == "__main__":
    # CLI usage: python run_codex_agent.py "prompt" [timeout] [model]
    if len(sys.argv) < 2:
        print("Usage: python run_codex_agent.py \"prompt\" [timeout] [model]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    model = sys.argv[3] if len(sys.argv) > 3 else "sonnet"
    
    try:
        result = run_codex_agent(prompt, timeout, model)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)