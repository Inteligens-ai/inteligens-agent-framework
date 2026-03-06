# RFC-002 — Step Dependencies and Blocking States

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.1  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC introduces **dependency management and blocking states** to the Inteligens Agents Framework execution model.

The feature allows steps to be marked as partially complete or blocked when they depend on work from other steps, with automatic detection of dependency resolution and support for backward navigation.

This addresses real-world scenarios where:
- Backend implementation depends on AI service interfaces (Step 5 depends on Step 7)
- Frontend depends on Backend API contracts
- Tests depend on implementation completion
- Any cross-step dependency that prevents full completion

---

## 2. Motivation

**Problem Statement:**

During execution, agents may identify that their work cannot be fully completed because it depends on deliverables from steps that haven't been executed yet. For example:

- Step 5 (Backend Engineer) needs AI service interface definitions from Step 7 (AI Engineer)
- Step 6 (Frontend Engineer) needs API contracts from Step 5 (Backend Engineer)
- Step 9 (QA Strategist) needs implementation from Step 5 (Backend Engineer)

**Current Limitations:**

- No way to mark steps as partially complete
- No way to track which steps are blocked by dependencies
- No automatic detection when dependencies are resolved
- No safe way to navigate back to complete blocked steps
- Manual workarounds (editing backlog, restarting execution) are error-prone

**Solution:**

Introduce blocking states and dependency tracking that:
- Allow steps to be marked as `partial` or `blocked`
- Track dependencies between steps
- Automatically detect when dependencies are resolved
- Support safe backward navigation
- Maintain full observability in journal

---

## 3. Design Principles

The feature MUST:

- remain CLI-friendly
- preserve human-in-the-loop control
- maintain full journal traceability
- be backward compatible
- support automatic dependency detection
- allow manual dependency declaration

The feature MUST NOT:

- introduce background daemons
- require external services
- block normal lightweight usage
- force dependency declaration (optional)

---

## 4. Extended Execution State Model

The execution state machine is extended to include `partial` and `blocked` states:

```
planned → in_progress → completed
                      ↘
                       partial → blocked → completed
                                  ↑
                                  └── (dependency resolved)
```

### States

| State | Meaning |
|-------|---------|
| `planned` | Step not started |
| `in_progress` | Step being worked |
| `partial` | Step work started but incomplete due to dependencies |
| `blocked` | Step cannot proceed until dependencies are resolved |
| `completed` | Step fully accepted |
| `awaiting_approval` | Step finished but requires human approval |

**State Transitions:**

- `in_progress` → `partial`: When `--done --partial` is called
- `partial` → `blocked`: When dependencies are explicitly tracked
- `blocked` → `in_progress`: When dependencies are resolved (via `--resolve`)
- `partial` → `completed`: When work is completed after dependency resolution

---

## 5. Execution Plan Schema Extension

Each execution step MAY include:

```json
{
  "step": 5,
  "agent": "engineering/backend-engineer.md",
  "phase": "build",
  "requires_approval": false,
  "dependencies": [7],  // NEW: List of step numbers this step depends on
  "can_proceed_partial": true  // NEW: Whether step can be partially completed
}
```

### Fields

- **`dependencies`** (optional, array of integers): Step numbers that this step depends on. Defaults to `[]` if absent.
- **`can_proceed_partial`** (optional, boolean): Whether this step can be partially completed when dependencies are not met. Defaults to `false` if absent.

**Backward Compatibility:**

- Existing plans without these fields work normally
- Missing fields default to safe values (`[]` and `false`)

---

## 6. Execution State Schema Extension

The execution state is extended to track blocked steps:

```json
{
  "current_step": 7,
  "approved_steps": [3],
  "blocked_steps": {  // NEW: Track blocked/partial steps
    "5": {
      "status": "partial",
      "blocked_by": [7],
      "reason": "Backend requires AI service interface definition",
      "completed_at": "2026-03-02T10:00:00Z",
      "resolved_at": null
    }
  },
  "step_statuses": {  // NEW: Per-step status tracking
    "5": "partial",
    "7": "in_progress"
  },
  "plan": [...]
}
```

### Fields

- **`blocked_steps`** (optional, object): Maps step numbers to blocking metadata. Key is step number as string.
- **`step_statuses`** (optional, object): Maps step numbers to current status. Key is step number as string.

**Blocked Step Metadata:**

- `status`: Current status (`partial` or `blocked`)
- `blocked_by`: Array of step numbers this step depends on
- `reason`: Human-readable reason for blocking
- `completed_at`: ISO timestamp when step was marked as partial/blocked
- `resolved_at`: ISO timestamp when dependencies were resolved (null if not resolved)

