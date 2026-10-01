"""Validate the integrated figure library and run representative Python examples."""
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from figure_catalog import select

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/empirical-econ-figures'
GALLERY = ROOT/'gallery/empirical-econ-figures'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--check-tracked',action='store_true',help='Require all bundled skill and gallery files to be present in the Git index.')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'work/figure_validation')
    args=parser.parse_args()
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    catalog=json.loads((SKILL/'references/catalog.json').read_text(encoding='utf-8'))
    rows=catalog['templates'];assert len(rows)==50 and len(catalog['targets'])==40
    ids=[r['display_id'] for r in rows];assert len(set(ids))==50
    for row in rows:
        paths=[row['recipe'],row['schema'],*row['example_inputs'],*row.get('shared_resources',[])]
        paths += [x for values in row['entrypoints'].values() for x in values]
        paths += [v[k] for v in row.get('command_variants',[]) for k in ['entrypoint','runner','methods','manifest','native_entrypoint'] if v.get(k)]
        for name in paths:
            p=(SKILL/name).resolve();assert p.is_relative_to(SKILL.resolve()) and p.is_file(),name
    assert select(catalog,figure_id='A01')[0]['id']=='event_study_with_pre_post_averages'
    assert select(catalog,figure_id='event_study_pre_post_averages')[0]['display_id']=='A01'
    assert select(catalog,figure_id='A04',code_language='python')==[]
    event_rows=select(catalog,category='reduced_form',tag='Event study',code_language='stata')
    assert {'A01','A02','A03'}.issubset({r['display_id'] for r in event_rows})
    assert select(catalog,category='summary',code_language='python')
    assert not list(SKILL.rglob('*.png')) and not list(GALLERY.rglob('*.pdf'))
    pngs=list(GALLERY.rglob('*.png'));assert len(pngs)==97
    from PIL import Image
    for p in pngs:
        assert '__source_reference' not in p.name and not any(x in p.stem.split('_') for x in ['cn','zh'])
        with Image.open(p) as im:im.verify()
    pages=list(SKILL.rglob('*.md'))
    for p in pages:
        if not p.name.endswith('.zh-CN.md'):
            assert p.with_name(p.stem+'.zh-CN.md').exists(),p
        assert '[English]' in p.read_text(encoding='utf-8') and '[中文]' in p.read_text(encoding='utf-8'),p
    docs=[ROOT/'README.md',ROOT/'README.zh-CN.md',*pages,*GALLERY.glob('*.md'),ROOT/'docs/figure-integration.md',ROOT/'docs/figure-integration.zh-CN.md']
    links=0
    for p in docs:
        body=re.sub(r'```.*?```','',p.read_text(encoding='utf-8'),flags=re.S)
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',body):
            parsed=urlsplit(target.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            assert (p.parent/unquote(parsed.path)).resolve().is_file(),(p,target)
            links+=1
    for p in SKILL.rglob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
    for p in GALLERY.glob('*.md'):
        body=p.read_text(encoding='utf-8')
        assert len(re.findall(r'^\| [A-E]\d{2} \|',body,re.M))==50
        assert not re.search(r'!\[[^\]]*\]\(',body)
    checked=0
    tracked=None
    if args.check_tracked:
        proc=subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True,check=True)
        tracked=set(proc.stdout.decode('utf-8').split('\0'))
        required=[SKILL/'SHA256SUMS.txt',*pngs,*GALLERY.glob('*.md')]
        for p in required:assert p.relative_to(ROOT).as_posix() in tracked,('untracked bundle file',str(p))
    for line in (SKILL/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest,name=line.split('  ',1);p=SKILL/name
        assert p.resolve().is_relative_to(SKILL.resolve())
        assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
        if tracked is not None:assert p.relative_to(ROOT).as_posix() in tracked,('untracked skill resource',name)
        checked+=1
    runs=[]
    if args.smoke:
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
        def run(name,script,arguments,expected):
            proc=subprocess.run([sys.executable,'-X','utf8',str(script),*map(str,arguments)],cwd=out,env=env,capture_output=True,text=True,encoding='utf-8')
            (out/(name+'.log')).write_text(proc.stdout+proc.stderr,encoding='utf-8')
            assert proc.returncode==0,(name,proc.stderr)
            assert all(p.is_file() for p in expected),name
            runs.append({'case':name,'exit_code':proc.returncode})
        def folder(figure_id):return SKILL/Path(select(catalog,figure_id=figure_id)[0]['recipe']).parent
        a01=folder('A01');dest=out/'a01'
        run('actual_panel',a01/'event_study_with_pre_post_averages.py',['--output',dest],[dest/'event_study_with_pre_post_averages_python.png'])
        import csv
        contrast=list(csv.DictReader((dest/'event_study_with_pre_post_averages_python_contrast.csv').open(encoding='utf-8')))[0]
        expected=next(r for r in csv.DictReader((a01/'demo_contrasts.csv').open(encoding='utf-8')) if r['estimand']=='static_did')
        for field in ['estimate','se','ci_low','ci_high']:assert abs(float(contrast[field])-float(expected[field]))<1e-12
        trend=next(r for r in rows if r['id']=='multi_series_time_trend');base=SKILL/Path(trend['recipe']).parent
        dest=out/'trend.png'
        run('shared_line',base/'plot.py',['--input',base/'custom_demo.csv','--config',base/'custom_config.json','--output',dest,'--lang','en'],[dest])
        base=folder('A03');dest=out/'staggered'
        run('saved_stata_estimates',base/'plot_python.py',['--input',base/'audited_estimates.csv','--output-stem',dest],[dest.with_suffix('.png')])
    result={'status':'PASS','accepted_variants':50,'drawing_targets':40,'gallery_pngs':97,'checked_local_links':links,'manifest_records':checked,'tracked_bundle_checked':args.check_tracked,'python_runs':runs,'fresh_stata_run':False}
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
