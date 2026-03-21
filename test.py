class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        # 确保nums1是较短的数组，优化二分查找范围
        if len(nums1) > len(nums2):
            return self.findMedianSortedArrays(nums2, nums1)
        
        # 计算总长度的一半（向上取整），用于分割数组
        total = len(nums1) + len(nums2)
        half = (total + 1) // 2
        
        # 在较短的数组（nums1）上进行二分查找
        left, right = 0, len(nums1)
        
        while left < right:
            # 计算当前分割点
            m1 = (left + right) // 2
            m2 = half - m1
            
            # 检查分割点是否有效：nums1的左边部分 <= nums2的右边部分
            if nums1[m1] < nums2[m2 - 1]:
                left = m1 + 1  # 需要向右移动
            else:
                right = m1  # 需要向左移动
        
        # 最终分割点
        m1 = left
        m2 = half - m1
        
        # 计算左半部分的最大值（中位数的左半部分）
        left_max = max(
            nums1[m1 - 1] if m1 > 0 else float('-inf'),
            nums2[m2 - 1] if m2 > 0 else float('-inf')
        )
        
        # 如果总长度是奇数，直接返回左半部分的最大值
        if total % 2 == 1:
            return left_max
        
        # 计算右半部分的最小值
        right_min = min(
            nums1[m1] if m1 < len(nums1) else float('inf'),
            nums2[m2] if m2 < len(nums2) else float('inf')
        )
        
        # 如果总长度是偶数，返回左右中位数的平均值
        return (left_max + right_min) / 2