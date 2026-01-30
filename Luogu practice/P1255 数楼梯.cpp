#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

string BigNumAdd(string a, string b)
{
    string res;
    int i = a.size() - 1, j = b.size() - 1;
    int carry = 0;
    while (i >= 0 || j >= 0 || carry > 0)
    {
        int num1 = (i >= 0) ? (a[i--] - '0') : 0;
        int num2 = (j >= 0) ? (b[j--] - '0') : 0;
        int sum = num1 + num2 + carry;
        carry = sum / 10;
        res.push_back((sum % 10) + '0');
    }
    reverse(res.begin(), res.end());
    return res;
}

string way(int n)
{
    if (n == 1)
        return "1";
    if (n == 2)
        return "2";
    string a = "1", b = "2", ans;
    for (int i = 3; i <= n; i++)
    {
        ans = BigNumAdd(a, b);
        a = b;
        b = ans;
    }
    return ans;
}

int main()
{
    int n;
    cin >> n;
    cout << way(n) << endl;
    return 0;
}