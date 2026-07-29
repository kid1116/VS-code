import os
os.system("cls")

def binary_search(arr,l,r,x): #二分查找适用于有序数组
    if r>=1:
        mid=l+(r-l)//2
        
        if arr[mid]==x:
            return mid
        elif arr[mid]>x:
            return binary_search(arr,l,mid-1,x)
        else:
            return binary_search(arr,mid+1,r,x)
    else:
        return -1
    
print("开始测试：")
arr=[2,3,4,10,40]
x=10
result=binary_search(arr,0,len(arr)-1,x)
if result==-1:
    print("元素不存在！")
else:
    print("元素存在,且位置为：",result)
