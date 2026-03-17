#include <iostream>
using namespace std;

int snake[1200][1200];

int main()
{
    int n;
    cin >> n;

    int x = 0, y = 0;

    int now = 1;
    int dx = 1, dy = -1;

    while (now <= n * n)
    {
        snake[x][y] = now;
        now++;
        int nx = x + dx;
        int ny = y + dy;

        // 判断是否到达边界
        if (nx < 0 || nx >= n || ny < 0 || ny >= n)
        {

            if (dx == 1 && dy == -1) // 右上到左下
            {
                if (y == 0 && x != n - 1)
                    x++;
                else if (x == n - 1)
                    y++;
            }
            else // 左下到右上
            {
                if (x == 0 && y != n - 1)
                    y++;
                else if (y == n - 1)
                    x++;
            }
            dx = -dx;
            dy = -dy;
        }

        else
        {
            x = nx;
            y = ny;
        }
    }

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cout << snake[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}
