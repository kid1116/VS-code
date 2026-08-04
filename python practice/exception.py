def fun1():
    print("fun1")
    fun2()

def fun2():
    print("fun2")
    fun3()

def fun3():
    print("fun3")
    print(10 / 0)

if __name__ == "__main__":
    try:
        fun1()

    except Exception as e:
        print("Exception occurred:", e)



