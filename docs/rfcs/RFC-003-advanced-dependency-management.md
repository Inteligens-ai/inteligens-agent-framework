# RFC-003 — Advanced Dependency Management

**Status:** Proposed  
**Author:** Inteligens  
**Target Version:** v1.2  
**Last Updated:** 2026-03-02

---

## 1. Summary

This RFC extends RFC-002 with **advanced dependency management features** that provide intelligent assistance, automatic planning reviews, workaround suggestions, blocking metrics, and proactive dependency resolution.

While RFC-002 provides the foundation (blocking states, dependency tracking, basic navigation), this RFC adds:
- Automatic planning review triggers (PO + Scrum Master)
- Intelligent workaround suggestions
- Blocking metrics and analytics
- Circular dependency detection
- Step reordering suggestions
- Automatic backlog integration

---

## 2. Motivation

**Problem Statement:**

RFC-002 solves the basic problem of tracking dependencies, but real-world scenarios need more:

1. **Planning Impact**: When steps are blocked, the sprint plan and backlog may need updates. Currently, this is manual.
2. **Workaround Discovery**: Teams often use workarounds (mocks, stubs, contracts) but the framework doesn't suggest them.
3. **Visibility**: No metrics on blocking patterns, average blocking time, or dependency chains.
4. **Proactive Resolution**: Framework doesn't suggest reordering steps or breaking dependency chains.
5. **Integration**: Blocking information doesn't automatically flow to backlog/sprint plan.

**Solution:**

Add intelligent assistance layer that:
- Automatically triggers planning reviews when blocks occur
- Suggests technical workarounds based on agent types
- Provides blocking metrics and analytics
- Detects and warns about circular dependencies
- Suggests step reordering to optimize execution
- Integrates with backlog/sprint plan (suggestions or automatic)

---

## 3. Design Principles

The feature MUST:

- remain CLI-friendly
- preserve human-in-the-loop control
- provide suggestions, not enforcements
- maintain full observability
- be backward compatible with RFC-002
- work with existing execution model

The feature MUST NOT:

- automatically modify execution plans without human approval
- require external services
- introduce background processes
- force workaround implementation

---

## 4. Features

### 4.1 Automatic Planning Review Trigger

When a step is marked as `partial` or `blocked`, automatically suggest a planning review.

**Behavior:**

```bash
python execution_runner.py --done --partial --blocked-by 7 --reason "Need AI service interface"

# Framework output:
# ⚠️  Step 5 marked as partial (blocked by Step 7)
# 📋 Planning review suggested:
#    Blocking may impact sprint plan and backlog.
#    Run: python execution_runner.py --review-planning
```

**New Command: `--review-planning`**

```bash
python execution_runner.py --review-planning
```

Creates a temporary execution plan with:
- Step 1: Product Owner (review product impact, update backlog)
- Step 2: Scrum Master (update sprint plan, assess risks)

Provides context:
- List of all blocked/partial steps
- Blocking reasons
- Dependency chains
- Suggested backlog updates

**Implementation:**

```python
def cmd_review_planning():
    """Create temporary plan for PO + Scrum Master review"""
    state = load_json(STATE_FILE)
    blocked_steps = state.get("blocked_steps", {})
    
    if not blocked_steps:
        print("✅ No blocked steps. Planning review not needed.")
        return
    
    # Create temporary plan
    review_plan = {
        "generated": datetime.now(UTC).isoformat(),
        "swarm_version": "7.3.0",
        "task": "Review and update planning artifacts due to blocking dependencies",
        "execution_plan": [
            {
                "step": 1,
                "agent": "product/product-owner.md",
                "phase": "plan",
                "context": {
                    "blocked_steps": blocked_steps,
                    "action": "Review product impact and update BACKLOG.md"
                }
            },
            {
                "step": 2,
                "agent": "project-management/scrum-master.md",
                "phase": "plan",
                "context": {
                    "blocked_steps": blocked_steps,
                    "action": "Update SPRINT_PLAN.md and assess risks"
                }
            }
        ]
    }
    
    # Save temporary plan
    review_plan_path = ".agents/swarm/review_planning_plan.json"
    save_json(review_plan_path, review_plan)
    
    print("📋 Planning review plan created:")
    print(f"   Plan: {review_plan_path}")
    print("   Steps: Product Owner → Scrum Master")
    print("   Run: python execution_runner.py --init {review_plan_path}")
```

---