---

## 7. Runner Semantics

### 7.1 On `--done --partial`

New optional flag for `--done`:

```bash
python execution_runner.py --done --partial --blocked-by 7 --reason "Waiting for AI service interface"
```

**Behavior:**

- Marks current step as `partial`
- Records in `blocked_steps` with metadata
- Updates `step_statuses`
- Writes journal entry with status `PARTIAL`
- Advances `current_step` (allows continuing to next step)
- Does NOT mark step as fully completed

**Validation:**

- `--blocked-by` must be a valid step number
- Step must exist in execution plan
- Reason is optional but recommended

### 7.2 On `--block`

New CLI command:

```bash
python execution_runner.py --block --blocked-by 7 --reason "Cannot proceed without AI service interface"
```

**Behavior:**

- Marks current step as `blocked`
- Records in `blocked_steps` with metadata
- Updates `step_statuses`
- Writes journal entry with status `BLOCKED`
- Advances `current_step` (allows continuing to next step)

**Difference from `--done --partial`:**

- `--block` is for steps that cannot proceed at all
- `--done --partial` is for steps that have partial work completed

### 7.3 On `--back`

New CLI command for backward navigation:

```bash
python execution_runner.py --back 5  # Navigate to step 5
python execution_runner.py --back   # Navigate to previous step
```

**Behavior:**

- If step number provided: Navigate to that specific step
- If no step number: Navigate to previous step (current_step - 1)
- Validates step exists
- Updates `current_step`
- Shows step instructions (same as `--next`)
- Writes journal entry for navigation

**Validation:**

- Step number must be valid (1 to max step)
- Step must exist in execution plan
- Warns if navigating to future step (but allows it)

### 7.4 On `--resolve`

New CLI command for dependency resolution:

```bash
python execution_runner.py --resolve 5  # Check and resolve dependencies for step 5
python execution_runner.py --resolve    # Auto-detect and suggest resolutions
```

**Behavior:**

- If step number provided: Check if that step's dependencies are resolved
- If no step number: Auto-detect all blocked steps with resolved dependencies
- For each resolved step:
  - Update `blocked_steps[step]["resolved_at"]`
  - Update `step_statuses[step]` to `in_progress`
  - Write journal entry
  - Suggest navigating back: `python execution_runner.py --back <step>`

**Dependency Resolution Logic:**

A step's dependencies are considered resolved when:
- All dependency steps have status `completed` OR
- All dependency steps have status `awaiting_approval` (and will be approved)

### 7.5 On `--done` (automatic detection)

When `--done` is called, the runner automatically:

1. Checks if any blocked steps depend on the completed step
2. If yes, suggests running `--resolve` for those steps
3. Prints message: "Step X completed. Blocked steps may be resolved: [5, 6]. Run `--resolve` to check."

### 7.6 On `--next` (dependency warnings)

When `--next` is called, the runner:

1. Checks if current step has unresolved dependencies (from plan)
2. If yes, warns: "⚠️  Step X depends on steps [7] which are not yet completed. You may proceed, but consider using `--done --partial` if blocked."
3. Shows list of currently blocked steps (from state)

---

## 8. Planner Semantics

### 8.1 Dependency Detection (Optional)

The Swarm Planner MAY detect common dependency patterns:

- Backend depends on AI (service interfaces)
- Frontend depends on Backend (API contracts)
- Tests depend on implementation
- DevOps depends on architecture decisions

**Heuristics:**

```python
def detect_dependencies(steps_data: list) -> dict:
    dependencies = {}
    
    # Backend often depends on AI for service interfaces
    backend_step = find_step(steps_data, "backend-engineer")
    ai_step = find_step(steps_data, "ai-engineer")
    if backend_step and ai_step and backend_step["step"] < ai_step["step"]:
        dependencies[backend_step["step"]] = [ai_step["step"]]
    
    # Frontend depends on Backend
    frontend_step = find_step(steps_data, "frontend-engineer")
    if frontend_step and backend_step and frontend_step["step"] < backend_step["step"]:
        dependencies[frontend_step["step"]] = [backend_step["step"]]
    
    return dependencies
```

**Note:** This is optional. Dependencies can also be declared manually or detected at runtime.

### 8.2 Plan Generation Warnings

After generating execution plan, planner SHOULD warn about detected dependencies:

```
✅ Plan generated: .agents/swarm/execution_plan.json
⚠️  Steps requiring approval: 3, 10, 11, 13
⚠️  Steps with dependencies detected:
  Step 5 depends on Step 7 (Backend → AI service interfaces)
```

