// 题干：运用“修身治平”策略解决迷宫问题，编写完整C++代码并测试。用队列实现广度优先搜索，得到最短路径。

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cassert>
#include <string>
using namespace std;
struct Point
{
    int r, c;
    bool operator==(const Point &p) const { return r == p.r && c == p.c; }
};
using Maze = vector<string>;
const int dr[] = {0, 1, 0, -1}, dc[] = {1, 0, -1, 0}; // 依次尝试右、下、左、上
bool valid(const Maze &a, Point p)
{
    if (a.empty() || a[0].empty())
        return false;
    for (const auto &row : a)
        if (row.size() != a[0].size())
            return false;
    return p.r >= 0 && p.r < (int)a.size() && p.c >= 0 && p.c < (int)a[0].size() && a[p.r][p.c] == '0';
}

// 广度优先按层搜索，入队时标记，parent记录第一次到达该格的前驱。
vector<Point> solve(const Maze &a, Point start, Point goal)
{
    if (!valid(a, start) || !valid(a, goal))
        return {};
    vector<vector<bool>> seen(a.size(), vector<bool>(a[0].size(), false));
    vector<vector<Point>> parent(a.size(), vector<Point>(a[0].size(), {-1, -1}));
    queue<Point> q;
    q.push(start);
    seen[start.r][start.c] = true;
    while (!q.empty())
    {
        Point p = q.front();
        q.pop();
        if (p == goal)
        {
            vector<Point> path;
            for (Point x = goal; !(x == Point{-1, -1}); x = parent[x.r][x.c])
                path.push_back(x);
            reverse(path.begin(), path.end());
            return path;
        }
        for (int d = 0; d < 4; ++d)
        {
            Point next{p.r + dr[d], p.c + dc[d]};
            if (valid(a, next) && !seen[next.r][next.c])
            {
                seen[next.r][next.c] = true;
                parent[next.r][next.c] = p;
                q.push(next);
            }
        }
    }
    return {};
}

void test(string name, const Maze &a, Point s, Point g, bool expected, int shortest = -1)
{
    auto path = solve(a, s, g);
    assert(!path.empty() == expected);
    cout << name << ": ";
    if (path.empty())
    {
        cout << "NO PATH\n";
        return;
    }
    assert(path.front() == s && path.back() == g);
    for (size_t i = 0; i < path.size(); ++i)
    {
        assert(valid(a, path[i]));
        if (i)
            assert(abs(path[i].r - path[i - 1].r) + abs(path[i].c - path[i - 1].c) == 1);
    }
    if (shortest >= 0)
        assert((int)path.size() - 1 == shortest);
    cout << "steps=" << path.size() - 1 << "\n";
    for (auto p : path)
        cout << '(' << p.r << ',' << p.c << ") ";
    cout << '\n';
    Maze view = a;
    for (auto p : path)
        view[p.r][p.c] = '*';
    for (auto row : view)
        cout << row << '\n';
}
int main()
{
    Maze a = {"0000000", "0111110", "0000010", "0111010", "0000000"};
    test("reachable", a, {0, 0}, {4, 0}, true, 4);
    test("unreachable", {"010", "111", "010"}, {0, 0}, {2, 2}, false);
    test("single cell", {"0"}, {0, 0}, {0, 0}, true, 0);
    test("blocked start", {"10"}, {0, 0}, {0, 1}, false);
    test("empty maze", {}, {0, 0}, {0, 0}, false);
    test("invalid endpoint", {"00"}, {-1, 0}, {0, 1}, false);
    cout << "ALL MAZE TESTS PASSED (0=road, 1=wall, *=path; coordinates start at 0)\n";
}
