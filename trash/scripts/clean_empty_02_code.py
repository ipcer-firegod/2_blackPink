#!/usr/bin/env python3
"""
清理 menu_JS 下所有空的 `02-code` 目录。

用法: 在仓库根目录运行
    python .\scripts\clean_empty_02_code.py

脚本行为：递归遍历 `menu_JS`，查找名称为 `02-code` 的目录，
当且仅当该目录完全为空（没有文件也没有子目录）时，删除之。
输出被删除目录的列表和统计信息。
"""
import os
import sys
from pathlib import Path


def main():
    root = Path("menu_JS")
    if not root.exists() or not root.is_dir():
        print("未找到 'menu_JS' 目录，退出。请在仓库根目录运行脚本。")
        return 1

    removed = []
    failed = []

    # 从下往上遍历（topdown=False），确保可以删除空目录
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for d in list(dirnames):
            if d == '02-code':
                p = Path(dirpath) / d
                try:
                    # 认为 "空" 是指目录内没有任何项
                    if not any(p.iterdir()):
                        p.rmdir()
                        removed.append(str(p))
                    else:
                        # 目录非空，跳过
                        pass
                except Exception as e:
                    failed.append((str(p), str(e)))

    print(f"扫描完毕。共删除 {len(removed)} 个空的 '02-code' 目录。")
    if removed:
        print("已删除：")
        for r in removed:
            print(" -", r)
    if failed:
        print(f"删除失败 {len(failed)} 项：")
        for p, err in failed:
            print(" -", p, "错误：", err)

    return 0


if __name__ == '__main__':
    sys.exit(main())
