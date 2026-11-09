#include <windows.h>
#include <iostream>
#define main student_main
#include "student.cpp"
#undef main
int main()
{
    int before = GetConsoleOutputCP();
    int result = student_main();
    int after = GetConsoleOutputCP();
    std::cerr << "BEFORE=" << before << " AFTER=" << after << " INPUT=" << GetConsoleCP() << "\n";
    return result == 0 && before == 65001 && after == 65001 && GetConsoleCP() == 65001 ? 0 : 91;
}