### 4.2 Intelligent Workaround Suggestions

When a step is blocked, suggest technical workarounds based on agent types and dependency patterns.

**Behavior:**

```bash
python execution_runner.py --done --partial --blocked-by 7 --reason "Need AI service interface"

# Framework output:
# ⚠️  Step 5 marked as partial (blocked by Step 7)
# 💡 Suggested workarounds:
#    - Create mock AI service interface
#    - Define interface contract (OpenAPI/Protocol Buffers)
#    - Implement stub service for local development
# 
# Consider implementing workaround to unblock progress
```

**Workaround Database:**

```python
WORKAROUND_SUGGESTIONS = {
    "engineering/backend-engineer.md": {
        "engineering/ai-engineer.md": [
            "Create mock AI service interface",
            "Define interface contract (OpenAPI/Protocol Buffers)",
            "Implement stub service for local development",
            "Use dependency injection to abstract AI service"
        ],
        "engineering/frontend-engineer.md": [
            "Create API contract first (OpenAPI spec)",
            "Use mock API server (JSON Server, MSW)",
            "Define interface contracts and share with frontend"
        ]
    },
    "engineering/frontend-engineer.md": {
        "engineering/backend-engineer.md": [
            "Use mock API responses",
            "Create static JSON fixtures",
            "Use API mocking tools (MSW, MirageJS)",
            "Work with API contract (OpenAPI spec)"
        ]
    },
    "testing/qa-strategist.md": {
        "engineering/backend-engineer.md": [
            "Create test doubles (mocks, stubs)",
            "Use contract testing (Pact, Spring Cloud Contract)",
            "Test against API contracts"
        ]
    }
}
```

**Implementation:**

```python
def suggest_workarounds(step_agent, blocked_by_agents, plan):
    """Suggest workarounds based on agent types"""
    suggestions = []
    
    for blocked_by_step_num in blocked_by_agents:
        blocked_by_step = find_step(plan, blocked_by_step_num)
        blocked_by_agent = blocked_by_step.get("agent", "")
        
        agent_workarounds = WORKAROUND_SUGGESTIONS.get(step_agent, {})
        workarounds = agent_workarounds.get(blocked_by_agent, [])
        
        suggestions.extend(workarounds)
    
    if suggestions:
        print("💡 Suggested workarounds:")
        for suggestion in set(suggestions):  # Remove duplicates
            print(f"   - {suggestion}")
        print("\nConsider implementing workaround to unblock progress")
    
    return suggestions
```

---

### 4.3 Blocking Metrics and Analytics

Track and display metrics about blocking patterns.

**New Command: `--metrics`**

```bash
python execution_runner.py --metrics
```

**Output:**

```
📊 Execution Metrics:

Blocking Statistics:
  Total blocked steps: 2
  Partial: 1
  Blocked: 1
  Blocking ratio: 15.4% (2/13 steps)

Time Metrics:
  Average blocking time: 2h 15m
  Longest block: Step 5 (3h 30m)
  Total blocking time: 4h 45m

Dependency Analysis:
  Most common dependency: Step 7 (blocked by 2 steps)
  Blocking chains detected: 1
    Chain: Step 5 → Step 7 → Step 9

Step Status:
  Completed: 3
  In Progress: 1
  Partial: 1
  Blocked: 1
  Pending: 7
```

**Implementation:**

