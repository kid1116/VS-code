#include <windows.h>
#include <iostream>
#define main homework_main
#include "homework_old.cpp"
#undef main
int main()
{
    if (!SetConsoleOutputCP(932) || !SetConsoleCP(932))
        return 90;
    int before = GetConsoleOutputCP();
    int code = homework_main();
    int after = GetConsoleOutputCP();
    std::cerr << "CONSOLE_CP_BEFORE=" << before << " AFTER=" << after << " INPUT=" << GetConsoleCP() << "\n";
    if (code != 0 || after != CP_UTF8 || GetConsoleCP() != CP_UTF8)
        return 91;
    return 0;
}
