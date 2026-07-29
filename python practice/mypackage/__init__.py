"""
mypackage - 一个演示 Python 包用法的示例包

这个包展示了：
1. __init__.py 的作用（包初始化、导出控制）
2. __all__ 控制 from package import * 的行为
3. 包级别的变量和函数
"""

print(f"[Package] mypackage 被导入了！（__init__.py 执行）")

# __all__ 控制 from mypackage import * 时导出哪些名字
__all__ = ["math_utils", "string_utils", "package_info", "PI"]

# 包级别的常量
PI = 3.1415926535
VERSION = "1.0.0"

# 从子模块导入，方便用户直接通过 mypackage.xxx 访问
from . import math_utils
from . import string_utils


def package_info():
    """返回包的信息"""
    return f"mypackage v{VERSION} - Python 包演示"


# 可以在这里定义包级别的初始化逻辑
print(f"[OK] mypackage v{VERSION} 初始化完成")
