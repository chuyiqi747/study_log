# 11.07 练习：文件读写（读 .txt / .csv，并写回汇总）
# 跑法：python 11.07_file_io.py
# 数据在同目录 data/ 下；脚本用 Path(__file__) 定位，从任何目录启动都能找到

from pathlib import Path
import csv
from collections import defaultdict

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

print("[0] 当前工作目录:", Path.cwd())
print("[0] 数据目录(相对脚本定位):", DATA)

# ---------- 1. 读 txt：with + encoding ----------
print("\n=== 1. 读 txt（with + utf-8）===")
with open(DATA / "notes.txt", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.rstrip()}")

# 编码坑演示：故意用 gbk 解 utf-8 中文
print("\n[1] 编码坑演示（故意用 gbk 读 utf-8 文件）:")
try:
    with open(DATA / "notes.txt", encoding="gbk") as f:
        f.read()
    print("  这次没报错（本机默认编码不同），但规则不变：中文一律显式 utf-8")
except UnicodeDecodeError as e:
    print("  果然崩了 ->", type(e).__name__, "：用错密码本解字节")

# ---------- 2. 三种读法 ----------
print("\n=== 2. 三种读法对比 ===")
with open(DATA / "notes.txt", encoding="utf-8") as f:
    whole = f.read()
with open(DATA / "notes.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("  read() 字符数:", len(whole))
print("  readlines() 行数:", len(lines), "| 第一行:", repr(lines[0]))
print("  for line in f（推荐，逐行低成本）:")
with open(DATA / "notes.txt", encoding="utf-8") as f:
    for line in f:
        print("   ", line.rstrip())

# ---------- 3. CSV：split(',') 是错的 ----------
print("\n=== 3. 为什么不能用 split(',') ===")
with open(DATA / "scores.csv", encoding="utf-8", newline="") as f:
    raw_lines = f.read().splitlines()
bad = raw_lines[1].split(",")
print("  split(',') 切出", len(bad), "列:", bad)
with open(DATA / "scores.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
print("  csv.reader 表头:", header)
print("  csv.reader 切出", len(rows[0]), "列:", rows[0])

# ---------- 4. DictReader 按列名取 ----------
print("\n=== 4. DictReader：每行变字典 ===")
with open(DATA / "scores.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(f"  {row['姓名']} / {row['科目']} / {row['分数']} / {row['备注'] or '(空)'}")

# ---------- 5. 综合项目：统计平均分并写回报告 ----------
print("\n=== 5. 综合项目：读 CSV -> 统计 -> 写 report.txt ===")
scores = defaultdict(list)
with open(DATA / "scores.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        if not row["分数"].strip():      # 跳过缺考（空分数）
            continue
        scores[row["姓名"]].append(int(row["分数"]))   # 文本转整数！

result = sorted(
    ((name, sum(ns) / len(ns)) for name, ns in scores.items()),
    key=lambda kv: kv[1], reverse=True,
)
report = "成绩汇总（按平均分降序）\n"
report += "\n".join(f"  {name}: {avg:.1f}" for name, avg in result) + "\n"
with open(DATA / "report.txt", "w", encoding="utf-8") as f:
    f.write(report)
print(report.rstrip())
print("  已写出:", DATA / "report.txt")

# ---------- 6. 写文件：'w' 覆盖 vs 'a' 追加 ----------
print("\n=== 6. 写文件：'w' 覆盖 vs 'a' 追加 ===")
with open(DATA / "log_demo.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(["第一行", "第二行"]) + "\n")
with open(DATA / "log_demo.txt", "a", encoding="utf-8") as f:
    print("第三行（追加）", file=f)
with open(DATA / "log_demo.txt", encoding="utf-8") as f:
    print(f.read().rstrip())
