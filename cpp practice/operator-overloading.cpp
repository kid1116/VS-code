#include <iostream>
using namespace std;

class Person
{
public:
    int m_A;
    int m_B;

    Person(int a, int b) : m_A(a), m_B(b)
    {
        // cout << "Person(int a, int b) constructor called." << endl;
    }
    Person() : m_A(0), m_B(0)
    {
        // cout << "Person() constructor called." << endl;
    }
    // ~Person()
    // {
    //     cout << "~Person() destructor called." << endl;
    // }

    // friend Person operator+(const Person &, const Person &);
};

Person operator+(const Person &p1, const Person &p2)
{
    Person temp;
    temp.m_A = p1.m_A + p2.m_A;
    temp.m_B = p1.m_B + p2.m_B;
    return temp;
};

int main()
{
    Person p1(10, 20), p2(30, 40);
    Person p3 = p1 + p2;
    cout << "sum.m_A = " << p3.m_A << endl;
    cout << "sum.m_B = " << p3.m_B << endl;
    return 0;
}