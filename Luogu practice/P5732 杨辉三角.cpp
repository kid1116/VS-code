#include <iostream>
using namespace std;

int tri[20][300];

int main()
{
    int n;
    cin >> n;
    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            if (j == 0 || j == i)
                tri[i][j] = 1;
            else
                tri[i][j] = tri[i - 1][j - 1] + tri[i - 1][j];
            cout << tri[i][j] << " ";
        }
        cout << endl;
    }
}