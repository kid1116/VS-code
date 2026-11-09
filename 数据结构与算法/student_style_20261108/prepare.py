from pathlib import Path
import shutil,json

target=Path(r'D:\VS code\58125117-吴天宇-第三次作业')
work=Path(__file__).resolve().parent
manifest=[]
for source in sorted(target.rglob('*.cpp')):
    relative=source.relative_to(target)
    backup=work/'original'/relative
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists():
        shutil.copy2(source,backup)
    manifest.append(str(relative))
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Backed up',len(manifest),'source files.')
