#include <iostream>
#include <array>
#include <algorithm>
using namespace std;

int main()
{
    array<int, 20> nums{0};
    int x;
    int cnt = 0;
    for (int i = 0; i < 20; i++)
    {
        cin >> x;
        auto it = find(nums.begin(), nums.begin() + cnt, x);
        if (it == nums.begin() + cnt)
            nums[cnt++] = x;
    }

    for (int i = 0; i < cnt; i++)
    {
        cout << nums[i] << " ";
    }
    return 0;
}