```python
def get_blocking_metrics(state, plan):
    """Calculate blocking metrics"""
    blocked_steps = state.get("blocked_steps", {})
    step_statuses = state.get("step_statuses", {})
    
    total_steps = len(plan)
    total_blocked = len(blocked_steps)
    partial_count = sum(1 for s in blocked_steps.values() if s["status"] == "partial")
    blocked_count = sum(1 for s in blocked_steps.values() if s["status"] == "blocked")
    
    # Calculate blocking times
    now = datetime.now(UTC)
    blocking_times = []
    for step_num, step_data in blocked_steps.items():
        completed_at = datetime.fromisoformat(step_data["completed_at"])
        blocking_time = now - completed_at
        blocking_times.append(blocking_time)
    
    avg_blocking_time = sum(blocking_times, timedelta(0)) / len(blocking_times) if blocking_times else timedelta(0)
    
    # Find most common dependency
    dependency_counts = {}
    for step_data in blocked_steps.values():
        for dep in step_data.get("blocked_by", []):
            dependency_counts[dep] = dependency_counts.get(dep, 0) + 1
    
    most_common_dep = max(dependency_counts.items(), key=lambda x: x[1])[0] if dependency_counts else None
    
    # Detect blocking chains
    blocking_chains = detect_blocking_chains(blocked_steps, plan)
    
    return {
        "total_blocked": total_blocked,
        "partial_count": partial_count,
        "blocked_count": blocked_count,
        "blocking_ratio": total_blocked / total_steps if total_steps > 0 else 0,
        "avg_blocking_time": avg_blocking_time,
        "longest_block": max(blocking_times) if blocking_times else timedelta(0),
        "total_blocking_time": sum(blocking_times, timedelta(0)),
        "most_common_dependency": most_common_dep,
        "blocking_chains": blocking_chains,
        "step_statuses": step_statuses
    }

def cmd_metrics():
    """Display execution metrics"""
    state = load_json(STATE_FILE)
    plan_file = load_json(".agents/swarm/execution_plan.json")
    plan = plan_file.get("execution_plan", [])
    
    metrics = get_blocking_metrics(state, plan)
    
    # Format and display
    print("📊 Execution Metrics:\n")
    print("Blocking Statistics:")
    print(f"  Total blocked steps: {metrics['total_blocked']}")
    print(f"  Partial: {metrics['partial_count']}")
    print(f"  Blocked: {metrics['blocked_count']}")
    print(f"  Blocking ratio: {metrics['blocking_ratio']:.1%} ({metrics['total_blocked']}/{len(plan)} steps)")
    # ... rest of output
```

---

### 4.4 Circular Dependency Detection

Detect and warn about circular dependencies that would cause deadlocks.

**Behavior:**

```bash
python execution_runner.py --next
# ⚠️  Circular dependencies detected:
#    Step 5 → Step 7 → Step 5
#    This will cause deadlock. Consider reordering steps.
```

**Implementation:**

```python
def detect_circular_dependencies(plan):
    """Detect circular dependencies using DFS"""
    graph = {}
    for step in plan:
        graph[step["step"]] = step.get("dependencies", [])
    
    cycles = []
    visited = set()
    rec_stack = set()
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, path):
                    return True
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
                return True
        
        rec_stack.remove(node)
        path.pop()
        return False
    
    for node in graph:
        if node not in visited:
            dfs(node, [])
    
    return cycles

def warn_circular_dependencies(plan):
    """Warn about circular dependencies"""
    cycles = detect_circular_dependencies(plan)
    
    if cycles:
        print("⚠️  Circular dependencies detected:")
        for cycle in cycles:
            print(f"   {' → '.join(map(str, cycle))}")
        print("   This will cause deadlock. Consider reordering steps.")
        return True
    
    return False
```

---

### 4.5 Step Reordering Suggestions

Suggest optimal step ordering based on dependencies.

**New Command: `--suggest-reorder`**

```bash
python execution_runner.py --suggest-reorder
```

**Output:**

```
💡 Suggested step reordering to resolve dependencies:

Current order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Suggested order: [1, 2, 3, 4, 7, 5, 6, 8, 9, 10, 11, 12, 13]

Changes:
  - Step 7 moved before Step 5 (resolves dependency)
  - This would eliminate 1 blocking dependency

To apply: python execution_runner.py --reorder
```

**Implementation:**

```python
def suggest_step_reordering(plan):
    """Suggest reordering using topological sort"""
    # Build dependency graph
    graph = {step["step"]: step.get("dependencies", []) for step in plan}
    
    # Topological sort
    in_degree = {step["step"]: 0 for step in plan}
    for step in plan:
        for dep in step.get("dependencies", []):
            in_degree[step["step"]] += 1
    
    queue = [step["step"] for step in plan if in_degree[step["step"]] == 0]
    reordered = []
    
    while queue:
        node = queue.pop(0)
        reordered.append(node)
        
        for step in plan:
            if node in step.get("dependencies", []):
                in_degree[step["step"]] -= 1
                if in_degree[step["step"]] == 0:
                    queue.append(step["step"])
    
    current_order = [step["step"] for step in plan]
    
    if reordered != current_order:
        return reordered
    
    return None
```

---

### 4.6 Backlog Integration (Suggestions)

Suggest backlog updates when blocks occur (optional automatic updates).

**Behavior:**

