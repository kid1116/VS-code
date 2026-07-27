class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int: #滑动窗口
        dic={}
        max_subs_len=0
        start=0
        for i in range(len(s)):
            if s[i] in dic and start<=dic[s[i]]:
                start=dic[s[i]]+1
            else:
                max_subs_len=max(max_subs_len,i-start+1)
            dic[s[i]]=i
        return max_subs_len

            

