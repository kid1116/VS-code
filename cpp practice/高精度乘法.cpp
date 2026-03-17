#include <iostream>
#include <string>
#include <vector>
#include <algorithm> // 用于reverse
using namespace std;

// 高精度乘法：a × b，返回结果字符串（a、b均为非负数字字符串）
string bigNumberMultiply(string a, string b) {
            // 特殊情况：有一个数是0，直接返回"0"
            if (a == "0" || b == "0")
                return "0";

            int m = a.size(), n = b.size();
            // 结果数组：长度m+n，初始化为0（存储每一位的乘积，先不处理进位）
            vector<int> res(m + n, 0);

            // 第一步：逐位相乘，把结果存入数组（不处理进位）
            // 从右往左遍历a的每一位（对应手工乘法的被乘数）
            for (int i = m - 1; i >= 0; --i)
            {
                // 从右往左遍历b的每一位（对应手工乘法的乘数）
                for (int j = n - 1; j >= 0; --j)
                {
                    // 转成整型数字相乘
                    int mul = (a[i] - '0') * (b[j] - '0');
                    // 乘积的个位存到i+j+1，十位暂存到i+j（后续统一处理进位）
                    res[i + j + 1] += mul;
                }
            }

            // 第二步：处理进位（从右往左遍历数组）
            int carry = 0;
            for (int k = m + n - 1; k >= 0; --k)
            {
                int total = res[k] + carry;
                res[k] = total % 10; // 当前位保留个位
                carry = total / 10;  // 进位传递到前一位
            }

            // 第三步：转成字符串，去掉前导0
            string result;
            // 找到第一个非0的位置，跳过前导0
            int start = 0;
            while (start < m + n && res[start] == 0)
            {
                start++;
            }
            // 把数组转成字符串
            for (int k = start; k < m + n; ++k)
            {
                result.push_back(res[k] + '0');
            }

            return result;
}

// 测试示例
int main() {
            // 测试1：小数字验证（123 × 45 = 5535）
            string a = "123";
            string b = "45";
            cout << a << " × " << b << " = " << bigNumberMultiply(a, b) << endl;

            // 测试2：大数字验证（999 × 999 = 998001）
            string c = "999";
            string d = "999";
            cout << c << " × " << d << " = " << bigNumberMultiply(c, d) << endl;

            // 测试3：超大数字（比如之前的5000步台阶数相乘）
            string e = "12345678901234567890"; // 20位
            string f = "98765432109876543210"; // 20位
            cout << e << " × " << f << " = " << endl
                 << bigNumberMultiply(e, f) << endl;

            return 0;
}