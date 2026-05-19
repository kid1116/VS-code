#include <iostream>
#include <iomanip>
#include <vector>
#include "Employee.cpp"
#include "SalariedEmployee.cpp"
#include "CommissionEmployee.cpp"
#include "BasePlusCommissionEmployee.cpp"

using namespace std;

void virtualViapointer(const Employee *const); // 通过基类指针调用
void virtualViaReference(const Employee &);    // 通过基类引用调用

int main()
{
    cout << fixed << setprecision(2);

    SalariedEmployee se("John", "Doe", "111", 1000);
    CommissionEmployee ce("Sue", "Smith", "222", 10000, .06);
    BasePlusCommissionEmployee be("Mike", "Andy", "333", 10000, .06, 300);

    cout << "Employees processed individually using static binding:\n\n"; // 静态绑定：通过对象调用函数，编译器在编译时就确定了函数调用的地址
    se.print();
    cout << "earned: $" << se.earnings() << "\n\n";
    ce.print();
    cout << "earned: $" << ce.earnings() << "\n\n";
    be.print();
    cout << "earned: $" << be.earnings() << "\n\n";

    // create vector of three base—class pointers:
    vector<Employee *> employees(3);
    employees[0] = &se;
    employees[1] = &ce;
    employees[2] = &be;

    cout << "Employees processed polymorphically via dynamic binding:\n\n"; // 动态绑定:通过基类的指针或引用调用虚函数实现多态

    cout << "virtual function calls made off base-class pointers:\n";
    for (const Employee *employeePtr : employees)
    {
        virtualViapointer(employeePtr);
    }

    cout << "\nvirtual function calls made off base-class references:\n";
    for (const Employee *employeePtr : employees)
    {
        virtualViaReference(*employeePtr);
    }

    return 0;
}

void virtualViapointer(const Employee *const baseClassPtr)
{
    baseClassPtr->print();
    cout << "earned: $" << baseClassPtr->earnings() << "\n\n";
}

void virtualViaReference(const Employee &baseClassRef)
{
    baseClassRef.print();
    cout << "earned: $" << baseClassRef.earnings() << "\n\n";
}
