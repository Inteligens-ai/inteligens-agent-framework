# RFC-004 — Ad-hoc Agent Sessions

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.1  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC introduces **Ad-hoc Agent Sessions** to the Inteligens Agents Framework, enabling direct agent calls while maintaining full traceability, auditability, and observability.

The feature addresses the common development scenario where engineers need to make quick corrections, adjustments, or iterations by calling agents directly (e.g., `@backend-engineer.md fix this bug`), which currently bypasses framework tracking.

**Problem:** Direct agent calls lose traceability, auditability, and observability.

**Solution:** Ad-hoc sessions that track all agent interactions while allowing flexible, direct agent usage.

---

## 2. Motivation

**Problem Statement:**

During development, it's common to:
- Make quick corrections outside the structured execution flow
- Iterate on solutions with multiple agent interactions
- Fix bugs discovered during execution
- Adjust implementations based on feedback
- Have back-and-forth conversations with agents

**Current Limitation:**

When agents are called directly (e.g., via IDE `@agent` syntax), these interactions:
- Are not recorded in the execution journal
- Don't appear in execution state
- Lose context from the main execution plan
- Have no audit trail
- Are invisible to the framework

This creates a **governance gap** where important work happens outside framework observability.

**Solution:**

Ad-hoc sessions provide a lightweight mechanism to:
- Track all direct agent interactions
- Maintain context from the main execution plan
- Link sessions to specific execution steps
- Provide full audit trail
- Enable observability without breaking workflow

---

## 3. Design Principles

The feature MUST:

- remain CLI-friendly
- preserve human-in-the-loop control
- maintain full journal traceability
- allow flexible, direct agent usage
- not interfere with normal execution flow
- be backward compatible

The feature MUST NOT:

- require complex setup
- force structured workflows for ad-hoc work
- break existing execution model
- require external services

---

## 4. Ad-hoc Session Model

### 4.1 Session Lifecycle

```
Created → Active → [Interactions...] → Completed
```

**States:**
- `active`: Session is open, accepting interactions
- `completed`: Session is closed, no more interactions
- `archived`: Session is archived (future)

### 4.2 Session Schema

```json
{
  "session_id": "adhoc-2026-03-02T10-30-00-backend-engineer",
  "type": "ad-hoc",
  "agent": "engineering/backend-engineer.md",
  "task": "Fix authentication bug",
  "linked_to_step": 5,
  "linked_to_plan": ".agents/swarm/execution_plan.json",
  "created_at": "2026-03-02T10:30:00Z",
  "status": "active",
  "interactions": [
    {
      "timestamp": "2026-03-02T10:30:15Z",
      "type": "request",
      "content": "Fix authentication bug in login endpoint",
      "context": "Step 5 in progress",
      "artifacts": []
    },
    {
      "timestamp": "2026-03-02T10:32:00Z",
      "type": "response",
      "content": "Fixed: Updated JWT validation logic",
      "artifacts": ["src/auth/jwt.py", "tests/test_auth.py"]
    }
  ],
  "artifacts_modified": ["src/auth/jwt.py", "tests/test_auth.py"],
  "summary": null,
  "completed_at": null
}
```

### 4.3 Session Storage

Sessions are stored in:
```
.agents/swarm/sessions/{session_id}.json
```

Temporary plans for sessions:
```
.agents/swarm/sessions/{session_id}_plan.json
```

---

## 5. CLI Commands

### 5.1 Create Session

```bash
python execution_runner.py --session <agent> --task "<task description>" [--link-step <step>] [--context "<context>"]
```

**Parameters:**
- `--session <agent>`: Agent path (e.g., `engineering/backend-engineer.md`)
- `--task "<task>"`: Task description
- `--link-step <step>`: (Optional) Link to execution step number
- `--context "<context>"`: (Optional) Additional context

**Behavior:**
- Generates unique session ID
- Creates session file
- Creates temporary execution plan
- Records session start in journal
- Prints session details and usage instructions

**Example:**
```bash
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug" \
    --link-step 5
```

**Output:**
```
✅ Ad-hoc session created: adhoc-2026-03-02T10-30-00-backend-engineer
   Agent: engineering/backend-engineer.md
   Task: Fix authentication bug
   Linked to: Step 5
   Session file: .agents/swarm/sessions/adhoc-2026-03-02T10-30-00-backend-engineer.json
   Plan file: .agents/swarm/sessions/adhoc-2026-03-02T10-30-00-backend-engineer_plan.json

📝 All interactions will be tracked in:
   - Journal: .agents/swarm/execution_journal.md
   - Session: .agents/swarm/sessions/adhoc-2026-03-02T10-30-00-backend-engineer.json

💡 Use this agent in your IDE with context:
   @engineering/backend-engineer.md Fix authentication bug

💡 To record interaction:
   python execution_runner.py --session-log adhoc-2026-03-02T10-30-00-backend-engineer --interaction 'Fixed bug'

💡 To close session:
   python execution_runner.py --session-close adhoc-2026-03-02T10-30-00-backend-engineer
```

