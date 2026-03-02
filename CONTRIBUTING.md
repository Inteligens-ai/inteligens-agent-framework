# Contributing to Inteligens Agents Framework

Thank you for your interest in improving the Inteligens Agents Framework.

---

## 🌿 Branch Workflow

The project follows a **Git Flow**-inspired branching strategy:

```
main (production)
  ↑
develop (integration)
  ↑
feature/* | fix/* | release/*
```

### Branch Types

#### `main`
- **Purpose:** Production-ready code
- **Protection:** Only merges from `develop` or `release/*`
- **Tags:** All releases are tagged here (e.g., `v1.0.0`, `v1.1.0`)
- **Status:** Always stable and deployable

#### `develop`
- **Purpose:** Integration branch for ongoing development
- **Protection:** Requires pull request review
- **Source:** All feature branches merge here
- **Status:** Should be stable but may contain WIP features

#### `feature/*`
- **Purpose:** New features or enhancements
- **Naming:** `feature/description` (e.g., `feature/approval-gates`, `feature/skip-command`)
- **Source:** Branch from `develop`
- **Merge:** Pull request to `develop`
- **Delete:** After merge

#### `fix/*`
- **Purpose:** Bug fixes
- **Naming:** `fix/description` (e.g., `fix/execution-runner-prompt`, `fix/missing-dependency`)
- **Source:** Branch from `develop` (or `main` for hotfixes)
- **Merge:** Pull request to `develop`
- **Delete:** After merge

#### `release/*`
- **Purpose:** Prepare new release
- **Naming:** `release/v1.x.x` (e.g., `release/v1.1.0`)
- **Source:** Branch from `develop`
- **Merge:** Pull request to both `develop` and `main`
- **Status:** Only bug fixes, no new features
- **Delete:** After merge and tag

#### `hotfix/*`
- **Purpose:** Critical production fixes
- **Naming:** `hotfix/description` (e.g., `hotfix/security-patch`)
- **Source:** Branch from `main`
- **Merge:** Pull request to both `main` and `develop`
- **Delete:** After merge

---

## 🔄 Workflow Steps

### Starting a New Feature

```bash
# 1. Ensure develop is up to date
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/my-new-feature

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 4. Push and create pull request
git push origin feature/my-new-feature
```

### Fixing a Bug

```bash
# 1. Ensure develop is up to date
git checkout develop
git pull origin develop

# 2. Create fix branch
git checkout -b fix/bug-description

# 3. Fix and commit
git add .
git commit -m "fix: resolve bug description"

# 4. Push and create pull request
git push origin fix/bug-description
```

### Preparing a Release

```bash
# 1. Ensure develop is ready
git checkout develop
git pull origin develop

# 2. Create release branch
git checkout -b release/v1.1.0

# 3. Update version numbers, CHANGELOG.md
# 4. Only bug fixes, no new features
# 5. Test thoroughly

# 6. Merge to main and tag
git checkout main
git merge release/v1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags

# 7. Merge back to develop
git checkout develop
git merge release/v1.1.0
git push origin develop

# 8. Delete release branch
git branch -d release/v1.1.0
git push origin --delete release/v1.1.0
```

---

## 📝 Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, config, etc.)

### Examples

```bash
feat(execution-runner): add --skip command

Allows skipping non-applicable steps during execution.
Useful for backend-only projects that don't need frontend steps.

Closes #123

---

fix(planner): correct requires_approval logic

Fixed issue where approval gates were not properly marked
in generated execution plans.

Fixes #456

---

docs(guides): add language-specific setup guide

Added comprehensive guide for Python, Node.js, Go, Rust, Java, C#
with dependency management and best practices.

---

chore(deps): update pytest to 7.4.0
```

### Scope (Optional)

- `execution-runner`
- `swarm-planner`
- `agent-router`
- `docs`
- `examples`
- `tests`

---

## 🔧 Pull Request Process

### Before Submitting

- [ ] Code builds and runs locally
- [ ] Tests pass (if applicable)
- [ ] No secrets or sensitive data committed
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow convention
- [ ] Branch is up to date with target branch

### PR Title Format

```
<type>(<scope>): <description>
```

Examples:
- `feat(execution-runner): add --skip command`
- `fix(planner): correct approval gate logic`
- `docs(guides): add Scrum guide`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (describe)

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated (if applicable)
```

### Review Process

1. **Automated Checks:** CI/CD runs tests and linting
2. **Code Review:** At least one maintainer approval required
3. **Discussion:** Address review comments
4. **Merge:** Squash and merge (preferred) or merge commit

---

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

### Release Checklist

1. **Create release branch** from `develop`
   ```bash
   git checkout -b release/v1.1.0 develop
   ```

2. **Update version numbers**
   - Update `README.md` badge
   - Update `CHANGELOG.md` with new version
   - Update any version references in code

3. **Final testing**
   - Run all tests
   - Test example projects
   - Verify documentation

4. **Merge to main**
   ```bash
   git checkout main
   git merge release/v1.1.0
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin main --tags
   ```

5. **Merge back to develop**
   ```bash
   git checkout develop
   git merge release/v1.1.0
   git push origin develop
   ```

6. **Create GitHub Release**
   - Use tag `v1.1.0`
   - Copy relevant section from `CHANGELOG.md`
   - Attach any release artifacts

7. **Cleanup**
   ```bash
   git branch -d release/v1.1.0
   git push origin --delete release/v1.1.0
   ```

---

## 🐛 Issues

### Reporting Bugs

Use clear, reproducible descriptions:

- **Title:** Brief summary
- **Description:** Steps to reproduce, expected vs actual behavior
- **Environment:** OS, Python version, framework version
- **Logs:** Include relevant error messages or stack traces
- **Labels:** Use `bug` label

### Feature Requests

- **Title:** Clear feature description
- **Description:** Use case, benefits, potential implementation
- **Labels:** Use `enhancement` label

---

## 🧭 Development Setup

### Prerequisites

- Python 3.10+
- Git
- (Optional) Virtual environment

### Setup

```bash
# Clone repository
git clone <repo-url>
cd inteligens-agent-framework

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if any)
pip install -r requirements.txt

# Test framework
python .agents/swarm/swarm_planner.py --task "test"
```

---

## 📚 Documentation

### When to Update Documentation

- New features require usage documentation
- API changes require reference updates
- Workflow changes require guide updates
- Examples should be kept up to date

### Documentation Structure

- `README.md` - Project overview and quick start
- `docs/guides/` - User guides (Usage, Language-Specific, Scrum)
- `docs/architecture/` - Architecture documentation
- `docs/roadmap/` - Roadmap and evolution plans
- `CHANGELOG.md` - Version history

---

## 🧭 Philosophy

This project values:

- **Human-in-the-loop safety** - Humans remain in control
- **Deterministic execution** - Predictable behavior
- **Clear agent responsibilities** - Each agent has a defined role
- **Production realism** - Focus on real-world use cases
- **Governance first** - Safety over speed

---

## ❓ Questions?

- Open an issue for bugs or feature requests
- Check existing documentation first
- Review closed issues for similar questions

---

**Thank you for contributing!** 🎉
