#include <iostream>
using namespace std;

bool mat[150][150];

int main()
{
    int n, m, k;
    cin >> n >> m >> k;
    for (int i = 0; i < m; i++)
    {
        int x, y;
        cin >> x >> y;
        x += 2;
        y += 2;
        mat[x][y] = true;
        mat[x - 1][y - 1] = true;
        mat[x - 1][y + 1] = true;
        mat[x + 1][y + 1] = true;
        mat[x + 1][y - 1] = true;
        for (int j = x - 2; j < x + 3; j++)
        {
            mat[j][y] = true;
        }
        for (int j = y - 2; j < y + 3; j++)
        {
            mat[x][j] = true;
        }
    }

    for (int i = 0; i < k; i++)
    {
        int x, y;
        cin >> x >> y;
        x += 2;
        y += 2;
        mat[x][y] = true;
        for (int j = x - 2; j < x + 3; j++)
        {
            for (int m = y - 2; m < y + 3; m++)
            {
                mat[j][m] = true;
            }
        }
    }

    int count = 0;
    for (int i = 3; i < n + 3; i++)
    {
        for (int j = 3; j < n + 3; j++)
        {
            if (!mat[i][j])
                count++;
        }
    }

    cout << count << endl;
    return 0;
}