### 5.2 Log Interaction

```bash
python execution_runner.py --session-log <session_id> --type <type> --content "<content>" [--artifacts <file1> <file2> ...]
```

**Parameters:**
- `--session-log <session_id>`: Session ID to log to
- `--type <type>`: Interaction type (`request`, `response`, `correction`, `clarification`)
- `--content "<content>"`: Interaction content
- `--artifacts <files...>`: (Optional) Modified artifacts

**Behavior:**
- Validates session exists and is active
- Adds interaction to session
- Updates artifacts_modified list
- Records in journal
- Prints confirmation

**Example:**
```bash
python execution_runner.py --session-log adhoc-2026-03-02T10-30-00-backend-engineer \
    --type response \
    --content "Fixed: Updated JWT validation logic in src/auth/jwt.py" \
    --artifacts src/auth/jwt.py tests/test_auth.py
```

### 5.3 Close Session

```bash
python execution_runner.py --session-close <session_id> [--summary "<summary>"]
```

**Parameters:**
- `--session-close <session_id>`: Session ID to close
- `--summary "<summary>"`: (Optional) Session summary

**Behavior:**
- Validates session exists
- Sets status to `completed`
- Records completion timestamp
- Records summary (if provided)
- Records in journal
- Prints session statistics

**Example:**
```bash
python execution_runner.py --session-close adhoc-2026-03-02T10-30-00-backend-engineer \
    --summary "Fixed authentication bug, updated tests, verified security"
```

### 5.4 List Sessions

```bash
python execution_runner.py --sessions [--status <status>] [--agent <agent>]
```

**Parameters:**
- `--sessions`: List all sessions
- `--status <status>`: (Optional) Filter by status (`active`, `completed`)
- `--agent <agent>`: (Optional) Filter by agent

**Behavior:**
- Scans sessions directory
- Filters by criteria (if provided)
- Displays session summary table
- Shows session statistics

**Example:**
```bash
python execution_runner.py --sessions --status active
```

**Output:**
```
📋 Active Ad-hoc Sessions:

Session ID                                    Agent                          Task                    Linked Step
adhoc-2026-03-02T10-30-00-backend-engineer   engineering/backend-engineer  Fix authentication bug  5
adhoc-2026-03-02T11-15-00-qa-strategist      testing/qa-strategist         Review test coverage    None

Total: 2 active sessions
```

### 5.5 Show Session Details

```bash
python execution_runner.py --session-show <session_id>
```

**Behavior:**
- Loads session file
- Displays formatted session details
- Shows all interactions
- Lists modified artifacts
- Displays statistics

---

## 6. Journal Integration

All session events are recorded in the main execution journal:

### Session Start

```markdown
### Ad-hoc Session Started — 2026-03-02T10:30:00Z
Session ID: `adhoc-2026-03-02T10-30-00-backend-engineer`
Agent: `engineering/backend-engineer.md`
Task: Fix authentication bug
Linked to: Step 5 of main execution plan
Session file: `.agents/swarm/sessions/adhoc-2026-03-02T10-30-00-backend-engineer.json`
---
```

### Session Interaction

```markdown
### Ad-hoc Session Interaction — 2026-03-02T10:32:00Z
Session ID: `adhoc-2026-03-02T10-30-00-backend-engineer`
Agent: `engineering/backend-engineer.md`
Type: response
Content: Fixed: Updated JWT validation logic in src/auth/jwt.py
Artifacts: src/auth/jwt.py, tests/test_auth.py
---
```

### Session Close

```markdown
### Ad-hoc Session Closed — 2026-03-02T10:45:00Z
Session ID: `adhoc-2026-03-02T10-30-00-backend-engineer`
Agent: `engineering/backend-engineer.md`
Total interactions: 3
Artifacts modified: 2
Summary: Fixed authentication bug, updated tests, verified security
---
```

---

## 7. Integration with Main Execution

### 7.1 Linking to Execution Steps

Sessions can be linked to execution steps:

```bash
python execution_runner.py --session backend-engineer.md --task "Fix bug" --link-step 5
```

**Benefits:**
- Maintains context from main execution
- Shows relationship between ad-hoc work and planned steps
- Enables traceability across execution flow

### 7.2 Independent Sessions

Sessions can also be independent:

```bash
python execution_runner.py --session qa-strategist.md --task "Review test coverage"
```

**Use cases:**
- Exploratory work
- Quick reviews
- Independent investigations
- Pre-execution planning

---

## 8. Example Workflows

### 8.1 Quick Bug Fix During Execution

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

### 8.2 Multiple Iterations

