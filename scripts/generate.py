"""Generate TOOLS.md and the README.md category table from data/tools.csv."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT_DIR / "data" / "tools.csv"
TOOLS_MD_PATH = ROOT_DIR / "TOOLS.md"
README_MD_PATH = ROOT_DIR / "README.md"
ICONS_DIR = ROOT_DIR / "assets" / "icons"

START_MARKER = "<!-- CATEGORIES:START -->"
END_MARKER = "<!-- CATEGORIES:END -->"

REQUIRED_COLUMNS = (
    "#",
    "Tool",
    "Category",
    "Best For",
    "Repo URL",
    "License",
    "Language",
    "Notes",
)

CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "Workflow Automation (No/Low-code)": (
        "Visual flow builders and integration platforms for automating tasks across apps, "
        "APIs, and services with minimal code."
    ),
    "Workflow Orchestration (Code-first)": (
        "Programmatic and declarative engines for coordinating long-running, stateful, "
        "and event-driven workflows in code."
    ),
    "Data Orchestration & Pipelines": (
        "Schedulers, transformation frameworks, and data-movement tools for building and "
        "operating ETL, ELT, and ML pipelines."
    ),
    "CI/CD & Build Automation": (
        "Continuous integration servers, runners, build systems, and task runners for "
        "automating software builds, tests, and releases."
    ),
    "GitOps & Deployment": (
        "Tools that synchronize cluster state, packages, and infrastructure changes "
        "automatically from Git repositories."
    ),
    "Infrastructure as Code & Config Mgmt": (
        "Provisioning, image-building, and configuration management tools for defining "
        "and maintaining infrastructure declaratively."
    ),
    "RPA & Desktop/UI Automation": (
        "Robotic process automation and desktop scripting tools for automating graphical "
        "interfaces and repetitive OS-level tasks."
    ),
    "Browser, Scraping & Test Automation": (
        "Frameworks and drivers for controlling web and mobile browsers, scraping web data, "
        "and running end-to-end UI tests."
    ),
    "AI Agents & AI Workflows": (
        "Frameworks and visual builders for orchestrating LLM pipelines, multi-agent "
        "systems, and tool-using AI workflows."
    ),
    "Low-code & Business Automation": (
        "Application builders and campaign platforms with built-in triggers and workflows "
        "for internal tools and business operations."
    ),
    "Task Queues & Scheduling": (
        "Distributed background job queues and workers for scheduling and executing "
        "asynchronous application tasks."
    ),
    "Developer Workflow Automation": (
        "Tools that automate repository maintenance, dependency updates, versioning, "
        "and package publishing."
    ),
    "Home & IoT Automation": (
        "Platforms for connecting smart-home devices, sensors, and local services through "
        "automated rules and triggers."
    ),
}

DEFAULT_CATEGORY_DESCRIPTION = (
    "Automation tools and frameworks grouped under this category."
)


def icon_slug(category: str) -> str:
    """Return the deterministic SVG filename stem for a category name."""
    return re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")


def gfm_anchor(heading: str) -> str:
    """Compute the GitHub Flavored Markdown heading anchor for a heading string."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-")


def escape_cell(value: str) -> str:
    """Normalize a cell string for inclusion in a Markdown table."""
    cleaned = " ".join(value.replace("\r", " ").replace("\n", " ").split())
    return cleaned.replace("|", "\\|")


def load_tools(csv_path: Path) -> list[tuple[str, list[dict[str, str]]]]:
    """Read data/tools.csv and group rows by category in first-seen CSV order."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Missing input CSV: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing headers.")
        missing = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

        grouped: dict[str, list[dict[str, str]]] = {}
        for row_num, raw_row in enumerate(reader, start=2):
            row = {col: (raw_row.get(col) or "").strip() for col in REQUIRED_COLUMNS}
            if not row["Tool"] or not row["Category"] or not row["Repo URL"]:
                raise ValueError(
                    f"Row {row_num} is missing Tool, Category, or Repo URL."
                )
            grouped.setdefault(row["Category"], []).append(row)

    return list(grouped.items())


def resolve_icon_relpath(category: str) -> str:
    """Return the repository-relative path to a category's SVG icon and verify it exists."""
    slug = icon_slug(category)
    rel_path = f"assets/icons/{slug}.svg"
    icon_file = ICONS_DIR / f"{slug}.svg"
    if not icon_file.is_file():
        raise FileNotFoundError(
            f"Missing category icon for '{category}': {rel_path}"
        )
    return rel_path


