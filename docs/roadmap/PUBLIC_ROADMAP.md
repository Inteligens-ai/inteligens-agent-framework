# Inteligens Agents Framework — Public Roadmap

> High-level product direction for the Agent Operating Framework (AOF)

---

## ✅ v1.0 — Assisted Auto-Execution (Current)

- Multi-agent orchestration (15+ specialized roles)
- Human-in-the-loop execution by design
- Sprint-aware build phase
- Execution journal and state tracking
- Approval Gates (human checkpoints between critical phases)
- Sprint Reviewer and Sprint Closure
- IDE-agnostic operation (Cursor, VSCode, Claude Code, CLI)

---

## ✅ v1.0.1 — Strengthened Agent Personas

- All agent personas rewritten with explicit role priming
- Output contracts: each agent now specifies exact artifacts and formats to produce
- Failure modes defined per agent (what agents must NOT do)
- Definition of Done made objective and verifiable per agent
- Consistent structure across all 15 agent roles

---

## 🚧 v1.1 — Execution Control

Focus: make the execution loop safer and more observable.

- `--status` command: show current step, completed steps, pending approvals
- `--back` command: navigate to previous steps safely
- DoD validation on `--done`: interactive checklist before advancing
- Registry validation on `--init`: detect broken agent references before execution starts
- Ad-hoc agent sessions (`--session`): tracked direct agent calls outside the main flow
- Step dependency management (`--block --depends-on <step>`, `--done --partial`, `--resolve <context>`): declare which step is the blocker; resolution context is injected into the prompt when the blocked step resumes
- Out-of-order step execution (`--run-ahead <step>`): run a future planned step now to unblock the current one — fully tracked in journal, step marked as already executed when cursor reaches it organically
- Bug triage and fix workflow (`--report-bug --introduced-at <step>`, `--triage-bug`): attribute bugs to the step that introduced them for retrospective pattern detection
- Production Readiness Sprint (`--production-sprint`): structured MVP → production transition

---

## 🔜 v1.2 — Planner Intelligence

Focus: make the planner smarter without losing determinism.

- Router-driven plan generation (replaces hardcoded 13-step sequence)
- Fallback to default sequence when router confidence is low
- Context injection: detect stack (requirements.txt, package.json, go.mod, etc.)
- Minimum confidence threshold for agent selection
- Plans reflect task type — not every task needs all 13 steps
- Inter-step dependency declarations: known dependencies between steps surfaced to the operator at `--init` before execution starts

---

## 🔜 v1.3 — Intelligent Planning

Focus: smarter decomposition and adaptive flows.

- Task decomposition: complex tasks broken into subtasks with dependencies
- Dependency-aware step ordering (topological sort)
- Adaptive project type detection (ML, IoT, Data Science, Security, Edge, etc.)
- Project-specific step templates (automatic step selection based on project type)
- Backlog ingestion (issues → execution plan)

---

## 🔮 v2.0 — Adaptive Swarm

Focus: controlled autonomy at scale.

- Semi-autonomous execution loops (run until next approval gate)
- Multi-sprint orchestration with sprint chaining
- Parallel agent coordination
- Swarm health scoring and bottleneck detection
- Dynamic plan adaptation based on execution history

---

## 🧪 Future Research

These are intentionally not committed to a release:

- Daily Sync Orchestrator
- Cross-project swarm memory
- Self-healing execution loops
- Fully distributed agent coordination

---

**Philosophy:** automation with governance, not blind autonomy.
