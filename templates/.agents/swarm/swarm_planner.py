#!/usr/bin/env python3
import json, argparse, subprocess, os
from datetime import datetime

NOW = datetime.utcnow().isoformat() + "Z"
BASE = ".agents/swarm"

PHASE_ORDER = {"plan":1,"design":2,"build":3,"test":4,"release":5}
AGENT_GROUPS = {
    "product/": "plan",
    "project-management/": "plan",
    "engineering/staff-architect": "design",
    "engineering/tech-lead": "design",
    "engineering/backend": "build",
    "engineering/frontend": "build",
    "engineering/ai": "build",
    "engineering/data": "build",
    "testing/": "test",
    "security/": "test",
    "engineering/devops": "release",
}

def infer_agent_phase(agent_name: str) -> str:
    for prefix, phase in AGENT_GROUPS.items():
        if prefix in agent_name:
            return phase
    return "build"

def safe_read_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_swarm_policies():
    planner_path = os.path.join(BASE, "planner.md")
    autonomous_path = os.path.join(BASE, "autonomous_mode.md")
    planner_text = safe_read_text(planner_path)
    autonomous_text = safe_read_text(autonomous_path)
    return {
        "planner_loaded": bool(planner_text.strip()),
        "autonomous_loaded": bool(autonomous_text.strip()),
        "planner_length": len(planner_text),
        "autonomous_length": len(autonomous_text),
    }

def build_execution_plan(router_output: dict):
    agents = router_output["top"]
    enriched = []
    for a in agents:
        phase = infer_agent_phase(a["agent"])
        enriched.append({**a, "phase": phase, "phase_order": PHASE_ORDER.get(phase, 3)})
    enriched.sort(key=lambda x: x["phase_order"])

    steps = []
    for i, agent in enumerate(enriched, 1):
        steps.append({
            "step": i,
            "agent": agent["agent"],
            "phase": agent["phase"],
            "confidence": agent["confidence"],
            "parallelizable": agent["phase"] == "build",
            "status": "planned",
        })
    return steps

def main():
    p = argparse.ArgumentParser(description="Swarm Planner v7.1 (Policy-Aware) — hybrid")
    p.add_argument("--task", required=True)
    p.add_argument("--product", default=None)
    p.add_argument("--router", default=".agents/router/agent_router.py")
    args = p.parse_args()

    policy_info = load_swarm_policies()

    cmd = ["python", args.router, "--task", args.task, "--format", "json"]
    if args.product:
        cmd += ["--product", args.product]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit("Router failed")
    router_output = json.loads(r.stdout)
    plan = build_execution_plan(router_output)

    out = {
        "generated": NOW,
        "swarm_version": "7.1.0",
        "policy_aware": True,
        "policy_status": policy_info,
        "task": args.task,
        "product": args.product,
        "execution_plan": plan,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
