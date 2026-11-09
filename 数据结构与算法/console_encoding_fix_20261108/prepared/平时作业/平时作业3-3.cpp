/*
题干：编写递归算法解决迷宫问题。
四邻接迷宫，坐标从0开始。搜索时间O(n*m)，空间O(n*m)。
*/
#ifdef _WIN32
#include <windows.h>
#endif
#include <iostream>
#include <vector>

using namespace std;

const int N = 20;
int maze[N][N], n, m; // 0表示通路，1表示墙；n、m不超过20
bool visited[N][N];
int dx[4] = {0, 1, 0, -1};
int dy[4] = {1, 0, -1, 0}; // 按右、下、左、上的顺序尝试

struct Point
{
    int x, y;
};
vector<Point> path;

bool legal(int x, int y)
{
    return x >= 0 && x < n && y >= 0 && y < m && maze[x][y] == 0;
}

bool solve(int x, int y, int ex, int ey)
{
    visited[x][y] = true;
    path.push_back({x, y});
    if (x == ex && y == ey)
        return true;

    for (int i = 0; i < 4; i++)
    {
        int nx = x + dx[i], ny = y + dy[i];
        if (legal(nx, ny) && !visited[nx][ny])
        {
            if (solve(nx, ny, ex, ey))
                return true;
        }
    }
    path.pop_back(); // 这条分支失败，从当前路径中删除该点
    return false;
}

void runCase(const char *name, int sx, int sy, int ex, int ey)
{
    cout << name << endl;
    path.clear();
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            visited[i][j] = false;

    if (!legal(sx, sy) || !legal(ex, ey) || !solve(sx, sy, ex, ey))
    {
        cout << "没有找到通路" << endl << endl;
        return;
    }
    cout << "步数：" << (int)path.size() - 1 << endl;
    for (int i = 0; i < (int)path.size(); i++)
        cout << "(" << path[i].x << "," << path[i].y << ") ";
    cout << endl << endl;
}

int main()
{
#ifdef _WIN32
    // Windows控制台统一使用UTF-8，避免中文乱码
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

    int a[5][7] = {
        {0, 0, 0, 0, 0, 0, 0},
        {0, 1, 1, 1, 1, 1, 0},
        {0, 0, 0, 0, 0, 1, 0},
        {0, 1, 1, 1, 0, 1, 0},
        {0, 0, 0, 0, 0, 0, 0}
    };
    n = 5;
    m = 7;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            maze[i][j] = a[i][j];
    runCase("测试1：有通路的迷宫", 0, 0, 4, 0);

    int b[3][3] = {{0, 1, 0}, {1, 1, 1}, {0, 1, 0}};
    n = m = 3;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            maze[i][j] = b[i][j];
    runCase("测试2：没有通路的迷宫", 0, 0, 2, 2);

    n = m = 1;
    maze[0][0] = 0;
    runCase("测试3：入口和出口相同", 0, 0, 0, 0);
    return 0;
}
