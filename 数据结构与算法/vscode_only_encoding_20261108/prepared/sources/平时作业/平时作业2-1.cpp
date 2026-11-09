/*
题干：运用“路漫漫而求索”策略解决迷宫问题，使用栈进行深度优先搜索。
四邻接迷宫，坐标从0开始。搜索时间O(n*m)，空间O(n*m)。
*/
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

// 用数组模拟栈，每个位置记录下一次要尝试的方向
bool solve(int sx, int sy, int ex, int ey)
{
    struct Step
    {
        int x, y, dir;
    };
    Step s[N * N];
    int top = 0;
    s[top] = {sx, sy, 0};
    visited[sx][sy] = true;

    while (top >= 0)
    {
        int x = s[top].x, y = s[top].y;
        if (x == ex && y == ey)
        {
            for (int i = 0; i <= top; i++)
                path.push_back({s[i].x, s[i].y});
            return true;
        }
        if (s[top].dir == 4)
        {
            top--; // 四个方向都走不通，退回上一个位置
            continue;
        }

        int d = s[top].dir;
        s[top].dir++;
        int nx = x + dx[d], ny = y + dy[d];
        if (legal(nx, ny) && !visited[nx][ny])
        {
            visited[nx][ny] = true;
            s[++top] = {nx, ny, 0};
        }
    }
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
