# EVOLUTION ROADMAP — Inteligens Agents Framework

> Technical evolution plan for the Agent Operating Framework (AOF)

---

## Purpose

This document defines the **technical evolution strategy** of the Inteligens Agents Framework.

Unlike the public roadmap, this document focuses on:

- architectural maturity
- execution safety
- human governance
- swarm intelligence progression
- operational discipline

It is intended for architects, maintainers, and advanced contributors.

---

# Current State — v1.0.x Foundation

## What is working

- Assisted auto-execution loop
- Multi-agent orchestration (15+ roles)
- Phase-based delivery (plan → design → build → test → release)
- Sprint-aware build context
- Execution journal and state tracking
- IDE-agnostic operation
- Human-in-the-loop enforcement
- Approval Gates (human checkpoints between critical phases)
- **Strengthened agent personas** (v1.0.1): output contracts, failure modes, verifiable DoD per agent

This establishes a **controlled execution baseline**.

---

## Known Limitations

### 1. Fixed execution flow

The planner generates the same 13-step sequence for every task. A task asking for a single API endpoint goes through the same flow as a full product build. This creates noise and erodes trust in the plan output.

**Target (v1.2):** Router-driven plan generation with fallback to default sequence.

---

### 2. Limited execution observability

No way to view current progress, go back to a previous step, or handle blocked/partial steps. Accidental `--done` corrupts execution state with no recovery path.

**Target (v1.1):** `--status`, `--back`, DoD validation on `--done`.

---

### 3. No tracking for ad-hoc work

Direct agent calls outside the execution plan (quick fixes, iterations) bypass framework observability entirely. This creates a governance gap in real development workflows.

**Target (v1.1):** `--session` command for tracked ad-hoc agent calls.

---

### 4. No step dependency model

Steps cannot be marked as blocked or partially complete when they depend on a future step. Workaround is manual state editing.

**Target (v1.1):** `--block`, `--done --partial`, `--resolve` commands.

---

### 5. No context from the repository

The planner and runner have no knowledge of the existing codebase: stack, architecture patterns, ADRs. Every prompt starts from zero.

**Target (v1.2):** Stack detection (requirements.txt, package.json, go.mod, etc.).

---

# Decision Model (Target)

The framework evolves toward a three-level decision system.

---

## Level 0 — Deterministic Flow (v1)

Characteristics:
- predefined step sequence
- human-driven progression
- minimal planner intelligence
- safe and predictable

Status: **implemented**

---

## Level 1 — Context-Aware Planning (v1.2 / v1.3)

Planned capabilities:
- task-sensitive plan generation (router-driven)
- stack-aware prompts (context injection)
- project type detection and adaptive step selection
- improved task decomposition with dependency awareness

Goal: reduce mechanical planning friction while preserving full human control.

---

## Level 2 — Bounded Autonomy (v2.0 / research)

Long-term direction:
- semi-autonomous execution until the next approval gate
- adaptive plan updates based on execution results
- swarm health scoring and bottleneck detection

Important: autonomy will remain bounded and observable. No silent actions.

---

# Architectural Evolution Phases

## Phase A — Execution Control (v1.1)

Focus: make the execution loop safer, more observable, and recoverable.

Specific improvements:
1. `--status` command: current step, completion summary, pending approvals
2. `--back` command: safe navigation to previous steps with journal tracking
3. DoD validation on `--done`: interactive checklist before advancing
4. Registry validation on `--init`: check all agent references in the plan exist in registry before execution starts — fail fast with a clear error instead of silent broken steps
5. `--session <agent>`: tracked ad-hoc agent calls with full journal audit trail
6. Step dependencies: `--block`, `--done --partial`, `--resolve`
7. Bug triage workflow: `--report-bug`, `--triage-bug`, `--bug-fix-sprint`
8. Production readiness sprint: `--production-sprint` for MVP → production transition

Success criteria:
- accidental `--done` is recoverable
- all agent interactions (structured and ad-hoc) appear in the journal
- blocked steps have explicit state and resolution path

---

## Phase B — Planner Intelligence (v1.2)

Focus: make the planner generate useful plans instead of always the same 13 steps.

Specific improvements:
1. Router integration: planner calls the router, uses top agents per phase
2. Confidence threshold: steps with low confidence scores are omitted or flagged
3. Context injection: detect project stack from file system, inject into prompts
4. Fallback: when router output is ambiguous, fall back to default sequence (never fail silently)

Success criteria:
- a task like "add a health check endpoint" does not generate a 13-step plan
- plans include router reasoning (which agents were selected and why)
- context injection improves prompt quality measurably

---

## Phase C — Adaptive Planning (v1.3)

Focus: intelligent decomposition and project-type awareness.

Specific improvements:
1. Task decomposition: complex tasks broken into subtasks with explicit dependencies
2. Dependency graph: topological ordering of steps
3. Project type detection: ML, IoT, Data Science, Security, Edge — automatic step selection
4. Backlog ingestion: convert issues/stories into execution plans

Risks:
- over-decomposition: generating too many subtasks adds noise, not value
- loss of determinism: keep human override always available

Mitigation: decomposition is a suggestion, not enforced. Human can always modify the plan.

---

## Phase D — Adaptive Swarm (v2.0)

Focus: controlled autonomy and multi-sprint coordination.

Topics:
- semi-autonomous execution loops (run until approval gate)
- multi-sprint orchestration with context continuity
- parallel agent coordination
- swarm health scoring and bottleneck detection
- dynamic plan adaptation

This phase is intentionally distant. Autonomy without proven governance is a liability.

---

# UX Target (Operator Experience)

The desired operator experience:

- running a senior engineering team
- not prompting a chatbot repeatedly
- not micromanaging every step
- maintaining full control and visibility

Target flow:
```
User defines initiative
→ Planner proposes structured execution (adapted to task type)
→ Human validates and approves
→ Swarm executes incrementally
→ Approval gates pause for human review at critical phases
→ Sprint closes cleanly with full audit trail
```

Key property: **the human remains the governor, not the typist.**

---

# Success Criteria

### Safety
- No silent destructive actions
- No uncontrolled agent loops
- Full execution traceability (structured and ad-hoc)
- Recoverable from user mistakes

### Engineering Realism
- Sprint outputs are shippable increments
- Deliverables are immediately useful
- Architecture remains coherent across steps
- Technical debt is tracked, not hidden

### Operator Confidence
- The system feels predictable
- The system feels inspectable
- The system feels governable
- Plans reflect the actual task, not a generic template

---

# Relationship to Public Roadmap

This document is the technical counterpart of `docs/roadmap/PUBLIC_ROADMAP.md`.

Public roadmap = external visibility
Evolution roadmap = internal technical compass

Both must remain aligned but serve different audiences.

---

# Long-Term Vision

The endgame is **not** full autonomy.

The endgame is:
- disciplined agent swarms
- observable execution
- safe acceleration of engineering work
- human-guided intelligent systems

**Guiding principle:** controlled autonomy over blind automation.
