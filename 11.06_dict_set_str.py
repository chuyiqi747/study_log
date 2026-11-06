# 11.06 练习：字典 / 集合 / 字符串（巩固加深版）
# 今天不重复昨天：先钉死三个卡过的点，再用新武器，最后串成小项目
# 跑法：python 11.06_dict_set_str.py

from collections import Counter, defaultdict
import string

words = ["apple", "banana", "apple", "orange", "banana", "apple"]

# ---------- 0. 昨天卡过的三个点，跑一遍确认 ----------
# (1) 方括号的双重身份：字面量 vs 下标访问
lst = ["a", "b"]        # [] 造列表
d = {}                  # {} 造字典（不是空集合！）
d["a"] = 1              # [] 是"按键赋值"，不是把 d 变成列表
print("[0] 双重身份:", lst, d, "| lst[0] =", lst[0], "| d['a'] =", d["a"])

# (2) get 是软取，而且只读不写
print("[0] get 不存在的键:", d.get("pear", 0), "| 字典仍是:", d)

# (3) Counter 是 dict 的亲儿子
c = Counter(words)
print("[0] Counter 是 dict?:", isinstance(c, dict), "| 没数过的键:", c["pear"])

# ---------- 1. 字典：同一件计数的四种写法 ----------
c1 = {}
for w in words:
    c1[w] = c1.get(w, 0) + 1                 # ① get

c2 = {}
for w in words:
    c2[w] = c2.setdefault(w, 0) + 1          # ② setdefault

c3 = defaultdict(int)                         # ③ 循环体最干净
for w in words:
    c3[w] += 1

c4 = Counter(words)                           # ④ 一行出结果

print("\n[1] 四种写法结果一致?:", c1 == c2 == dict(c3) == dict(c4))
print("[1] 计数结果:", c1)

# items() 遍历 + 按值排序 + 字典推导式
print("[1] 按次数排序:", sorted(c1.items(), key=lambda kv: kv[1], reverse=True))
print("[1] 词频条形图:", {w: "*" * n for w, n in c1.items()})
print("[1] items() 遍历:")
for word, n in c1.items():
    print(f"      {word}: {n}")

# ---------- 2. 集合：从去重到做比较 ----------
py = {"python", "list", "dict", "set", "function"}
js = {"javascript", "array", "dict", "set", "function"}
print("\n[2] 两篇都提到:", sorted(py & js))
print("[2] 只有 Python:", sorted(py - js))
print("[2] 只有 JS:", sorted(js - py))
print("[2] 只出现在一边(^):", sorted(py ^ js))
print("[2] 全部概念(|):", sorted(py | js))
print("[2] 集合推导式(长度>3):", sorted({w for w in py | js if len(w) > 3}))
print("[2] 空集合 != 空字典:", set() != {})

# ---------- 3. 字符串：split 与 join 互逆 ----------
s = "hello world python"
parts = s.split()
back = " ".join(parts)
print("\n[3] split →", parts)
print("[3] join  →", repr(back), "| 还原成功?:", back == s)
print("[3] 换分隔符:", "a-b-c".split("-"), "->", "|".join("a-b-c".split("-")))

raw = "  Hello,  WORLD!!  "
cleaned = raw.strip().lower().replace(",", "").replace("!", "")
print("[3] 链式清洗:", repr(cleaned))

# ---------- 综合项目：两篇短文用词对比器 ----------
def normalize(text):
    """统一小写 → 去标点 → 切词。返回词列表（保留重复！）"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()


a = "Python is great. Python is easy. I love python lists and dicts."
b = "Python is popular. I love python sets and dicts too."
wa, wb = normalize(a), normalize(b)
sa, sb = set(wa), set(wb)

print("\n=== 用词对比器 ===")
print("两篇都用到:", sorted(sa & sb))
print("只在第一篇:", sorted(sa - sb))
print("只在第二篇:", sorted(sb - sa))
# 计数必须用保留重复的 wa/wb，不能用 sa/sb（集合去重后全是 1）
print("第一篇 Top3:", Counter(wa).most_common(3))
print("第二篇 Top3:", Counter(wb).most_common(3))

# 挑战：过滤停用词后再统计（自己先写，再看下一行）
stop = {"is", "a", "the", "i", "and", "too", "do", "you"}
fa = [w for w in wa if w not in stop]
fb = [w for w in wb if w not in stop]
print("\n[挑战] 过滤停用词后 第一篇 Top3:", Counter(fa).most_common(3))
print("[挑战] 过滤停用词后 第二篇 Top3:", Counter(fb).most_common(3))
