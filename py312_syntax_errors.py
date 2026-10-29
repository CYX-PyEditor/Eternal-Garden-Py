# py312_syntax_errors.py
# Python 3.12 语法错误全集

# ===== 1. 关键字 / 保留字被赋值 =====
class = 10
def return(): pass #不通过
True = 1
None = 2

# ===== 2. 缩进错误 =====
    unexpected_indent = 1  #不通过

def missing_indent():
print("no indent")

if True:
    x = 1
  y = 2

# ===== 3. 冒号缺失 =====
if True
    pass

def f()
    pass

for i in range(3)
    print(i)

while True
    break

class C
    pass

# ===== 4. 赋值目标非法 =====
5 = x
x + 1 = 2
foo() = 3

# ===== 5. 函数定义 / 调用错误 =====
def g(a=1, b): pass #不通过
def h(a, a): pass  #不通过
f(a=1, 2)  #f未成功定义不应认为有效

# ===== 6. 导入语法错误 =====
import os from sys  #不通过
from import x  # 不通过

# ===== 7. 数字字面量错误 =====
n = 012  #不通过
m = 1.2.3  #不通过
hx = 0x  #不通过
bn = 0b102  #不通过
oc = 0o8  #不通过

# ===== 8. 作用域错误（await / yield 在函数外）=====
await foo()  #不通过
yield 1#不通过

# ===== 9. 表达式错误 =====
x = *[1, 2]#不通过
y = **{"a": 1}#不通过

# ===== 10. 复合语句残缺 =====
else: pass#不通过
elif x: pass#不通过
except ValueError: pass#不通过
finally: pass#不通过

# ===== 11. 空语句块 =====
if True:
def f():

# ===== 12. PEP 695（3.12）type 语句错误 =====
type Alias#不通过
type Alias =
type Alias = int          # 合法对照行

def generic[T: pass
class C[T: pass

# ===== 13. PEP 701（3.12）f-string 错误 =====
f1 = f"{x"#不通过
f2 = f"{}"#不通过
f3 = f"{x!z}"#不通过

# ===== 14. 海象运算符错误 =====
if (x :=): pass#不通过

# ===== 15. except* 语法错误 =====
try: pass
except* : pass#不通过

# ===== 16. 字符串未闭合（吞掉本行剩余）=====
s = "hello  #不通过
t = 'world#不通过

# ===== 17. 括号未闭合（吞掉后续内容）=====
p = (1, 2, 3
q = [1, 2, 3
r = {"a": 1

# ===== 18. 三引号未闭合（吞掉文件剩余，必须放最后）=====
u = '''triple#不通过
