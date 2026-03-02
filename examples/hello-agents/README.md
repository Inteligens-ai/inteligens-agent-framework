# Hello Agents — Minimal Example

This example demonstrates the full assisted execution flow.

## Step 1 — Generate plan

```bash
python3 .agents/swarm/swarm_planner.py --task "build simple api"
```

The plan is saved to `.agents/swarm/execution_plan.json` by default.

## Step 2 — Initialize execution

```bash
python3 .agents/swarm/execution_runner.py --init
```

This uses the default plan path (`.agents/swarm/execution_plan.json`).

## Step 3 — Run first step

```bash
python3 .agents/swarm/execution_runner.py --next
```

Follow the instructions shown by the runner.

---

This proves the framework is working end-to-end.
