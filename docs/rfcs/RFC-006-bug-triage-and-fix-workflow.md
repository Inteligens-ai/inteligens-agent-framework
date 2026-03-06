# RFC-006 — Bug Triage and Bug Fix Workflow

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.1  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC introduces **Bug Triage and Bug Fix Workflow** to the Inteligens Agents Framework, enabling structured bug reporting, triage, and fix workflows that integrate seamlessly with Scrum methodology.

The feature addresses two critical gaps:

1. **Bugs discovered during execution**: When errors occur, agents in the IDE often fix them directly without framework guidance, losing observability and proper agent routing.
2. **Bugs discovered by humans**: When a human discovers a bug (in production, testing, or review), there's no structured way to integrate it into the Scrum backlog and execution flow.

**Problem:** No structured bug workflow, no integration with backlog, no guidance on which agent should fix bugs.

**Solution:** Bug reporting, triage, and fix workflow with automatic backlog integration, agent routing, and bug-fix sprint support.

---

## 2. Motivation

### 2.1 Problem Statement

**Scenario 1: Bug discovered during execution**

During Step 5 (Backend), a bug is discovered:
- Agent in IDE immediately starts fixing it
- No framework guidance on which agent should act
- No structured process for bug fixes
- Fix happens outside framework observability
- No integration with backlog or sprint planning

**Scenario 2: Bug discovered by human**

A human discovers a bug in production:
- No way to report it to the framework
- No integration with backlog
- No triage process
- No assignment to appropriate agent
- No tracking in sprint context

### 2.2 Current Limitations

The framework currently:
- Has no bug reporting mechanism
- Has no bug triage process
- Has no bug-fix sprint type
- Does not integrate bugs into backlog
- Does not guide which agent should fix bugs
- Loses observability when bugs are fixed outside framework

### 2.3 Scrum Context

In traditional Scrum:
- Bugs are added to backlog
- Bugs are triaged (priority, severity, effort)
- Bugs are assigned to sprints
- Critical bugs may interrupt current sprint (hotfix)
- Bug fixes follow same sprint process as features

The framework needs to support this workflow.

---

## 3. Design Principles

The feature MUST:

- integrate seamlessly with Scrum methodology
- maintain full observability and traceability
- guide which agent should fix bugs
- support bugs discovered during execution and by humans
- integrate with backlog automatically
- support bug-fix sprints
- remain CLI-friendly
- preserve human-in-the-loop control

The feature MUST NOT:

- require external bug tracking systems
- break existing execution flow
- force bug fixes to interrupt current sprint
- lose context from main execution

---

## 4. Bug Triage and Fix Model

### 4.1 Bug Report Schema

```json
{
  "bug_id": "BUG-001",
  "description": "Face recognition fails in low light conditions",
  "severity": "critical|high|medium|low",
  "priority": "critical|high|medium|low",
  "status": "reported|triaged|assigned|in_progress|fixed|closed",
  "discovered_by": "human|agent|system",
  "discovered_at": "2026-03-02T10:00:00Z",
  "reproduce_steps": "1. Start face recognition\n2. Use in low light\n3. Observe failure",
  "environment": "production|staging|development|local",
  "affected_step": 5,
  "affected_agent": "engineering/backend-engineer.md",
  "suggested_agent": "engineering/backend-engineer.md",
  "estimated_effort": 2,
  "sprint_assigned": null,
  "fixed_at": null,
  "fixed_by": null,
  "resolution": null,
  "linked_issues": []
}
```

### 4.2 Bug Severity Levels

- **Critical**: System down, data loss, security breach
- **High**: Major feature broken, significant impact
- **Medium**: Feature partially broken, workaround exists
- **Low**: Minor issue, cosmetic, edge case

### 4.3 Bug Status Flow

```
reported → triaged → assigned → in_progress → fixed → closed
                ↓
            (rejected)
```

### 4.4 Agent Routing Logic

The framework will suggest which agent should fix a bug based on:

- **Affected step**: Which step discovered the bug
- **Bug description**: Keywords and context analysis
- **Affected files**: If bug is linked to specific files
- **Agent expertise**: Match bug type to agent specialization

**Example routing:**
- Authentication bug → `engineering/backend-engineer.md`
- UI bug → `engineering/frontend-engineer.md`
- AI/ML bug → `engineering/ai-engineer.md`
- Security bug → `security/appsec-engineer.md`
- Test bug → `quality/qa-strategist.md`

---

## 5. CLI Commands

### 5.1 Report Bug

```bash
python execution_runner.py --report-bug \
    --description "Face recognition fails in low light" \
    --severity high \
    --priority high \
    --reproduce "Steps to reproduce..." \
    --environment production \
    --discovered-by human \
    --current-step 5
```

**What happens:**
1. Creates bug report with unique ID (BUG-001, BUG-002, ...)
2. Analyzes bug description to suggest agent
3. Adds bug to backlog automatically
4. Records in execution journal
5. Shows suggested next actions

**Output:**
```
✅ Bug reported: BUG-001
📋 Description: Face recognition fails in low light
🔍 Severity: High
🎯 Priority: High
🤖 Suggested agent: engineering/ai-engineer.md
📝 Added to backlog automatically

Suggested actions:
1. Fix now (ad-hoc session): --session ai-engineer.md --bug BUG-001
2. Add to backlog: --add-to-backlog BUG-001
3. Triage first: --triage-bug BUG-001
```

### 5.2 Triage Bug

```bash
python execution_runner.py --triage-bug [BUG-ID]
```

**Without BUG-ID:** Shows all untriaged bugs

**With BUG-ID:** Interactive triage for specific bug

**What happens:**
1. Shows bug details
2. Allows priority/severity adjustment
3. Allows effort estimation
4. Suggests sprint assignment
5. Updates backlog

**Output:**
```
🔍 Bug Triage: BUG-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ false
```

**Interactive triage:**
```
Current values:
- Severity: High
- Priority: High
- Estimated effort: Unknown
- Suggested agent: engineering/ai-engineer.md
- Sprint assignment: None

Options:
1. Adjust severity/priority
2. Set effort estimate (1-8 points)
3. Assign to current sprint
4. Assign to next sprint
5. Create hotfix sprint
6. Reject bug
7. Save and continue
```

### 5.3 Bug Fix Sprint

```bash
python execution_runner.py --bug-fix-sprint --bug-id BUG-001 [--same-sprint|--next-sprint|--hotfix]
```

**What happens:**
1. Creates focused bug-fix execution plan
2. Includes only relevant steps for the bug
3. Preserves context from main execution
4. Links to original bug report
5. Executes fix workflow

**Bug-fix sprint steps:**
- Step 1: Product Owner — Review bug, update backlog
- Step 2: Scrum Master — Plan bug fix sprint
- Step 3: Staff Architect — Review fix approach (if needed)
- Step 4: [Suggested Agent] — Fix the bug
- Step 5: QA Strategist — Test the fix
- Step 6: AppSec Engineer — Security review (if security-related)
- Step 7: Release Manager — Prepare fix release

**Options:**
- `--same-sprint`: Fix in current sprint (if capacity allows)
- `--next-sprint`: Schedule for next sprint
- `--hotfix`: Critical bug, interrupt current sprint

### 5.4 List Bugs

```bash
python execution_runner.py --bugs [--status reported|triaged|assigned|in_progress|fixed|closed]
```

Shows all bugs with their status, severity, and assignment.

### 5.5 Show Bug

```bash
python execution_runner.py --bug BUG-001
```

Shows detailed information about a specific bug.

---

## 6. Integration with Existing Features

### 6.1 Integration with Ad-hoc Sessions (RFC-004)

When a bug is discovered during execution, use ad-hoc session for immediate fix:

