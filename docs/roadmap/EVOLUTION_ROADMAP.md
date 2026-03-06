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

### 3. Single-sprint mental model and MVP → Production gap

Current execution assumes:

- one primary sprint context
- linear progression
- limited multi-sprint orchestration
- MVP and production are the same thing

**Additional Problem:**

Agents often deliver MVP functionality but defer production concerns (deployment, monitoring, scaling, security hardening) to backlog. There's no structured way to transition from MVP to production:

- Production items accumulate in backlog
- No clear process for production readiness sprint
- Context loss when starting new sprint for production
- Manual workaround required (create new plan, copy backlog)

**Impact:**
- MVP works but not production-ready
- Production concerns accumulate as technical debt
- No structured path from MVP to production
- Manual process loses framework observability

**Workaround:** Manually create new execution plan, copy backlog items, start fresh sprint (loses context).

**Future (v1.1+):**
- Production Readiness Sprint type (`--production-sprint`)
- Automatic extraction of production items from backlog
- Context preservation from MVP sprint
- Production-focused step templates
- Backlog continuity between sprints

**Future (v2.0):** Full multi-sprint orchestration with sprint chaining and dependencies.

**See:** [RFC-005: Production Readiness Sprint](../rfcs/RFC-005-production-readiness-sprint.md)

This is acceptable for v1 but will not scale.

---

### 4. Partial swarm observability

We still lack:

- richer execution telemetry
- swarm health indicators
- progress analytics
- bottleneck detection

---

### 6. Execution control limitations

Current execution model has gaps:

- **No undo/back command**: Cannot revert accidental `--done` or go back to previous steps
- **No confirmation for critical actions**: `--done` executes immediately without confirmation
- **No execution history correction**: If `--done` is called by mistake, history becomes inconsistent
- **No ad-hoc review mode**: Cannot request review from specific agent with full observability (current workaround loses journal tracking)

**Impact:**
- Accidental `--done` can corrupt execution state
- No way to review or redo previous steps
- Ad-hoc reviews bypass framework observability

**Workaround:** Manual state editing (risky) or restart execution plan.

**Future (v1.1+):**
- Add `--back` command to navigate to previous steps
- Add confirmation prompts for `--done` (or `--done --confirm`)
- Add `--undo` or `--revert` to correct accidental actions
- Add `--review <agent>` command that creates temporary plan with observability
- Execution history correction mechanism

---

### 7. No tracking for direct agent calls

Current execution model has a governance gap:

- **No ad-hoc session tracking**: Direct agent calls (e.g., `@agent fix bug`) bypass framework observability
- **Lost traceability**: Quick corrections, iterations, and adjustments are not recorded
- **No audit trail**: Important work happens outside framework tracking
- **Context loss**: Ad-hoc work loses connection to main execution plan

**Impact:**
- Direct agent calls are common in real development but invisible to framework
- No way to track quick fixes, iterations, or adjustments
- Governance gap: work happens without observability
- Difficult to understand full project history

**Workaround:** None. Direct agent calls are completely untracked.

**Future (v1.1+):**
- Add `--session <agent>` command for tracked ad-hoc sessions
- Full interaction logging (`--session-log`)
- Session management (`--session-close`, `--sessions`, `--session-show`)
- Session linking to execution steps (optional)
- Complete audit trail in execution journal
- Enables quick corrections while maintaining observability

**See:** [RFC-004: Ad-hoc Agent Sessions](../rfcs/RFC-004-ad-hoc-agent-sessions.md)

---

### 9. No bug triage and fix workflow

Current execution model lacks structured bug handling:

- **No bug reporting mechanism**: Bugs discovered during execution or by humans cannot be formally reported
- **No bug triage process**: No way to prioritize, estimate effort, or assign bugs to sprints
- **No bug-fix sprint type**: Cannot create focused bug-fix execution plans
- **No agent routing for bugs**: Framework doesn't guide which agent should fix bugs
- **No backlog integration**: Bugs are not automatically added to backlog
- **Loss of observability**: When bugs are fixed outside framework (e.g., direct agent calls), work is not tracked

