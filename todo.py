# -*- coding: utf-8 -*-
"""
todo.py —— 只放「数据 + 行为」，不碰文件、不组织业务流程。

两种身份：
  被 import 时  -> 提供 Task / TodoList / Ledger 给别人用
  直接运行时    -> 跑末尾的自测块（if __name__ == "__main__"）
"""
from __future__ import annotations

from collections import defaultdict

# ↓ 顶层代码：import 时会真的执行一遍。
#   真实项目别在顶层放 print（这叫"副作用"），这里特意留着，让你亲眼看见加载过程。
print(f"[todo.py] 顶层代码执行了，此时 __name__ = {__name__!r}")


class Task:
    """一条待办"""

    def __init__(self, title, priority="普通"):
        self.title = title
        self.priority = priority
        self.done = False

    def mark_done(self):
        self.done = True

    def __repr__(self):
        mark = "已完成" if self.done else "未完成"
        return f"Task({mark} {self.title} / {self.priority})"


class TodoList:
    """一个待办本：每个对象自带一份列表"""

    def __init__(self, owner="我"):
        self.owner = owner
        self.items = []

    def add(self, title, priority="普通"):
        self.items.append(Task(title, priority))

    def done(self, title):
        for t in self.items:
            if t.title == title:
                t.mark_done()
                return True
        return False

    def pending(self):
        return [t for t in self.items if not t.done]

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"TodoList({self.owner}, 共{len(self)}项, 未完成{len(self.pending())}项)"


class Ledger:
    """记账本（11-09 跟写 3 搬过来的，用来证明"拆文件不改类"）"""

    def __init__(self):
        self.records = []

    def add(self, item, amount, category="其他"):
        self.records.append({"项目": item, "金额": amount, "分类": category})

    @property
    def balance(self):
        return sum(r["金额"] for r in self.records)

    def by_category(self):
        sums = defaultdict(float)
        for r in self.records:
            sums[r["分类"]] += r["金额"]
        return dict(sums)


# ── 只有「直接运行本文件」才会执行 ─────────────────────────────
if __name__ == "__main__":
    print("—— 这段是 todo.py 的自测，被 import 时不会出现 ——")
    demo = TodoList("自测")
    demo.add("试一条")
    demo.add("再试一条", "高")
    demo.done("试一条")
    print("   ", demo)
    print("   未完成:", demo.pending())
