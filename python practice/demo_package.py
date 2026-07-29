"""
demo_package.py - 演示 Python 包的用法

本文件演示了多种导入和使用包的方式：
1. import package                    - 导入整个包
2. from package import module        - 从包中导入模块
3. from package.module import func   - 从包的模块中导入函数
4. from package import *             - 导入 __all__ 中定义的所有内容
5. 相对导入（在包内部使用）
6. 子包的使用

运行方式：在 python practice 目录下运行
    python demo_package.py
"""

print("=" * 60)
print("Python 包 (Package) 用法演示")
print("=" * 60)

# ============================================================
# 方式 1：导入整个包
# 这会执行 mypackage/__init__.py
# ============================================================
print("\n>>> 方式 1: import mypackage")
import mypackage

print(f"\n包信息: {mypackage.package_info()}")
print(f"PI 常量: {mypackage.PI}")
print(f"__all__ 导出列表: {mypackage.__all__}")

# ============================================================
# 方式 2：从包中导入模块
# ============================================================
print("\n>>> 方式 2: from mypackage import math_utils")
from mypackage import math_utils as mu

# 使用导入的模块
print(f"10 + 5 = {mu.add(10, 5)}")
print(f"10 * 5 = {mu.multiply(10, 5)}")
print(f"10 / 3 = {mu.divide(10, 3):.2f}")
print(f"斐波那契前 10 项: {mu.fibonacci(10)}")
print(f"半径 5 的圆面积: {mu.circle_area(5):.2f}")

# ============================================================
# 方式 3：从包的模块中直接导入函数
# ============================================================
print("\n>>> 方式 3: from mypackage.string_utils import reverse, is_palindrome")
from mypackage.string_utils import reverse, is_palindrome, count_words

text = "Hello Python 包"
print(f'原文本: "{text}"')
print(f"反转:   {reverse(text)}")
print(f"单词数: {count_words(text)}")
print(f"'racecar' 是回文吗？ {is_palindrome('racecar')}")
print(f"'Python' 是回文吗？   {is_palindrome('Python')}")
print(f"'A man a plan a canal Panama' 是回文吗？ {is_palindrome('A man a plan a canal Panama')}")

# ============================================================
# 方式 4：使用子包 (subpkg)
# ============================================================
print("\n>>> 方式 4: from mypackage.subpkg import power, is_prime, safe_sqrt")
from mypackage.subpkg import power, is_prime, safe_sqrt, format_table

print(f"2^10 = {power(2, 10)}")
print(f"sqrt(16) = {safe_sqrt(16)}")
print(f"sqrt(-9) = {safe_sqrt(-9)}")
print(f"17 是素数吗？ {is_prime(17)}")
print(f"100 是素数吗？ {is_prime(100)}")

# 子包的表格功能
print("\n表格功能演示：")
headers = ["姓名", "年龄", "城市"]
data = [
    ["张三", 25, "北京"],
    ["李四", 30, "上海"],
    ["王五", 28, "广州"],
]
print(format_table(data, headers))

# ============================================================
# 方式 5：通过包层级访问子包中的函数
# ============================================================
print("\n>>> 方式 5: 通过 mypackage.subpkg.xxx 访问")
print(f"10 是素数吗？ {mypackage.subpkg.is_prime(10)}")

# ============================================================
# 方式 6：from package import * （受 __all__ 控制）
# ============================================================
print("\n>>> 方式 6: from mypackage import *")
from mypackage import *
# 注意：这里会导入 mypackage.__all__ 中列出的所有内容
# 但不包括 VERSION（它不在 __all__ 中）
print(f"PI = {PI}")  # PI 在 __all__ 中，可以直接访问
# print(VERSION)  # 这行会报错，因为 VERSION 不在 __all__ 中

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("总结：Python 包的关键概念")
print("=" * 60)
print("""
包的结构：
   mypackage/              <-- 包目录
   ├── __init__.py         <-- 包初始化文件（必须）
   ├── math_utils.py       <-- 模块
   ├── string_utils.py     <-- 模块
   └── subpkg/             <-- 子包
       ├── __init__.py
       └── advanced.py

关键概念：
   1. __init__.py 使目录成为包，可以包含初始化代码
   2. __all__ 控制 from package import * 的导出
   3. 相对导入 (. 和 ..) 用于包内部模块之间的引用
   4. 子包可以嵌套，形成层级结构
   5. 包可以有包级别的变量和函数
""")
