#!/usr/bin/env python3
"""
Codex Agent Runner - Helper for running Codex CLI as a subprocess.
Used by orchestrator.py for parallel agent execution.
"""

import subprocess
import json
import sys
import os
from typing import Optional


def run_agent(prompt: str, timeout: int = 300, model: str = "sonnet") -> str:
    """
    Run a Codex agent with the given prompt.
    
    Args:
        prompt: The prompt to send to the agent
        timeout: Timeout in seconds
        model: Model to use (sonnet, opus, etc.)
    
    Returns:
        The agent's response text
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Use exec with stdin for prompt
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


if __name__ == "__main__":
    # CLI usage: python run_codex_agent.py "prompt" [timeout] [model]
    if len(sys.argv) < 2:
        print("Usage: python run_codex_agent.py \"prompt\" [timeout] [model]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    model = sys.argv[3] if len(sys.argv) > 3 else "sonnet"
    
    try:
        result = run_agent(prompt, timeout, model)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)