#include <iostream>
using namespace std;

int compare(const int a[], const int b[], int n1, int n2)
{
    int i = 0;

    // 先对公共部分进行比较
    while (i < n1 && i < n2)
    {
        if (a[i] != b[i])
        {
            return (a[i] < b[i]) ? -1 : 1;
        }
        i++;
    }

    // 如果公共部分相等，则比较数组长度
    if (n1 == n2)
    {
        return 0;
    }
    else
    {
        return n1 < n2 ? -1 : 1;
    }
}

int main()
{
    int a[] = {1, 2, 3};
    int b[] = {1, 2, 3};
    int c[] = {1, 2, 3, 4};

    // 获取数组的长度
    int n1 = sizeof(a) / sizeof(a[0]);
    int n2 = sizeof(b) / sizeof(b[0]);
    int n3 = sizeof(c) / sizeof(c[0]);

    cout << compare(a, b, n1, n2) << endl;
    cout << compare(a, c, n1, n3) << endl;
}