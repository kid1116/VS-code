#include <iostream>
using namespace std;

class Person
{
public:
    int m_A;
    int m_B;
    friend void operator+(Person& p1, Person& p2)
    {
        cout << "m_A: " << p1.m_A + p2.m_A << endl;
        cout << "m_B: " << p1.m_B + p2.m_B << endl;
    }
};

int main()
{
    Person p1, p2;
    p1.m_A = 10;
    p1.m_B = 20;
    p2.m_A = 30;
    p2.m_B = 40;
    p1 + p2; // 通过友元函数重载运算符+

    return 0;
    
}