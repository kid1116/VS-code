from pathlib import Path
import json,hashlib,re,shutil

work=Path(__file__).resolve().parent
target=Path(r'C:\Users\12120\Desktop\58125117-吴天宇-第三次作业')
templates=work.parent/'student_style_20261108/modified'
backup=work/'original'
stage=work/'modified'
manifest=[]

for source in sorted(target.rglob('*.cpp')):
    relative=source.relative_to(target)
    template=templates/relative
    assert template.is_file(),relative
    old=source.read_bytes()
    original=backup/relative;original.parent.mkdir(parents=True,exist_ok=True)
    assert not original.exists(),'Backup already exists; do not overwrite originals.'
    original.write_bytes(old)
    text=template.read_text(encoding='utf-8-sig')
    assert not re.search(r'_WIN32|windows\.h|SetConsole|CP_UTF8|\bassert\s*\(|\bthrow\b|\btemplate\s*<|\bfilesystem\b|\bwmain\b',text),relative
    revised=stage/relative;revised.parent.mkdir(parents=True,exist_ok=True)
    revised.write_text(text,encoding='utf-8-sig')
    manifest.append({'source':str(revised),'destination':str(source),'relative':str(relative),'original_hash':hashlib.sha256(old).hexdigest()})

assert len(manifest)==6
protected={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob('*')
           if p.is_file() and p.suffix!='.cpp' and 'output' not in p.relative_to(target).parts}
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'protected_files.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared 6 student-style C++ files and backed up the desktop originals.')
for entry in manifest:
    old_lines=len(Path(entry['destination']).read_text(encoding='utf-8-sig').splitlines())
    new_lines=len(Path(entry['source']).read_text(encoding='utf-8-sig').splitlines())
    print(entry['relative'],str(old_lines)+' -> '+str(new_lines)+' lines')
