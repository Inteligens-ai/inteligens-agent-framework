# RFC-005 — Production Readiness Sprint

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.1  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC introduces **Production Readiness Sprint** support to the Inteligens Agents Framework, enabling structured transition from MVP to production-ready systems.

The feature addresses the common scenario where agents deliver MVP functionality but defer production concerns (deployment, monitoring, scaling, security hardening) to future work. This RFC provides a structured approach to handle production readiness as a dedicated sprint type.

---

## 2. Motivation

**Problem Statement:**

During MVP development, agents often:
- Focus on core functionality
- Defer production concerns to backlog
- Leave deployment, monitoring, and scaling for "later"
- Create technical debt that accumulates

**Current Limitation:**

The framework's single-sprint model assumes:
- One sprint = complete project
- MVP and production are the same thing
- No distinction between development and production readiness

**Real-World Scenario:**

1. **Sprint 1 (MVP):** Core functionality works, but:
   - No production deployment config
   - No monitoring/observability
   - No CI/CD pipeline
   - Basic security only
   - No scaling considerations

2. **Sprint 2 (Production):** Need to:
   - Set up production deployment
   - Add monitoring and alerting
   - Implement CI/CD
   - Harden security
   - Add scaling capabilities
   - Performance optimization

**Current Workaround:**

- Manually create new execution plan
- Copy backlog items from Sprint 1
- Start fresh sprint
- Lose context and continuity

**Solution:**

Production Readiness Sprint provides:
- Structured transition from MVP to production
- Context preservation from previous sprint
- Focused steps for production concerns
- Integration with backlog continuity

---

## 3. Design Principles

The feature MUST:

- preserve context from MVP sprint
- maintain backlog continuity
- focus on production-specific concerns
- be optional (not all projects need production sprint)
- remain CLI-friendly
- maintain full observability

The feature MUST NOT:

- require external services
- break existing single-sprint model
- force production sprint for all projects

---

## 4. Production Readiness Sprint Model

### 4.1 Sprint Types

The framework will support multiple sprint types:

- **`mvp`** (default): Standard development sprint
- **`production-readiness`**: Focused on production concerns
- **`enhancement`**: Feature additions to existing system
- **`maintenance`**: Bug fixes and improvements
- **`bug-fix`**: Focused bug-fix sprint (see [RFC-006: Bug Triage and Fix Workflow](./RFC-006-bug-triage-and-fix-workflow.md))

### 4.2 Production Readiness Sprint Characteristics

**Focus Areas:**
- Production deployment configuration
- CI/CD pipeline setup
- Monitoring and observability
- Security hardening
- Performance optimization
- Scaling preparation
- Disaster recovery
- Documentation for operations

**Key Differences from MVP Sprint:**

| Aspect | MVP Sprint | Production Readiness Sprint |
|--------|-----------|---------------------------|
| **Focus** | Core functionality | Production concerns |
| **Deployment** | Local/development | Production-ready |
| **Monitoring** | Basic logging | Full observability |
| **Security** | Basic review | Hardened security |
| **Testing** | Unit/integration | Production-like testing |
| **Documentation** | Development docs | Operations docs |

---

## 5. Execution Plan Schema Extension

Execution plans will support sprint type:

```json
{
  "generated": "2026-03-02T10:00:00Z",
  "swarm_version": "7.3.0",
  "task": "Prepare face recognition access control system for production deployment",
  "sprint_type": "production-readiness",
  "previous_sprint": {
    "sprint_id": "sprint-1-mvp",
    "backlog_file": "BACKLOG.md",
    "sprint_plan_file": "SPRINT_PLAN.md",
    "artifacts_dir": "."
  },
  "execution_plan": [
    {
      "step": 1,
      "agent": "product/product-owner.md",
      "phase": "plan",
      "context": {
        "sprint_type": "production-readiness",
        "previous_sprint_items": ["US-009", "US-010", "US-011"]
      }
    },
    ...
  ]
}
```

### 5.1 Sprint Type Detection

The planner will detect sprint type from task description:

```python
def detect_sprint_type(task: str) -> str:
    """Detect sprint type from task description"""
    
    task_lower = task.lower()
    
    if any(keyword in task_lower for keyword in [
        "production", "deploy to prod", "production ready",
        "production deployment", "go live", "launch"
    ]):
        return "production-readiness"
    
    if any(keyword in task_lower for keyword in [
        "enhance", "add feature", "new feature"
    ]):
        return "enhancement"
    
    if any(keyword in task_lower for keyword in [
        "fix", "bug", "maintenance", "improve"
    ]):
        return "maintenance"
    
    return "mvp"  # default
```

