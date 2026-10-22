#include <iostream>
#include <string>
using namespace std;

class String
{
private:
    string str;

public:
    String(const string &s) : str(s) {}
    void frequency();
};

// 利用ASCII码表的特点，统计字符串中各个字符出现的次数
void String::frequency()
{
    int cnt[256] = {0};          // 定义一个数组，存储每个字符出现的次数
    bool printed[256] = {false}; // 定义一个数组，标记每个字符是否已经输出过

    for (unsigned char c : str)
    {
        cnt[c]++;
    }

    for (unsigned char c : str)
    {
        if (!printed[c])
        {
            cout << c << "出现的次数为：" << cnt[c] << endl;
            printed[c] = true; // 标记该字符已经输出过
        }
    }
}

int main()
{
    string input;
    cout << "请输入一个字符串：" << endl;
    getline(cin, input);
    String s(input);
    s.frequency();
}