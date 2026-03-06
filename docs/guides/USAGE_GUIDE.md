# Usage Guide — Inteligens Agents Framework

This guide explains how to operate the framework in a real engineering workflow.

---

## 🧭 Execution Model

The framework follows an assisted execution loop:

1. Planner generates the execution plan
2. Runner advances step-by-step
3. Human validates deliverables
4. Journal records progress

The system is intentionally **human-in-the-loop**.

---

## 🚀 Basic Flow

### 1. Generate the plan

```bash
python .agents/swarm/swarm_planner.py --task "your project goal"
```

The plan is saved to `.agents/swarm/execution_plan.json` by default. You can specify a custom path:

```bash
python .agents/swarm/swarm_planner.py --task "your project" --output custom_plan.json
```

**Note:** The planner automatically marks steps that require approval (architecture, security, release, closure). You'll see a warning indicating which steps are gated.

---

### 2. Initialize execution

```bash
python .agents/swarm/execution_runner.py --init
```

This uses `.agents/swarm/execution_plan.json` by default. To use a custom plan:

```bash
python .agents/swarm/execution_runner.py --init path/to/plan.json
```

---

### 3. Advance execution

```bash
python .agents/swarm/execution_runner.py --next
```

---

### 4. Mark step as completed

```bash
python .agents/swarm/execution_runner.py --done
```

---

### Approval Flow (optional)

Some steps automatically require explicit approval before proceeding. The Swarm Planner marks these steps with `requires_approval: true` based on heuristics (architecture decisions, security reviews, releases, sprint closure).

**When a step requires approval:**

1. Complete the step work
2. Run `--done` as usual
3. The system will indicate: "Step completed but awaiting approval"
4. Review the deliverables
5. Run `--approve` to approve and continue
6. Run `--next` to proceed to the next step

**Example flow:**

```bash
# Step 3 requires approval
python execution_runner.py --next    # Shows step 3
# ... do the work ...
python execution_runner.py --done    # "Step completed but awaiting approval"
python execution_runner.py --approve # "Step approved"
python execution_runner.py --next    # Shows step 4
```

**Note:** Steps without `requires_approval` proceed normally after `--done`.

---

## 🧠 Sprint-Aware Execution

During build phases, the runner injects:

- current sprint context
- sprint goals
- focused backlog items
- guardrails

Agents must work **only within the active sprint scope**.

---

## 🔒 Safety Principles

The framework:

- does NOT auto-execute code
- does NOT modify repositories silently
- requires human validation
- keeps full execution traceability

---

## 🏗️ Architecture and Technology Decisions

**Agents make architectural decisions** — the framework delegates technology choices to specialized agents (Staff Architect, Tech Lead) based on project requirements.

### How It Works

1. **Staff Architect (Step 3)** analyzes requirements and selects:
   - Programming language and framework
   - Architecture patterns (MVC, microservices, serverless, etc.)
   - Technology stack
   - Infrastructure approach

2. **Tech Lead (Step 4)** creates:
   - Implementation plan
   - Coding standards
   - Project structure
   - Development guidelines

3. **Architecture Decision Records (ADRs)** document key decisions in `docs/ADR-*.md`

### What You Can Expect

Agents will generate:
- **Language-appropriate project structure** (see [Language-Specific Guide](LANGUAGE_SPECIFIC_GUIDE.md))
- **Framework-specific configuration** files
- **Best practices** for the chosen stack
- **Documentation** explaining architectural choices

### Best Practices

- **Review architecture decisions** before approving Step 3
- **Validate technology choices** against your organization's standards
- **Check ADRs** to understand rationale
- **Provide feedback** if architecture doesn't meet requirements
- **Trust agent expertise** but maintain human oversight

**Note:** Architecture decisions require approval (Step 3 is gated). Always review `docs/ARCHITECTURE.md` and `docs/ADR-*.md` before approving.

---

## 🧪 Recommended Workflow

For best results:

