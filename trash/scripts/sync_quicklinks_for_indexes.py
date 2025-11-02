#!/usr/bin/env python3
"""
为所有 `04-code/index.html` 与 `06-练习/index.html` 页面同步插入/替换统一的快速链接区域。

策略：
 - 遍历 `menu_JS` 下所有目录，查找路径匹配 `*/04-code/index.html` 和 `*/06-练习/index.html`。
 - 对于每个 index.html：
     * 计算所属的天次目录 (parent of the `04-code` or `06-练习` folder)
     * 在天次目录内寻找笔记目录（优先 `03-笔记`，其次 `02-笔记`），并选择 README.md 或首个 .md 文件作为笔记目标
     * 寻找 PPT 目录（优先 `01-PPT` / `01-ppt`），并选取首个 .pdf 文件作为目标；若无 pdf，则指向 PPT 目录（若存在）或回退到主 `menu/09-PDF/`
     * 生成统一的 HTML 快速链接片段，并替换原文件中已有的 `<div class="quick-links">...</div>`（若存在），否则插入到 `</header>` 之后

用法: 在仓库根目录运行
    python .\scripts\sync_quicklinks_for_indexes.py

输出：打印修改的文件列表与为每个文件选择的笔记/PDF 路径。
"""
import re
from pathlib import Path
import os
import sys


ROOT = Path(".")


def find_note(day_dir: Path):
    # possible note dirs
    for name in ("03-笔记", "02-笔记"):
        p = day_dir / name
        if p.exists() and p.is_dir():
            # prefer README.md
            readme = p / "README.md"
            if readme.exists():
                return readme.relative_to(ROOT)
            # else find any .md
            mds = sorted(p.glob("*.md"))
            if mds:
                return mds[0].relative_to(ROOT)
    return None


def find_ppt(day_dir: Path):
    for name in ("01-PPT", "01-ppt"):
        p = day_dir / name
        if p.exists() and p.is_dir():
            # find pdf
            pdfs = sorted(p.glob("*.pdf"))
            if pdfs:
                return pdfs[0].relative_to(ROOT)
            # no pdf, return folder
            return p.relative_to(ROOT)
    # fallback to global PDF folder
    global_pdf = Path("menu/09-PDF")
    if global_pdf.exists():
        return global_pdf
    return None


def make_quicklinks_html(note_target, ppt_target):
    parts = []
    parts.append('            <div class="quick-links">')
    parts.append('                <a href="../06-练习/index.html" class="quick-link secondary">我的练习</a>')
    if note_target:
        parts.append(f'                <a href="{note_target.as_posix()}" class="quick-link secondary">查看笔记</a>')
    else:
        parts.append('                <a href="../../../../StudyLog_JS" class="quick-link secondary">查看笔记</a>')
    parts.append('                <a href="../../../../StudyLog_JS" class="quick-link secondary">查看我的笔记</a>')
    if ppt_target:
        parts.append(f'                <a href="{ppt_target.as_posix()}" class="quick-link accent">查看PDF资料</a>')
    else:
        parts.append('                <a href="menu/09-PDF/" class="quick-link accent">查看PDF资料</a>')
    parts.append('                <a href="../../../../index.html" class="quick-link">返回主索引</a>')
    parts.append('            </div>')
    return "\n".join(parts)


def process_index(idx_path: Path):
    content = idx_path.read_text(encoding='utf-8')
    day_dir = idx_path.parent.parent

    note = find_note(day_dir)
    ppt = find_ppt(day_dir)

    qhtml = make_quicklinks_html(note, ppt)

    # replace existing quick-links block
    new_content = None
    m = re.search(r"<div\s+class=\"quick-links\">.*?</div>", content, flags=re.S)
    if m:
        new_content = content[:m.start()] + qhtml + content[m.end():]
    else:
        m2 = re.search(r"</header>", content, flags=re.I)
        if m2:
            insert_pos = m2.end()
            new_content = content[:insert_pos] + "\n" + qhtml + content[insert_pos:]
        else:
            m3 = re.search(r"<body[^>]*>", content, flags=re.I)
            if m3:
                insert_pos = m3.end()
                new_content = content[:insert_pos] + "\n" + qhtml + content[insert_pos:]
            else:
                print(f"无法在 {idx_path} 找到插入点，跳过。")
                return False, note, ppt

    idx_path.write_text(new_content, encoding='utf-8')
    return True, note, ppt


def main():
    root = Path("menu_JS")
    if not root.exists():
        print("未找到 menu_JS 目录，确保在仓库根目录运行脚本。")
        return 1

    targets = list(root.rglob('04-code/index.html')) + list(root.rglob('06-练习/index.html'))
    targets = sorted(set(targets))
    if not targets:
        print("未找到目标 index.html 文件。")
        return 0

    modified = []
    for t in targets:
        ok, note, ppt = process_index(t)
        if ok:
            modified.append((str(t), str(note) if note else None, str(ppt) if ppt else None))

    print(f"处理完毕，共修改 {len(modified)} 个 index.html 文件：")
    for path, note, ppt in modified:
        print(f" - {path}\n    笔记 -> {note}\n    PPT -> {ppt}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
