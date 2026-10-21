#include <iostream>
using namespace std;

// 采用动态数组表示多项式
class Polynomial
{
    friend int Calpolynomial(const Polynomial &p, float x);
    friend int FastCalpolynomial(const Polynomial &p, float x);

private:
    int degree;
    float *coef;

public:
    Polynomial(int d)
    {
        degree = d;
        coef = new float[degree + 1];
        for (int i = 0; i <= degree; i++)
            coef[i] = 0.0;
    }
    void setCoefficient(int index, float value)
    {
        if (index >= 0 && index <= degree)
            coef[index] = value;
    }

    float getCoefficient(int index) const
    {
        if (index >= 0 && index <= degree)
            return coef[index];
        else
            return 0.0;
    }
};

// 直接计算多项式的值
int Calpolynomial(const Polynomial &p, float x)
{
    float result = 0.0;
    for (int i = 0; i <= p.degree; i++)
    {
        result += p.getCoefficient(i) * pow(x, i);
    }
    return result;
}

// 使用霍纳法则快速计算多项式的值
int FastCalpolynomial(const Polynomial &p, float x)
{
    float result = 0.0;
    for (int i = p.degree; i >= 0; i--)
    {
        result = result * x + p.getCoefficient(i);
    }
    return result;
}

int main()
{
    // 创建一个三次多项式 p(x) = 1 + 2x + 3x^2 + 4x^3
    Polynomial p(3);
    p.setCoefficient(0, 1.0);
    p.setCoefficient(1, 2.0);
    p.setCoefficient(2, 3.0);
    p.setCoefficient(3, 4.0);
    cout << "Polynomial value at x=2: " << Calpolynomial(p, 2) << endl;
    cout << "Fast Polynomial value at x=2: " << FastCalpolynomial(p, 2) << endl;

    return 0;
}