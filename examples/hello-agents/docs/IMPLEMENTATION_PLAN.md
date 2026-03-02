# Implementation Plan — Simple REST API

**Tech Lead:** engineering/tech-lead.md  
**Date:** 2026-03-02  
**Phase:** design  
**Status:** Ready for Implementation

---

## Overview

This document provides an actionable implementation plan for building the REST API based on the architecture defined in [ARCHITECTURE.md](./ARCHITECTURE.md) and the framework decision in [ADR-001](./ADR-001-framework-choice.md).

**Framework:** FastAPI  
**Target:** MVP with three health check endpoints  
**Scope:** Minimal, shippable implementation

---

## Implementation Tasks

### Task 1: Project Setup & Dependencies
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-006 (Project Dependencies)  
**Estimate:** 1 point

**Actions:**
1. Create `requirements.txt` with:
   - `fastapi>=0.104.0`
   - `uvicorn[standard]>=0.24.0`
   - `pytest>=7.4.0`
   - `pytest-asyncio>=0.21.0` (optional, for async support)
2. Create `.gitignore` file (US-008):
   - Python cache: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`
   - Virtual environments: `venv/`, `env/`, `.venv/`
   - IDE files: `.vscode/`, `.idea/`, `*.swp`
   - OS files: `.DS_Store`, `Thumbs.db`
   - Test artifacts: `.pytest_cache/`, `.coverage`, `htmlcov/`
   - Distribution: `dist/`, `build/`, `*.egg-info/`

**Acceptance Criteria:**
- [ ] requirements.txt includes all necessary dependencies
- [ ] Version pins are explicit (no `>=` without upper bound for MVP)
- [ ] .gitignore excludes all appropriate files
- [ ] Files are properly formatted

**Deliverables:**
- `requirements.txt`
- `.gitignore`

---

### Task 2: FastAPI Application Structure
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-004 (API Framework Setup)  
**Estimate:** 2 points (partially)

**Actions:**
1. Create `main.py` with:
   - FastAPI application instance
   - Import statements for FastAPI and Pydantic
   - Basic application configuration
2. Set up response models using Pydantic:
   - `StatusResponse` model for `/` and `/health`
   - `VersionResponse` model for `/version`
3. Configure version from environment variable:
   - Default to "1.0.0" if not set
   - Use `os.getenv("API_VERSION", "1.0.0")`

**Code Structure:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Hello Agents API", version="1.0.0")

class StatusResponse(BaseModel):
    status: str

class VersionResponse(BaseModel):
    version: str

API_VERSION = os.getenv("API_VERSION", "1.0.0")
```

**Acceptance Criteria:**
- [ ] FastAPI application properly initialized
- [ ] Response models defined with Pydantic
- [ ] Version is configurable via environment variable
- [ ] Code follows FastAPI best practices

**Deliverables:**
- `main.py` (partial - endpoints added in Task 3)

---

### Task 3: Implement Root Endpoint (GET /)
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-001 (Root Endpoint)  
**Estimate:** 1 point

**Actions:**
1. Add route handler for `GET /`
2. Return `{"status": "ok"}` with HTTP 200
3. Use `StatusResponse` model for response

**Implementation:**
```python
@app.get("/", response_model=StatusResponse)
def root():
    return StatusResponse(status="ok")
```

**Acceptance Criteria:**
- [ ] GET / returns HTTP 200
- [ ] Response body is JSON: `{"status": "ok"}`
- [ ] Response time < 100ms (target)
- [ ] No authentication required
- [ ] Uses Pydantic response model

**Deliverables:**
- Updated `main.py` with root endpoint

---

### Task 4: Implement Health Check Endpoint (GET /health)
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-002 (Health Check Endpoint)  
**Estimate:** 1 point

**Actions:**
1. Add route handler for `GET /health`
2. Return `{"status": "healthy"}` with HTTP 200
3. Use `StatusResponse` model for response

**Implementation:**
```python
@app.get("/health", response_model=StatusResponse)
def health():
    return StatusResponse(status="healthy")
```

