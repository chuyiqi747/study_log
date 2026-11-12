# -*- coding: utf-8 -*-
"""
storage.py —— 只管「对象 ↔ CSV 文件」，不定义业务类。

进阶第三步才用到：把 I/O 从类里搬出来，todo.py 就完全不依赖磁盘了。
注意这里 import 了 todo —— 模块之间也可以互相引用，方向是 main → storage → todo。
"""
from __future__ import annotations

import csv
from pathlib import Path

from todo import Task, TodoList

FIELDS = ["标题", "优先级", "完成"]


def save_csv(book, path):
    """把一个 TodoList 写成 CSV"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="" 交给 csv 管换行；utf-8 保证中文不乱码（11-07 的固定搭配）
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for t in book.items:
            w.writerow({"标题": t.title, "优先级": t.priority,
                        "完成": "是" if t.done else "否"})
    return path


def load_csv(path, owner="我"):
    """从 CSV 还原出一个 TodoList（返回的是对象，不是字典列表）"""
    book = TodoList(owner)
    # utf-8-sig：自动吞掉可能存在的 BOM（11-07 实跑踩过的坑）
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            t = Task(row["标题"], row["优先级"])
            if row["完成"] == "是":
                t.mark_done()
            book.items.append(t)
    return book
