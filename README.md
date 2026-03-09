# Inteligens Agents Framework

Agent-Native Engineering with Human Governance

> A governance-first execution framework for multi-agent AI systems.

A lightweight orchestration layer designed to coordinate specialized AI agents 
as a senior engineering team — while keeping humans firmly in control.

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-v1.0.1-blue">
  <img alt="status" src="https://img.shields.io/badge/status-stable-green">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-yellow">
  <img alt="python" src="https://img.shields.io/badge/python-3.10%2B-blue">
</p>

---

🚀 Overview

Inteligens Agents Framework is an Agent Operating Framework (AOF) 
built around one core principle:

Autonomy without governance is chaos.

It enables:

🧠 multi-agent planning  
🧭 structured execution flows  
🛡️ explicit human-in-the-loop approval gates  
⚡ IDE-agnostic operation (Cursor, VSCode, CLI, Antigravity)  
🏗️ sprint-aware delivery  

This is not a fully autonomous system by design.
It is a controlled execution environment.

---

## 🎯 Design Philosophy

The framework follows three core principles:

### 1. Governed AI
Autonomy without control is a liability.  
Every execution step is observable and reviewable.

### 2. Agent Specialization
Each agent has a clear senior role (PO, Architect, Backend, QA…).

### 3. Incremental Delivery
Work is organized by phases and sprints to ensure real software delivery.

---

## 🏗️ Architecture

<p align="center">
  <img src="docs/architecture/inteligens_agents_architecture_v1.png" width="720">
</p>

**Flow:**

User → Router → Swarm Planner → Execution Runner → Human Review

---

## ⚡ Quick Start

### 0. Set up product context (recommended)

Copy the product template to your project root and fill it in:

```bash
cp .agents/docs/PRODUCT_TEMPLATE.md PRODUCT.md
```

This gives every agent persistent context about your product — stack, architecture decisions, compliance constraints, conventions, and documentation language. Without it, agents start from zero on every sprint.

See `docs/guides/PRODUCT_SETUP.md` for full instructions.

### 1. Generate a plan

```bash
python .agents/swarm/swarm_planner.py \
  --task "build a RAG pipeline" \
  --sprint "Sprint 1"
```

The plan is saved to `.agents/swarm/execution_plan.json` by default.
If `PRODUCT.md` is present, product context is automatically injected into the plan.

### 2. Initialize execution

```bash
python .agents/swarm/execution_runner.py --init
```

Or specify a custom plan path:
```bash
python .agents/swarm/execution_runner.py --init path/to/plan.json
```

### 3. Execute next step

```bash
python .agents/swarm/execution_runner.py --next
```

### 4. Mark step as done

```bash
python .agents/swarm/execution_runner.py --done
```

---

## 🧠 Assisted Auto‑Execution

v1 introduces **assisted auto‑execution**, which provides:

- step‑by‑step execution
- sprint context awareness
- agent‑specific prompts
- execution journal
- human approval loop

This allows high automation **without losing control**.

---

## 📂 Project Structure

```
.agents/
  agents/
  router/
  swarm/
docs/
  manifesto/
  roadmap/
  rfcs/
  guides/
examples/
```

---

## 🧪 Compatibility

The framework is IDE‑agnostic and works with:

- Cursor
- VSCode
- Antigravity
- Claude Code
- Pure CLI

---

## 🛡️ Security Model

The framework intentionally:

- ❌ does NOT auto‑execute code
- ❌ does NOT mutate repositories silently
- ✅ requires human confirmation
- ✅ keeps full execution trace

## Human-in-the-Loop Safety

The framework supports optional approval gates between critical steps.

See:
- `docs/architecture/APPROVAL_GATES.md`

---

## 📚 Documentation

### Getting Started

- **[Usage Guide](docs/guides/USAGE_GUIDE.md)** - How to operate the framework
- **[Language-Specific Guide](docs/guides/LANGUAGE_SPECIFIC_GUIDE.md)** - Setup for Python, Node.js, Go, Rust, Java, C#
- **[Scrum Guide](docs/guides/SCRUM_GUIDE.md)** - How the framework implements Scrum

### Architecture & Design

