"""
string_utils 模块 - 提供字符串处理工具函数
"""

__all__ = ["reverse", "count_words", "is_palindrome", "truncate"]

print("  [String] string_utils 模块被导入")


def reverse(s):
    """反转字符串"""
    return s[::-1]


def count_words(s):
    """统计单词数量"""
    return len(s.split())


def is_palindrome(s):
    """判断是否为回文"""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def truncate(s, max_len, suffix="..."):
    """截断字符串到指定长度"""
    if len(s) <= max_len:
        return s
    return s[:max_len] + suffix
