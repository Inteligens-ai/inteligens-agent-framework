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

## 📚 Additional Guides

- **[Language-Specific Guide](LANGUAGE_SPECIFIC_GUIDE.md)** - Setup and best practices for Python, Node.js, Go, Rust, Java
- **[Scrum Guide](SCRUM_GUIDE.md)** - How the framework implements Scrum methodology
- **[Approval Gates](../architecture/APPROVAL_GATES.md)** - Detailed approval process
- **[Agents Framework](AGENTS_FRAMEWORK.md)** - Framework overview and design philosophy

---

**Philosophy:** structured progress over uncontrolled generation.