---

## 6. CLI Commands

### 6.1 Create Production Readiness Sprint

```bash
python execution_runner.py --production-sprint [--previous-sprint <dir>]
```

**Parameters:**
- `--production-sprint`: Create production readiness sprint
- `--previous-sprint <dir>`: (Optional) Path to previous sprint directory

**Behavior:**
- Detects previous sprint artifacts (BACKLOG.md, SPRINT_PLAN.md)
- Extracts production-related backlog items
- Creates new execution plan with production focus
- Preserves context from previous sprint
- Links to previous sprint artifacts

**Example:**
```bash
# After MVP sprint is closed
cd /path/to/project
python execution_runner.py --production-sprint

# Or specify previous sprint location
python execution_runner.py --production-sprint --previous-sprint /path/to/mvp-sprint
```

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

### 6.2 Enhanced Planner for Production Sprint

The planner will generate production-focused steps:

```python
def generate_production_sprint_plan(task, previous_sprint_context):
    """Generate execution plan for production readiness sprint"""
    
    # Base steps (same as MVP)
    base_steps = [
        {"step": 1, "agent": "product/product-owner.md", "phase": "plan"},
        {"step": 2, "agent": "project-management/scrum-master.md", "phase": "plan"},
        ...
    ]
    
    # Production-specific adjustments
    if sprint_type == "production-readiness":
        # Emphasize production concerns
        # Step 3: Staff Architect → focus on production architecture
        # Step 5: Backend → production configuration
        # Step 8: DevOps/SRE → production deployment (extended)
        # Step 9: QA → production-like testing
        # Step 10: AppSec → security hardening
        ...
    
    return execution_plan
```

---

## 7. Production-Focused Steps

### 7.1 Product Owner (Step 1)

**Production Focus:**
- Review production backlog items from previous sprint
- Prioritize production concerns
- Define production acceptance criteria
- Identify production risks

**Output:**
- Updated `BACKLOG.md` with production items prioritized
- Production acceptance criteria

### 7.2 Scrum Master (Step 2)

**Production Focus:**
- Plan production readiness sprint
- Identify production dependencies
- Define production DoD
- Assess production risks

**Output:**
- `SPRINT_PLAN.md` focused on production
- Production timeline and dependencies

### 7.3 Staff Architect (Step 3)

**Production Focus:**
- Production architecture review
- Scalability design
- High availability considerations
- Disaster recovery planning
- Production deployment architecture

**Output:**
- `docs/PRODUCTION_ARCHITECTURE.md`
- `docs/ADR-*-production.md`
- Scalability and HA design

### 7.4 DevOps/SRE (Step 8) - Extended

**Production Focus:**
- Production deployment configuration
- CI/CD pipeline for production
- Infrastructure as Code (IaC)
- Container orchestration (if applicable)
- Production environment setup
- Deployment automation
- Rollback procedures

**Output:**
- Production deployment configs
- CI/CD pipeline
- Infrastructure code
- Deployment runbooks

### 7.5 QA Strategist (Step 9) - Extended

**Production Focus:**
- Production-like testing
- Load testing
- Stress testing
- Chaos engineering (if applicable)
- Production test scenarios
- Performance testing

**Output:**
- Production test plans
- Load test results
- Performance benchmarks

### 7.6 AppSec Engineer (Step 10) - Extended

**Production Focus:**
- Production security hardening
- Security scanning for production
- Compliance validation
- Security monitoring setup
- Incident response planning

**Output:**
- Production security review
- Security hardening checklist
- Compliance documentation

---

## 8. Backlog Continuity

### 8.1 Extracting Production Items

The framework will automatically extract production-related items from previous sprint backlog:

```python
def extract_production_items(backlog_file):
    """Extract production-related items from backlog"""
    
    production_keywords = [
        "production", "deploy", "monitoring", "observability",
        "scaling", "performance", "ci/cd", "pipeline",
        "security", "hardening", "compliance", "disaster recovery"
    ]
    
    production_items = []
    
    # Parse backlog and find items with production keywords
    for story in backlog["stories"]:
        if any(keyword in story["description"].lower() 
               for keyword in production_keywords):
            production_items.append(story)
    
    return production_items
```

### 8.2 Backlog Integration

Production sprint will:
- Read previous sprint's `BACKLOG.md`
- Extract production-related items
- Create new backlog section: "Production Readiness Items"
- Maintain links to original stories

---

