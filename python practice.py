import time 
import os
os.system("cls")

def sumOfN1(n):
    start=time.time()

    sum=0
    for i in range(n+1):
        sum=sum+i
    end=time.time()

    return sum,end-start

def sumOfN2(n):
    start =time.time()
    sum=(int)((n*(n+1))/2)
    end=time.time()
    return sum,end-start
    
for i in range(5):
    print("Sum and time required are",sumOfN1(100000))

print("Sum and time required are",sumOfN2(100000))
        
