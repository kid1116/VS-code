# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre=None
        cur=head
        while cur: #循环直到current为空，即遍历完整个链表
            nxt=cur.next #保存下一个节点
            cur.next=pre #将当前节点指向前一个节点
            pre=cur #将当前节点作为前一个节点
            cur=nxt #将下一个节点作为当前节点 
        return pre
        
            


        