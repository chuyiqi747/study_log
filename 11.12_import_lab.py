# -*- coding: utf-8 -*-
"""
11.12_import_lab.py —— 观察 import 到底干了什么（六个实验）

运行：python 11.12_import_lab.py
每个实验用独立子进程跑，互不污染，输出可直接对照教程。
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run(*args, cwd=None):
    r = subprocess.run(
        [sys.executable, *args],
        cwd=cwd or HERE,
        capture_output=True, text=True, encoding="utf-8", env=ENV,
    )
    return (r.stdout + r.stderr).strip()


def hr(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


hr("实验 1｜import 会「执行」那个文件，不是把文字复制过来")
print("\n".join("  " + line for line in run("main.py").splitlines()[:4]))
print("  ↑ 第一行 [todo.py] 出现在 main 的所有输出之前：")
print("    import todo 时，todo.py 从头到尾被跑了一遍")

hr("实验 2｜同一个文件，两种身份：__name__ 不一样")
print("  A) 直接运行 todo.py：")
for line in run("todo.py").splitlines():
    print("     ", line)
print("  B) 被别人 import：")
for line in run("-c", "import todo").splitlines():
    print("     ", line)
print("  [结论] 直接跑时 __name__ == '__main__'（自测块执行）；")
print("         被 import 时 __name__ == 'todo'（自测块跳过）")

hr("实验 3｜重复 import 只执行一次（sys.modules 缓存）")
print("  " + run("-c", "import todo; import todo; import todo; print('三次 import 结束')"))
print("  [结论] 只有一行 [todo.py] 顶层输出 —— Python 缓存了已加载的模块")

hr("实验 4｜模块是一个「柜子」，点号就是按名字取")
print("  " + run(
    "-c",
    "import todo; from todo import Task; "
    "print('todo.Task is Task ->', todo.Task is Task); "
    "print('todo 里公开名字 ->', [n for n in vars(todo) if not n.startswith('_')])",
))

hr("实验 5｜去哪找模块：启动目录 vs 脚本所在目录")
print("  A) 在 E:/ 下执行 python -c 'import todo'：")
print("     ", run("-c", "import todo", cwd=HERE.parent).splitlines()[-1])
print("  B) 同样在 E:/ 下，但用绝对路径运行 main.py：")
print("     ", run(str(HERE / "main.py"), cwd=HERE.parent).splitlines()[0])
print("  [结论] sys.path[0] 是「入口脚本所在目录」（-c 时是当前目录）；")
print("         用绝对路径跑脚本，模块所在目录自动进 path，所以照样能 import")

hr("实验 6｜搜索顺序与命名冲突")
print("  " + run("-c", "import sys; print('sys.path 前3项:', sys.path[:3])"))
print("  [结论] 当前目录排在最前，所以别把自己的文件叫 csv.py / json.py / sys.py")
