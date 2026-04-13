# Contributing to PyData Kampala

Thank you for your interest in contributing! This project is community-driven and every contribution matters — whether it's fixing a typo, reporting a bug, or adding a feature.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Branch Workflow](#branch-workflow)
4. [Commit Messages](#commit-messages)
5. [Opening a Pull Request](#opening-a-pull-request)
6. [Review Process](#review-process)
7. [Your First Contribution](#your-first-contribution)
8. [Maintainer Triage](#maintainer-triage)

---

## Code of Conduct

By participating you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

---

## Getting Started

Follow the [local development setup](README.md#local-development-setup) instructions in the README to get the project running on your machine.

Install pre-commit hooks so the linter and formatter run automatically:

```bash
pre-commit install
```

---

## Branch Workflow

1. **Fork** the repository to your own GitHub account.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/pydatakla.git
   cd pydatakla
   ```
3. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
   Use a descriptive prefix:
   | Prefix | Use for |
   |--------|---------|
   | `feat/` | New feature |
   | `fix/` | Bug fix |
   | `docs/` | Documentation only |
   | `chore/` | Build, tooling, dependencies |
   | `test/` | Adding or fixing tests |

4. **Make your changes**, commit, and push to your fork.
5. Open a pull request against `main` on this repository.

---

## Commit Messages

We follow a simple version of [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short imperative summary>

Optional body explaining *why*, not what.
```

Examples:
- `feat: add sponsor logo upload endpoint`
- `fix: correct schedule ordering by date`
- `docs: add local setup instructions to README`

Keep the subject line under 72 characters. Use the body for anything that needs more context.

---

## Opening a Pull Request

- Fill in the pull request template completely.
- Link the related issue with `Closes #<issue-number>` in the description.
- Keep PRs focused — one logical change per PR makes review faster.
- Ensure CI passes (lint + tests) before requesting a review.
- Add or update tests for any behaviour you change.

---

## Review Process

1. A maintainer will review your PR within **5 business days**.
2. They may leave comments or request changes — please respond or make updates within a reasonable time.
3. Once approved, a maintainer will merge using **squash merge** to keep the history clean.
4. If your PR goes stale (no activity for 30 days) it may be closed with a note to reopen.

---

## Your First Contribution

Not sure where to start? Look for issues labelled:

- [`good first issue`](../../labels/good%20first%20issue) — small, well-defined tasks ideal for newcomers.
- [`help wanted`](../../labels/help%20wanted) — tasks where the maintainers welcome outside help.

Some beginner-friendly areas:

- Improve template HTML/CSS styling
- Add missing docstrings or inline comments
- Write tests for untested views or model methods
- Update copy or content on informational pages (About, Code of Conduct)
- Fix typos or grammar in documentation

If you find a bug but don't know how to fix it yet, **opening an issue is also a valuable contribution**.

---

## Maintainer Triage

Issues are triaged on a best-effort basis:

| Label | Meaning |
|-------|---------|
| `good first issue` | Suitable for new contributors |
| `help wanted` | Extra help is welcome |
| `bug` | Confirmed bug |
| `enhancement` | Feature request or improvement |
| `question` | Needs clarification |
| `wontfix` | Out of scope or intentional behaviour |

Maintainers aim to:
- Acknowledge new issues within **3 business days**.
- Add a triage label within **5 business days**.
- Close stale issues (no activity for 60 days) after a warning comment.
