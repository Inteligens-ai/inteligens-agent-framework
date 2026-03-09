# Documentation Standard — Inteligens Agent Framework

> This standard applies to all documents produced by agents during sprint execution.
> Agents must comply with this standard when producing any output artifact.

---

## Configuration

| Setting | Default | Options | Description |
|---|---|---|---|
| `DOCS_LANGUAGE` | `en` | `en`, `pt-br` | Language for all sprint documents |
| `DOCS_DATE_FORMAT` | `YYYY-MM-DD` | ISO 8601 | Date format for all timestamps |

**Override via PRODUCT.md:** if the project contains a `PRODUCT.md` file with a `DOCS_LANGUAGE` field, that value takes precedence over the default here. This is the recommended approach for multi-product setups. See `docs/guides/PRODUCT_SETUP.md`.

**To change globally:** edit the default value in this file. Applies to all projects that do not have a `PRODUCT.md`.

---

## Mandatory Header

Every document produced by an agent must begin with this metadata block, before any other content:

```
**Agent:** <registry key — e.g., engineering/backend-engineer.md>
**Phase:** <plan | design | build | test | release | review | retrospective | closure>
**Sprint:** <sprint identifier — e.g., Sprint 1 or a named sprint>
**Date:** <YYYY-MM-DD>
**Status:** <DRAFT | COMPLETE | APPROVED | BLOCKED>
```

This block is mandatory. It cannot be removed, renamed, or moved to the end of the document.

---

## Status Values

Status values are used in two different contexts. Use only the values listed below for each context. No emoji. No variations. No free-form text in status fields.

### Document Status (Header)

Use in the mandatory header block `Status:` field:

| Value | Meaning |
|---|---|
| `DRAFT` | Document is being written |
| `COMPLETE` | Document is finished |
| `APPROVED` | Document has been approved |
| `BLOCKED` | Document cannot be completed due to blockers |

### Definition of Done Status (Checklist)

Use in the Definition of Done checklist table:

| Value | Meaning |
|---|---|
| `DONE` | Criterion fully met and verifiable by a third party |
| `PARTIAL` | Criterion partially met — the same cell must describe what is missing |
| `BLOCKED` | Cannot proceed — a blocker must be declared in the Handoff block |
| `PENDING` | Not yet started |
| `FAILED` | Criterion not met — must be escalated, not silently ignored |

**Rule:** a single item cannot be marked `DONE` and simultaneously described as having problems. If it has problems, it is `PARTIAL` or `BLOCKED`. The status must reflect reality, not intent.

---

## Section Structure

- **H1** (`#`): document title only — one per document
- **H2** (`##`): major sections
- **H3** (`###`): subsections
- **H4** (`####`): avoid — restructure as a table if depth is needed

Section names defined in an agent's Output Contract are mandatory and cannot be renamed or removed.

---

## Mandatory Closing Block

Every document must end with these two sections, in this order:

### Handoff

```
## Handoff

**To:** <next agent registry key>
**Delivers:** <what this document provides to the next agent — one sentence per item>
**Pending:** <unresolved items that the next agent should be aware of. "None" if clean.>
**Blockers:** <active blockers that must be resolved before the next agent can proceed. "None" if clean.>
```

### Definition of Done — Checklist

```
## Definition of Done

| Criterion | Status |
|---|---|
| <criterion from this agent's DoD> | DONE | PARTIAL | BLOCKED | PENDING | FAILED |
```

Every criterion from the agent's Definition of Done section must appear in this table. Status must match the actual state of the document, not a desired state.

---

## Extension Rules

Agents may add sections beyond what is specified in their Output Contract.

Rules for optional sections:
- Optional section titles must end with `[OPTIONAL]`
- Optional sections must appear after all mandatory sections and before the closing block
- Optional sections may be omitted without any note

Agents must not:
- Remove mandatory sections
- Rename mandatory sections
- Reorder the header block or the closing block
- Use status values not listed in this standard

---

## Language Rules

When `DOCS_LANGUAGE` is set to `pt-br`:
- All section titles, metadata labels, and content must be in Brazilian Portuguese
- Status values remain in English (both document status: `DRAFT`, `COMPLETE`, `APPROVED`, `BLOCKED` and DoD status: `DONE`, `PARTIAL`, `BLOCKED`, `PENDING`, `FAILED`) — they are identifiers, not prose
- Registry keys remain as-is (they are paths, not prose)

When `DOCS_LANGUAGE` is set to `en`:
- All content in English

Mixed-language documents are not permitted.

---

## Quick Reference

```
[Header block]
  Agent / Phase / Sprint / Date / Status (DRAFT|COMPLETE|APPROVED|BLOCKED)

[Content sections — mandatory per Output Contract]

[Optional sections — marked [OPTIONAL], after mandatory content]

[Handoff block]
  To / Delivers / Pending / Blockers

[Definition of Done checklist]
  One row per criterion / Status (DONE|PARTIAL|BLOCKED|PENDING|FAILED)
```
