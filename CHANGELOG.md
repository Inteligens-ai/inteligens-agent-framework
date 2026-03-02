# Changelog

All notable changes to the Inteligens Agents Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] — 2026-03-02

### 🔧 Improvements & Fixes

#### Execution Runner Enhancements
- **Added `--skip` command** to skip non-applicable steps during execution
- **Enhanced `--next` command prompts** with more context:
  - Overall task description
  - Last 3 completed steps summary
  - Phase-specific instructions
  - References to relevant artifacts (BACKLOG.md, ARCHITECTURE.md, etc.)
- **Improved approval flow logic** to prevent premature blocking
- **Better error messages** for approval-related operations

#### Documentation
- **Added Language-Specific Guide** (`docs/guides/LANGUAGE_SPECIFIC_GUIDE.md`)
  - Setup instructions for Python, Node.js, Go, Rust, Java, C#
  - Dependency management best practices
  - Running and testing projects per language
- **Added Scrum Guide** (`docs/guides/SCRUM_GUIDE.md`)
  - How the framework implements Scrum methodology
  - Sprint artifacts and execution flow
  - Agent roles in Scrum context
  - Approval gates in Scrum
- **Added Contributing Guide** (`CONTRIBUTING.md`)
  - Branch workflow (main, develop, feature, fix, release, hotfix)
  - Commit message conventions
  - Pull request process
  - Release process
- **Updated Usage Guide** with architecture decisions section
- **Updated README.md** with documentation links section

#### Example Project
- **Complete hello-agents example** (`examples/hello-agents/`)
  - Full FastAPI REST API with health check endpoints
  - Comprehensive test suite (≥80% coverage)
  - Complete documentation (Architecture, ADR, Security Review, Threat Model)
  - Docker and deployment configurations
  - Demonstrates complete framework execution flow (all 13 steps)

#### Bug Fixes
- Fixed `cmd_next()` blocking logic for steps requiring approval
- Fixed execution flow to properly handle approval gates
- Corrected `datetime.utcnow()` deprecation warnings
- Fixed missing dependency handling in example projects

#### Documentation Improvements
- Documented iterative error correction process
- Added troubleshooting section for agent errors
- Documented fixed execution flow limitation
- Updated all guides with correct paths and commands

### 📝 Notes

- This is a patch release with improvements and bug fixes
- No breaking changes
- All changes are backward compatible
- Example project serves as proof of concept for the framework

---

## [1.0.0] — 2026-03-02

### 🎉 Initial Release

First stable release of the Inteligens Agents Framework — an Agent Operating Framework (AOF) for orchestrating specialized AI agents with human governance.

### ✨ Core Features

#### Agent Router (v6)
- Risk-aware routing based on product risk profiles
- Hardware-aware node selection (GPU, RAM, CPU capacity)
- Phase detection (plan, design, build, test, release)
- Confidence scoring for agent selection
- Support for product-specific routing rules
- Runtime overlay system for private/public modes

#### Swarm Planner (v7.3)
- Multi-agent execution plan generation
- Phase-based step ordering
- Support for `requires_approval` flag in execution plans
- Policy-aware planning
- Backward-compatible plan format

#### Execution Runner (v8)
- Step-by-step assisted execution flow
- State management with `execution_state.json`
- Execution journal tracking (`execution_journal.md`)
- Sprint-aware build context injection
- Human-in-the-loop by design

### 🛡️ Governance & Safety

#### Approval Gates
- **Human checkpoints** between critical phases
- `requires_approval` flag in execution plans
- `--approve` command for explicit approval
- Blocked progression until approval
- Journal tracking of approval events (RFC-001 compliant)
- Support for architecture, security, release, and sprint closure gates

### 📋 Execution Model

- **Assisted auto-execution**: High automation without losing control
- **Sprint-aware delivery**: Context injection during build phases
- **IDE-agnostic operation**: Works with Cursor, VSCode, Antigravity, CLI
- **Full traceability**: Complete execution journal and state tracking
- **Incremental delivery**: Phase-based workflow (plan → design → build → test → release)

### 👥 Agent System

- **18+ specialized agent roles**:
  - Product: Product Owner
  - Project Management: Scrum Master, Release Manager, Sprint Reviewer, Sprint Closer
  - Engineering: Staff Architect, Tech Lead, Backend, Frontend, AI, Data, DevOps/SRE
  - Security: AppSec Engineer
  - Testing: QA Strategist, API Tester, Performance Benchmarker
  - Design: UI Designer, UX Researcher
- **Agent registry** with tags, commands, guidelines, and handoffs
- **Definition of Done** per agent role

### 📚 Documentation

- Complete usage guides
- Architecture documentation
- RFC-001: Approval Gates specification
- Public roadmap and evolution roadmap
- Manifesto and design philosophy
- Contributing guidelines

### 🔧 Technical Details

- **Language**: Python 3.10+
- **Format**: JSON for state, Markdown for journal
- **State Management**: Persistent execution state
- **Journal Format**: Markdown with timestamps (UTC)
- **Plan Format**: JSON with execution steps

### 🎯 Design Principles

- **Governed AI**: Autonomy without control is a liability
- **Agent Specialization**: Each agent has a clear senior role
- **Incremental Delivery**: Work organized by phases and sprints
- **Human-in-the-Loop**: Every execution step is observable and reviewable

---

[1.0.1]: https://github.com/inteligens/agents-framework/releases/tag/v1.0.1
[1.0.0]: https://github.com/inteligens/agents-framework/releases/tag/v1.0.0
