from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_DIRS = [
    "idea/intake",
    "idea/registry",
    "idea/agents/idea_generator/prompts",
    "idea/agents/idea_generator/outputs",
    "idea/agents/literature_judge/prompts",
    "idea/agents/literature_judge/outputs",
    "idea/ideas/idea_001/elicit",
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
    "idea/intake/human_seed.md",
    "idea/intake/human_seed.json",
    "idea/registry/idea_registry.csv",
    "idea/registry/loop_log.csv",
    "idea/agents/idea_generator/state.json",
    "idea/agents/literature_judge/state.json",
    "idea/ideas/idea_001/question_intake.json",
    "idea/ideas/idea_001/data_fit.json",
    "idea/ideas/idea_001/contribution_scorecard.json",
    "idea/ideas/idea_001/topic_decision.md",
    "code/_write_version_log.do",
    "code/00_setup.do",
    "code/build/00_build_sample.do",
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
    "workflow_state",
]

PROJECT_YAML_REQUIRED_STRINGS = [
    "workflow_state:",
    "active_stage:",
    "active_idea_id:",
    "active_rq_id:",
    "topic_gate_status:",
    "identification_gate_status:",
    "last_empirical_run_id:",
    "current_reproduction_target:",
    "idea_loop:",
    "max_idea_search_rounds: 10",
]


def read_text_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


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

    readme_text = read_text_if_exists(project_root / "README.md")
    for required_string in README_REQUIRED_STRINGS:
        if required_string not in readme_text:
            errors.append(f"README.md should mention: {required_string}")

    yaml_text = read_text_if_exists(project_root / "project.yaml")
    for required_string in PROJECT_YAML_REQUIRED_STRINGS:
        if required_string not in yaml_text:
            errors.append(f"project.yaml should include: {required_string}")

    registry_path = project_root / "idea/registry/idea_registry.csv"
    if registry_path.exists():
        header = registry_path.read_text(encoding="utf-8").splitlines()
        if header:
            required_columns = [
                "idea_id",
                "round",
                "source",
                "normalized_question",
                "uses_existing_data",
                "requires_new_data",
                "new_data_allowed",
                "public_data_available",
                "data_fit_status",
                "total_score",
                "decision",
                "failure_reasons",
                "next_action",
            ]
            for column_name in required_columns:
                if column_name not in header[0].split(","):
                    errors.append(f"idea_registry.csv missing column: {column_name}")

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