---

## 9. Journal Requirements

Blocking events MUST be recorded in:

```
.agents/swarm/execution_journal.md
```

**Required entries:**

### Partial Completion

```markdown
### Done Step 5 — 2026-03-02T10:00:00Z
Agent: `engineering/backend-engineer.md`
Status: PARTIAL
Blocked by: [7]
Reason: Backend requires AI service interface definition
```

### Blocked

```markdown
### Block Step 5 — 2026-03-02T10:00:00Z
Agent: `engineering/backend-engineer.md`
Status: BLOCKED
Blocked by: [7]
Reason: Cannot proceed without AI service interface
```

### Navigation

```markdown
### Navigate — 2026-03-02T11:00:00Z
From: Step 7
To: Step 5
Reason: Returning to complete blocked step
```

### Resolution

```markdown
### Resolve Step 5 — 2026-03-02T11:00:00Z
Agent: `engineering/backend-engineer.md`
Status: RESOLVED
Dependencies resolved: [7]
Suggested action: Navigate back to Step 5 to complete work
```

---

## 10. Example Workflow

### Scenario: Backend depends on AI

```bash
# Step 5: Backend identifies dependency
python execution_runner.py --next
# ... agent works on backend ...
# Agent identifies: "Need AI service interface from Step 7"

# Mark as partial
python execution_runner.py --done --partial --blocked-by 7 --reason "Waiting for AI service interface definition"

# Continue to Step 7
python execution_runner.py --next
# ... agent works on AI service ...
python execution_runner.py --done

# Framework detects dependency resolved
# Output: "Step 7 completed. Blocked steps may be resolved: [5]. Run `--resolve 5` to check."

# Resolve dependencies
python execution_runner.py --resolve 5
# Output: "Step 5 dependencies resolved. Navigate back: `python execution_runner.py --back 5`"

# Return to Step 5
python execution_runner.py --back 5
# ... complete remaining backend work ...
python execution_runner.py --done
```

---

## 11. Backward Compatibility

**Execution Plans:**

- Plans without `dependencies` field work normally (defaults to `[]`)
- Plans without `can_proceed_partial` field work normally (defaults to `false`)
- No breaking changes

**Execution State:**

- State files without `blocked_steps` work normally (treated as empty `{}`)
- State files without `step_statuses` work normally (treated as empty `{}`)
- No breaking changes

**CLI Commands:**

- Existing commands (`--next`, `--done`, `--approve`, `--skip`) unchanged
- New commands (`--block`, `--back`, `--resolve`) are optional
- `--done --partial` is optional flag, doesn't affect normal `--done`

---

## 12. Future Extensions (Non-Goals for v1.1)

Explicitly out of scope:

- Automatic dependency resolution without human confirmation
- Circular dependency detection (may warn, but won't prevent)
- Dependency graph visualization
- Parallel execution of independent steps
- Dynamic plan reordering based on dependencies

These may be considered for v2.0+.

---

## 13. Acceptance Criteria

- [ ] Execution runner supports `--block` command
- [ ] Execution runner supports `--done --partial` flag
- [ ] Execution runner supports `--back` command
- [ ] Execution runner supports `--resolve` command
- [ ] Automatic dependency detection in `--done`
- [ ] Dependency warnings in `--next`
- [ ] Swarm planner detects common dependency patterns (optional)
- [ ] Swarm planner warns about dependencies in plan output
- [ ] Journal entries for all blocking events
- [ ] Backward compatibility maintained
- [ ] Documentation updated (Usage Guide, Roadmap, Architecture)

---

## 14. Decision

**Status:** Proposed for v1.1

**Rationale:**

This RFC addresses a critical gap in the framework's execution model. Real-world projects frequently have inter-step dependencies, and the current model forces workarounds that lose observability and are error-prone.

The proposed solution:
- Maintains CLI-friendly operation
- Preserves human-in-the-loop control
- Adds full observability
- Is backward compatible
- Supports both automatic and manual dependency management

**Next Steps:**

1. Review and approve RFC
2. Implement execution runner changes
3. Implement planner enhancements (optional)
4. Update documentation
5. Test with real-world scenarios
6. Release in v1.1

---

**See Also:**

- [RFC-001: Approval Gates](RFC-001-approval-gates.md) — Related state management
- [Usage Guide](../../guides/USAGE_GUIDE.md) — User-facing documentation
- [Evolution Roadmap](../../roadmap/EVOLUTION_ROADMAP.md) — Technical roadmap
