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

This project was built using the Inteligens Agents Framework, following a structured multi-agent workflow:

1. **Product Owner** - Defined backlog and user stories
2. **Scrum Master** - Planned sprint and organized tasks
3. **Staff Architect** - Designed architecture and chose FastAPI
4. **Tech Lead** - Created implementation plan and standards
5. **Backend Engineer** - Implemented the API (this step)

See the `docs/` directory for detailed architecture and design decisions.

## License

This is an example project demonstrating the Inteligens Agents Framework.
