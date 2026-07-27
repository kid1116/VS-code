#include <iostream>
#include <iomanip>
using namespace std;

int snake[10][10];

int main()
{
    int n;
    cin >> n;

    snake[0][0] = 1;
    int x = 0, y = 0;
    int now = 2;
    while (now <= n * n)
    {
        while (y + 1 < n && snake[x][y + 1] == 0)
        {
            y++;
            snake[x][y] = now;
            now++;
        }
        while (x + 1 < n && snake[x + 1][y] == 0)

        {
            x++;
            snake[x][y] = now;
            now++;
        }
        while (y - 1 >= 0 && snake[x][y - 1] == 0)
        {
            y--;
            snake[x][y] = now;
            now++;
        }
        while (x - 1 >= 0 && snake[x - 1][y] == 0)
        {
            x--;
            snake[x][y] = now;
            now++;
        }
    }

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cout << setw(2) << snake[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}