#include <iostream>
#include <fstream>

using namespace std;

class Person
{
public:
    char name[20];
    int age;
};

int main()
{
    ifstream ifs;
    ifs.open("person.dat", ios::binary);

    if (!ifs)
    {
        cout << "Error opening file!" << endl;
        return 1;
    }

    cout << "Reading binary file..." << endl;
    Person p;
    while (ifs.read((char *)&p, sizeof(p)))

        cout << "Name: " << p.name << ", Age: " << p.age << endl;

    ifs.close();
    return 0;
}