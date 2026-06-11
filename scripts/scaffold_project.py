from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PROJECT_DIRS = [
    "idea",
    "references/reference_by_human/pdfs",
    "references/reference_by_ai/raw",
    "references/reference_by_ai/systematic_review",
    "references/reference_by_ai/pdfs",
    "references/reference_merged/pdfs",
    "notes",
    "data/raw",
    "data/build",
    "data/codebook",
    "code/build",
    "output/raw",
    "output/figures",
    "output/tables",
    "draft/images",
    "draft/figures",
    "draft/tables",
    "work",
    "paper/tex",
    "paper/replication_package/code",
    "paper/replication_package/data",
    "paper/replication_package/output",
]


def copy_template(repo_root: Path, template_path: str, destination: Path) -> None:
    source = repo_root / template_path
    if not source.exists():
        raise FileNotFoundError(f"Missing template: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def create_empty_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def scaffold_project(dest: Path, slug: str, title: str, repo_root: Path) -> None:
    if dest.exists() and any(dest.iterdir()):
        raise RuntimeError(f"Destination exists and is not empty: {dest}")

    dest.mkdir(parents=True, exist_ok=True)

    for relative_dir in PROJECT_DIRS:
        (dest / relative_dir).mkdir(parents=True, exist_ok=True)

    copy_template(repo_root, "templates/project/README.md", dest / "README.md")
    copy_template(repo_root, "templates/project/project.yaml", dest / "project.yaml")

    readme_text = (dest / "README.md").read_text(encoding="utf-8")
    readme_text = readme_text.replace("<Project Title>", title)
    (dest / "README.md").write_text(readme_text, encoding="utf-8")

    yaml_text = (dest / "project.yaml").read_text(encoding="utf-8")
    yaml_text = yaml_text.replace("<project_slug>", slug)
    yaml_text = yaml_text.replace("<Project Title>", title)
    (dest / "project.yaml").write_text(yaml_text, encoding="utf-8")

    create_empty_file(dest / "idea/question_intake.json")
    create_empty_file(dest / "idea/anchor_references.md")
    copy_template(repo_root, "templates/references/elicit_systematic_review_config.json", dest / "idea/elicit_systematic_review_config.json")
    create_empty_file(dest / "idea/elicit_search.csv")
    create_empty_file(dest / "idea/elicit_screen.csv")
    create_empty_file(dest / "idea/elicit_fulltext.csv")
    create_empty_file(dest / "idea/elicit_extract.csv")
    create_empty_file(dest / "idea/prior_literature.md")
    create_empty_file(dest / "idea/gap_map.csv")
    create_empty_file(dest / "idea/contribution_scorecard.json")
    create_empty_file(dest / "idea/alternative_questions.json")
    create_empty_file(dest / "idea/topic_decision.md")

    create_empty_file(dest / "notes/idea_notes.md")
    create_empty_file(dest / "notes/project_notes.md")
    create_empty_file(dest / "notes/meeting_notes.md")
    create_empty_file(dest / "notes/decision_log.md")
    create_empty_file(dest / "notes/identification.md")
    create_empty_file(dest / "notes/estimand_registry.csv")
    create_empty_file(dest / "notes/assumption_register.csv")
    create_empty_file(dest / "notes/data_requirements.yaml")
    create_empty_file(dest / "notes/robustness_plan.csv")
    create_empty_file(dest / "notes/pap.md")
    write_text(dest / "notes/identification_status.json", "{\n  \"status\": \"redesign\"\n}\n")
    create_empty_file(dest / "notes/run_log.md")
    copy_template(repo_root, "templates/writing/journal_target_profile.md", dest / "notes/journal_target_profile.md")

    copy_template(repo_root, "templates/references/README.md", dest / "references/README.md")
    create_empty_file(dest / "references/reference_by_human/ref.bib")
    create_empty_file(dest / "references/reference_by_human/notes.md")
    create_empty_file(dest / "references/reference_by_human/paper_registry.jsonl")
    create_empty_file(dest / "references/reference_by_ai/ref.bib")
    create_empty_file(dest / "references/reference_by_ai/paper_registry.jsonl")
    create_empty_file(dest / "references/reference_by_ai/reference_overview.csv")
    create_empty_file(dest / "references/reference_by_ai/screening_notes.md")
    create_empty_file(dest / "references/reference_merged/ref.bib")
    create_empty_file(dest / "references/reference_merged/approved_papers.jsonl")
    create_empty_file(dest / "references/reference_merged/literature_review.md")

    copy_template(repo_root, "templates/stata/00_build_sample.do", dest / "code/build/00_build_sample.do")
    copy_template(repo_root, "templates/stata/00_setup.do", dest / "code/00_setup.do")
    copy_template(repo_root, "templates/stata/01_estimation.do", dest / "code/01_estimation.do")
    copy_template(repo_root, "templates/stata/02_robustness.do", dest / "code/02_robustness.do")
    copy_template(repo_root, "templates/stata/03_figures.do", dest / "code/03_figures.do")
    copy_template(repo_root, "templates/stata/04_tables.do", dest / "code/04_tables.do")
    copy_template(repo_root, "templates/stata/99_master.do", dest / "code/99_master.do")

    write_text(dest / "output/README.md", "# Output\n\n`raw/` is case-specific raw output. `figures/` and `tables/` are cleaned paper-ready artifacts.\n")
    copy_template(repo_root, "templates/writing/main.tex", dest / "draft/main.tex")
    copy_template(repo_root, "templates/writing/figure_wrapper.tex", dest / "draft/figures/figure_main_result.tex")
    copy_template(repo_root, "templates/writing/table_wrapper.tex", dest / "draft/tables/table_main_results.tex")
    copy_template(repo_root, "templates/writing/results_packet.md", dest / "draft/results_packet.md")
    write_text(dest / "work/README.md", "# Work\n\nExploratory branches live here. Promote only after human review.\n")
    write_text(dest / "paper/README.md", "# Paper\n\nSubmission-stage TeX copy and replication package.\n")
    copy_template(repo_root, "templates/submission/replication_README.md", dest / "paper/replication_package/README.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", required=True, help="Destination project folder. Should be outside the skill repo.")
    parser.add_argument("--slug", required=True, help="Project slug.")
    parser.add_argument("--title", default=None, help="Human-readable project title.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    dest = Path(args.dest).expanduser().resolve()

    title = args.title
    if title is None:
        title = args.slug.replace("-", " ").title()

    scaffold_project(dest, args.slug, title, repo_root)


if __name__ == "__main__":
    main()