- Review each agent output
- Commit incrementally
- Validate Definition of Done
- Keep sprint scope tight
- **Expect and handle errors iteratively** — Pass errors back to agents for self-correction (see [Troubleshooting](#-troubleshooting))
- **Review architecture decisions** before approving (see [Architecture](#️-architecture-and-technology-decisions))

---

## 🧭 Troubleshooting

### Execution Issues

If execution seems inconsistent:

- verify execution_state.json
- check execution_journal.md
- confirm the correct plan was loaded
- ensure you ran `--done` before `--next`

### Agent Errors and Iterative Correction

**Agents are subject to errors** — this is expected and part of the iterative development process.

**Common agent errors:**
- Missing dependencies in `requirements.txt` (e.g., `httpx` for FastAPI tests)
- Incomplete file generation
- Incorrect configuration values
- Missing imports or syntax errors

**How to handle agent errors:**

1. **Identify the error** — Run tests, check logs, or validate the generated code
2. **Pass the error to the agent** — Include the error message, stack trace, or test output in your next prompt to the agent
3. **Let the agent self-correct** — The agent will analyze the error and fix it in the next iteration
4. **Validate the fix** — Re-run tests or validate the corrected code
5. **Continue execution** — Mark the step as `--done` once the issue is resolved

**Example workflow:**

```bash
# Step 5 completed, but tests fail
pytest
# ERROR: ModuleNotFoundError: No module named 'httpx'

# Pass error to agent in next chat/context
# Agent analyzes and updates requirements.txt

# Reinstall dependencies
pip install -r requirements.txt

# Re-run tests
pytest
# ✅ All tests pass

# Mark step as done
python .agents/swarm/execution_runner.py --done
```

**Why this approach works:**
- The framework is **iterative by design** — errors are expected and correctable
- Context-aware agents can analyze errors and propose fixes
- Human validation ensures quality before proceeding
- This process improves agent accuracy over time

**Note:** Some errors may require manual intervention (e.g., complex architectural decisions, security issues). Always review agent corrections before proceeding.

---

## 🔗 Handling Dependencies Between Steps

**Note:** This section describes features planned for v1.1+. For current workarounds, see [Current Limitations](#-current-limitations) below.

In real-world projects, steps often depend on work from other steps. For example:
- Step 5 (Backend) may need AI service interface definitions from Step 7 (AI Engineer)
- Step 6 (Frontend) may need API contracts from Step 5 (Backend)
- Step 9 (QA) may need implementation from Step 5 (Backend)

### Marking Steps as Partial or Blocked

When a step cannot be fully completed due to dependencies:

**Option 1: Partial Completion**

```bash
# Step 5: Backend identifies dependency on Step 7
python execution_runner.py --next    # Shows step 5
# ... agent works on backend ...
# Agent identifies: "Need AI service interface from Step 7"

# Mark as partially complete
python execution_runner.py --done --partial --blocked-by 7 --reason "Waiting for AI service interface definition"
```

This marks the step as `partial` and records the dependency, allowing you to continue to the next step.

**Option 2: Block Step**

```bash
# If step cannot proceed at all
python execution_runner.py --block --blocked-by 7 --reason "Cannot proceed without AI service interface"
```

This marks the step as `blocked` (no partial work completed).

### Continuing Execution

After marking a step as partial or blocked, you can continue normally:

```bash
# Continue to Step 7
python execution_runner.py --next    # Shows step 7
# ... agent works on AI service ...
python execution_runner.py --done
```

### Automatic Dependency Resolution Detection

When you complete a step that other steps depend on, the framework automatically detects this:

```bash
# After completing Step 7
python execution_runner.py --done
# Output: "Step 7 completed. Blocked steps may be resolved: [5]. Run `--resolve 5` to check."
```

### Resolving Dependencies

Check if dependencies are resolved:

```bash
# Resolve specific step
python execution_runner.py --resolve 5

# Or auto-detect all resolved dependencies
python execution_runner.py --resolve
```

If dependencies are resolved, the framework will:
- Update the step status to `in_progress`
- Record resolution in journal
- Suggest navigating back: `python execution_runner.py --back 5`

### Returning to Blocked Steps

Navigate back to complete blocked work:

```bash
# Return to specific step
python execution_runner.py --back 5

# Or return to previous step
python execution_runner.py --back
```

This shows the step instructions again, allowing you to complete the remaining work.

### Complete Example Workflow

```bash
# Step 5: Backend identifies dependency
python execution_runner.py --next    # Step 5
# ... partial work done ...
python execution_runner.py --done --partial --blocked-by 7 --reason "Waiting for AI service interface"

# Continue to Step 7
python execution_runner.py --next    # Step 7
# ... AI service work completed ...
python execution_runner.py --done
# Framework detects: "Step 7 completed. Blocked steps may be resolved: [5]."

# Resolve dependencies
python execution_runner.py --resolve 5
# Output: "Step 5 dependencies resolved. Navigate back: `python execution_runner.py --back 5`"

# Return to Step 5
python execution_runner.py --back 5
# ... complete remaining backend work ...
python execution_runner.py --done
```

### Dependency Warnings

When you run `--next`, the framework warns if the current step has unresolved dependencies (from the execution plan):

```bash
python execution_runner.py --next
# ⚠️  Step 5 depends on steps [7] which are not yet completed.
#     You may proceed, but consider using `--done --partial` if blocked.
```

### Best Practices

1. **Document dependencies clearly**: Use descriptive reasons when marking steps as partial/blocked
2. **Check resolution regularly**: Run `--resolve` after completing steps to detect resolved dependencies
3. **Complete blocked work promptly**: Return to blocked steps as soon as dependencies are resolved
4. **Update backlog if needed**: Consider updating `BACKLOG.md` or `SPRINT_PLAN.md` to document dependencies for team visibility

**See:** [RFC-002: Step Dependencies](../rfcs/RFC-002-step-dependencies.md) for complete specification.

**Note:** Advanced features (automatic planning reviews, workaround suggestions, blocking metrics) are planned for v1.2. See [RFC-003: Advanced Dependency Management](../rfcs/RFC-003-advanced-dependency-management.md).

---

## 🔄 Ad-hoc Agent Sessions

**Note:** This section describes features planned for v1.1+. For current limitations, see [Current Limitations](#-current-limitations) below.

During development, you often need to make quick corrections, adjustments, or iterations by calling agents directly (e.g., `@backend-engineer.md fix this bug`). Ad-hoc sessions allow you to track these interactions while maintaining full observability.

### Creating an Ad-hoc Session

```bash
# Create session linked to current execution step
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug" \
    --link-step 5

# Or create independent session
python execution_runner.py --session testing/qa-strategist.md \
    --task "Review test coverage"
```

**Output:**
```
✅ Ad-hoc session created: adhoc-2026-03-02T10-30-00-backend-engineer
   Agent: engineering/backend-engineer.md
   Task: Fix authentication bug
   Linked to: Step 5
   Session file: .agents/swarm/sessions/adhoc-2026-03-02T10-30-00-backend-engineer.json

💡 Use this agent in your IDE with context:
   @engineering/backend-engineer.md Fix authentication bug

💡 To record interaction:
   python execution_runner.py --session-log <session_id> --interaction 'Fixed bug'
```

### Using the Agent Directly

After creating a session, use the agent directly in your IDE:

```
@engineering/backend-engineer.md Fix authentication bug in login endpoint
```

The agent will work normally, but you'll track the interaction.

### Logging Interactions

After each agent interaction, log it:

```bash
# Log agent response
python execution_runner.py --session-log adhoc-2026-03-02T10-30-00-backend-engineer \
    --type response \
    --content "Fixed: Updated JWT validation logic in src/auth/jwt.py" \
    --artifacts src/auth/jwt.py tests/test_auth.py
```

**Interaction Types:**
- `request`: Your request to the agent
- `response`: Agent's response/work
- `correction`: Correction or iteration
- `clarification`: Clarification question

### Closing a Session

When done with ad-hoc work:

```bash
python execution_runner.py --session-close adhoc-2026-03-02T10-30-00-backend-engineer \
    --summary "Fixed authentication bug, updated tests, verified security"
```

### Managing Sessions

**List all sessions:**
```bash
python execution_runner.py --sessions
```

**List active sessions only:**
```bash
python execution_runner.py --sessions --status active
```

**Show session details:**
```bash
python execution_runner.py --session-show adhoc-2026-03-02T10-30-00-backend-engineer
```

### Complete Example Workflow

```bash
# Step 5 is in progress, bug discovered
python execution_runner.py --next    # Shows step 5

# Create ad-hoc session for bug fix
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug discovered during Step 5" \
    --link-step 5

# Use agent in IDE
# @engineering/backend-engineer.md Fix authentication bug in login endpoint

# After fix, log interaction
python execution_runner.py --session-log adhoc-2026-03-02T10-30-00-backend-engineer \
    --type response \
    --content "Fixed: Updated JWT validation logic" \
    --artifacts src/auth/jwt.py tests/test_auth.py

# Close session
python execution_runner.py --session-close adhoc-2026-03-02T10-30-00-backend-engineer \
    --summary "Fixed authentication bug, updated tests"

# Continue with main execution
python execution_runner.py --next    # Continue step 5
```

### Benefits

- **Full traceability**: All interactions recorded in journal
- **Complete audit trail**: Every agent call is tracked
- **Context preservation**: Sessions can link to execution steps
- **Flexibility**: Quick corrections without breaking workflow
- **Observability**: All work visible in framework

**See:** [RFC-004: Ad-hoc Agent Sessions](../rfcs/RFC-004-ad-hoc-agent-sessions.md) for complete specification.

---

## 🚀 MVP to Production Transition

**Note:** This section describes features planned for v1.1+. For current workarounds, see [Current Limitations](#-current-limitations) below.

It's common for agents to deliver MVP functionality but defer production concerns (deployment, monitoring, scaling, security hardening) to the backlog. The framework provides a structured way to transition from MVP to production.

### Understanding MVP vs Production

**MVP Sprint:**
- Focus: Core functionality
- Deployment: Local/development
- Monitoring: Basic logging
- Security: Basic review
- Testing: Unit/integration tests
- Goal: Working system with core features

**Production Readiness Sprint:**
- Focus: Production concerns
- Deployment: Production-ready configuration
- Monitoring: Full observability
- Security: Hardened security
- Testing: Production-like testing
- Goal: Production-ready system

### Creating a Production Readiness Sprint

After your MVP sprint is closed, create a production readiness sprint:

```bash
# After MVP sprint is closed
python execution_runner.py --production-sprint
```

**What happens:**
- Framework detects previous sprint artifacts (BACKLOG.md, SPRINT_PLAN.md)
- Extracts production-related items from backlog
- Creates production-focused execution plan
- Preserves context from MVP sprint
- Links to previous sprint artifacts

**Output:**
```
✅ Production Readiness Sprint initialized
   Previous sprint: Sprint 1 (MVP)
   Backlog items identified: 6 production-related items
   Sprint type: production-readiness
   Plan: .agents/swarm/execution_plan.json
   
📋 Production focus areas:
   - Deployment configuration
   - CI/CD pipeline
   - Monitoring and observability
   - Security hardening
   - Performance optimization
```

### Production-Focused Execution

The production sprint executes the same 13 steps, but with production focus:

**Step 1-2: Planning**
- PO prioritizes production items from backlog
- Scrum Master plans production sprint
- Focus on production acceptance criteria

**Step 3-4: Design**
- Architect reviews production architecture
- Designs for scalability and high availability
- Production deployment architecture

**Step 5-7: Build**
- Backend: Production configuration
- DevOps: Production deployment setup
- Focus on production concerns

**Step 8: DevOps/SRE (Extended)**
- Production deployment configuration
- CI/CD pipeline for production
- Infrastructure as Code
- Deployment automation
- Rollback procedures

**Step 9: QA (Extended)**
- Production-like testing
- Load testing
- Stress testing
- Performance testing

**Step 10: AppSec (Extended)**
- Production security hardening
- Security scanning
- Compliance validation
- Security monitoring

**Step 11-13: Release & Closure**
- Production release preparation
- Production documentation
- Sprint closure with production readiness validated

### Example Workflow

```bash
# Sprint 1: MVP Development
python execution_runner.py --init
# Task: "Build face recognition access control system MVP"
# ... executes all 13 steps ...
# Closes with backlog items for production:
#   - Production deployment configuration
#   - CI/CD pipeline setup
#   - Monitoring and observability
#   - Security hardening

# Sprint 2: Production Readiness
python execution_runner.py --production-sprint
# Framework automatically:
#   - Detects previous sprint
#   - Extracts production items
#   - Creates production-focused plan

# Task: "Prepare face recognition access control system for production deployment"

# Execute production-focused steps
python execution_runner.py --next
# ... work through production steps ...
python execution_runner.py --done
# ... continue until production-ready ...
```

### Backlog Continuity

The production sprint maintains continuity with MVP sprint:

- **Reads MVP backlog:** Extracts production items automatically
- **Preserves context:** References MVP architecture and decisions
- **Maintains links:** Links production stories to MVP stories
- **Builds on MVP:** Works with existing codebase

### Current Workaround (v1.0)

Until v1.1 is released, you can manually create a production sprint:

1. **Extract production items** from MVP backlog manually
2. **Create new execution plan:**
   ```bash
   python execution_runner.py --init
   # Task: "Prepare [project] for production deployment"
   ```
3. **Update backlog** with production items
4. **Execute** with production focus in mind

**Limitation:** Loses automatic context preservation and backlog extraction.

**See:** [RFC-005: Production Readiness Sprint](../rfcs/RFC-005-production-readiness-sprint.md) for complete specification.

---

## 🐛 Bug Triage and Fix Workflow

**Note:** This section describes features planned for v1.1+. For current workarounds, see [Current Limitations](#-current-limitations) below.

The framework provides structured bug reporting, triage, and fix workflows that integrate seamlessly with Scrum methodology.

### Reporting Bugs

When a bug is discovered (during execution or by a human), report it to the framework:

```bash
# Bug discovered during execution
python execution_runner.py --report-bug \
    --description "Authentication fails with special characters in password" \
    --severity medium \
    --priority medium \
    --reproduce "1. Create user with password containing @#$%\n2. Try to login\n3. Authentication fails" \
    --environment development \
    --discovered-by agent \
    --current-step 5

# Bug discovered by human (production)
python execution_runner.py --report-bug \
    --description "Face recognition accuracy drops below 90% in production" \
    --severity critical \
    --priority critical \
    --reproduce "1. Deploy to production\n2. Monitor accuracy metrics\n3. Accuracy drops below 90%" \
    --environment production \
    --discovered-by human
```

**What happens:**
- Creates bug report with unique ID (BUG-001, BUG-002, ...)
- Analyzes bug description to suggest which agent should fix it
- Adds bug to backlog automatically
- Records in execution journal
- Shows suggested next actions

### Triage Bugs

Triage bugs to prioritize, estimate effort, and assign to sprints:

```bash
# Show all untriaged bugs
python execution_runner.py --triage-bug

# Triage specific bug
python execution_runner.py --triage-bug BUG-001
```

**Interactive triage:**
- Adjust severity/priority
- Set effort estimate (1-8 points)
- Assign to current sprint, next sprint, or create hotfix sprint
- Reject bug if not valid

### Fixing Bugs

**Option 1: Immediate fix via ad-hoc session**

For bugs discovered during execution, fix immediately using ad-hoc session:

```bash
# Report bug
python execution_runner.py --report-bug \
    --description "Authentication fails" \
    --severity medium \
    --current-step 5

# Framework suggests: --session backend-engineer.md --bug BUG-001

# Create ad-hoc session linked to bug
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug BUG-001" \
    --bug BUG-001 \
    --link-step 5

# Use agent in IDE
# @engineering/backend-engineer.md Fix authentication bug BUG-001

# After fix, close session and mark bug as fixed
python execution_runner.py --session-close <session-id> \
    --summary "Fixed authentication bug BUG-001" \
    --bug-fixed BUG-001
```

**Option 2: Bug-fix sprint**

For critical bugs or bugs that need structured fix workflow:

```bash
# Create bug-fix sprint
python execution_runner.py --bug-fix-sprint --bug-id BUG-001 [--same-sprint|--next-sprint|--hotfix]
```

**Options:**
- `--same-sprint`: Fix in current sprint (if capacity allows)
- `--next-sprint`: Schedule for next sprint
- `--hotfix`: Critical bug, interrupt current sprint

**Bug-fix sprint includes:**
- Step 1: Product Owner — Review bug, update backlog
- Step 2: Scrum Master — Plan bug fix sprint
- Step 3: Staff Architect — Review fix approach (if needed)
- Step 4: [Suggested Agent] — Fix the bug
- Step 5: QA Strategist — Test the fix
- Step 6: AppSec Engineer — Security review (if security-related)
- Step 7: Release Manager — Prepare fix release

### Bug Status Flow

```
reported → triaged → assigned → in_progress → fixed → closed
                ↓
            (rejected)
```

### Integration with Backlog

Bugs are automatically added to backlog with format:

```markdown
## Bug Reports

### BUG-001: Authentication fails with special characters
- **Severity:** Medium
- **Priority:** Medium
- **Status:** Reported
- **Discovered by:** Agent
- **Environment:** Development
- **Suggested agent:** engineering/backend-engineer.md
- **Estimated effort:** 2 points
- **Sprint:** Not assigned

**Description:**
Authentication fails when password contains special characters (@#$%).

**Steps to reproduce:**
1. Create user with password containing @#$%
2. Try to login
3. Authentication fails

**Fix:**
[To be filled by assigned agent]
```

### Example Workflows

**Workflow 1: Bug discovered during execution (immediate fix)**

```bash
# Step 5 in progress, bug discovered
python execution_runner.py --report-bug \
    --description "Authentication fails" \
    --severity medium \
    --current-step 5

# Fix immediately with ad-hoc session
python execution_runner.py --session backend-engineer.md --bug BUG-001 --link-step 5
# ... fix bug ...
python execution_runner.py --session-close <session-id> --bug-fixed BUG-001

# Continue with step 5
python execution_runner.py --done
```

**Workflow 2: Critical bug in production (hotfix)**

```bash
# Human discovers critical bug
python execution_runner.py --report-bug \
    --description "Face recognition accuracy drops below 90%" \
    --severity critical \
    --environment production \
    --discovered-by human

# Triage confirms: Critical, hotfix needed
python execution_runner.py --triage-bug BUG-002

# Create hotfix sprint
python execution_runner.py --bug-fix-sprint --bug-id BUG-002 --hotfix

# Execute fix workflow
python execution_runner.py --next    # Step 1: PO reviews
# ... execute fix workflow ...
```

**Workflow 3: Bug triage and next sprint assignment**

```bash
# Bug reported during execution
python execution_runner.py --report-bug --description "UI bug" --severity medium

# Continue with current sprint
# ... finish sprint ...

# Before next sprint, triage bugs
python execution_runner.py --triage-bug

# Assign to next sprint
python execution_runner.py --triage-bug BUG-003
# Set: Priority Medium, Effort 1 point, Assign to next sprint

# Next sprint planning includes BUG-003
python execution_runner.py --init
# Task: "Fix UI bug BUG-003 and add feature X"
```

**See:** [RFC-006: Bug Triage and Fix Workflow](../rfcs/RFC-006-bug-triage-and-fix-workflow.md) for complete specification.

---

## ⚠️ Current Limitations

The framework has some known limitations that will be addressed in future versions:

### Execution Control

- **No `--back` command**: Currently, you cannot navigate backward to previous steps. If you need to review a previous step, you'll need to manually check the journal or restart the execution plan.
- **No undo for `--done`**: If you accidentally run `--done` when you meant `--next`, the step will be marked as completed and the execution state will advance. There's currently no way to undo this action.
  - **Workaround**: You can manually edit `.agents/swarm/execution_state.json` to revert `current_step`, but this is risky and not recommended.
- **No confirmation prompts**: Critical actions like `--done` execute immediately without confirmation.

### Ad-hoc Reviews and Direct Agent Calls

- **No `--review` command**: To request a review from a specific agent outside the normal execution flow, you currently need to:
  - Create a custom execution plan manually, or
  - Call the agent directly via IDE prompt (but this bypasses framework observability)
- **No ad-hoc session tracking**: Direct agent calls (e.g., `@agent fix bug`) are not tracked, losing traceability and audit trail
  - **Workaround**: None. Direct agent calls are completely untracked.
  - **Future (v1.1+)**: Ad-hoc agent sessions (`--session`, `--session-log`, `--session-close`) will provide full tracking for direct agent calls

### Dependency Management

- **No dependency tracking**: The framework cannot track dependencies between steps. If Step 5 (Backend) depends on Step 7 (AI Engineer), there's no way to:
  - Mark Step 5 as partially complete or blocked
  - Track which steps are waiting on others
  - Automatically detect when dependencies are resolved
  - Navigate back to complete blocked steps
- **Current workaround**: Manually update `BACKLOG.md` and `SPRINT_PLAN.md` to document dependencies, mark steps as done even if partial, and manually return to complete work later. This loses framework observability.

### MVP to Production Transition

- **No production readiness sprint**: The framework focuses on single-sprint MVP execution. When agents defer production concerns (deployment, monitoring, scaling, security hardening) to backlog, there's no structured way to transition to production:
  - Production items accumulate in backlog
  - No clear process for production readiness sprint
  - Context loss when starting new sprint for production
  - Manual workaround required (create new plan, copy backlog)
- **Current workaround**: Manually create new execution plan, extract production items from backlog, start fresh sprint (loses context and framework integration).

### Bug Triage and Fix Workflow

- **No bug reporting mechanism**: Bugs discovered during execution or by humans cannot be formally reported to the framework
- **No bug triage process**: No way to prioritize, estimate effort, or assign bugs to sprints
- **No bug-fix sprint type**: Cannot create focused bug-fix execution plans
- **No agent routing for bugs**: Framework doesn't guide which agent should fix bugs
- **No backlog integration**: Bugs are not automatically added to backlog
- **Loss of observability**: When bugs are fixed outside framework (e.g., direct agent calls), work is not tracked
- **Current workaround**: Fix bugs ad-hoc without framework integration, manually add to backlog if needed

**These limitations will be addressed in v1.1+** (see [Evolution Roadmap](../roadmap/EVOLUTION_ROADMAP.md), [RFC-002: Step Dependencies](../rfcs/RFC-002-step-dependencies.md), [RFC-005: Production Readiness Sprint](../rfcs/RFC-005-production-readiness-sprint.md), and [RFC-006: Bug Triage and Fix Workflow](../rfcs/RFC-006-bug-triage-and-fix-workflow.md)).

---

## 📚 Additional Guides

- **[Language-Specific Guide](LANGUAGE_SPECIFIC_GUIDE.md)** - Setup and best practices for Python, Node.js, Go, Rust, Java
- **[Scrum Guide](SCRUM_GUIDE.md)** - How the framework implements Scrum methodology
- **[Approval Gates](../architecture/APPROVAL_GATES.md)** - Detailed approval process
- **[Agents Framework](AGENTS_FRAMEWORK.md)** - Framework overview and design philosophy

---

**Philosophy:** structured progress over uncontrolled generation.