```bash
# Report bug
python execution_runner.py --report-bug \
    --description "Authentication fails with special characters" \
    --severity medium \
    --current-step 5

# Framework suggests: --session backend-engineer.md --bug BUG-001

# Create ad-hoc session linked to bug
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug BUG-001" \
    --bug BUG-001 \
    --link-step 5

# Fix bug using agent
# @engineering/backend-engineer.md Fix authentication bug BUG-001

# Log fix
python execution_runner.py --session-log <session-id> \
    --type response \
    --content "Fixed: Updated JWT validation to handle special characters"

# Close session and mark bug as fixed
python execution_runner.py --session-close <session-id> \
    --summary "Fixed authentication bug BUG-001" \
    --bug-fixed BUG-001
```

### 6.2 Integration with Backlog

Bugs are automatically added to backlog with format:

```markdown
## Bug Reports

### BUG-001: Face recognition fails in low light
- **Severity:** High
- **Priority:** High
- **Status:** Reported
- **Discovered by:** Human
- **Environment:** Production
- **Suggested agent:** engineering/ai-engineer.md
- **Estimated effort:** 2 points
- **Sprint:** Not assigned

**Description:**
Face recognition accuracy drops below 90% in low light conditions.

**Steps to reproduce:**
1. Start face recognition system
2. Use in low light environment (< 50 lux)
3. Observe recognition failure

**Fix:**
[To be filled by assigned agent]
```

### 6.3 Integration with Production Readiness Sprint (RFC-005)

Bugs can be included in production readiness sprints:

```bash
# Create production readiness sprint
python execution_runner.py --production-sprint

# Framework automatically includes:
# - Production-related bugs
# - Critical bugs from backlog
# - Security bugs
```

---

## 7. Workflow Examples

### 7.1 Bug Discovered During Execution

```bash
# Step 5 (Backend) in progress
python execution_runner.py --next    # Shows step 5

# Bug discovered: Authentication fails
python execution_runner.py --report-bug \
    --description "Authentication fails with special characters in password" \
    --severity medium \
    --priority medium \
    --reproduce "1. Create user with password containing @#$%\n2. Try to login\n3. Authentication fails" \
    --environment development \
    --discovered-by agent \
    --current-step 5

# Framework output:
# ✅ Bug reported: BUG-001
# 🤖 Suggested agent: engineering/backend-engineer.md
# 
# Suggested actions:
# 1. Fix now (ad-hoc session): --session backend-engineer.md --bug BUG-001
# 2. Add to backlog: Already added
# 3. Triage first: --triage-bug BUG-001

# Option 1: Fix immediately with ad-hoc session
python execution_runner.py --session engineering/backend-engineer.md \
    --task "Fix authentication bug BUG-001" \
    --bug BUG-001 \
    --link-step 5

# Use agent in IDE
# @engineering/backend-engineer.md Fix authentication bug BUG-001

# After fix, log and close
python execution_runner.py --session-close <session-id> \
    --summary "Fixed authentication bug BUG-001" \
    --bug-fixed BUG-001

# Continue with step 5
python execution_runner.py --done
python execution_runner.py --next    # Step 6
```

### 7.2 Bug Discovered by Human (Production)

```bash
# Human discovers bug in production
python execution_runner.py --report-bug \
    --description "Face recognition accuracy drops below 90% in production" \
    --severity critical \
    --priority critical \
    --reproduce "1. Deploy to production\n2. Monitor accuracy metrics\n3. Accuracy drops below 90%" \
    --environment production \
    --discovered-by human

# Framework output:
# ✅ Bug reported: BUG-002
# 🚨 CRITICAL BUG DETECTED
# 🤖 Suggested agent: engineering/ai-engineer.md
# 
# Suggested actions:
# 1. Create hotfix sprint: --bug-fix-sprint --bug-id BUG-002 --hotfix
# 2. Triage first: --triage-bug BUG-002

# Triage bug
python execution_runner.py --triage-bug BUG-002

# Interactive triage confirms: Critical, High priority, 3 points
# Decision: Hotfix sprint

# Create hotfix sprint
python execution_runner.py --bug-fix-sprint --bug-id BUG-002 --hotfix

# Framework creates focused bug-fix execution plan
# Execute fix workflow
python execution_runner.py --next    # Step 1: PO reviews bug
python execution_runner.py --done
python execution_runner.py --next    # Step 2: Scrum Master plans fix
python execution_runner.py --done
python execution_runner.py --next    # Step 3: AI Engineer fixes bug
# ... agent fixes bug ...
python execution_runner.py --done
python execution_runner.py --next    # Step 4: QA tests fix
python execution_runner.py --done
python execution_runner.py --next    # Step 5: Release Manager prepares hotfix
python execution_runner.py --done

# Bug fixed and released
```