**Acceptance Criteria:**
- [ ] GET /health returns HTTP 200
- [ ] Response body is JSON: `{"status": "healthy"}`
- [ ] Response time < 50ms (target)
- [ ] No authentication required
- [ ] Uses Pydantic response model

**Deliverables:**
- Updated `main.py` with health endpoint

---

### Task 5: Implement Version Endpoint (GET /version)
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-003 (Version Endpoint)  
**Estimate:** 1 point

**Actions:**
1. Add route handler for `GET /version`
2. Return `{"version": "1.0.0"}` (or configured version) with HTTP 200
3. Use `VersionResponse` model for response
4. Use `API_VERSION` constant from environment

**Implementation:**
```python
@app.get("/version", response_model=VersionResponse)
def version():
    return VersionResponse(version=API_VERSION)
```

**Acceptance Criteria:**
- [ ] GET /version returns HTTP 200
- [ ] Response body is JSON: `{"version": "1.0.0"}` (or configured value)
- [ ] Version is configurable (not hardcoded)
- [ ] Response time < 50ms (target)
- [ ] Uses Pydantic response model

**Deliverables:**
- Updated `main.py` with version endpoint

---

### Task 6: Project Documentation (README.md)
**Owner:** `engineering/backend-engineer.md`  
**Story:** US-007 (Project Documentation)  
**Estimate:** 1 point

**Actions:**
1. Create/update `README.md` with:
   - Project description
   - Installation steps (pip install -r requirements.txt)
   - How to run the API (uvicorn main:app --reload)
   - How to run tests (pytest)
   - Endpoint documentation (all three endpoints)
   - Environment variables (API_VERSION)

**Content Sections:**
- Project Overview
- Requirements
- Installation
- Running the API
- Running Tests
- API Endpoints
- Configuration

**Acceptance Criteria:**
- [ ] README.md includes project description
- [ ] README.md includes installation steps
- [ ] README.md includes how to run the API
- [ ] README.md includes how to run tests
- [ ] README.md includes endpoint documentation

**Deliverables:**
- `README.md`

---

## Technical Standards

### Code Quality Standards

#### Python Style
- Follow PEP 8 style guide
- Use type hints for function parameters and return types
- Maximum line length: 100 characters (relaxed from 79 for readability)
- Use descriptive variable and function names

#### FastAPI Best Practices
- Use Pydantic models for request/response validation
- Use `response_model` parameter in route decorators
- Keep route handlers simple and focused
- Use dependency injection for shared resources (if needed)

#### Code Organization
- Single-file structure for MVP (`main.py`)
- Clear separation: imports, models, configuration, routes
- Group related code together
- Add docstrings for functions (optional for MVP, but recommended)

#### Error Handling
- Let FastAPI handle default errors (500, 404, etc.)
- No custom error handlers for MVP
- Ensure endpoints return proper HTTP status codes

### Testing Standards

#### Test Structure
- Tests in `tests/test_main.py`
- Use FastAPI `TestClient` for integration tests
- One test file per module (main.py → test_main.py)

#### Test Coverage
- Target: ≥ 80% code coverage
- All endpoints must have tests
- Test both success cases and edge cases
- Verify status codes and response bodies

#### Test Naming
- Use descriptive test names: `test_root_endpoint_returns_ok`
- Follow pattern: `test_<endpoint>_<scenario>`
- Group related tests in classes (optional)

