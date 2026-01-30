#include <iostream>
#include <vector> //动态数组
using namespace std;
using Matrix = vector<vector<char>>; // 给二维矩阵起别名，简化书写，语义清晰

Matrix rotate90(Matrix &mat) // 旋转90度
{
    int n = mat.size();
    Matrix temp(n, vector<char>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            temp[j][n - 1 - i] = mat[i][j];
    return temp;
}

Matrix rotate180(Matrix &mat) // 旋转180度
{
    int n = mat.size();
    Matrix temp(n, vector<char>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            temp[n - 1 - i][n - 1 - j] = mat[i][j];
    return temp;
}

Matrix rotate270(Matrix &mat) // 旋转270度
{
    int n = mat.size();
    Matrix temp(n, vector<char>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            temp[n - 1 - j][i] = mat[i][j];
    return temp;
}

Matrix flip(Matrix &mat) // 翻转
{
    int n = mat.size();
    Matrix temp(n, vector<char>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            temp[i][n - 1 - j] = mat[i][j];
    return temp;
}

Matrix combine1(Matrix &mat) // 组合1
{
    Matrix temp(mat); // 拷贝构造函数
    temp = flip(temp);
    temp = rotate90(temp);
    return temp;
}

Matrix combine2(Matrix &mat) // 组合2
{
    Matrix temp(mat);
    temp = flip(temp);
    temp = rotate180(temp);
    return temp;
}

Matrix combine3(Matrix &mat) // 组合3
{
    Matrix temp(mat);
    temp = flip(temp);
    temp = rotate270(temp);
    return temp;
}

int main()
{
    // input:
    int n;
    cin >> n;
    Matrix initial(n, vector<char>(n)); // 创建n行n列的初始二维矩阵
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> initial[i][j];

    Matrix target(n, vector<char>(n)); // 创建n行n列的目标二维矩阵
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> target[i][j];

    // process&judge:
    int ans = 0;
    if (rotate90(initial) == target) // 旋转90度
        ans = 1;
    else if (rotate180(initial) == target) // 旋转180度
        ans = 2;
    else if (rotate270(initial) == target) // 旋转270度
        ans = 3;
    else if (flip(initial) == target) // 翻转
        ans = 4;
    else if (combine1(initial) == target || combine2(initial) == target || combine3(initial) == target) // 组合1,2,3
        ans = 5;
    else if (initial == target) // 无需操作
        ans = 6;
    else // 无法转换
        ans = 7;

    cout << ans << endl; // output
    return 0;
}