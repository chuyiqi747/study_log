# -*- coding: utf-8 -*-
"""
main.py —— 程序入口：只负责「组装和使用」，不定义任何类。

运行：python main.py
（从别的目录用绝对路径运行也可以：python E:/sty_log/main.py）
"""
from __future__ import annotations

from pathlib import Path

import todo                              # ① 整个模块搬来，用 todo.xxx
from todo import Task, TodoList           # ② 只取需要的名字，直接用
from todo import TodoList as Book         # ③ 取过来顺手改个名
from storage import save_csv, load_csv    # ④ 从另一个模块取函数

DATA = Path(__file__).resolve().parent / "data"


def main():
    print("=== 身份与命名空间 ===")
    print("  main.py 里 __name__ =", repr(__name__))
    print("  todo.py 里 __name__ =", repr(todo.__name__))
    print("  todo.Task 和 Task 是同一个类吗? ->", todo.Task is Task)
    print("  Book 就是 TodoList 吗?          ->", Book is TodoList)
    print("  todo 模块里有这些公开名字       ->",
          [n for n in vars(todo) if not n.startswith("_")])

    print("\n=== 用 todo.py 里的类干活 ===")
    book = TodoList("学习者")
    book.add("写周记")
    book.add("复习模块拆分", "高")
    book.add("跑步")
    print("  ", book)
    book.done("写周记")
    print("  未完成:", [t.title for t in book.pending()])

    print("\n=== 再单独造一个 Task ===")
    one = Task("临时任务")
    print("  ", one)

    print("\n=== 交给 storage.py 存盘、再读回来 ===")
    path = save_csv(book, DATA / "todos_from_main.csv")
    print("  已写出:", path.name)
    back = load_csv(path, owner="学习者")
    print("  读回来:", back)
    print("  明细:", back.items)


if __name__ == "__main__":
    main()
