# RFC-001 — Approval Gates (Hardened)

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.1  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC introduces **Approval Gates** to the Inteligens Agents Framework execution model.

Approval Gates add structured human checkpoints to high‑risk phases while preserving the framework’s core principles:

- lightweight
- deterministic
- human‑in‑the‑loop
- IDE‑agnostic

The goal is to improve **execution safety, auditability, and governance discipline** without introducing heavy orchestration complexity.

---

## 2. Motivation

Current behavior:

- Steps advance via `--done`
- No formal approval semantics
- No structured human checkpoints

Risks:

- premature progression
- insufficient review on critical phases
- weak audit trail for sensitive steps

Approval Gates solve this by introducing an explicit **awaiting_approval** state.

---

## 3. Design Principles

The feature MUST:

- remain CLI‑friendly
- preserve human‑in‑the‑loop control
- avoid heavy policy engines
- remain optional per step
- be planner‑driven, not runner‑hardcoded

The feature MUST NOT:

- introduce background daemons
- require external services
- block normal lightweight usage

---

## 4. Execution State Model

The execution state machine becomes:

```
planned → in_progress → completed
                      ↘
                       awaiting_approval → completed
```

### States

| State | Meaning |
|------|--------|
| planned | Step not started |
| in_progress | Step being worked |
| completed | Step fully accepted |
| awaiting_approval | Step finished but requires human approval |

---

## 5. Gate Configuration

### 5.1 Planner Responsibility

Approval is determined **at planning time**.

Each execution step MAY include:

```json
"requires_approval": true | false
```

The **Swarm Planner MUST** decide this flag using heuristics such as:

- phase
- agent role
- risk level
- future policy rules

The **Execution Runner MUST NOT infer approval rules on its own.**

---

## 6. Runner Semantics

### 6.1 On `--done`

When a step finishes:

IF:

```
requires_approval == true
```

THEN runner MUST:

- set status → `awaiting_approval`
- block progression
- write journal entry

ELSE:

- set status → `completed`
- allow normal progression

---

### 6.2 On `--next`

IF current step status is:

```
awaiting_approval
```

Runner MUST:

- block advancement
- print clear instruction:

```
Step awaiting approval. Run:
python execution_runner.py --approve
```

Runner MUST NOT auto‑advance.

---

### 6.3 On `--approve` (NEW)

New CLI command:

```bash
python execution_runner.py --approve
```

Behavior:

- validates current step is `awaiting_approval`
- transitions step → `completed`
- records approval in journal
- unlocks progression

IF step is not awaiting approval:

- runner MUST fail with clear message

---

## 7. Journal Requirements

Approval events MUST be recorded in:

```
.agents/swarm/execution_journal.md
```

Required fields:

- timestamp (UTC)
- step number
- agent
- action: APPROVED

Example:

```markdown
### Approval — Step 8 — 2026-03-02T12:00:00Z
Agent: security/appsec-engineer.md
Status: APPROVED
```

---

## 8. Initial Gated Phases

For v1.1, planner SHOULD gate:

- architecture decisions
- security reviews
- release steps
- sprint closure

Planner MAY evolve heuristics in future versions.

---

## 9. Backward Compatibility

If `requires_approval` is absent:

- default MUST be `false`
- legacy plans MUST continue working

No breaking changes expected for v1.0 users.

---

## 10. Future Extensions (Non‑Goals for v1.1)

Explicitly out of scope:

- role‑based approvals
- multi‑approver workflows
- policy engines
- distributed approval services

These MAY be considered in future RFCs.

---

## 11. Acceptance Criteria

This RFC is considered implemented when:

- [ ] planner can emit `requires_approval`
- [ ] runner enters `awaiting_approval`
- [ ] `--next` blocks correctly
- [ ] `--approve` transitions state
- [ ] journal records approval
- [ ] legacy plans still run

---

## 12. Risks

| Risk | Mitigation |
|------|-----------|
| Over‑gating slows flow | Planner heuristics remain conservative |
| User confusion | Clear CLI messaging |
| State bugs | Deterministic transitions only |

---

## 13. Decision

**Status:** READY FOR IMPLEMENTATION (post review)

This feature is considered **foundational for safe semi‑autonomous execution** in future versions of the Inteligens Agents Framework.

---

**Inteligens — Agent‑native engineering**
