#include <iostream>
#include "DivideByZeroException.h"

using namespace std;

double quotient(int numerator, int denominator)
{
    if (denominator == 0)
    {
        throw DivideByZeroException();
    }
    return static_cast<double>(numerator) / denominator;
}

int main()
{
    int num1, num2;

    cout << "Enter two integers (EOF to quit): ";
    while (cin >> num1 >> num2)
    {
        try
        {
            double result = quotient(num1, num2);
            cout << "Result: " << result << endl;
        }
        catch (DivideByZeroException &e)
        {
            cout << "Error: " << e.what() << endl;
        }

        cout << "\nEnter two integers (EOF to quit): ";
    }
    return 0;
}
