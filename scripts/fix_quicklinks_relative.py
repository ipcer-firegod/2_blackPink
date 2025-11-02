#!/usr/bin/env python3
"""
修正 04-code/ 和 06-练习/ 下 index.html 中 quick-links 的路径：
将以仓库根相对的路径（以 'menu_JS/' 或 'menu/' 开头）转换为从该 index 文件位置出发的相对路径（使用 ../ 等）。

用法：在仓库根运行
    python .\scripts\fix_quicklinks_relative.py

该脚本只修改 href 中以 'menu_JS/' 或 'menu/' 开头的链接；其它链接保留不变。
"""
import re
from pathlib import Path
import sys
import os


ROOT = Path('.').resolve()


def fix_file(path: Path):
    text = path.read_text(encoding='utf-8')
    changed = False

    def repl(m):
        nonlocal changed
        href = m.group(1)
        # only fix links starting with menu_JS/ or menu/
        if href.startswith('menu_JS/') or href.startswith('menu/'):
            target = (ROOT / href).resolve()
            try:
                rel = os.path.relpath(str(target), start=str(path.parent))
            except Exception:
                rel = href
            # convert backslashes to forward slashes for HTML
            rel = rel.replace('\\', '/')
            changed = True
            return f'href="{rel}"'
        else:
            return m.group(0)

    new_text = re.sub(r'href="([^"]+)"', repl, text)
    if changed:
        path.write_text(new_text, encoding='utf-8')
    return changed


def main():
    root = ROOT / 'menu_JS'
    if not root.exists():
        print("未找到 menu_JS，退出")
        return 1

    targets = list(root.rglob('04-code/index.html')) + list(root.rglob('06-练习/index.html'))
    targets = sorted(set(targets))
    modified = []
    for t in targets:
        try:
            ok = fix_file(t)
            if ok:
                modified.append(str(t))
        except Exception as e:
            print(f"处理 {t} 时出错：{e}")

    print(f"处理完成，共修改 {len(modified)} 个文件。")
    for m in modified:
        print(' -', m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