## 9. Example Workflow

### 9.1 MVP Sprint (Sprint 1)

```bash
# Sprint 1: MVP Development
python execution_runner.py --init
# Task: "Build face recognition access control system MVP"
# ... executes all 13 steps ...
# Closes with backlog items for production
```

**Backlog after Sprint 1:**
```markdown
### Backlog Items for Future
- Production deployment configuration
- CI/CD pipeline setup
- Monitoring and observability
- Security hardening
- Performance optimization
- Scaling preparation
```

### 9.2 Production Readiness Sprint (Sprint 2)

```bash
# Sprint 2: Production Readiness
python execution_runner.py --production-sprint

# Framework:
# - Detects previous sprint artifacts
# - Extracts production items from backlog
# - Creates production-focused plan
# - Preserves context

# Task: "Prepare face recognition access control system for production deployment"

# Executes steps with production focus:
# - Step 1: PO prioritizes production items
# - Step 2: Scrum Master plans production sprint
# - Step 3: Architect designs production architecture
# - Step 8: DevOps sets up production deployment
# - Step 9: QA runs production-like tests
# - Step 10: AppSec hardens security
# ...
```

---

## 10. Context Preservation

### 10.1 Previous Sprint Context

Production sprint maintains context from MVP sprint:

- **Architecture decisions:** References previous ADRs
- **Codebase:** Works with existing code
- **Backlog:** Continues from previous backlog
- **Artifacts:** References previous sprint artifacts
- **Learnings:** Incorporates sprint retrospective insights

### 10.2 Context Injection

During production sprint execution, agents receive:

```markdown
## Previous Sprint Context

**Sprint 1 (MVP):**
- Architecture: FastAPI-based REST API
- Key decisions: ADR-001 (framework choice)
- Completed features: Face recognition, access control
- Known limitations: [from sprint closure]
- Production backlog items: [extracted items]

**Current Sprint (Production Readiness):**
- Focus: Production deployment and operations
- Goal: Make MVP production-ready
- Timeline: [production sprint timeline]
```

---

## 11. Sprint Type Configuration

### 11.1 Manual Override

Users can explicitly specify sprint type:

```bash
python execution_runner.py --sprint-type production-readiness --task "..."
```

### 11.2 Automatic Detection

Planner automatically detects from task:

```bash
python execution_runner.py --task "Prepare system for production deployment"
# Detects: production-readiness
```

---

## 12. Integration with Multi-Sprint (v2.0)

This RFC prepares for v2.0 multi-sprint orchestration:

- Production sprint is a building block for multi-sprint
- Sprint chaining will use production sprint pattern
- Backlog continuity established
- Context preservation mechanism ready

---

## 13. Backward Compatibility

- Existing single-sprint MVP workflows unchanged
- Production sprint is **optional**
- Default sprint type remains `mvp`
- No breaking changes

---

## 14. Future Extensions (Non-Goals for v1.1)

Explicitly out of scope:

- Automatic sprint chaining (v2.0)
- Multi-sprint orchestration (v2.0)
- Sprint dependencies across sprints (v2.0)
- Sprint metrics aggregation (v2.0)

These will be addressed in v2.0 multi-sprint orchestration.

---

## 15. Acceptance Criteria

- [ ] `--production-sprint` command creates production readiness sprint
- [ ] Planner detects sprint type from task description
- [ ] Production items extracted from previous sprint backlog
- [ ] Context preserved from previous sprint
- [ ] Production-focused steps generated
- [ ] Backlog continuity maintained
- [ ] Documentation updated (Usage Guide, Scrum Guide)
- [ ] Backward compatibility maintained

---

## 16. Decision

**Status:** Proposed for v1.1

**Rationale:**

This RFC addresses a critical gap: the transition from MVP to production. Currently, this is manual and loses context. Production Readiness Sprint provides:

- Structured approach to production concerns
- Context preservation from MVP sprint
- Focused execution on production needs
- Foundation for v2.0 multi-sprint

**Next Steps:**

1. Review and approve RFC
2. Implement sprint type detection in planner
3. Implement `--production-sprint` command
4. Add production-focused step templates
5. Test with real MVP → Production transition
6. Release in v1.1

---

**See Also:**

- [Scrum Guide](../../guides/SCRUM_GUIDE.md) — Sprint methodology
- [Usage Guide](../../guides/USAGE_GUIDE.md) — General framework usage
- [Evolution Roadmap](../../roadmap/EVOLUTION_ROADMAP.md) — Technical roadmap (Multi-Sprint v2.0)
