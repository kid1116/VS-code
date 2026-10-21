#include <algorithm>
// 定义稀疏矩阵类
class SparseMatrix
{
public:
    SparseMatrix(int r, int c, int t)
    {
        rows = r;
        cols = c;
        terms = t;
        smArray = new Term[terms];
    }

    SparseMatrix FastTranspose();

private:
    int rows, cols, terms;
    Term *smArray;
};

class Term
{
    friend class SparseMatrix;

private:
    int row, col, value;
};

SparseMatrix SparseMatrix::FastTranspose() // 只用一个辅助数组实现
{
    SparseMatrix b(cols, rows, terms);

    if (terms > 0)
    {
        int *rowStart = new int[cols];

        std::fill(rowStart, rowStart + cols, 0);

        for (int i = 0; i < terms; i++)
        {
            rowStart[smArray[i].col]++;
        }

        // 利用辅助数组rowStart原地计算每一行的起始位置
        int sum = 0;
        for (int i = 0; i < cols; i++)
        {
            int temp = rowStart[i];
            rowStart[i] = sum;
            sum += temp;
        }

        for (int i = 0; i < terms; i++)
        {
            int j = rowStart[smArray[i].col]++;
            b.smArray[j].row = smArray[i].col;
            b.smArray[j].col = smArray[i].row;
            b.smArray[j].value = smArray[i].value;
        }

        delete[] rowStart;
    }
    return b;
}
