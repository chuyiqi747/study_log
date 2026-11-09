# -*- coding: utf-8 -*-
"""
11-09 · 类跟写：定义一个待办 / 记账类（属性 + 方法）

运行：python 11.09_class_todo.py
六段演示一次跑完；每段对应 教程_2026-11-09.md 里的一节。
"""
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def hr(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


# ── 0. self 是什么 ────────────────────────────────────────────
hr("第 0 段｜self 是什么：定义写 2 个参数，调用只给 1 个")


class Demo:
    def __init__(self, name):
        print(f"  [__init__ 执行] self 是刚造好的对象，收到 name={name!r}")
        self.name = name          # 给"这个柜子"装一个抽屉

    def say(self, word):
        return f"{self.name} 说：{word}"


d = Demo("小柜子")
print("  d.say('你好')        ->", d.say("你好"))
print("  Demo.say(d, '你好')  ->", Demo.say(d, "你好"))
print("  两种写法结果相同?    ->", d.say("你好") == Demo.say(d, "你好"))
print("  [结论] self 就是 d 自己；d.say(x) 是 Demo.say(d, x) 的简写")


# ── 1. 最小类（跟写 1） ───────────────────────────────────────
hr("第 1 段｜跟写 1：最小类 Task（属性 + 方法 + __repr__）")


class Task:
    def __init__(self, title, priority="普通"):
        self.title = title
        self.priority = priority
        self.done = False         # 刚建好，默认未完成

    def mark_done(self):
        self.done = True          # 改自己的属性

    def __repr__(self):
        mark = "已完成" if self.done else "未完成"
        return f"Task({mark} {self.title} / {self.priority})"


t1 = Task("写周记")
t2 = Task("复习类", "高")
print("  刚造好:", t1, "|", t2)
t1.mark_done()
print("  t1.mark_done() 之后:", t1, "|", t2, " <- t2 完全没被影响")
print("  若不写 __repr__，打印出来是 <__main__.Task object at 0x...>")


# ── 2. 待办本（跟写 2） ───────────────────────────────────────
hr("第 2 段｜跟写 2：待办本 TodoList（自带列表 + 一组方法）")


class TodoList:
    def __init__(self, owner="我"):
        self.owner = owner
        self.items = []           # 关键：每个待办本自带一份空列表

    def add(self, title, priority="普通"):
        self.items.append(Task(title, priority))   # append：没有 = 也改了数据

    def done(self, title):
        for t in self.items:
            if t.title == title:
                t.mark_done()
                return True
        return False

    def pending(self):
        return [t for t in self.items if not t.done]   # 列表推导式

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"TodoList({self.owner}, 共{len(self)}项, 未完成{len(self.pending())}项)"


todo = TodoList()
todo.add("写周记")
todo.add("复习类", "高")
todo.add("跑步")
print("  加了 3 项:", todo)
print("  全部明细:", todo.items)
todo.done("写周记")
print("  完成'写周记'后待办:", todo.pending())


# ── 3. 记账本（跟写 3） ───────────────────────────────────────
hr("第 3 段｜跟写 3：记账本 Ledger（字典分组，接上 11-06）")


class Ledger:
    def __init__(self):
        self.records = []

    def add(self, item, amount, category="其他"):
        self.records.append({"项目": item, "金额": amount, "分类": category})

    @property
    def balance(self):
        return sum(r["金额"] for r in self.records)   # 像属性一样用，不加括号

    def by_category(self):
        sums = defaultdict(float)
        for r in self.records:
            sums[r["分类"]] += r["金额"]
        return dict(sums)


book = Ledger()
book.add("午饭", -25, "餐饮")
book.add("工资", 8000, "收入")
book.add("地铁", -4, "交通")
book.add("晚饭", -30, "餐饮")
print("  账单:", book.records)
print("  余额 book.balance（没括号）:", book.balance)
print("  按分类汇总:", book.by_category())


# ── 4. 两个必踩的坑 ───────────────────────────────────────────
hr("第 4 段｜两个坑：'每个对象一份' vs '大家共用一份'")


class BadList:
    items = []                    # 写在类里 = 所有对象共用同一个列表

    def add(self, x):
        self.items.append(x)


a, b = BadList(), BadList()
a.add("A 的任务")
print("  坑① 类属性 items=[] : a 加一条后，b.items =", b.items, " <- 串了")


class BadDefault:
    def __init__(self, items=[]):  # 可变默认参数：这个列表只造一次
        self.items = items


c, e = BadDefault(), BadDefault()
c.items.append("C 的任务")
print("  坑② 默认参数 items=[]: c 加一条后，e.items =", e.items, " <- 也串了")


class GoodList:
    def __init__(self):
        self.items = []           # 每次造对象都新建一份

    def add(self, x):
        self.items.append(x)


g, h = GoodList(), GoodList()
g.add("G 的任务")
print("  正确写法 __init__ 里 self.items=[] : h.items =", h.items, " <- 干净")
print("  [呼应] defaultdict(list) 用'配方'每次造新列表，正是同一个道理")


# ── 5. 进阶：dataclass ────────────────────────────────────────
hr("第 5 段｜进阶：@dataclass 帮你自动写 __init__ / __repr__")


@dataclass
class Entry:
    item: str
    amount: float
    category: str = "其他"
    note: str = ""


e1 = Entry("午饭", -25, "餐饮")
print("  自动生成:", e1)
print("  可直接比较:", e1 == Entry("午饭", -25, "餐饮"))
print("  字段注解:", Entry.__annotations__)


# ── 6. 综合项目：存 / 读 CSV（接上 11-07） ─────────────────────
hr("第 6 段｜综合项目：TodoBook 存进 CSV 再读回来")


class TodoBook(TodoList):
    """在 TodoList 的图纸上加两个按钮：save / load"""

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        # newline="" 把换行交给 csv 模块；utf-8 保证中文不乱码
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["标题", "优先级", "完成"])
            w.writeheader()
            for t in self.items:
                w.writerow({"标题": t.title, "优先级": t.priority,
                            "完成": "是" if t.done else "否"})
        return path

    @classmethod
    def load(cls, path, owner="我"):
        obj = cls(owner)
        # utf-8-sig：自动吃掉可能存在的 BOM（11-07 踩过的坑）
        with open(path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                t = Task(row["标题"], row["优先级"])
                if row["完成"] == "是":
                    t.mark_done()
                obj.items.append(t)
        return obj


path = DATA / "todos.csv"
my = TodoBook("学习者")
my.add("写周记")
my.add("复习类", "高")
my.done("写周记")
my.save(path)
print("  已写出:", path.name)
back = TodoBook.load(path, owner="学习者")
print("  读回来:", back)
print("  明细:", back.items)
print("  未完成:", [t.title for t in back.pending()])
