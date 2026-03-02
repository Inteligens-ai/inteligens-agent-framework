#!/usr/bin/env python3
import json, argparse, os
from datetime import datetime

NOW = datetime.utcnow().isoformat() + "Z"
STATE_FILE = ".agents/swarm/execution_state.json"
JOURNAL_FILE = ".agents/swarm/execution_journal.md"

def load_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def append_journal(text: str):
    os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_registry():
    path = ".agents/agents/registry.json"
    if not os.path.exists(path):
        raise SystemExit("❌ registry.json not found. Run generator first.")
    return load_json(path)

def init_state(plan):
    state = {"generated": NOW, "current_step": 1, "completed_steps": [], "plan": plan}
    save_json(STATE_FILE, state)
    append_journal(f"\n## Init — {NOW}\nLoaded plan for task: **{plan.get('task','')}**\n")
    return state

def load_state():
    st = load_json(STATE_FILE)
    if not st:
        raise SystemExit("❌ execution_state.json not found. Run --init first.")
    return st

def build_agent_prompt(agent_name: str, registry):
    meta = registry["agents"].get(agent_name)
    if not meta:
        return f"# Agent: {agent_name}\n(No metadata found)"
    title = meta.get("title", agent_name)
    cmds = meta.get("commands", [])
    guidelines = meta.get("guidelines", [])
    handoffs = meta.get("handoffs", {})
    dod = meta.get("definition_of_done", [])

    lines = []
    lines.append(f"# Agent Execution — {title}")
    lines.append(f"**Agent file:** `.agents/agents/{agent_name}`")
    lines.append("")
    lines.append("## What to do now")
    lines.append("- Read the agent persona file and follow its rules.")
    lines.append("- Produce concrete artifacts (code/docs) ready to commit.")
    lines.append("")
    if cmds:
        lines.append("## Suggested Commands")
        for c in cmds:
            lines.append(f"- {c}")
        lines.append("")
    if guidelines:
        lines.append("## Guidelines")
        for g in guidelines:
            lines.append(f"- {g}")
        lines.append("")
    if handoffs:
        lines.append("## Handoffs")
        for k,v in handoffs.items():
            lines.append(f"- If you need **{k}** → handoff to `{v}`")
        lines.append("")
    if dod:
        lines.append("## Definition of Done")
        for item in dod:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)

def cmd_init(plan_path: str):
    plan = load_json(plan_path)
    if not plan:
        raise SystemExit(f"❌ Cannot load plan: {plan_path}")
    st = init_state(plan)
    print("✅ Execution state initialized.")
    print(f"Current step: {st['current_step']}")

def cmd_next():
    reg = load_registry()
    st = load_state()
    steps = st["plan"]["execution_plan"]
    idx = st["current_step"] - 1
    if idx >= len(steps):
        print("🎉 All steps completed.")
        return
    step = steps[idx]
    prompt = build_agent_prompt(step["agent"], reg)
    print("# =====================================")
    print(f"# STEP {st['current_step']} — phase={step.get('phase')}")
    print(f"# Agent: {step['agent']}")
    print("# =====================================\n")
    print(prompt)

def cmd_done(note: str | None):
    st = load_state()
    steps = st["plan"]["execution_plan"]
    idx = st["current_step"] - 1
    if idx >= len(steps):
        print("Nothing to complete.")
        return
    step = steps[idx]
    st["completed_steps"].append({"step": step["step"], "agent": step["agent"], "completed_at": NOW, "note": note})
    st["current_step"] += 1
    save_json(STATE_FILE, st)
    append_journal(f"\n### Done step {step['step']} — {NOW}\n- Agent: `{step['agent']}`\n- Note: {note or ''}\n")
    print(f"✅ Step {step['step']} completed.")
    print(f"➡️ Next step: {st['current_step']}")

def main():
    p = argparse.ArgumentParser(description="Execution Runner v8 (hybrid)")
    p.add_argument("--init", help="Initialize from execution plan JSON")
    p.add_argument("--next", action="store_true")
    p.add_argument("--done", action="store_true")
    p.add_argument("--note", type=str, default=None)
    args = p.parse_args()
    if args.init:
        return cmd_init(args.init)
    if args.next:
        return cmd_next()
    if args.done:
        return cmd_done(args.note)
    p.print_help()

if __name__ == "__main__":
    main()
