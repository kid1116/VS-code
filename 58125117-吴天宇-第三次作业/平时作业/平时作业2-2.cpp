/* 题干：列车按1,2,...,n进入仅容纳一列车序列的站线。n=3和n=4时，
   哪些出站序列可能，哪些不可能？站线长度足够容纳n辆车。
   思路：站线是栈。依次检查目标车号，若不在栈顶则继续进站，仍不匹配则非法。
   单个排列判定O(n)时间、O(n)空间；枚举全部排列O(n*n!)时间。
*/
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <cassert>
using namespace std;
bool possible(const vector<int> &target)
{
    vector<int> st;
    int next = 1, n = (int)target.size();
    for (int x : target)
    {
        while ((st.empty() || st.back() != x) && next <= n)
            st.push_back(next++);
        if (st.empty() || st.back() != x)
            return false;
        st.pop_back();
    }
    return true;
}
int main()
{
    for (int n : {3, 4})
    {
        vector<int> p(n);
        iota(p.begin(), p.end(), 1);
        int yes = 0, no = 0;
        cout << "n=" << n << "\nPOSSIBLE: ";
        do
        {
            if (possible(p))
            {
                for (int x : p)
                    cout << x;
                cout << ' ';
                ++yes;
            }
        } while (next_permutation(p.begin(), p.end()));
        cout << "\nIMPOSSIBLE: ";
        do
        {
            if (!possible(p))
            {
                for (int x : p)
                    cout << x;
                cout << ' ';
                ++no;
            }
        } while (next_permutation(p.begin(), p.end()));
        cout << "\ncounts=" << yes << " possible, " << no << " impossible\n";
        assert(yes == (n == 3 ? 5 : 14));
        assert(no == (n == 3 ? 1 : 10));
    }
    cout << "ALL TRAIN TESTS PASSED\n";
}