**Impact:**
- Bugs discovered during execution are fixed ad-hoc without framework guidance
- Bugs discovered by humans have no structured way to enter Scrum workflow
- No integration between bug fixes and sprint planning
- Loss of traceability for bug fixes
- No metrics or analytics on bug resolution

**Example Scenarios:**

**Scenario 1: Bug discovered during execution**
- Step 5 (Backend) in progress, bug discovered
- Agent in IDE immediately starts fixing it
- No framework guidance on which agent should act
- Fix happens outside framework observability
- No integration with backlog or sprint planning

**Scenario 2: Bug discovered by human**
- Human discovers bug in production
- No way to report it to framework
- No integration with backlog
- No triage process
- No assignment to appropriate agent
- No tracking in sprint context

**Workaround:** None. Bugs are fixed ad-hoc without framework integration.

**Future (v1.1+):**
- Add `--report-bug` command for structured bug reporting
- Automatic backlog integration for bugs
- Agent routing suggestions based on bug type
- `--triage-bug` command for interactive bug triage
- `--bug-fix-sprint` command for focused bug-fix execution plans
- Bug-fix sprint type (same-sprint, next-sprint, hotfix)
- Integration with ad-hoc sessions for immediate fixes
- Bug status flow and tracking

**See:** [RFC-006: Bug Triage and Fix Workflow](../rfcs/RFC-006-bug-triage-and-fix-workflow.md)

---

### 8. No dependency management

Current execution model cannot handle inter-step dependencies:

- **No blocking states**: Cannot mark steps as blocked or partially complete when dependencies are not met
- **No dependency tracking**: No way to declare or track which steps depend on others
- **No automatic resolution detection**: Framework doesn't detect when dependencies are resolved
- **No backward navigation**: Cannot safely return to blocked steps to complete work

**Impact:**
- Real-world scenarios (e.g., Backend depends on AI service interfaces) require manual workarounds
- Steps must be marked as complete even when partially done
- No observability for blocked work
- Manual tracking in backlog/sprint plan (loses framework integration)

**Example Scenario:**
- Step 5 (Backend) identifies it needs AI service interface from Step 7 (AI Engineer)
- Current workaround: Mark Step 5 as done, manually update backlog, continue to Step 7, manually return to Step 5 later
- Problem: Loses observability, error-prone, no automatic detection

**Workaround:** Manual backlog updates, manual state editing, or restart execution plan.

**Future (v1.1+):**
- Add `--block` command to mark steps as blocked
- Add `--done --partial` flag for partial completion
- Add `--back` command for backward navigation
- Add `--resolve` command for automatic dependency resolution detection
- Add `dependencies` field to execution plan schema
- Add `blocked_steps` tracking to execution state
- Automatic detection when dependencies are resolved
- Planner warnings for detected dependencies

**See:** [RFC-002: Step Dependencies and Blocking States](../rfcs/RFC-002-step-dependencies.md)

---

### 5. Fixed execution flow

The planner currently generates a fixed sequence of 13 steps optimized for software development projects:

- Always includes: Product Owner, Scrum Master, Staff Architect, Tech Lead, Backend, Frontend, AI Engineer, DevOps, QA, AppSec, Release Manager, Sprint Reviewer, Sprint Closer
- Focused on software development workflow (plan → design → build → test → release)
- Does not automatically adapt to other project types (data science, research, ML pipelines, hardware/IoT, edge computing, etc.)

**Workaround:** Create custom execution plans manually for different project types.

**Future (v1.3+):** Intelligent planning with semantic task understanding will generate adaptive flows based on project type and requirements.

#### Planned Project Type Support

The framework will detect project types and adapt execution plans accordingly:

