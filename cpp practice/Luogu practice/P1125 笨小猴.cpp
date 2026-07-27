#include <iostream>
#include <cmath>
#include <unordered_map>
using namespace std;

void isprime(int x)
{
    bool flag = true;
    if (x == 0 || x == 1)
        flag = false;
    if (x == 2)
        flag = true;
    for (int i = 2; i <= sqrt(x); i++)
    {
        if (x % i == 0)
            flag = false;
    }
    if (flag)
    {
        cout << "Lucky Word" << endl;
        cout << x;
    }

    else
    {
        cout << "No Answer" << endl;
        cout << "0";
    }
}

int main()
{
    string s;
    cin >> s;

    unordered_map<char, int> mp;
    for (char c : s)
        mp[c]++;

    int max = 0, min = 1000000000;

    for (auto it : mp)
    {
        if (it.second > max)
            max = it.second;
        if (it.second < min)
            min = it.second;
    }

    int num = max - min;
    if (mp.size() == 1)
        num = max;
    isprime(num);
    return 0;
}