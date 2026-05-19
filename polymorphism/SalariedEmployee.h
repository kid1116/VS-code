#ifndef SALARIED_H
#define SALARIED_H

#include <string>
#include "Employee.h"

class SalariedEmployee : public Employee
{
public:
    SalariedEmployee(const std::string &, const std::string &, const std::string &, double = 0.0);
    virtual ~SalariedEmployee() {}

    void setWeeklySalary(double);
    double getWeeklySalary() const;

    virtual double earnings() const override; // override pure virtual
    virtual void print() const override; // override virtual

private:
    double weeklySalary;
};
#endif