# Hello Agents API

A simple REST API with health check endpoints built using FastAPI. This project demonstrates the Inteligens Agents Framework execution flow end-to-end.

## Project Overview

This API provides three health check endpoints:
- `GET /` - Root endpoint returning API status
- `GET /health` - Health check endpoint for monitoring
- `GET /version` - API version information

## Requirements

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. Navigate to the project directory:
```bash
cd examples/hello-agents
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** During framework execution, some steps may update `requirements.txt` (e.g., when agents correct missing dependencies). If `requirements.txt` is modified, reinstall dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the API server using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Running in Production Mode

For production, use:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=main --cov-report=html
```

View the coverage report by opening `htmlcov/index.html` in your browser.

### Test Coverage

The test suite includes comprehensive tests for:
- All three endpoints (/, /health, /version)
- HTTP status code validation
- Response body structure validation
- Pydantic model validation
- Error handling (404, 405)
- Content type validation
- HTTP method validation

**Coverage Target:** ≥ 80% (enforced by pytest configuration)

Run tests with coverage threshold:

```bash
pytest --cov=main --cov-fail-under=80
```

## API Endpoints

### GET /

Root endpoint to verify the API is running.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "ok"
}
```

**Status Code:** 200 OK

---

### GET /health

Health check endpoint for monitoring systems.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Code:** 200 OK

---

### GET /version

Returns the API version information.

**Request:**
```bash
curl http://localhost:8000/version
```

**Response:**
```json
{
  "version": "1.0.0"
}
```

**Status Code:** 200 OK

---

## Configuration

### Environment Variables

- `API_VERSION` - Sets the API version returned by `/version` endpoint (default: "1.0.0")

**Example:**
```bash
export API_VERSION="1.0.0"
uvicorn main:app --reload
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Project Structure

```
examples/hello-agents/
├── main.py              # FastAPI application and routes
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── tests/              # Test directory
│   └── test_main.py    # Unit tests for endpoints
├── docs/               # Architecture documentation
│   ├── ADR-001-framework-choice.md
│   ├── ARCHITECTURE.md
│   └── IMPLEMENTATION_PLAN.md
└── BACKLOG.md          # Product backlog
```

## Development

This project was built using the **Inteligens Agents Framework**, following a complete structured multi-agent workflow through all 13 execution steps:

### Framework Execution Flow

1. **Product Owner** - Created product backlog with user stories (`BACKLOG.md`)
2. **Scrum Master** - Planned sprint with sprint goal, board, and timeline (`SPRINT_PLAN.md`, `SPRINT_BOARD.md`)
3. **Staff Architect** ⚠️ *Approval Gate* - Designed architecture and chose FastAPI (`docs/ARCHITECTURE.md`, `docs/ADR-001-framework-choice.md`)
4. **Tech Lead** - Created implementation plan and coding standards (`docs/IMPLEMENTATION_PLAN.md`)
5. **Backend Engineer** - Implemented the API endpoints (`main.py`, `requirements.txt`)
6. **Frontend Engineer** - Skipped (backend-only project) (`docs/FRONTEND_SKIP.md`)
7. **AI Engineer** - Skipped (no AI features needed)
8. **DevOps/SRE** - Created deployment configurations (`Dockerfile`, `docs/DEPLOYMENT.md`)
9. **QA Strategist** - Created test suite with ≥80% coverage (`tests/`, `docs/TEST_PLAN.md`)
10. **AppSec Engineer** ⚠️ *Approval Gate* - Conducted security review (`docs/SECURITY_REVIEW.md`, `docs/THREAT_MODEL.md`)
11. **Release Manager** ⚠️ *Approval Gate* - Prepared release (`RELEASE_NOTES.md`, `RELEASE_CHECKLIST.md`)
12. **Sprint Reviewer** - Reviewed sprint outcomes (`SPRINT_REVIEW.md`, `SPRINT_METRICS.md`)
13. **Sprint Closer** ⚠️ *Approval Gate* - Closed sprint (`SPRINT_CLOSURE.md`)

### What This Example Demonstrates

This example proves the framework's ability to:

- ✅ **Generate complete project structure** from a simple task description
- ✅ **Follow Scrum methodology** with proper artifacts (backlog, sprint plan, board)
- ✅ **Enforce approval gates** at critical phases (architecture, security, release, closure)
- ✅ **Create comprehensive documentation** (architecture, ADRs, security reviews, test plans)
- ✅ **Generate production-ready code** with tests, Docker, and deployment configs
- ✅ **Maintain execution traceability** through execution journal and state files

### Key Artifacts Generated

**Planning:**
- `BACKLOG.md` - Product backlog with 8 user stories
- `SPRINT_PLAN.md` - Sprint planning with timeline and DoD
- `SPRINT_BOARD.md` - Visual sprint board

**Design:**
- `docs/ARCHITECTURE.md` - Complete system architecture
- `docs/ADR-001-framework-choice.md` - Architecture decision record
- `docs/IMPLEMENTATION_PLAN.md` - Detailed implementation guide

**Implementation:**
- `main.py` - FastAPI application with 3 endpoints
- `requirements.txt` - Python dependencies
- `tests/` - Comprehensive test suite (20+ tests, ≥80% coverage)

**Security:**
- `docs/SECURITY_REVIEW.md` - Complete security assessment
- `docs/THREAT_MODEL.md` - Threat analysis and mitigation

**Release:**
- `RELEASE_NOTES.md` - Release documentation
- `RELEASE_CHECKLIST.md` - Release validation checklist

**Sprint Closure:**
- `SPRINT_REVIEW.md` - Sprint review and outcomes
- `SPRINT_METRICS.md` - Sprint metrics and analytics
- `SPRINT_CLOSURE.md` - Sprint closure documentation

### Execution Journal

The framework maintains execution state in `.agents/swarm/`:
- `execution_plan.json` - Generated execution plan with 13 steps
- `execution_state.json` - Current execution state
- `execution_journal.md` - Complete execution log with approvals

See the `docs/` directory for detailed architecture and design decisions.

## License

This is an example project demonstrating the Inteligens Agents Framework.
