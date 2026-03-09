# Product Context

> Copy this file to the root of your project as `PRODUCT.md`.
> Fill in every required field before running your first sprint.
> This file is read by the Swarm Planner and injected as context into every agent prompt.

---

## Identity

**Name:** <product name> <!-- REQUIRED -->
**Description:** <what the product does, for whom, and what problem it solves — 2-3 sentences> <!-- REQUIRED -->
**Status:** <in-development | mvp | production> <!-- REQUIRED -->
**Repository:** <repository URL or path> <!-- OPTIONAL -->

---

## Documentation

**DOCS_LANGUAGE:** en <!-- REQUIRED -->
<!-- Options: en | pt-br -->
<!-- This value overrides DOCUMENTATION_STANDARD.md for all documents produced in this product. -->

---

## Tech Stack

<!-- List the technologies in use. Agents will use this to make stack-consistent decisions. -->
<!-- Remove lines that do not apply. Add lines as needed. -->

- **Language:** <e.g., Python 3.12>
- **Backend Framework:** <e.g., FastAPI | Django | Express>
- **Frontend Framework:** <e.g., React 18 | Vue 3 | None>
- **Database:** <e.g., PostgreSQL 15 | SQLite | MongoDB>
- **ORM / Query Layer:** <e.g., SQLAlchemy | Prisma | None>
- **Infrastructure:** <e.g., Docker | Kubernetes | bare metal>
- **CI/CD:** <e.g., GitHub Actions | GitLab CI | None>
- **Testing:** <e.g., pytest | Jest | Vitest>
- **Package Manager:** <e.g., pip | npm | pnpm | bun>

---

## Architecture Decisions

<!-- Summarize decisions already made. Agents must not contradict these. -->
<!-- Reference ADR files if they exist: e.g., "See docs/adr/ for full records." -->

- <decision 1 — e.g., "REST API only, no GraphQL">
- <decision 2 — e.g., "All embeddings stored encrypted at rest (AES-256-GCM)">
- <decision 3 — e.g., "Frontend and backend are separate deployable units">

---

## Compliance Constraints

<!-- List regulatory and legal requirements that agents must respect. -->
<!-- Remove if not applicable. -->

- <e.g., LGPD compliance required for all user data>
- <e.g., Biometric data must never be stored in plain text>
- <e.g., Audit logs are immutable — append only, no deletes>

---

## Conventions

<!-- Code style, naming, structure conventions already established. -->
<!-- Agents will follow these when generating code or documentation. -->

- <e.g., snake_case for Python, camelCase for JavaScript>
- <e.g., All API endpoints versioned under /api/v1/>
- <e.g., Branch naming: feature/, fix/, chore/>
- <e.g., Commit messages follow Conventional Commits>

---

## Out of Scope

<!-- What agents must NOT propose, suggest, or implement in this product. -->
<!-- This prevents agents from introducing unwanted technologies or patterns. -->

- <e.g., No GraphQL — REST only>
- <e.g., No microservices — monolith for now>
- <e.g., No cloud-specific services — must run on-premises>

---

## Notes

<!-- Any other context agents should know before starting a sprint. -->
<!-- Optional. Remove if not needed. -->
