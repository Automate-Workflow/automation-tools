# Contributing

Thank you for contributing to `Automate-Workflow/automation-tools`.

`data/tools.csv` is the single source of truth for this directory. `TOOLS.md` and the category table inside `README.md` are generated from `data/tools.csv` by `scripts/generate.py` and must not be hand-edited.

## How to add a tool

1. Add one row to `data/tools.csv` with these columns:
   `#, Tool, Category, Best For, Repo URL, License, Language, Notes`
2. Run the generator with standard Python 3 (standard library only):
   ```bash
   python scripts/generate.py
   ```
3. Verify that generated output passes the check:
   ```bash
   python scripts/generate.py --check
   ```
4. Commit `data/tools.csv`, `TOOLS.md`, and `README.md` together.

If you propose a new category, include a matching 64x64 SVG line icon in `assets/icons/<slug>.svg` following the repository palette and add a concise one-line description in `scripts/generate.py`.

## Inclusion criteria

Every entry added to `data/tools.csv` must meet all of the following requirements:

- **Public repository**: The source code repository must be publicly accessible.
- **Canonical URL**: Link to the official upstream repository rather than mirrors, aggregators, or personal forks (unless a fork is the recognized community successor).
- **Automation focus**: The project must genuinely be an automation tool within the scope of this directory.
- **Maintenance status**: The project must be actively maintained or historically significant. State which applies in the `Notes` column if the repository is archived, unmaintained, or a legacy predecessor.
- **License stated**: State the license as declared in the upstream repository (for example `MIT`, `Apache-2.0`, `GPL-3.0`, or specific source-available terms). Do not guess or omit non-OSI license caveats.

## Pull request checklist

- [ ] Added or updated exactly the relevant row(s) in `data/tools.csv`.
- [ ] Preserved existing CSV formatting (UTF-8, valid CSV quoting).
- [ ] Ran `python scripts/generate.py` and committed regenerated `TOOLS.md` and `README.md`.
- [ ] Verified `python scripts/generate.py --check` exits with code 0.
- [ ] Confirmed no emoji or pictographic Unicode symbols appear in files or commit messages.
- [ ] Kept descriptions concise and factual without marketing language.

## Commit message style

- Use a short imperative subject line in plain ASCII (50-72 characters).
- Do not include emoji or pictographic symbols.
- Examples:
  - `Add Taskfile entry to CI/CD & Build Automation`
  - `Update license note for Terraform`
