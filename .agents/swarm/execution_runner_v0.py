#!/usr/bin/env python3
"""Execution Runner — Inteligens Agents Framework v1 SAFE
Assisted, stateful, sprint-aware execution with optional approval gates.
"""

import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = ".agents/swarm/execution_state.json"
JOURNAL_FILE = ".agents/swarm/execution_journal.md"


# ================================
# Helpers
# ================================

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_journal(text: str):
    Path(JOURNAL_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def step_requires_approval(step: dict) -> bool:
    """Backward-compatible approval check."""
    return step.get("requires_approval", False)


def get_step_status(step: dict) -> str:
    """Backward-compatible status getter."""
    return step.get("status", "planned")


def set_step_status(step: dict, status: str):
    step["status"] = status


# ================================
# Rendering (mantido do seu)
# ================================

def render_sprint_context(step: dict) -> str:
    sprint = step.get("sprint")
    if not sprint:
        return ""
    focus = "\n".join(f"- {item}" for item in sprint.get("focus_items", []))
    guards = "\n".join(f"- {g}" for g in sprint.get("guardrails", []))
    return f"""
## Sprint Context
Current Sprint: {sprint.get('name')}
Sprint Goal: {sprint.get('goal')}

### Focus Backlog Items
{focus}

### Guardrails
{guards}

⚠️ IMPORTANT:
- Work ONLY on the items above.
- Do NOT implement future sprint features.
- Deliver minimal, testable increments.
""".rstrip()


def render_agent_execution_block(step: dict) -> str:
    agent = step.get("agent", "")
    return f"""
# Agent Execution
Agent: {agent}

## What to do now
- Read the agent persona file and follow its rules.
- Produce concrete deliverables (code/docs) ready to commit.

## Definition of Done
- Produce deliverables aligned to the current phase.
- Keep scope minimal and shippable.
""".rstrip()


def build_prompt(step: dict) -> str:
    header = f"""# =====================================
# STEP {step.get('step')} — phase={step.get('phase')}
# Agent: {step.get('agent')}
# =====================================

Follow the agent persona and produce concrete deliverables.
""".rstrip()

    parts = [header, "", render_agent_execution_block(step)]
    sprint_block = render_sprint_context(step)
    if sprint_block:
        parts += ["", sprint_block]

    return "\n".join(parts).strip() + "\n"


# ================================
# Commands
# ================================

def cmd_init(plan_path: str):
    plan = load_json(plan_path)
    state = {
        "current_step": 1,
        "plan": plan,
        "initialized_at": now_iso(),
    }
    save_json(STATE_FILE, state)

    append_journal(
        f"## Init — {now_iso()}\n"
        f"Loaded plan for task: **{plan.get('task','')}**\n"
    )

    print("✅ Execution state initialized.")
    print("Current step: 1")


def cmd_next():
    state = load_json(STATE_FILE)
    steps = state["plan"]["execution_plan"]
    idx = state["current_step"] - 1

    if idx >= len(steps):
        print("🏁 Plan complete.")
        return

    step = steps[idx]

    # 🔒 Approval guard
    if get_step_status(step) == "awaiting_approval":
        print(
            "⛔ Step is awaiting approval.\n"
            "Run:\n"
            "  python .agents/swarm/execution_runner.py --approve"
        )
        return

    print(build_prompt(step))


def cmd_done():
    state = load_json(STATE_FILE)
    steps = state["plan"]["execution_plan"]
    idx = state["current_step"] - 1

    if idx >= len(steps):
        print("🏁 Plan already complete.")
        return

    step = steps[idx]

    # 🚦 Approval logic (backward compatible)
    if step_requires_approval(step):
        set_step_status(step, "awaiting_approval")

        append_journal(
            f"### Done Step {step.get('step')} — {now_iso()}\n"
            f"Status: AWAITING_APPROVAL\n"
            f"Agent: {step.get('agent')}\n"
        )

        save_json(STATE_FILE, state)
        print("⏸️ Step completed but awaiting approval.")
        return

    # ✅ normal flow
    set_step_status(step, "completed")
    state["current_step"] += 1
    save_json(STATE_FILE, state)

    append_journal(
        f"### Done Step {step.get('step')} — {now_iso()}\n"
        f"Status: COMPLETED\n"
        f"Agent: {step.get('agent')}\n"
    )

    print(f"✅ Step {step.get('step')} marked done.")


def cmd_approve():
    state = load_json(STATE_FILE)
    steps = state["plan"]["execution_plan"]
    idx = state["current_step"] - 1

    if idx >= len(steps):
        print("❌ No current step.")
        return

    step = steps[idx]

    if get_step_status(step) != "awaiting_approval":
        print("❌ Current step is not awaiting approval.")
        return

    set_step_status(step, "completed")
    state["current_step"] += 1
    save_json(STATE_FILE, state)

    append_journal(
        f"### Approval — Step {step.get('step')} — {now_iso()}\n"
        f"Agent: {step.get('agent')}\n"
        f"Status: APPROVED\n"
    )

    print("✅ Step approved. You may now run --next.")


# ================================
# CLI
# ================================

def main():
    p = argparse.ArgumentParser(
        description="Inteligens Execution Runner (sprint-aware + approval gates)"
    )
    p.add_argument("--init", help="Initialize from execution_plan.json")
    p.add_argument("--next", action="store_true")
    p.add_argument("--done", action="store_true")
    p.add_argument("--approve", action="store_true")

    a = p.parse_args()

    if a.init:
        cmd_init(a.init)
    elif a.next:
        cmd_next()
    elif a.done:
        cmd_done()
    elif a.approve:
        cmd_approve()
    else:
        p.print_help()


if __name__ == "__main__":
    main()