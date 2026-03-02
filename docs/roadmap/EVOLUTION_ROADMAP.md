# EVOLUTION ROADMAP — Inteligens Agents Framework

> Technical evolution plan for the Agent Operating Framework (AOF)

---

## 🎯 Purpose

This document defines the **technical evolution strategy** of the Inteligens Agents Framework.

Unlike the public roadmap, this document focuses on:

- architectural maturity
- execution safety
- human governance
- swarm intelligence progression
- operational discipline

It is intended for architects, maintainers, and advanced contributors.

---

# 🧭 Current State — v1 Foundation

## ✅ What is already working

The framework currently provides:

- Assisted auto-execution loop
- Multi-agent orchestration
- Phase-based delivery (plan → design → build → test → release)
- Sprint-aware build context
- Execution journal and state tracking
- IDE-agnostic operation
- Human-in-the-loop enforcement
- Approval Gates (human checkpoints between phases)

This establishes a **controlled execution baseline**.

---

## ⚠️ Known limitations

Despite the solid foundation, v1 still has important gaps:

### 1. Limited decision intelligence

The planner generates the flow but does not yet reason deeply about:

- task complexity
- risk surface
- architectural impact
- cross-agent dependencies

---

### 2. Approval Gates (Implemented in v1.0)

The system now includes:

- structured approval checkpoints via `requires_approval` flag
- explicit approval states (awaiting_approval)
- auditable gate transitions via journal

Future improvements (v1.1+):
- Enhanced approval visibility and metrics
- Better approval observability
- Approval analytics

---

### 3. Single-sprint mental model

Current execution assumes:

- one primary sprint context
- linear progression
- limited multi-sprint orchestration

This is acceptable for v1 but will not scale.

---

### 4. Partial swarm observability

We still lack:

- richer execution telemetry
- swarm health indicators
- progress analytics
- bottleneck detection

---

# 🧠 Decision Model (Target)

The framework will evolve toward a **three-level decision system**.

---

## 🟢 Level 0 — Deterministic Flow (v1)

Characteristics:

- predefined step sequence
- human-driven progression
- minimal planner intelligence
- safe but rigid

Status: **implemented**

---

## 🟡 Level 1 — Context-Aware Planning (v1.x / v2)

Planned capabilities:

- task-sensitive planning
- dynamic agent routing
- basic risk awareness
- improved decomposition
- smarter sprint shaping

Goal:

> reduce mechanical planning while preserving control.

---

## 🔴 Level 2 — Bounded Autonomy (future)

Long-term research direction:

- adaptive swarm behavior
- guarded autonomous loops
- policy-aware execution
- self-adjusting flows

Important:

> autonomy will remain bounded and observable.

---

# 🏗️ Architectural Evolution

## Phase A — Governance Hardening (next)

Focus:

- better execution visibility
- stronger audit trail
- improved state machine

Success criteria:

- zero uncontrolled transitions
- explicit approval points
- full journal traceability

---

## Phase B — Planner Intelligence

Focus:

- backlog ingestion
- semantic task understanding
- improved decomposition
- dependency awareness

Risks:

- over-planning
- hidden complexity
- loss of determinism

Mitigation:

> keep human override always available.

---

## Phase C — Multi-Sprint Orchestration

Focus:

- sustained delivery cycles
- sprint chaining
- backlog continuity
- long-running initiatives

This is where the framework becomes significantly more powerful.

---

## Phase D — Adaptive Swarm (research)

Exploration topics:

- parallel agent waves
- swarm health scoring
- bottleneck prediction
- guarded autonomy

This phase is **intentionally distant**.

---

# 🧪 UX Target (Operator Experience)

The desired operator experience should feel like:

- running a senior engineering team
- not prompting a chatbot repeatedly
- not micromanaging every step
- but still maintaining control

---

## Example Target Flow

```text
User defines initiative
→ Planner proposes structured execution
→ Human validates
→ Swarm executes incrementally
→ Reviewer validates
→ Sprint closes cleanly
```

Key property:

> The human remains the governor, not the typist.

---

# 📏 Success Criteria

The framework evolution will be considered successful if:

### Safety

- No silent destructive actions
- No uncontrolled agent loops
- Full execution traceability

---

### Engineering realism

- Sprint outputs are shippable
- Deliverables are incrementally useful
- Architecture remains coherent
- Technical debt does not explode

---

### Operator confidence

- The system feels predictable
- The system feels inspectable
- The system feels governable

---

### Strategic positioning

The framework must clearly differentiate from:

- one-shot code generators
- fully autonomous hype agents
- black-box AI pipelines

Positioning target:

> Agent-native engineering with governance.

---

# 🗺️ Relationship to Public Roadmap

This document is the **technical counterpart** of:

```
docs/roadmap/PUBLIC_ROADMAP.md
```

Public roadmap = external visibility  
Evolution roadmap = internal technical compass

Both must remain aligned but serve different audiences.

---

# 🔮 Long-Term Vision

The endgame is **not** full autonomy.

The endgame is:

- disciplined agent swarms
- observable execution
- safe acceleration of engineering work
- human-guided intelligent systems

---

**Guiding principle:**

> Controlled autonomy over blind automation.
