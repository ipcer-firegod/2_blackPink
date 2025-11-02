import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / 'menu_JS'

def is_day_dir(p: Path):
    # treat directories with names starting with 'd' or containing 'd' followed by a digit as day folders
    name = p.name
    return name.startswith('d') or name.startswith('D')

def gather_htmls(day_dir: Path):
    htmls = []
    for p in day_dir.rglob('*.html'):
        # skip index files in 02-code/04-code/06-练习 etc
        if p.name.lower() == 'index.html':
            continue
        # skip files inside 06-练习
        if '06-练习' in p.parts:
            continue
        htmls.append(p)
    # sort by path for deterministic order
    htmls.sort()
    return htmls

def make_index(day_dir: Path, html_paths):
    code_dir = day_dir / '04-code'
    code_dir.mkdir(parents=True, exist_ok=True)
    index_path = code_dir / 'index.html'

    rel_to = code_dir

    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append('<html lang="zh-CN">')
    lines.append('<head>')
    lines.append('    <meta charset="UTF-8">')
    lines.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append(f'    <title>{day_dir.name} - 代码索引</title>')
    lines.append('    <link rel="stylesheet" href="../../../../css/3_menu_code.css">')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('    <div class="container">')
    lines.append('        <header>')
    lines.append(f'            <h1 style="color: white;">{day_dir.name} - 代码示例</h1>')
    lines.append(f'            <p>本章节包含{day_dir.name}的学习示例</p>')
    lines.append('        </header>')
    lines.append('        ') 
    lines.append('        <div class="quick-links">')
    lines.append('            <a href="../06-练习/index.html" class="quick-link secondary">我的练习</a>')
    lines.append('            <a href="../03-笔记/README.md" class="quick-link secondary">查看笔记</a>')
    lines.append('            <a href="../../../../StudyLog_JS" class="quick-link secondary">查看我的笔记</a>')
    lines.append('            <a href="../01-ppt/" class="quick-link accent">查看PDF资料</a>')
    lines.append('            <a href="../../../../index.html" class="quick-link">返回主索引</a>')
    lines.append('        </div>')
    lines.append('')
    lines.append('        <section>')
    lines.append('            <h2>示例文件列表</h2>')
    lines.append('            <ul>')

    for p in html_paths:
        try:
            rel = os.path.relpath(p, rel_to)
        except Exception:
            rel = str(p)
        # normalize to forward slashes for href
        href = rel.replace('\\\\', '/').replace('\\', '/')
        text = p.name
        lines.append(f'                <li><a href="{href}">{text}</a></li>')

    lines.append('            </ul>')
    lines.append('        </section>')
    lines.append('')
    lines.append('        <footer>')
    lines.append('            <p>© 2025 JS 技术学习资料 | 持续更新中</p>')
    lines.append('        </footer>')
    lines.append('</body>')
    lines.append('</html>')

    index_path.write_text('\n'.join(lines), encoding='utf-8')
    return index_path

def main():
    if not MENU.exists():
        print('menu_JS not found at', MENU)
        return

    processed = []

    # walk immediate subfolders of menu_JS
    for module in MENU.iterdir():
        if not module.is_dir():
            continue
        for day in module.iterdir():
            if not day.is_dir():
                continue
            # treat day folders as those starting with 'd' or containing 'day' or numeric prefix
            if not (day.name.lower().startswith('d') or day.name[0].isdigit()):
                # still process if it contains 02-code or 04-code
                pass

            # gather html files excluding indexes and 06-练习
            htmls = gather_htmls(day)
            if not htmls:
                # if no html examples, skip
                continue

            # create/update 04-code/index.html
            idx = make_index(day, htmls)

            # remove 02-code/index.html if exists
            old_index = day / '02-code' / 'index.html'
            if old_index.exists():
                try:
                    old_index.unlink()
                    removed = True
                except Exception:
                    removed = False
            else:
                removed = False

            processed.append((str(day), str(idx), removed, len(htmls)))

    print('Processed:', len(processed), 'day folders')
    for p in processed:
        print(p)

if __name__ == '__main__':
    main()