- **[Agents Framework](docs/guides/AGENTS_FRAMEWORK.md)** - Framework overview
- **[Approval Gates](docs/architecture/APPROVAL_GATES.md)** - Human checkpoints
- **[RFC-001: Approval Gates](docs/rfcs/RFC-001-approval-gates.md)** - Technical specification
- **[RFC-002: Step Dependencies](docs/rfcs/RFC-002-step-dependencies.md)** - Dependency management (v1.1)
- **[RFC-003: Advanced Dependency Management](docs/rfcs/RFC-003-advanced-dependency-management.md)** - Intelligent assistance (v1.2)
- **[RFC-004: Ad-hoc Agent Sessions](docs/rfcs/RFC-004-ad-hoc-agent-sessions.md)** - Tracked direct agent calls (v1.1)
- **[RFC-005: Production Readiness Sprint](docs/rfcs/RFC-005-production-readiness-sprint.md)** - MVP → Production transition (v1.1)
- **[RFC-006: Bug Triage and Fix Workflow](docs/rfcs/RFC-006-bug-triage-and-fix-workflow.md)** - Structured bug handling (v1.1)

### Roadmap

- **[Public Roadmap](docs/roadmap/PUBLIC_ROADMAP.md)** - High-level product direction
- **[Evolution Roadmap](docs/roadmap/EVOLUTION_ROADMAP.md)** - Technical evolution strategy

---

## 🗺️ Roadmap

### ✅ v1.0 — Assisted Auto-Execution (Current)

- Agent Router (intent → specialist)
- Swarm Planner (multi-agent plan generation)
- Execution Runner (step-by-step assisted flow)
- Sprint-aware execution context
- Human-in-the-loop by design
- IDE-agnostic operation
- Approval Gates (human checkpoints between phases)

---

### 🟡 v1.1 — Governance Hardening (Planned)

Focus: production safety and execution discipline.

- Improved execution observability
- Sprint metrics enrichment
- Stronger auditability of agent actions
- Execution navigation (`--back` command)
- Step dependency management (`--block`, `--done --partial`, `--resolve`)
- Automatic dependency resolution detection
- Ad-hoc review mode with full observability
- Ad-hoc agent sessions (`--session`, `--session-log`, `--session-close`) for tracked direct agent calls
- Production Readiness Sprint (`--production-sprint`) for structured MVP → Production transition
- Bug Triage and Fix Workflow (`--report-bug`, `--triage-bug`, `--bug-fix-sprint`) for structured bug handling

---

### 🟡 v1.2 — Advanced Dependency Management (Planned)

Focus: intelligent dependency assistance and planning integration.

- Automatic planning review triggers (PO + Scrum Master)
- Intelligent workaround suggestions
- Blocking metrics and analytics (`--metrics`)
- Circular dependency detection
- Step reordering suggestions (`--suggest-reorder`)
- Backlog integration suggestions

---

### 🟡 v1.3 — Intelligent Planning (Planned)

Focus: smarter planning from real inputs.

- Backlog ingestion (issues → execution plan)
- Context-aware planning
- Smarter task decomposition
- Improved router confidence scoring
- **Adaptive project type detection** (ML, Hardware, IoT, Data Science, Security, Edge, etc.)
- **Project-specific step templates** (automatic step selection based on project type)
- **Hybrid project support** (combines steps from multiple project types)

---

### 🔵 v2.0 — Adaptive Swarm (Future)

Focus: controlled autonomy at scale.

- Semi-autonomous execution loops
- Multi-sprint orchestration
- Parallel swarm coordination
- Dynamic plan adaptation

---

### 🧪 Research Track (Exploratory)

These are **intentionally not committed** to a release:

- Daily Sync Orchestrator  
- Fully distributed agents  
- Self-healing execution loops  
- Cross-project swarm memory  

---

📍 See full details in:

- `docs/roadmap/PUBLIC_ROADMAP.md`
- `docs/roadmap/EVOLUTION_ROADMAP.md`

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Branch workflow and guidelines
- Commit message conventions
- Pull request process
- Release process
- Development setup

**Quick start:** Open an issue before large changes, then follow the branch workflow in `CONTRIBUTING.md`.

---

## 📜 License

MIT License.

---

<p align="center">
  Built with ⚙️ by Inteligens
</p>
