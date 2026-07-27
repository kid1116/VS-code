#include <iostream>
#include <iomanip>
#include <vector>
#include "Employee.cpp"
#include "SalariedEmployee.cpp"
#include "CommissionEmployee.cpp"
#include "BasePlusCommissionEmployee.cpp"

using namespace std;

void virtualViapointer(const Employee *const);
void virtualViaReference(const Employee &);

int main()
{
    cout << fixed << setprecision(2);

    SalariedEmployee se("John", "Doe", "111", 1000);
    CommissionEmployee ce("Sue", "Smith", "222", 10000, .06);
    BasePlusCommissionEmployee be("Mike", "Andy", "333", 10000, .06, 300);

    cout << "Employees processed individually using static binding:\n\n";
    se.print();
    cout << "earned: $" << se.earnings() << "\n\n";
    ce.print();
    cout << "earned: $" << ce.earnings() << "\n\n";
    be.print();
    cout << "earned: $" << be.earnings() << "\n\n";

    vector<Employee *> employees(3);
    employees[0] = &se;
    employees[1] = &ce;
    employees[2] = &be;

    cout << "Employees processed polymorphically via dynamic binding:\n\n";

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
