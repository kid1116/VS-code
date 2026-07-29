"""
math_utils 模块 - 提供数学工具函数

演示模块级别的函数定义和 __all__ 的用法
"""

__all__ = ["add", "subtract", "multiply", "divide", "fibonacci", "circle_area"]

print("  [Math] math_utils 模块被导入")


def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


def multiply(a, b):
    """乘法"""
    return a * b


def divide(a, b):
    """除法（带除零检查）"""
    if b == 0:
        raise ValueError("除数不能为零！")
    return a / b


def fibonacci(n):
    """返回斐波那契数列前 n 项"""
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def circle_area(radius):
    """计算圆的面积"""
    from . import PI  # 相对导入包级别的常量
    return PI * radius ** 2
