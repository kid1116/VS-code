/*
题干：为栈增加输出、分裂和合并函数。
分裂后，一个栈包含原栈的下半部分，另一个包含剩余元素；
合并时，把第二个栈放在第一个栈上面。
*/
#include <iostream>
#include <vector>
using namespace std;

class Stack
{
private:
    vector<int> a; // 从栈底到栈顶存放

public:
    void push(int x)
    {
        a.push_back(x);
    }

    bool pop(int &x)
    {
        if (a.empty())
            return false;
        x = a.back();
        a.pop_back();
        return true;
    }

    void print()
    {
        cout << "栈底 [ ";
        for (int i = 0; i < (int)a.size(); i++)
            cout << a[i] << " ";
        cout << "] 栈顶" << endl;
    }

    void split(Stack &s1, Stack &s2)
    {
        s1.a.clear();
        s2.a.clear();
        int mid = (int)a.size() / 2; // 奇数个元素时，下半部分取整
        for (int i = 0; i < (int)a.size(); i++)
        {
            if (i < mid)
                s1.push(a[i]);
            else
                s2.push(a[i]);
        }
    }

    void merge(Stack &s1, Stack &s2)
    {
        a.clear();
        for (int i = 0; i < (int)s1.a.size(); i++)
            push(s1.a[i]);
        for (int i = 0; i < (int)s2.a.size(); i++)
            push(s2.a[i]);
    }
};

int main()
{
    int num[] = {0, 1, 4, 5};
    for (int i = 0; i < 4; i++)
    {
        Stack s, s1, s2, s3;
        for (int j = 1; j <= num[i]; j++)
            s.push(j);

        cout << "元素个数：" << num[i] << endl;
        cout << "原栈：";
        s.print();
        s.split(s1, s2); // s1、s2与原栈是不同的栈
        cout << "下半部分：";
        s1.print();
        cout << "剩余部分：";
        s2.print();
        s3.merge(s1, s2); // 把结果存入另一个栈
        cout << "合并结果：";
        s3.print();
        cout << endl;
    }
    return 0;
}
