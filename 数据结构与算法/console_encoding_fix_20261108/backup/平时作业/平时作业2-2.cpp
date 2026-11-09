/*
题干：列车按1、2、……、n的顺序进入一条站线。
当n=3和n=4时，分别求出可能和不可能的出站顺序。
思路：用一个栈模拟进站和出站，再枚举所有排列进行判断。
*/
#include <iostream>
#include <algorithm>
using namespace std;

bool check(int a[], int n)
{
    int s[10], top = -1;
    int next = 1; // 下一辆还没有进站的车
    for (int i = 0; i < n; i++)
    {
        // 需要的车还不在栈顶，就继续让后面的车进站
        while ((top == -1 || s[top] != a[i]) && next <= n)
            s[++top] = next++;

        if (top == -1 || s[top] != a[i])
            return false;
        top--;
    }
    return true;
}

void print(int a[], int n)
{
    for (int i = 0; i < n; i++)
        cout << a[i];
    cout << " ";
}

int main()
{
    for (int n = 3; n <= 4; n++)
    {
        int a[10], yes = 0, no = 0;
        for (int i = 0; i < n; i++)
            a[i] = i + 1;

        cout << "n=" << n << endl;
        cout << "可能的顺序：";
        do
        {
            if (check(a, n))
            {
                print(a, n);
                yes++;
            }
        } while (next_permutation(a, a + n));

        // 从最小排列重新开始，找出不可能的顺序
        for (int i = 0; i < n; i++)
            a[i] = i + 1;
        cout << endl << "不可能的顺序：";
        do
        {
            if (!check(a, n))
            {
                print(a, n);
                no++;
            }
        } while (next_permutation(a, a + n));
        cout << endl << "可能：" << yes << "种，不可能：" << no << "种" << endl << endl;
    }
    return 0;
}
