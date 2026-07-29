"""
advanced 模块 - 高级工具函数

演示：
1. 从父包进行相对导入（..）
2. 从同级模块进行相对导入（.）
3. 函数组合使用
"""

import math

# 从父包（mypackage）相对导入
from .. import PI, VERSION
from ..math_utils import circle_area
from ..string_utils import reverse

print("    [Advanced] advanced 模块被导入（使用了父包相对导入）")


def power(base, exp):
    """幂运算"""
    return base ** exp


def safe_sqrt(x):
    """安全开方（处理负数）"""
    if x < 0:
        return complex(0, math.sqrt(-x))  # 返回虚数
    return math.sqrt(x)


def is_prime(n):
    """判断素数"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def format_table(data, headers):
    """
    将数据格式化为表格字符串

    演示：结合父包的 string_utils 函数
    """
    # 计算每列最大宽度
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # 构建表格
    lines = []
    # 表头
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    # 数据行
    for row in data:
        line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        lines.append(line)

    return "\n".join(lines)
