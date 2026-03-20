class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        #使用哈希表，时间复杂度O(n)，空间换时间
        box={}
        for i,x in enumerate(nums):
            if target-x in box:
                return [box[target-x],i]
            box[x]=i