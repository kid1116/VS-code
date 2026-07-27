#include <iostream>
#include <fstream>
using namespace std;

class Person
{
public:
    char name[20];
    int age;
};

void test1()
{
    ofstream ofs;

    ofs.open("person.dat", ios::out | ios::binary);

    Person p1 = {"Jack", 20};
    ofs.write((const char*)&p1, sizeof(p1));
    
    ofs.close();
}

int main()
{
    test1();
    return 0;
}