**1. Machine Learning / AI Projects**
- **Detection:** Keywords: "ml", "machine learning", "model", "training", "neural network", "deep learning", "face recognition", "computer vision"
- **Additional Steps:**
  - Data Engineer (data collection, preprocessing, validation)
  - ML Engineer (model training, hyperparameter tuning)
  - Model Validator (model evaluation, performance metrics)
  - ML Ops Engineer (model deployment, monitoring, versioning)
- **Special Considerations:**
  - Model versioning and rollback
  - Data pipeline steps
  - Model performance monitoring
  - A/B testing support
  - Model registry integration

**2. Hardware / IoT Projects**
- **Detection:** Keywords: "hardware", "iot", "sensor", "camera", "device", "embedded", "raspberry pi", "arduino", "edge device"
- **Additional Steps:**
  - Hardware Engineer (hardware selection, calibration, configuration)
  - Embedded Systems Engineer (firmware, device programming)
  - Edge Deployment Specialist (edge optimization, deployment)
  - Hardware Tester (hardware-in-the-loop testing)
- **Special Considerations:**
  - Hardware calibration steps
  - Edge device optimization
  - Firmware versioning
  - Hardware testing procedures
  - Integration with physical devices

**3. Data Science / Analytics Projects**
- **Detection:** Keywords: "data science", "analytics", "data pipeline", "etl", "data warehouse", "data lake", "bi"
- **Additional Steps:**
  - Data Engineer (data pipelines, ETL, data quality)
  - Data Analyst (exploratory data analysis, insights)
  - Data Scientist (statistical analysis, modeling)
  - Data Ops Engineer (data infrastructure, monitoring)
- **Special Considerations:**
  - Data pipeline orchestration
  - Data quality validation
  - Data governance steps
  - Analytics dashboard creation

**4. Security-Critical Projects**
- **Detection:** Keywords: "security", "access control", "biometric", "authentication", "authorization", "compliance", "lgpd", "gdpr"
- **Additional Steps:**
  - Compliance Officer / Privacy Engineer (regulatory compliance, privacy)
  - Security Architect (security architecture, threat modeling)
  - Penetration Tester (security testing, vulnerability assessment)
- **Special Considerations:**
  - Compliance documentation (LGPD, GDPR, etc.)
  - Security audit steps
  - Privacy impact assessments
  - Regulatory approval gates

**5. Integration-Heavy Projects**
- **Detection:** Keywords: "integration", "api", "microservices", "legacy", "third-party", "external system"
- **Additional Steps:**
  - Integration Engineer (API integration, system integration)
  - API Designer (API contracts, specifications)
  - Integration Tester (integration testing, contract testing)
- **Special Considerations:**
  - API contract management
  - Mock/stub generation for external systems
  - Integration testing frameworks
  - Contract testing (Pact, etc.)

**6. Performance-Critical Projects**
- **Detection:** Keywords: "performance", "optimization", "scalability", "latency", "throughput", "real-time"
- **Additional Steps:**
  - Performance Engineer (profiling, optimization)
  - Load Testing Specialist (load testing, stress testing)
  - Performance Analyst (performance metrics, tuning)
- **Special Considerations:**
  - Performance profiling steps
  - Load testing automation
  - Performance benchmarks
  - Optimization recommendations

**7. Edge Computing Projects**
- **Detection:** Keywords: "edge", "edge computing", "fog computing", "on-premise", "offline", "local processing"
- **Additional Steps:**
  - Edge Deployment Specialist (edge optimization, deployment)
  - Edge Infrastructure Engineer (edge infrastructure, networking)
  - Edge Tester (edge-specific testing)
- **Special Considerations:**
  - Edge device constraints (CPU, memory, power)
  - Offline capability requirements
  - Edge-cloud synchronization
  - Edge-specific deployment strategies

