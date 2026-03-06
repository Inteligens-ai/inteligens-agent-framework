# Inteligens Agents Framework — Public Roadmap

> High-level product direction for the Agent Operating Framework (AOF)

---

## ✅ v1.0 — Assisted Auto‑Execution (Current)
- Multi‑agent orchestration
- Human‑in‑the‑loop execution
- Sprint‑aware build phase
- Execution journal & state tracking
- Sprint Reviewer & Sprint Closure
- Approval Gates (human checkpoints)

---

## 🚧 v1.1 — Governance Hardening
- Enhanced execution visibility
- Sprint metrics enrichment
- Improved approval observability
- Execution navigation (`--back` command)
- Action safety (confirmation prompts, undo/revert)
- Ad-hoc review mode with full observability (`--review <agent>`)
- Ad-hoc agent sessions (`--session`, `--session-log`, `--session-close`) for tracked direct agent calls
- Step dependency management (`--block`, `--done --partial`, `--resolve`)
- Automatic dependency resolution detection
- Backward navigation for blocked steps
- Production Readiness Sprint (`--production-sprint`) for structured MVP → Production transition
- Bug Triage and Fix Workflow (`--report-bug`, `--triage-bug`, `--bug-fix-sprint`) for structured bug handling and Scrum integration

---

## 🔜 v1.2 — Advanced Dependency Management
- Automatic planning review triggers (PO + Scrum Master)
- Intelligent workaround suggestions
- Blocking metrics and analytics (`--metrics`)
- Circular dependency detection
- Step reordering suggestions (`--suggest-reorder`)
- Backlog integration suggestions

---

## 🔜 v1.3 — Intelligent Planning
- Backlog ingestion
- Context‑aware planning
- Smarter task decomposition
- Reduced prompt friction
- **Adaptive project type detection** (ML, Hardware, IoT, Data Science, Security, Edge, etc.)
- **Project-specific step templates** (automatic step selection based on project type)
- **Hybrid project support** (combines steps from multiple project types)

---

## 🔮 v2.0 — Adaptive Swarm
- Semi‑autonomous execution loops
- Multi‑sprint orchestration
- Agent memory improvements
- Parallel swarm coordination

---

## 🧪 Future Research
- Daily Sync Orchestrator
- Fully distributed agents
- Autonomous risk detection
- Self‑healing pipelines

---

**Philosophy:** automation with governance, not blind autonomy.
