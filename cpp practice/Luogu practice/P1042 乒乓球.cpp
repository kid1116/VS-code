#include <iostream>
#include <string>
#include <cmath>
#include <algorithm>
using namespace std;

char m;
string s;

void compete(int num)
{
    int a = 0, b = 0;
    for (char c : s)
    {
        c == 'W' ? a++ : b++;
        if (max(a, b) >= num && abs(a - b) >= 2)
        {
            cout << a << ':' << b << endl;
            a = 0, b = 0;
        }
    }
    cout << a << ':' << b << endl;
}

int main()
{
    while (cin >> m && m != 'E')
        s += m;
    compete(11);
    cout << endl;
    compete(21);
    return 0;
}
