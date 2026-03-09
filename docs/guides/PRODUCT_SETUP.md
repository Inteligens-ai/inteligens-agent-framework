# Product Setup Guide

> How to configure a product to use the Inteligens Agent Framework with full context injection.

---

## Overview

By default, every sprint starts from zero — agents know only the task description you provide.

With a `PRODUCT.md` file in your project root, agents receive persistent product context on every sprint: tech stack, architecture decisions, compliance constraints, and conventions. This eliminates repeated context loss between sprints and produces consistent, product-aware output across all agents.

---

## Setup Steps

### 1. Copy the template

```bash
cp <framework-path>/.agents/docs/PRODUCT_TEMPLATE.md PRODUCT.md
```

Or, if using the framework as a submodule:

```bash
cp inteligens-agents/.agents/docs/PRODUCT_TEMPLATE.md PRODUCT.md
```

### 2. Fill in the file

Open `PRODUCT.md` and complete every required field. Remove optional sections that do not apply. The file lives in the root of your product repository.

Minimum required fields:

```markdown
**Name:** My Product
**Description:** <what it does, for whom, what problem it solves>
**Status:** in-development
**DOCS_LANGUAGE:** pt-br
```

### 3. Run the planner with a sprint identifier

```bash
python .agents/swarm/swarm_planner.py \
  --task "Implement user authentication with JWT" \
  --sprint "Sprint 1"
```

The planner will detect `PRODUCT.md` automatically and inject its content into the execution plan. Output will confirm:

```
Plan generated: .agents/swarm/execution_plan.json
Product context loaded: PRODUCT.md (My Product)
Documentation language: pt-br
Sprint: Sprint 1
Steps requiring approval: 3, 10, 11, 13, 14
```

---

## How Context Is Used

The product context is stored in `execution_plan.json` under `product_context`. Every agent that runs against this plan has access to:

- Product name and description
- Tech stack — agents will not propose technologies outside the defined stack
- Architecture decisions — agents will not contradict existing ADRs
- Compliance constraints — agents will enforce defined rules without being reminded
- Conventions — agents will follow naming and structure conventions
- Out of scope — agents will not suggest what is explicitly excluded

---

## Language Configuration

The `DOCS_LANGUAGE` field in `PRODUCT.md` sets the documentation language for all documents produced in this product. It overrides the default in `.agents/docs/DOCUMENTATION_STANDARD.md`.

| `DOCS_LANGUAGE` | Effect |
|---|---|
| `en` | All sprint documents in English (default) |
| `pt-br` | All sprint documents in Brazilian Portuguese |

Status values remain in English regardless of language setting — they are identifiers, not prose:
- **Document status (header):** `DRAFT`, `COMPLETE`, `APPROVED`, `BLOCKED`
- **Definition of Done status (checklist):** `DONE`, `PARTIAL`, `BLOCKED`, `PENDING`, `FAILED`

---

## Sprint Identification

The `--sprint` flag adds a sprint identifier to the execution plan and to all document headers produced during that sprint. Use a consistent naming convention across your products:

```bash
# Numeric
--sprint "Sprint 1"

# Named
--sprint "Sprint Auth"

# Date-based
--sprint "2026-Q1-S1"
```

All documents will include this identifier in their mandatory header block, making it easy to trace which sprint produced each artifact.

---

## File Location

The planner looks for `PRODUCT.md` in this order:

1. `PRODUCT.md` (project root — recommended)
2. `.agents/PRODUCT.md` (alternative location)

The first file found is used. If neither exists, the planner runs without product context.

---

## Version Control

`PRODUCT.md` should be committed to your product repository. It represents the product's current architectural state and evolves with the product.

Update `PRODUCT.md` when:
- A new architectural decision is made (add to Architecture Decisions)
- A new technology is adopted (update Tech Stack)
- A compliance requirement is identified (add to Compliance Constraints)
- Something is explicitly ruled out (add to Out of Scope)

---

## Multi-Product Setup

Each product has its own `PRODUCT.md` in its own repository. The framework itself does not have a `PRODUCT.md` — the template lives at `.agents/docs/PRODUCT_TEMPLATE.md` and is the reference for all products.

```
my-org/
├── product-a/
│   ├── PRODUCT.md          ← product A context
│   └── inteligens-agents/  ← framework (submodule)
├── product-b/
│   ├── PRODUCT.md          ← product B context
│   └── inteligens-agents/  ← framework (submodule)
└── inteligens-agents/      ← framework source
    └── .agents/docs/
        └── PRODUCT_TEMPLATE.md  ← canonical template
```
