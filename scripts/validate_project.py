from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_DIRS = [
    "idea",
    "references",
    "notes",
    "data/raw",
    "data/build",
    "code/build",
    "output/raw",
    "output/figures",
    "output/tables",
    "draft/images",
    "draft/figures",
    "draft/tables",
    "work",
    "paper/tex",
    "paper/replication_package",
]

REQUIRED_FILES = [
    "README.md",
    "project.yaml",
    "draft/main.tex",
]

FORBIDDEN_TOP_LEVEL_DIRS = [
    "design",
    "docs",
    "papers",
]

FORBIDDEN_DEFAULT_DIRS = [
    "output/manifests",
]

README_REQUIRED_STRINGS = [
    "Elicit API key environment variable",
    "Overleaf remote URL",
    "Overleaf token source",
    "Required pre-flight before agent work",
]


def validate_project(project_root: Path) -> list[str]:
    errors = []

    for relative_dir in REQUIRED_DIRS:
        if not (project_root / relative_dir).is_dir():
            errors.append(f"Missing required directory: {relative_dir}")

    for relative_file in REQUIRED_FILES:
        if not (project_root / relative_file).is_file():
            errors.append(f"Missing required file: {relative_file}")

    for relative_dir in FORBIDDEN_TOP_LEVEL_DIRS:
        if (project_root / relative_dir).exists():
            errors.append(f"Project should not contain top-level `{relative_dir}/`.")

    for relative_dir in FORBIDDEN_DEFAULT_DIRS:
        if (project_root / relative_dir).exists():
            errors.append(f"Project should not contain default `{relative_dir}/`.")

    notes_root = project_root / "notes"
    if notes_root.exists():
        child_dirs = []
        for child in notes_root.iterdir():
            if child.is_dir():
                child_dirs.append(child.name)
        if child_dirs:
            names = ", ".join(sorted(child_dirs))
            errors.append(f"`notes/` should be flat by default. Found subdirectories: {names}")

    readme_path = project_root / "README.md"
    if readme_path.exists():
        readme_text = readme_path.read_text(encoding="utf-8")
        for required_string in README_REQUIRED_STRINGS:
            if required_string not in readme_text:
                errors.append(f"README.md should mention: {required_string}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    errors = validate_project(project_root)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("Project structure validation passed.")


if __name__ == "__main__":
    main()
