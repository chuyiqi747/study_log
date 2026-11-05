# 11.05 练习：字典 / 集合 / 字符串
# 跟写三个小例子，再完成进阶"词频统计"
# 跑法：python 11.05_dict_set_str.py

# ---------- 1. 字典计数 ----------
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
count = {}
for w in words:
    count[w] = count.get(w, 0) + 1
print("字典计数:", count)

# ---------- 2. 集合去重 ----------
nums = [1, 2, 2, 3, 3, 3, 1]
print("集合去重:", list(set(nums)))
# 保序去重
print("保序去重:", list(dict.fromkeys(nums)))
# 集合运算
a, b = {1, 2, 3}, {3, 4, 5}
print("交集:", a & b, " 并集:", a | b, " 差集:", a - b)

# ---------- 3. 字符串切分 ----------
s = "hello world python"
print("split():", s.split())
print("split('o'):", s.split('o'))
print("反转:", s[::-1])

# ---------- 进阶：词频统计 ----------
import string
from collections import Counter

text = "Python is great. Python is easy. I love python! Do you love Python?"
text = text.lower().translate(str.maketrans('', '', string.punctuation))
word_list = text.split()
counts = Counter(word_list)
print("\n词频 Top5:")
for word, n in counts.most_common(5):
    print(f"  {word}: {n}")

# 挑战：忽略停用词
stop = {'is', 'a', 'the', 'you', 'do'}
filtered = [w for w in word_list if w not in stop]
print("\n忽略停用词后 Top5:")
for word, n in Counter(filtered).most_common(5):
    print(f"  {word}: {n}")
