# Usage Guide — Inteligens Agents Framework

This guide explains how to operate the framework in a real engineering workflow.

---

## 🧭 Execution Model

The framework follows an assisted execution loop:

1. Planner generates the execution plan
2. Runner advances step-by-step
3. Human validates deliverables
4. Journal records progress

The system is intentionally **human-in-the-loop**.

---

## 🚀 Basic Flow

### 1. Generate the plan

```bash
python .agents/swarm/swarm_planner.py --task "your project goal"
```

The plan is saved to `.agents/swarm/execution_plan.json` by default. You can specify a custom path:

```bash
python .agents/swarm/swarm_planner.py --task "your project" --output custom_plan.json
```

**Note:** The planner automatically marks steps that require approval (architecture, security, release, closure). You'll see a warning indicating which steps are gated.

---

### 2. Initialize execution

```bash
python .agents/swarm/execution_runner.py --init
```

This uses `.agents/swarm/execution_plan.json` by default. To use a custom plan:

```bash
python .agents/swarm/execution_runner.py --init path/to/plan.json
```

---

### 3. Advance execution

```bash
python .agents/swarm/execution_runner.py --next
```

---

### 4. Mark step as completed

```bash
python .agents/swarm/execution_runner.py --done
```

---

### Approval Flow (optional)

Some steps automatically require explicit approval before proceeding. The Swarm Planner marks these steps with `requires_approval: true` based on heuristics (architecture decisions, security reviews, releases, sprint closure).

**When a step requires approval:**

1. Complete the step work
2. Run `--done` as usual
3. The system will indicate: "Step completed but awaiting approval"
4. Review the deliverables
5. Run `--approve` to approve and continue
6. Run `--next` to proceed to the next step

**Example flow:**

```bash
# Step 3 requires approval
python execution_runner.py --next    # Shows step 3
# ... do the work ...
python execution_runner.py --done    # "Step completed but awaiting approval"
python execution_runner.py --approve # "Step approved"
python execution_runner.py --next    # Shows step 4
```

**Note:** Steps without `requires_approval` proceed normally after `--done`.

---

## 🧠 Sprint-Aware Execution

During build phases, the runner injects:

- current sprint context
- sprint goals
- focused backlog items
- guardrails

Agents must work **only within the active sprint scope**.

---

## 🔒 Safety Principles

The framework:

- does NOT auto-execute code
- does NOT modify repositories silently
- requires human validation
- keeps full execution traceability

---

## 🧪 Recommended Workflow

For best results:

- Review each agent output
- Commit incrementally
- Validate Definition of Done
- Keep sprint scope tight

---

## 🧭 Troubleshooting

If execution seems inconsistent:

- verify execution_state.json
- check execution_journal.md
- confirm the correct plan was loaded
- ensure you ran `--done` before `--next`

---

**Philosophy:** structured progress over uncontrolled generation.