**8. Hybrid Projects**
- Projects may combine multiple types (e.g., "face recognition access control" = ML + Hardware + Security)
- Framework will detect multiple types and combine relevant steps
- Example: ML + Hardware + Security → includes Data Engineer, ML Engineer, Hardware Engineer, Compliance Officer, etc.

#### Implementation Approach

**Phase 1 (v1.3):** Basic type detection and step adaptation
- Keyword-based project type detection
- Predefined step templates per project type
- Manual override capability

**Phase 2 (v1.4+):** Advanced semantic understanding
- LLM-based project type detection
- Dynamic step generation based on requirements
- Context-aware step selection
- Dependency-aware step ordering

**Phase 3 (v2.0+):** Fully adaptive planning
- Multi-type project support
- Automatic step optimization
- Learning from execution patterns
- Custom step templates

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

## 🟡 Level 1 — Context-Aware Planning (v1.3 / v2)

Planned capabilities:

- task-sensitive planning
- dynamic agent routing
- basic risk awareness
- improved decomposition
- smarter sprint shaping
- **project type detection and adaptation**
- **adaptive step selection based on project characteristics**
- **support for ML, Hardware, IoT, Data Science, Security, Edge, and hybrid projects**

**Project Type Adaptation:**

The planner will automatically detect project types and adapt execution plans:

- **ML/AI Projects:** Adds Data Engineer, ML Engineer, Model Validator, ML Ops steps
- **Hardware/IoT Projects:** Adds Hardware Engineer, Embedded Systems Engineer, Edge Deployment steps
- **Data Science Projects:** Adds Data Engineer, Data Analyst, Data Scientist, Data Ops steps
- **Security-Critical Projects:** Adds Compliance Officer, Security Architect, Penetration Tester steps
- **Integration Projects:** Adds Integration Engineer, API Designer, Integration Tester steps
- **Performance Projects:** Adds Performance Engineer, Load Testing Specialist steps
- **Edge Computing Projects:** Adds Edge Deployment Specialist, Edge Infrastructure Engineer steps
- **Hybrid Projects:** Combines relevant steps from multiple types

**Detection Methods:**

- **Phase 1 (v1.3):** Keyword-based detection from task description
- **Phase 2 (v1.4+):** LLM-based semantic understanding
- **Phase 3 (v2.0+):** Learning from execution patterns

Goal:

> reduce mechanical planning while preserving control, adapt to project needs automatically.

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
- execution control and navigation
- ad-hoc review capabilities with observability

Success criteria:

- zero uncontrolled transitions
- explicit approval points
- full journal traceability
- ability to navigate backward in execution
- ability to correct accidental actions
- ad-hoc reviews maintain full observability

### Specific improvements planned:

1. **Execution Navigation**
   - `--back` command to navigate to previous steps
   - `--undo` or `--revert` to correct accidental `--done`
   - Execution history correction mechanism
   - Safe state rollback with journal tracking

2. **Action Safety**
   - Confirmation prompts for critical actions (`--done --confirm` or interactive prompt)
   - Prevention of accidental state corruption
   - Clear warnings before irreversible actions

3. **Ad-hoc Review Mode**
   - `--review <agent>` command that creates temporary execution plan
   - Full observability (journal, state tracking) for ad-hoc reviews
   - Integration with main execution plan (optional linking)
   - Example: `--review security/appsec-engineer.md --task "Review API security"`

4. **Ad-hoc Agent Sessions**
   - `--session <agent>` command for tracked direct agent calls
   - Full traceability for all agent interactions outside structured flow
   - Session linking to execution steps (optional)
   - Interaction logging (`--session-log`)
   - Session management (`--session-close`, `--sessions`, `--session-show`)
   - Complete audit trail in execution journal
   - Enables quick corrections, iterations, and adjustments while maintaining observability
   - Example: Quick bug fix during execution → create session → use agent directly → log interactions → close session

**See:** [RFC-004: Ad-hoc Agent Sessions](../rfcs/RFC-004-ad-hoc-agent-sessions.md)