#### Test Implementation Example
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["version"] == "1.0.0"  # or configured value
```

### Documentation Standards

#### Code Documentation
- Docstrings for functions (optional for MVP)
- Type hints for all function signatures
- Clear variable names (self-documenting code)

#### README Documentation
- Clear, concise language
- Step-by-step instructions
- Code examples for common operations
- Environment variable documentation

### Version Control Standards

#### Git Practices
- Commit messages: Clear, descriptive
- One logical change per commit
- No secrets or sensitive data
- .gitignore properly configured

---

## Implementation Order

**Recommended Sequence:**

1. **Task 1:** Project Setup (requirements.txt, .gitignore)
   - Foundation for all other work
   - Can be done in parallel with Task 2

2. **Task 2:** FastAPI Application Structure
   - Sets up the framework
   - Defines response models
   - Prerequisite for endpoint implementation

3. **Task 3, 4, 5:** Implement Endpoints (can be done in any order)
   - Root endpoint (GET /)
   - Health endpoint (GET /health)
   - Version endpoint (GET /version)

4. **Task 6:** Documentation (README.md)
   - Written after implementation is complete
   - Documents the working system

**Dependencies:**
- Tasks 3-5 depend on Task 2 (application structure)
- Task 6 depends on Tasks 1-5 (complete implementation)

---

## Risks & Mitigations

### Risk 1: FastAPI Learning Curve
**Description:** Developer may be unfamiliar with FastAPI patterns  
**Impact:** Medium  
**Probability:** Low  
**Mitigation:**
- Clear code examples in implementation plan
- Architecture document provides guidance
- FastAPI has excellent documentation
- Simple use case (3 endpoints, no complex features)

### Risk 2: Environment Variable Configuration
**Description:** Version endpoint requires environment variable handling  
**Impact:** Low  
**Probability:** Low  
**Mitigation:**
- Simple `os.getenv()` with default value
- Well-documented in architecture and implementation plan
- Standard Python pattern

### Risk 3: Test Coverage Target (80%)
**Description:** May be challenging to achieve 80% coverage  
**Impact:** Low  
**Probability:** Low  
**Mitigation:**
- Simple codebase (3 endpoints, minimal logic)
- Clear test examples provided
- Coverage tools available (pytest-cov)
- Can adjust target if needed (but should be achievable)

### Risk 4: Response Time Targets
**Description:** Performance targets (< 100ms, < 50ms) may not be met  
**Impact:** Low  
**Probability:** Very Low  
**Mitigation:**
- FastAPI is high-performance framework
- Simple endpoints with no external dependencies
- Targets are conservative
- Performance testing can be added if needed

### Risk 5: Over-engineering
**Description:** May add unnecessary complexity beyond MVP scope  
**Impact:** Medium  
**Probability:** Low  
**Mitigation:**
- Clear scope definition in backlog
- Architecture emphasizes simplicity
- Implementation plan focuses on MVP
- Code review will catch over-engineering

---

## Validation Checklist

Before marking implementation as complete, verify:

- [ ] All three endpoints implemented and working
- [ ] All endpoints return correct HTTP status codes (200)
- [ ] All endpoints return correct JSON responses
- [ ] Response models use Pydantic
- [ ] Version is configurable via environment variable
- [ ] requirements.txt includes all dependencies
- [ ] .gitignore excludes appropriate files
- [ ] README.md is complete and accurate
- [ ] Code follows technical standards
- [ ] No hardcoded secrets or sensitive data
- [ ] All code is in `examples/hello-agents/` directory

---

## Testing Requirements

### Unit Tests
- [ ] Test for GET / endpoint
- [ ] Test for GET /health endpoint
- [ ] Test for GET /version endpoint
- [ ] Test version endpoint with different API_VERSION values
- [ ] All tests pass

### Test Execution
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=main --cov-report=html

# Verify coverage ≥ 80%
```

**Note:** Full test suite will be implemented by QA Strategist in Step 9, but basic tests should be created during implementation.

---

## Handoff to Backend Engineer

### Inputs Provided
- ✅ Architecture design (ARCHITECTURE.md)
- ✅ Framework decision (ADR-001)
- ✅ Implementation plan (this document)
- ✅ Technical standards defined
- ✅ Risks identified and mitigated

### Expected Outputs
- ✅ Working FastAPI application
- ✅ Three endpoints implemented
- ✅ requirements.txt and .gitignore
- ✅ README.md documentation
- ✅ Basic test structure (full suite in Step 9)

### Success Criteria
- All tasks completed according to acceptance criteria
- Code follows technical standards
- Ready for QA testing (Step 9)
- No blocking issues

---

## Next Steps

1. **Backend Engineer (Step 5):** Implement all tasks in this plan
2. **QA Strategist (Step 9):** Expand test suite and validate coverage
3. **AppSec Engineer (Step 10):** Security review (approval gate)

---

**Status:** ✅ Ready for Implementation  
**Plan Version:** 1.0  
**Last Updated:** 2026-03-02
