#include <iostream>
#include <string>
 
using namespace std;
 
template <typename T> 
T const& Max (T const& a, T const& b)  
{ 
    return a < b ? b:a; 
} //实际调用时根据不同的实参类型自动替换占位符T，如int、double、string等

int main ()
{
 
    int i = 39;
    int j = 20;
    cout << "Max(i, j): " << Max(i, j) << endl; 
 
    double f1 = 13.5; 
    double f2 = 20.7; 
    cout << "Max(f1, f2): " << Max(f1, f2) << endl; 
 
    string s1 = "Hello"; 
    string s2 = "World"; 
    cout << "Max(s1, s2): " << Max(s1, s2) << endl; 
 
    return 0;
}