```bash
# Create session
python execution_runner.py --session engineering/frontend-engineer.md \
    --task "Improve UI responsiveness"

# Iteration 1
# @engineering/frontend-engineer.md Optimize component rendering
python execution_runner.py --session-log <session_id> \
    --type request --content "Optimize component rendering"

# Agent response
python execution_runner.py --session-log <session_id> \
    --type response --content "Optimized: Used React.memo, reduced re-renders" \
    --artifacts src/components/UserList.tsx

# Iteration 2
# @engineering/frontend-engineer.md Add loading states
python execution_runner.py --session-log <session_id> \
    --type request --content "Add loading states"

# Agent response
python execution_runner.py --session-log <session_id> \
    --type response --content "Added: Loading skeletons for all async components" \
    --artifacts src/components/LoadingSkeleton.tsx src/components/UserList.tsx

# Close session
python execution_runner.py --session-close <session_id> \
    --summary "Improved UI responsiveness with optimizations and loading states"
```

### 8.3 Pre-execution Review

```bash
# Before starting execution, review architecture
python execution_runner.py --session engineering/staff-architect.md \
    --task "Review proposed architecture before execution"

# Use agent in IDE
# @engineering/staff-architect.md Review the architecture in docs/ARCHITECTURE.md

# Log review
python execution_runner.py --session-log <session_id> \
    --type response \
    --content "Reviewed: Architecture looks good, suggest adding caching layer" \
    --artifacts docs/ARCHITECTURE.md

# Close session
python execution_runner.py --session-close <session_id> \
    --summary "Architecture review completed, suggestions documented"

# Now start main execution
python execution_runner.py --init
```

---

## 9. Helper Scripts (Optional)

### 9.1 Quick Session Creation

```bash
#!/bin/bash
# .agents/bin/session.sh

AGENT=$1
TASK=$2
STEP=$3

# Get current step if not provided
if [ -z "$STEP" ]; then
    STEP=$(python .agents/swarm/execution_runner.py --current-step 2>/dev/null || echo "")
fi

# Create session
python .agents/swarm/execution_runner.py --session "$AGENT" --task "$TASK" ${STEP:+--link-step $STEP}
```

**Usage:**
```bash
.agents/bin/session.sh engineering/backend-engineer.md "Fix bug"
```

### 9.2 Auto-logging (Future)

Future enhancement: automatically detect agent interactions and log them.

---

## 10. Session Metrics

### 10.1 Session Statistics

Track:
- Total sessions created
- Active sessions
- Average interactions per session
- Most used agents
- Average session duration
- Artifacts modified per session

### 10.2 Command: `--session-metrics`

```bash
python execution_runner.py --session-metrics
```

**Output:**
```
📊 Ad-hoc Session Metrics:

Total sessions: 15
Active: 2
Completed: 13
Average interactions per session: 2.3
Average session duration: 12m 30s
Most used agent: engineering/backend-engineer.md (8 sessions)
Total artifacts modified: 45
```

---

## 11. Backward Compatibility

- All features are **additive**
- Existing execution flow unchanged
- Sessions are optional
- No breaking changes to existing commands
- Sessions directory created automatically

---

## 12. Future Extensions (Non-Goals for v1.1)

Explicitly out of scope:

- Automatic interaction detection (requires IDE integration)
- Session templates
- Session sharing/collaboration
- Real-time session monitoring
- Session analytics dashboard
- Integration with external tools

These may be considered for v1.2+.

---

## 13. Acceptance Criteria

- [ ] `--session` command creates ad-hoc session with tracking
- [ ] `--session-log` records interactions in session and journal
- [ ] `--session-close` closes session and records summary
- [ ] `--sessions` lists all sessions with filters
- [ ] `--session-show` displays session details
- [ ] All session events recorded in execution journal
- [ ] Sessions can be linked to execution steps
- [ ] Sessions can be independent
- [ ] Session files stored in `.agents/swarm/sessions/`
- [ ] Backward compatibility maintained
- [ ] Documentation updated (Usage Guide, Roadmap)

---

## 14. Decision

**Status:** Proposed for v1.1

**Rationale:**

This RFC addresses a critical governance gap: direct agent calls are common in real development workflows but currently bypass framework observability. Ad-hoc sessions provide a lightweight solution that:

- Maintains full traceability
- Preserves audit trail
- Enables observability
- Doesn't break existing workflows
- Is simple to use

**Next Steps:**

1. Review and approve RFC
2. Implement session management commands
3. Integrate with journal system
4. Test with real-world scenarios
5. Update documentation
6. Release in v1.1

---

**See Also:**

- [RFC-002: Step Dependencies](RFC-002-step-dependencies.md) — Related dependency management
- [Usage Guide](../../guides/USAGE_GUIDE.md) — User-facing documentation
- [Evolution Roadmap](../../roadmap/EVOLUTION_ROADMAP.md) — Technical roadmap
