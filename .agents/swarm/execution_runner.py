#!/usr/bin/env python3
import json
import argparse
import os
from datetime import datetime, UTC

STATE_FILE = ".agents/swarm/execution_state.json"
JOURNAL_FILE = ".agents/swarm/execution_journal.md"

def now_utc():
    return datetime.now(UTC).isoformat()

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def append_journal(text):
    os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def cmd_init(plan_path=None):
    # Default to .agents/swarm/execution_plan.json if not provided
    if plan_path is None:
        plan_path = ".agents/swarm/execution_plan.json"
    
    plan = load_json(plan_path)
    if not plan:
        raise SystemExit(f"❌ Execution plan not found: {plan_path}")

    state = {
        "current_step": 1,
        "approved_steps": [],
        "plan": plan.get("execution_plan", [])
    }
    save_json(STATE_FILE, state)

    append_journal(f"## Init — {now_utc()}")
    append_journal(f"Loaded plan for task: **{plan.get('task','unknown')}**")
    append_journal("---")

    print("✅ Execution state initialized.")
    print("Current step: 1")

def cmd_next():
    state = load_json(STATE_FILE)
    if not state:
        raise SystemExit("❌ State not initialized")

    step_idx = state["current_step"] - 1
    plan = state["plan"]

    if step_idx >= len(plan):
        print("🏁 Execution finished.")
        return

    step = plan[step_idx]
    
    # Verificar se há um step anterior aguardando aprovação
    # (isso só acontece se --done foi chamado em um step com requires_approval mas --approve não foi chamado)
    if step_idx > 0:
        prev_step = plan[step_idx - 1]
        if (prev_step.get("requires_approval") and 
            (step_idx - 1) not in state.get("approved_steps", [])):
            print("⏸️ Previous step completed but awaiting approval. Use --approve to continue.")
            print(f"\nStep {prev_step['step']} ({prev_step.get('agent')}) is waiting for approval.")
            return

    # Sempre mostrar o step atual (permitir execução)
    print("# =====================================")
    print(f"# STEP {step['step']} — phase={step.get('phase')}")
    print(f"# Agent: {step.get('agent')}")
    if step.get("requires_approval"):
        print("# ⚠️  This step requires approval after completion")
    print("# =====================================\n")
    print("Follow the agent persona and produce concrete deliverables.")

def cmd_done():
    state = load_json(STATE_FILE)
    if not state:
        raise SystemExit("❌ State not initialized")

    step_idx = state["current_step"] - 1
    plan = state["plan"]

    if step_idx >= len(plan):
        print("🏁 Nothing to complete.")
        return

    step = plan[step_idx]

    append_journal(f"### Done Step {step['step']} — {now_utc()}")
    append_journal(f"Agent: `{step.get('agent', 'unknown')}`")

    # Se requer aprovação, NÃO avança current_step ainda
    if step.get("requires_approval"):
        append_journal(f"Status: AWAITING_APPROVAL")
        print("⏸️ Step completed but awaiting approval. Use --approve to continue.")
        # NÃO avança current_step aqui
    else:
        state["current_step"] += 1
        append_journal(f"Status: COMPLETED")
        print("✅ Step marked as done.")
    
    save_json(STATE_FILE, state)

def cmd_approve():
    state = load_json(STATE_FILE)
    if not state:
        raise SystemExit("❌ State not initialized")

    step_idx = state["current_step"] - 1
    plan = state["plan"]

    if step_idx < 0 or step_idx >= len(plan):
        raise SystemExit("❌ No step to approve")

    step = plan[step_idx]

    # Validar que step requer aprovação
    if not step.get("requires_approval"):
        raise SystemExit("❌ Current step does not require approval")

    # Validar que ainda não foi aprovado
    if step_idx in state.get("approved_steps", []):
        raise SystemExit("❌ Step already approved")

    # Registrar aprovação
    state.setdefault("approved_steps", []).append(step_idx)
    
    # Registrar no journal (formato RFC)
    append_journal(f"### Approval — Step {step['step']} — {now_utc()}")
    append_journal(f"Agent: `{step.get('agent', 'unknown')}`")
    append_journal(f"Status: APPROVED")
    
    # Agora sim avança para o próximo step
    state["current_step"] += 1
    save_json(STATE_FILE, state)

    print("✅ Step approved.")

def main():
    p = argparse.ArgumentParser(description="Execution Runner — Step-by-step execution with Approval Gates")
    p.add_argument("--init", nargs="?", const=".agents/swarm/execution_plan.json",
                   help="Initialize execution (default: .agents/swarm/execution_plan.json)")
    p.add_argument("--next", action="store_true", help="Show next step")
    p.add_argument("--done", action="store_true", help="Mark current step as done")
    p.add_argument("--approve", action="store_true", help="Approve current gated step")
    args = p.parse_args()

    if args.init is not None:
        cmd_init(args.init)
    elif args.next:
        cmd_next()
    elif args.done:
        cmd_done()
    elif args.approve:
        cmd_approve()
    else:
        p.print_help()

if __name__ == "__main__":
    main()
