# Release Checklist — Inteligens Agents Framework

> Generic release checklist. Update version numbers as needed for each release.

## Pre-flight

- [ ] README reviewed and accurate
- [ ] LICENSE present (MIT)
- [ ] .gitignore validated (runtime artifacts excluded)
- [ ] No runtime artifacts committed
  - [ ] No execution_state.json in repo
  - [ ] No execution_journal.md in repo
  - [ ] No execution_plan.json in repo (should be in .agents/swarm/ and gitignored)
  - [ ] No .agents/runtime/ files committed
- [ ] examples folder clean (only README/docs, no state files)
- [ ] Internal docs (docs/pt-br/) excluded from public release

## Functional Tests

### Router
- [ ] agent_router.py works
- [ ] Router generates valid JSON output
- [ ] Router handles --task parameter
- [ ] Router handles --product parameter (optional)
- [ ] Router handles --format json/md

### Planner
- [ ] swarm_planner.py works
- [ ] Planner generates execution_plan.json (default: .agents/swarm/execution_plan.json)
- [ ] Plan includes all required fields (task, execution_plan, generated)
- [ ] Plan structure is valid JSON

### Execution Runner
- [ ] execution_runner --init works
- [ ] execution_runner --next works
- [ ] execution_runner --done works
- [ ] execution_runner --approve works (NEW - Approval Gates)
- [ ] Journal updates correctly on all commands
- [ ] State file persists correctly
- [ ] Approval flow works end-to-end:
  - [ ] Step with requires_approval blocks --next until approved
  - [ ] --done on gated step doesn't advance current_step
  - [ ] --approve advances current_step and unlocks progression
  - [ ] Approval events recorded in journal

## Documentation

- [ ] README.md complete and accurate
- [ ] USAGE_GUIDE.md includes Approval Flow section
- [ ] PUBLIC_ROADMAP.md reflects v1.0 features
- [ ] EVOLUTION_ROADMAP.md accurate
- [ ] RFC-001-approval-gates.md present
- [ ] APPROVAL_GATES.md architecture doc present
- [ ] All public docs in English
- [ ] Internal docs (pt-br) excluded from release

## Quality

- [ ] Version bumped in .agents/version.py (1.0.0)
- [ ] CHANGELOG.md updated with all v1.0.0 features
- [ ] No linter errors
- [ ] Code follows project conventions
- [ ] All critical paths tested manually

## Pre-Release

- [ ] All checkboxes above verified
- [ ] Final code review completed
- [ ] Documentation reviewed
- [ ] Examples tested (if applicable)

## Publish

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial stable release with Approval Gates"

# Push tag
git push origin v1.0.0

# Optional: Create GitHub release with CHANGELOG notes
```

---

**Release only when all boxes are checked.**

## Post-Release

- [ ] Update version badge in README (if needed)
- [ ] Announce release (if applicable)
- [ ] Monitor for issues
