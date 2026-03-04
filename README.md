# Repo Doctor

> Turn any repository into an open-source-ready, professional repo in one command.

Repo Doctor scans your Git repository, scores it against 17 open-source best-practice rules, and auto-generates any missing files — README, LICENSE, CI workflow, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY policy, and .gitignore — without ever touching your source code.

## Install

```bash
# With pipx (recommended)
pipx install git+https://github.com/JasperLiu1999/repo-doctor.git

# Or with uv
uv tool install git+https://github.com/JasperLiu1999/repo-doctor.git
```

## Quickstart

```bash
# Scan a repo and get a health score + report
repo-doctor scan /path/to/repo

# Preview what would be fixed (no files written)
repo-doctor fix --dry-run /path/to/repo

# Fix issues automatically
repo-doctor fix --yes /path/to/repo
```

### Example: scanning a bare repo

```
╭──────────────────── Repo Doctor ─────────────────────╮
│ Score: 21/100  Grade: D                              │
│ Stack: node  |  Passed: 5  |  Failed: 12  |  Total: 17 │
╰──────────────────────────────────────────────────────╯
```

### Example: after running `fix --yes`

```
╭──────────────────── Repo Doctor ─────────────────────╮
│ Score: 88/100  Grade: B                              │
│ Stack: node  |  Passed: 14  |  Failed: 3  |  Total: 17 │
╰──────────────────────────────────────────────────────╯
Score improved by 67 points!
```

## What it checks

17 rules across 6 categories:

| Category | Rules | Auto-fixable |
|----------|-------|:---:|
| **Basics** | README present, README has key sections, LICENSE present | 2 of 3 |
| **Community** | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY policy | 3 of 3 |
| **Build** | CI pipeline, test command, linter configured | 1 of 3 |
| **Hygiene** | .gitignore present, .gitignore coverage, no venv/caches, repo size | 2 of 4 |
| **Security** | No secret files (.env, .pem, id_rsa), no high-entropy strings | 0 of 2 |
| **Reproducibility** | Lockfile present, dependencies pinned | 0 of 2 |

Each rule produces a **pass/fail**, a **severity** (error/warn/info), and a **weight** toward the 0-100 score. Grade thresholds: A (90+), B (75+), C (55+), D (<55).

## How fixes work

Repo Doctor is **safe by default**:

1. Scans and identifies failing auto-fixable rules
2. Builds a **ChangePlan** (list of files to create or patch)
3. Shows a **rich diff preview** of every file
4. Only writes files after you confirm (or use `--yes`)
5. Re-scans and shows the score improvement

Guarantees:
- Never deletes files
- Never modifies your source code
- Only generates meta-files (README, LICENSE, CI, etc.)
- Templates are **stack-aware** — a Python repo gets `pytest` in CI, a Node repo gets `npm test`

## Detected stacks

Repo Doctor auto-detects your project type and tailors templates accordingly:

| Stack | Detected by |
|-------|-------------|
| Python | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` |
| Node | `package.json`, `package-lock.json`, `yarn.lock` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Swift | `Package.swift`, `*.xcodeproj`, `*.swift` |

## CLI Reference

```
repo-doctor scan [PATH]     Scan and produce a health report
repo-doctor fix [PATH]      Auto-generate missing files
repo-doctor init [PATH]     Create a .repo-doctor.yml config
```

### Key flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without writing files |
| `--yes`, `-y` | Apply changes without confirmation |
| `--strict` | Exit with code 1 if any warnings/errors |
| `--format` | Output format: `md`, `json`, or `both` (default) |
| `--only RULE` | Only run specific rule(s) |
| `--skip RULE` | Skip specific rule(s) |
| `--license` | License type: `mit` (default) or `apache-2.0` |

## Output files

After scanning, Repo Doctor writes:

- `repo-doctor.report.md` — Human-readable report
- `repo-doctor.report.json` — Machine-readable report (for CI integration)
- `repo-doctor.changes.md` — Summary of applied/planned changes

## Config

Create `.repo-doctor.yml` in your repo root, or run `repo-doctor init`:

```yaml
project_name: my-project
license: mit
ci: github-actions
readme: standard
skip:
  - lint_config
  - pinned_deps
```

## Development

```bash
git clone https://github.com/JasperLiu1999/repo-doctor.git
cd repo-doctor
uv sync --dev
uv run pytest -x -v        # run tests (79 tests)
uv run ruff check src/     # run linter
uv run repo-doctor scan .  # scan itself (scores 100/100)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, including how to add new rules.

## License

MIT
