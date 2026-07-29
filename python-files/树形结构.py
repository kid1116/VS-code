import os
from collections import deque

os.system("cls")

class TreeNode: #二叉树节点类
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self): #定义类的对象被打印时显示什么内容
        return f"TreeNode({self.val})"

# 创建节点
root =TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)
node6 = TreeNode(6)

# 连接节点
root.left = node2
root.right = node3
node2.left = node4
node2.right = node5
node3.right = node6

# 遍历二叉树
def preorder_travelsal(node): #DFS前序遍历
    if node is None:
        return 
    print(node.val,end=' ')
    preorder_travelsal(node.left)
    preorder_travelsal(node.right)

def level_order_traversal(root): #BFS层序遍历
    if root is None:
        return
    queue = deque([root]) 
    while queue:
        current_node = queue.popleft()
        print(current_node.val, end=' ') 
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

#输出结果：
print("前序遍历：")
preorder_travelsal(root)
print("\n层序遍历: ")
level_order_traversal(root) 