def render_tools_md(categories: list[tuple[str, list[dict[str, str]]]]) -> str:
    """Render the full TOOLS.md document from grouped CSV data."""
    total_tools = sum(len(rows) for _, rows in categories)
    total_categories = len(categories)

    lines: list[str] = [
        "<!-- Generated by scripts/generate.py from data/tools.csv. Do not hand-edit. -->",
        "",
        "# Automation Tools Directory",
        "",
        (
            f"A curated directory of {total_tools} automation tools across "
            f"{total_categories} categories, generated from [data/tools.csv](data/tools.csv)."
        ),
        "",
        "## Table of Contents",
        "",
        "| Icon | Category | Tools |",
        "| :---: | :--- | :---: |",
    ]

    for category, rows in categories:
        icon_path = resolve_icon_relpath(category)
        anchor = gfm_anchor(category)
        safe_cat = escape_cell(category)
        icon_tag = (
            f'<img src="{icon_path}" width="20" height="20" alt="{safe_cat}" />'
        )
        lines.append(f"| {icon_tag} | [{safe_cat}](#{anchor}) | {len(rows)} |")

    for category, rows in categories:
        description = CATEGORY_DESCRIPTIONS.get(category, DEFAULT_CATEGORY_DESCRIPTION)
        lines.extend(
            [
                "",
                "---",
                "",
                f"## {category}",
                "",
                description,
                "",
                "| Tool | Best For | License | Language | Notes |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
        )

        for row in rows:
            tool_name = escape_cell(row["Tool"])
            repo_url = row["Repo URL"]
            best_for = escape_cell(row["Best For"])
            license_name = escape_cell(row["License"])
            language = escape_cell(row["Language"])
            notes = escape_cell(row["Notes"])
            notes_cell = f" {notes} " if notes else " "
            lines.append(
                f"| [{tool_name}]({repo_url}) | {best_for} | {license_name} | {language} |{notes_cell}|"
            )

    lines.extend(
        [
            "",
            "---",
            "",
            "## License notes",
            "",
            (
                "Each listed tool is governed by its own license. Licensing terms, "
                "source-available clauses, and dual-licensing models vary by project "
                "and may change over time, so licenses should be confirmed directly "
                "on the repository before commercial use."
            ),
            "",
        ]
    )

    return "\n".join(lines)


def render_readme_categories(
    categories: list[tuple[str, list[dict[str, str]]]],
) -> str:
    """Render the README.md category summary table."""
    lines: list[str] = [
        "| Icon | Category | Tools | Link |",
        "| :---: | :--- | :---: | :--- |",
    ]

    for category, rows in categories:
        icon_path = resolve_icon_relpath(category)
        anchor = gfm_anchor(category)
        safe_cat = escape_cell(category)
        icon_tag = (
            f'<img src="{icon_path}" width="24" height="24" alt="{safe_cat}" />'
        )
        lines.append(
            f"| {icon_tag} | {safe_cat} | {len(rows)} | [View tools](TOOLS.md#{anchor}) |"
        )

    return "\n".join(lines)


def render_readme_md(
    readme_path: Path, categories: list[tuple[str, list[dict[str, str]]]]
) -> str:
    """Return README.md content with the category block updated between markers."""
    if not readme_path.is_file():
        raise FileNotFoundError(f"Missing README.md: {readme_path}")

    existing = readme_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    start_idx = existing.find(START_MARKER)
    end_idx = existing.find(END_MARKER)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise ValueError(
            f"README.md must contain {START_MARKER} followed by {END_MARKER}."
        )

    table_md = render_readme_categories(categories)
    before = existing[: start_idx + len(START_MARKER)]
    after = existing[end_idx:]
    return f"{before}\n{table_md}\n{after}"


def write_utf8_lf(path: Path, content: str) -> None:
    """Write text as UTF-8 without BOM using LF line endings."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def check_file(path: Path, expected: str) -> bool:
    """Return True if path exists and matches expected UTF-8 LF bytes exactly."""
    if not path.is_file():
        return False
    return path.read_bytes() == expected.encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for generating or verifying directory markdown files."""
    parser = argparse.ArgumentParser(
        description="Generate TOOLS.md and README.md category table from data/tools.csv."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if generated files differ from the committed files.",
    )
    args = parser.parse_args(argv)

    try:
        categories = load_tools(CSV_PATH)
        tools_content = render_tools_md(categories)
        readme_content = render_readme_md(README_MD_PATH, categories)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    total_tools = sum(len(rows) for _, rows in categories)
    total_categories = len(categories)

    if args.check:
        stale: list[str] = []
        if not check_file(TOOLS_MD_PATH, tools_content):
            stale.append("TOOLS.md")
        if not check_file(README_MD_PATH, readme_content):
            stale.append("README.md")
        if stale:
            print(
                f"Out of date: {', '.join(stale)}. Run 'python scripts/generate.py'.",
                file=sys.stderr,
            )
            return 1
        print(
            f"OK: TOOLS.md and README.md are up to date "
            f"({total_tools} tools, {total_categories} categories)."
        )
        return 0

    write_utf8_lf(TOOLS_MD_PATH, tools_content)
    write_utf8_lf(README_MD_PATH, readme_content)
    print(
        f"Generated TOOLS.md and updated README.md "
        f"({total_tools} tools, {total_categories} categories)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
