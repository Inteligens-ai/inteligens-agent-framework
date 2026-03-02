# Approval Gates — Inteligens Agents Framework

## Overview

Approval Gates introduce human-in-the-loop control between critical phases. Steps that require approval are automatically marked by the Swarm Planner based on heuristics defined in RFC-001.

## Automatic Gating

The Swarm Planner automatically marks steps with `requires_approval: true` for:

- **Architecture decisions**: Design phase with Staff Architect
- **Security reviews**: Test phase with AppSec Engineer
- **Release steps**: All release phase steps
- **Sprint closure**: Sprint closure phase

When you generate an execution plan, the planner will indicate which steps require approval:

```bash
python .agents/swarm/swarm_planner.py --task "your project"
# ✅ Plan generated: .agents/swarm/execution_plan.json
# ⚠️  Steps requiring approval: 3, 10, 11, 13
```

## CLI Flow

### 1. Generate plan (with automatic gating)

```bash
python .agents/swarm/swarm_planner.py --task "your project goal"
```

The plan is saved to `.agents/swarm/execution_plan.json` by default. You can specify a custom output path:

```bash
python .agents/swarm/swarm_planner.py --task "your project" --output custom_plan.json
```

### 2. Initialize execution

```bash
python .agents/swarm/execution_runner.py --init
```

This uses the default plan path (`.agents/swarm/execution_plan.json`). To use a custom plan:

```bash
python .agents/swarm/execution_runner.py --init path/to/plan.json
```

### 3. Execute step

```bash
python .agents/swarm/execution_runner.py --next
```

### 4. Mark step as done

```bash
python .agents/swarm/execution_runner.py --done
```

If the step requires approval, you'll see:
```
⏸️ Step completed but awaiting approval. Use --approve to continue.
```

### 5. Approve gated step

```bash
python .agents/swarm/execution_runner.py --approve
```

### 6. Continue to next step

```bash
python .agents/swarm/execution_runner.py --next
```

## How It Works

1. **Planning**: Planner marks steps with `requires_approval: true` based on phase and agent role
2. **Execution**: Runner blocks progression on gated steps until approval
3. **Approval**: Human reviews and approves using `--approve` command
4. **Journal**: All approval events are recorded in `execution_journal.md`

## Best Practices

- Review deliverables before approving
- Do not overuse gates (planner handles this automatically)
- Keep fast feedback loops
- Approval events are fully auditable via journal

## See Also

- [RFC-001: Approval Gates](../rfcs/RFC-001-approval-gates.md) — Full specification
- [Usage Guide](../guides/USAGE_GUIDE.md) — Complete workflow documentation