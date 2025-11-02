#!/usr/bin/env python3
"""
将所有 `06-练习/index.html` 中 quick-links 的 “我的练习” 锚点替换为指向 `../04-code/index.html` 的 “查看代码”。

用法：在仓库根运行
    python ./scripts/update_06_exer_links.py
"""
from pathlib import Path
import re
import sys


def process(path: Path):
    txt = path.read_text(encoding='utf-8')
    # match anchor that links to ../06-练习/index.html and replace whole anchor
    pattern = re.compile(r'<a\s+href="\.\./06-练习/index\.html"[^>]*>\s*我的练习\s*</a>', re.I)
    replacement = '<a href="../04-code/index.html" class="quick-link secondary">查看代码</a>'
    new_txt, n = pattern.subn(replacement, txt, count=1)
    if n > 0:
        path.write_text(new_txt, encoding='utf-8')
        return True
    return False


def main():
    root = Path('menu_JS')
    if not root.exists():
        print('menu_JS not found; run from repo root')
        return 1

    targets = list(root.rglob('06-练习/index.html'))
    modified = []
    for t in targets:
        try:
            if process(t):
                modified.append(str(t))
        except Exception as e:
            print('Error processing', t, e)

    print(f'处理完成，共修改 {len(modified)} 个文件。')
    for m in modified:
        print(' -', m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