### 7.3 Bug Triage and Next Sprint Assignment

```bash
# Bug reported during execution
python execution_runner.py --report-bug \
    --description "UI button not responsive on mobile" \
    --severity medium \
    --current-step 6

# Framework: Bug BUG-003 reported, added to backlog

# Continue with current sprint
# ... finish sprint ...

# Before next sprint, triage bugs
python execution_runner.py --triage-bug

# Shows untriaged bugs:
# BUG-003: UI button not responsive on mobile
# - Severity: Medium
# - Priority: Medium
# - Suggested agent: engineering/frontend-engineer.md
# - Estimated effort: 1 point

# Triage: Assign to next sprint
python execution_runner.py --triage-bug BUG-003
# Set: Priority Medium, Effort 1 point, Assign to next sprint

# Next sprint planning includes BUG-003
python execution_runner.py --init
# Task: "Fix UI bug BUG-003 and add feature X"
# ... sprint includes bug fix ...
```

---

## 8. File Structure

### 8.1 Bug Reports Storage

```
.agents/
  swarm/
    bugs/
      BUG-001.json
      BUG-002.json
      bugs_index.json
```

### 8.2 Bugs Index

```json
{
  "bugs": [
    {
      "bug_id": "BUG-001",
      "status": "fixed",
      "severity": "high",
      "priority": "high",
      "sprint_assigned": "Sprint-1"
    }
  ],
  "next_bug_id": 2
}
```

---

## 9. Acceptance Criteria

- [ ] `--report-bug` command creates bug report with unique ID
- [ ] Bug reports are automatically added to backlog
- [ ] Framework suggests which agent should fix bug
- [ ] `--triage-bug` allows interactive bug triage
- [ ] `--bug-fix-sprint` creates focused bug-fix execution plan
- [ ] Bugs can be fixed via ad-hoc sessions (RFC-004 integration)
- [ ] Bugs are tracked in execution journal
- [ ] Bugs can be assigned to current sprint, next sprint, or hotfix
- [ ] Bug status flow is enforced (reported → triaged → assigned → fixed → closed)
- [ ] Bug reports are stored in `.agents/swarm/bugs/`
- [ ] Backlog automatically includes bug reports section
- [ ] `--bugs` command lists all bugs with status
- [ ] `--bug BUG-ID` shows detailed bug information
- [ ] Integration with Production Readiness Sprint includes production bugs

---

## 10. Future Enhancements (v1.2+)

- **Automatic bug detection**: System detects bugs from test failures, logs, metrics
- **Bug patterns**: Learn from bug history to suggest fixes
- **Bug metrics**: Track bug resolution time, bug density, bug trends
- **Bug linking**: Link bugs to features, steps, commits
- **Bug templates**: Pre-filled bug reports for common issues
- **Bug prioritization AI**: AI-assisted bug prioritization based on impact

---

## 11. Decision

**Status:** Proposed for v1.1

This RFC addresses critical gaps in bug handling and integrates seamlessly with Scrum methodology. The feature provides structured bug workflow while maintaining framework observability and human control.

**Next steps:**
1. Review and approve RFC
2. Implement bug reporting and storage
3. Implement triage workflow
4. Implement bug-fix sprint type
5. Integrate with backlog and ad-hoc sessions
6. Update documentation

---

**See also:**
- [RFC-004: Ad-hoc Agent Sessions](./RFC-004-ad-hoc-agent-sessions.md)
- [RFC-005: Production Readiness Sprint](./RFC-005-production-readiness-sprint.md)
