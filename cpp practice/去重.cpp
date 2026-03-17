#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main()
{
    vector<int> result;
    int num;

    for (int i = 0; i < 20; i++)
    {
        cin >> num;
        if (find(result.begin(), result.end(), num) == result.end())
        {
            result.push_back(num);
        }
    }

    for (int i = 0; i < result.size(); i++)
    {
        cout << result[i] << " ";
    }

    return 0;
}