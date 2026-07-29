"""
subpkg - mypackage 的子包

演示子包的结构和相对导入
"""

print("    [SubPkg] subpkg 子包被导入")

from .advanced import (
    power,
    safe_sqrt,
    is_prime,
    format_table,
)

__all__ = ["power", "safe_sqrt", "is_prime", "format_table"]
