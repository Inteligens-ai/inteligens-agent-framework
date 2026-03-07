#!/usr/bin/env python3
"""Swarm Planner — Generates multi-agent execution plans with Approval Gates."""
import json
import argparse
import os
from datetime import datetime, UTC

def should_require_approval(step: dict) -> bool:
    """
    Determine if step requires approval based on RFC-001 heuristics.
    
    Gates are applied to:
    - Architecture decisions (design phase, staff-architect)
    - Security reviews (test phase, appsec-engineer)
    - Release steps (release phase)
    - Sprint closure (closure phase)
    """
    phase = step.get("phase", "")
    agent = step.get("agent", "")
    
    # Architecture decisions
    if phase == "design" and "staff-architect" in agent:
        return True
    
    # Security reviews
    if phase == "test" and "appsec-engineer" in agent:
        return True
    
    # Release steps
    if phase == "release":
        return True
    
    # Sprint retrospective
    if phase == "retrospective":
        return True

    # Sprint closure
    if phase == "closure":
        return True
    
    return False

def main():
    DEFAULT_OUTPUT = ".agents/swarm/execution_plan.json"
    
    parser = argparse.ArgumentParser(description="Swarm Planner — Generate execution plans with Approval Gates")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, 
                       help=f"Output path for execution plan (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    steps_data = [
        {"step": 1,  "agent": "product/product-owner.md",                              "phase": "plan"},
        {"step": 2,  "agent": "project-management/scrum-master.md",                    "phase": "plan"},
        {"step": 3,  "agent": "engineering/staff-architect.md",                        "phase": "design"},
        {"step": 4,  "agent": "engineering/tech-lead.md",                              "phase": "design"},
        {"step": 5,  "agent": "engineering/backend-engineer.md",                       "phase": "build"},
        {"step": 6,  "agent": "engineering/frontend-engineer.md",                      "phase": "build"},
        {"step": 7,  "agent": "engineering/ai-engineer.md",                            "phase": "build"},
        {"step": 8,  "agent": "engineering/devops-sre.md",                             "phase": "build"},
        {"step": 9,  "agent": "testing/qa-strategist.md",                              "phase": "test"},
        {"step": 10, "agent": "security/appsec-engineer.md",                           "phase": "test"},
        {"step": 11, "agent": "project-management/release-manager.md",                 "phase": "release"},
        {"step": 12, "agent": "project-management/sprint-reviewer.md",                 "phase": "review"},
        {"step": 13, "agent": "project-management/retrospective-facilitator.md",       "phase": "retrospective"},
        {"step": 14, "agent": "project-management/sprint-closer.md",                   "phase": "closure"},
    ]
    
    # Add requires_approval flag based on heuristics
    execution_plan = []
    for step_data in steps_data:
        step = step_data.copy()
        step["requires_approval"] = should_require_approval(step)
        execution_plan.append(step)

    plan = {
        "generated": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "swarm_version": "7.3.0",
        "task": args.task,
        "execution_plan": execution_plan,
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print(f"✅ Plan generated: {args.output}")
    
    # Show which steps require approval
    gated_steps = [s["step"] for s in execution_plan if s.get("requires_approval")]
    if gated_steps:
        print(f"⚠️  Steps requiring approval: {', '.join(map(str, gated_steps))}")

if __name__ == "__main__":
    main()