```bash
python execution_runner.py --done --partial --blocked-by 7 --reason "Need AI service interface"

# Framework output:
# 📝 Backlog update suggested:
#    Consider adding story to BACKLOG.md:
#    - ID: US-BLOCK-5
#    - Title: Resolve blocking dependency for Step 5
#    - Description: Need AI service interface from Step 7
#    - Dependencies: Step 7
#    - Priority: High
#    
#    Run: python execution_runner.py --update-backlog-suggestion
```

**New Command: `--update-backlog-suggestion`**

Generates a markdown snippet that can be added to `BACKLOG.md`:

```markdown
### US-BLOCK-5: Resolve Blocking Dependency for Step 5

**Description:** Step 5 (Backend Engineer) is blocked waiting for AI service interface definition from Step 7 (AI Engineer).

**Acceptance Criteria:**
- [ ] Step 7 is completed
- [ ] AI service interface is defined
- [ ] Step 5 can proceed with implementation
- [ ] Dependencies are resolved

**Priority:** High  
**Dependencies:** Step 7  
**Status:** Blocked
```

---

## 5. Integration with RFC-002

This RFC extends RFC-002:

- **RFC-002** provides: blocking states, dependency tracking, basic navigation
- **RFC-003** adds: intelligent assistance, automatic reviews, metrics, workarounds

Both work together:
1. RFC-002 commands (`--block`, `--done --partial`, `--resolve`) trigger RFC-003 features
2. RFC-003 features enhance RFC-002 workflows
3. All features maintain backward compatibility

---

## 6. Example Complete Workflow

```bash
# Step 5: Backend identifies dependency
python execution_runner.py --next    # Step 5
# ... agent works ...
python execution_runner.py --done --partial --blocked-by 7 --reason "Need AI service interface"

# Framework provides:
# ⚠️  Step 5 marked as partial (blocked by Step 7)
# 💡 Suggested workarounds:
#    - Create mock AI service interface
#    - Define interface contract (OpenAPI)
# 📋 Planning review suggested. Run: --review-planning
# 📝 Backlog update suggested. Run: --update-backlog-suggestion

# Review planning
python execution_runner.py --review-planning
# ... PO and Scrum Master review and update artifacts ...

# Check metrics
python execution_runner.py --metrics
# Shows blocking statistics

# Continue to Step 7
python execution_runner.py --next    # Step 7
# ... complete Step 7 ...
python execution_runner.py --done

# Resolve dependencies
python execution_runner.py --resolve 5
# Step 5 dependencies resolved

# Return to Step 5
python execution_runner.py --back 5
# ... complete remaining work ...
python execution_runner.py --done
```

---

## 7. Backward Compatibility

- All features are **optional** and **additive**
- Existing workflows continue to work
- New commands don't interfere with existing commands
- Metrics and suggestions are informational only

---

## 8. Future Extensions (Non-Goals for v1.2)

Explicitly out of scope:

- Automatic backlog file modification (only suggestions)
- Automatic step reordering (only suggestions)
- Automatic workaround implementation
- Real-time blocking notifications
- Integration with external project management tools

These may be considered for v2.0+.

---

## 9. Acceptance Criteria

- [ ] `--review-planning` command creates temporary plan with PO + Scrum Master
- [ ] Workaround suggestions appear when steps are blocked
- [ ] `--metrics` command displays blocking statistics
- [ ] Circular dependency detection warns about deadlocks
- [ ] `--suggest-reorder` provides optimal step ordering
- [ ] `--update-backlog-suggestion` generates backlog snippets
- [ ] All features integrate seamlessly with RFC-002
- [ ] Documentation updated (Usage Guide, Roadmap)
- [ ] Backward compatibility maintained

---

## 10. Decision

**Status:** Proposed for v1.2

**Rationale:**

RFC-002 provides the foundation for dependency management. RFC-003 adds intelligent assistance that makes the system more useful in real-world scenarios:

- Automatic planning reviews align with Scrum practices
- Workaround suggestions help teams unblock faster
- Metrics provide visibility into blocking patterns
- Reordering suggestions optimize execution flow

These features enhance RFC-002 without breaking changes.

**Next Steps:**

1. Review and approve RFC
2. Implement after RFC-002 is complete
3. Test with real-world scenarios
4. Release in v1.2

---

**See Also:**

- [RFC-002: Step Dependencies](RFC-002-step-dependencies.md) — Foundation
- [Usage Guide](../../guides/USAGE_GUIDE.md) — User-facing documentation
- [Evolution Roadmap](../../roadmap/EVOLUTION_ROADMAP.md) — Technical roadmap