5. **Production Readiness Sprint**
   - `--production-sprint` command for production-focused sprints
   - Automatic detection of sprint type (MVP, production-readiness, enhancement, maintenance)
   - Extraction of production items from previous sprint backlog
   - Context preservation from MVP sprint
   - Production-focused step templates
   - Backlog continuity between sprints
   - Structured MVP → Production transition
   - Example: MVP sprint closes → production sprint starts → extracts production items → executes production-focused steps

**See:** [RFC-005: Production Readiness Sprint](../rfcs/RFC-005-production-readiness-sprint.md)

6. **Dependency Management**
   - `--block` command to mark steps as blocked
   - `--done --partial` flag for partial completion with dependencies
   - `--back` command for backward navigation to previous steps
   - `--resolve` command for automatic dependency resolution detection
   - `dependencies` field in execution plan schema
   - `blocked_steps` tracking in execution state
   - Automatic detection when dependencies are resolved
   - Planner warnings for detected dependencies
   - Example: Backend (Step 5) depends on AI (Step 7) → mark as partial → continue → auto-detect resolution → navigate back

7. **Bug Triage and Fix Workflow**
   - `--report-bug` command for structured bug reporting
   - Automatic backlog integration for bugs
   - Agent routing suggestions based on bug type and context
   - `--triage-bug` command for interactive bug triage (priority, severity, effort, sprint assignment)
   - `--bug-fix-sprint` command for focused bug-fix execution plans
   - Bug-fix sprint type (same-sprint, next-sprint, hotfix)
   - Integration with ad-hoc sessions for immediate fixes
   - Bug status flow (reported → triaged → assigned → fixed → closed)
   - Bug tracking in execution journal
   - Support for bugs discovered during execution and by humans
   - Example: Bug discovered → report → triage → assign to sprint → fix via bug-fix sprint or ad-hoc session

**See:** [RFC-006: Bug Triage and Fix Workflow](../rfcs/RFC-006-bug-triage-and-fix-workflow.md)

---

## Phase B — Advanced Dependency Management (v1.2)

Focus:

- intelligent dependency assistance
- automatic planning reviews
- workaround suggestions
- blocking metrics and analytics
- circular dependency detection
- step reordering suggestions

Success criteria:

- automatic planning review triggers when blocks occur
- intelligent workaround suggestions based on agent types
- comprehensive blocking metrics
- proactive dependency resolution suggestions

### Specific improvements planned:

1. **Automatic Planning Reviews**
   - `--review-planning` command triggers PO + Scrum Master review
   - Automatic suggestion when steps are blocked
   - Temporary plan creation with context about blocking
   - Integration with backlog/sprint plan updates

2. **Intelligent Workaround Suggestions**
   - Context-aware workarounds based on agent types
   - Suggestions for mocks, stubs, contracts, interfaces
   - Workaround database for common patterns
   - Example: Backend blocked by AI → suggest mock interface

3. **Blocking Metrics and Analytics**
   - `--metrics` command for blocking statistics
   - Average blocking time, blocking ratio
   - Dependency chain detection
   - Most common dependencies analysis
   - Step status overview

4. **Circular Dependency Detection**
   - Automatic detection of circular dependencies
   - Warnings about potential deadlocks
   - Visualization of dependency cycles

5. **Step Reordering Suggestions**
   - `--suggest-reorder` command for optimal ordering
   - Topological sort-based suggestions
   - Dependency-aware reordering
   - Impact analysis of reordering

6. **Backlog Integration**
   - `--update-backlog-suggestion` generates backlog snippets
   - Automatic suggestions for blocking stories
   - Integration with existing backlog structure

**See:** [RFC-003: Advanced Dependency Management](../rfcs/RFC-003-advanced-dependency-management.md)

---

## Phase C — Planner Intelligence (v1.3+)

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
