#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

// 先合并质量较小的果子
vector<int> weight1[100010];
vector<int> weight2[100010];
int main()
{
    int n;
    cin >> n;
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;
        weight1[x].push_back(i);
    }

    sort(weight1, weight1 + n);
    int sum = 0;

     return 0;
}