#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main()
{
    int n, m, q; // n:数字个数;m:查询次数;q:查询数字
    cin >> n >> m;
    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];
    for (int i = 0; i < m; i++)
    {
        cin >> q;
        auto it = lower_bound(nums.begin(), nums.end(), q);
        // 核心：lower_bound二分查找第一个≥q的元素
        if (it != nums.end() && *it == q)
            cout << it - nums.begin() + 1 << ' ';
        else
            cout << "-1" << ' ';
    }

    return 0;
}