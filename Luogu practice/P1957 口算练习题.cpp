#include <iostream>
#include <string>
using namespace std;

int num(int t) // 判断非负整数的位数
{
    if (t == 0)
        return 1;
    int s = 0;
    while (t != 0)
    {
        t /= 10;
        s++;
    }
    return s;
}

int main()
{
    int n;
    cin >> n;
    string s;
    char a;
    int b, c;
    int flag;

    for (int i = 0; i < n; i++)
    {
        cin >> s;
        if (s[0] >= 'a' && s[0] <= 'z')
        {
            a = s[0];
            if (a == 'a')
            {
                flag = 1;
                cin >> b >> c;
            }
            else if (a == 'b')
            {
                flag = 2;
                cin >> b >> c;
            }
            else if (a == 'c')
            {
                flag = 3;
                cin >> b >> c;
            }
        }
        else
        {
            b = stoi(s);
            cin >> c;
        }
        if (flag == 1)
        {
            cout << b << "+" << c << "=" << b + c << endl;
            cout << num(b) + num(c) + num(b + c) + 2 << endl;
        }
        else if (flag == 2)
        {
            cout << b << "-" << c << "=" << b - c << endl;
            if (b < c)
                cout << num(b) + num(c) + num(b - c) + 3 << endl;
            else
                cout << num(b) + num(c) + num(b - c) + 2 << endl;
        }
        else if (flag == 3)
        {
            cout << b << "*" << c << "=" << b * c << endl;
            cout << num(b) + num(c) + num(b * c) + 2 << endl;
        }
    }

    return 0;
}