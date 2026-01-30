#include <iostream>
#include <string>

using namespace std;

class Employee
{
public:
    string firstName;
    string lastName;
    int monthlySalary;

    Employee(string firstName, string lastName, int salary)
    {
        salary = (salary < 0) ? 0 : salary;
        this->firstName = firstName;
        this->lastName = lastName;
        this->monthlySalary = salary;
    }
};

int main()
{
    string f1, f2;
    string l1, l2;
    int m1, m2;
    cin >> f1 >> l1 >> m1;
    Employee emp1(f1, l1, m1);

    cin >> f2 >> l2 >> m2;
    Employee emp2(f2, l2, m2);

    cout << "Employee 1: " << emp1.firstName << " " << emp1.lastName << "; Yearly Salary: " << emp1.monthlySalary * 12 << endl;
    cout << "Employee 2: " << emp2.firstName << " " << emp2.lastName << "; Yearly Salary: " << emp2.monthlySalary * 12 << endl;
    cout << "Increasing employee salaries by 10%" << endl;
    emp1.monthlySalary *= 1.1;
    emp2.monthlySalary *= 1.1;
    cout << "Employee 1: " << emp1.firstName << " " << emp1.lastName << "; Yearly Salary: " << emp1.monthlySalary * 12 << endl;
    cout << "Employee 2: " << emp2.firstName << " " << emp2.lastName << "; Yearly Salary: " << emp2.monthlySalary * 12 << endl;

    return 0;
}