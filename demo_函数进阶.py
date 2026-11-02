# -*- coding: utf-8 -*-
"""三个疑问的现场演示：可变默认参数 / *args **kwargs / 解包"""

print("=" * 55)
print("【演示 1】可变默认参数的陷阱：那个 [] 到底造了几次？")
print("=" * 55)

def add_item_bad(item, box=[]):
    print(f"  这次 box 的身份证 id = {id(box)}")
    box.append(item)
    return box

print("第一次调用 add_item_bad('苹果')：")
print("  返回值 =", add_item_bad("苹果"))
print("第二次调用 add_item_bad('香蕉')（我没传 box！）：")
print("  返回值 =", add_item_bad("香蕉"))
print("→ 注意看两次的 id 完全一样：它们是同一个列表。\n")

print("对照：用 None 做哨兵的正确写法")
def add_item_good(item, box=None):
    if box is None:          # 没给，就当场新建
        box = []
    print(f"  这次 box 的身份证 id = {id(box)}")
    box.append(item)
    return box

print("第一次调用：", add_item_good("苹果"))
print("第二次调用：", add_item_good("香蕉"))
print("→ id 变了：每次都是全新的空列表。\n")


print("=" * 55)
print("【演示 2】*args 和 **kwargs 是什么类型")
print("=" * 55)

def show(*args, **kwargs):
    print("  args   =", args,   "  类型:", type(args).__name__)
    print("  kwargs =", kwargs, "  类型:", type(kwargs).__name__)
    print("  求和 args:", sum(args))

show(1, 2, 3, name="小明", age=18)
print()

# 反过来：把列表/字典“拆开”喂进去
nums = [10, 20, 30]
info = {"name": "小红", "age": 20}
print("  把列表 nums 用 * 拆开传：")
show(*nums)
print("  把字典 info 用 ** 拆开传：")
show(**info)
print()


print("=" * 55)
print("【演示 3】为什么 value, msg = divide(...) 有两个变量")
print("=" * 55)

def divide(a, b):
    if b == 0:
        return None, "除数不能为 0"
    return a / b, "成功"

result = divide(10, 2)
print("  不拆包，整个接下来 result =", result, "  类型:", type(result).__name__)

value, msg = divide(10, 2)
print("  拆开后 value =", value, " | msg =", msg)

print("  其实 return a/b, '成功' 返回的是一个元组，等于同时交了两件东西")
print("  拆包 = 把元组里的元素，按位置一个个分给左边变量")
