# Markdown Management and Coordination

This repo contains multiple markdown sources with different purposes. This document is the canonical guide for managing, organizing, and updating markdown files across the repository.

## Goals

- Keep user-facing documentation discoverable and consistent.
- Treat markdown as a first-class asset with clear ownership and categories.
- Make it easier to add, update, and audit markdown files across the repo.
- Coordinate docs updates with release notes, changelog, and package publishing.

## Categories of markdown files

### User-facing docs

- `docs/` — primary user documentation for CLI usage, features, troubleshooting, GitHub action integration, custom languages, architecture, schemas, and roadmap.
- `README.md` and localized README translations — project landing pages for users.
- `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md` — governance and release documentation.

### Generated and package docs

- `code_review_graph/docs/LLM-OPTIMIZED-REFERENCE.md` — optimized reference used by the Python package and MCP docs tooling.
- `code-review-graph-vscode/README.md` and the extension walkthrough markdown files in `code-review-graph-vscode/media/walkthrough/`.

### Skills and assistant instructions

- `skills/*/SKILL.md` — bundled skill definitions used by `code_review_graph/skills.py`.
- `.github/copilot-instructions.md`, `.github/code-review-graph.instruction.md`, and other `.github/*.md` files — repository-level instructions and templates.

### Internal or archive markdown

- `.beads/README.md` — internal issue tracker reference.
- `docs/MAINTAINER_RECONCILIATION_2026-07-17.md` — archive notes for maintainers.

## Coordination rules

1. New docs in `docs/` should be added to `docs/INDEX.md`.
2. If a new user-facing markdown file is added outside `docs/`, update `README.md`, `docs/INDEX.md`, or the relevant landing page so the file is discoverable.
3. New skill markdown files under `skills/` should be added via `code_review_graph/skills.py` if they are meant to be bundled or generated.
4. Extension documentation changes in `code-review-graph-vscode/` should be kept in sync with the extension build and published package version.
5. When updating release notes, ensure `CHANGELOG.md` and the user-facing docs mention the package or extension lifecycle clearly.

## Maintenance workflow

- Audit markdown coverage with `python scripts/scan_markdown.py`.
- Add new docs to the correct category.
- Update `docs/INDEX.md` when a new `docs/*.md` page is introduced.
- Review tests in `tests/test_documentation.py` to keep documentation contract coverage up to date.
- When changing markdown references in `README.md`, keep translated README files consistent as part of the same doc update.

## Verification

- `tests/test_documentation.py` checks the GitHub action references and documentation examples.
- The new `docs/MARKDOWN_MANAGEMENT.md` file is the source of truth for markdown coordination.

## Using the markdown inventory script

Run the inventory script from the repository root:

```bash
python scripts/scan_markdown.py
```

This script prints a categorized list of markdown files and highlights the main documentation groups.

## Suggested additions

- If there is a new markdown category, add it to this file so reviewers can find the new docs immediately.
- If documentation is moved or renamed, update `docs/INDEX.md` and any landing-page references at the same time.
