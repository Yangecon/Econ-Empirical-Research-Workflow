"""Discover supported figure interfaces; does not estimate or execute templates."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def select(catalog, figure_id=None, category=None, tag=None, code_language=None):
    rows = catalog['templates']
    if figure_id:
        key = figure_id.casefold()
        rows = [r for r in rows if key in {str(r.get(f, '')).casefold()
                                         for f in ['id', 'display_id', 'source_view_id', 'canonical_name']}]
    if category:
        rows = [r for r in rows if r['category'] == category]
    if tag:
        rows = [r for r in rows if any(tag.casefold() in t.casefold() for t in r['tags'])]
    if code_language:
        rows = [r for r in rows if code_language in r['languages']]
    return sorted(rows, key=lambda r: r['display_id'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-root', type=Path, default=ROOT/'skills/empirical-econ-figures')
    parser.add_argument('--id')
    parser.add_argument('--category', choices=['reduced_form', 'structural_form', 'summary', 'research_design', 'prediction_evaluation'])
    parser.add_argument('--tag')
    parser.add_argument('--code-language', choices=['python', 'stata'])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    catalog = json.loads((args.skill_root/'references/catalog.json').read_text(encoding='utf-8'))
    rows = select(catalog, args.id, args.category, args.tag, args.code_language)
    if not rows:
        parser.exit(1, 'No matching accepted template; try another category, tag or ID.\n')
    if args.json:
        print(json.dumps(rows, ensure_ascii=True, indent=2))
    else:
        for row in rows:
            print(f"{row['display_id']}  {row['canonical_name']}  [{', '.join(row['languages'])}]")
            print('  recipe: '+row['recipe'])
            print('  tags: '+', '.join(row['tags']))


if __name__ == '__main__':
    main()
