#include <iostream>
#include <string>
using namespace std;

string change(string s)
{
    for (int i = 0; i < s.length(); i++)
    {
        while (i + 2 < s.length() && s[i] == 'h' && s[i + 1] == 'y' && s[i + 2] == 'w')
        {
            s.replace(i, 3, "wzh");
            i -= 2;
        }
    }
    return s;
}

int main()
{
    string s;
    cin >> s;
    cout << change(s) << endl;

    return 0;
}
