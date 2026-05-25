#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
using namespace std;

int main()
{
    ifstream myfile;
    myfile.open("example.txt", ios::in);
    if (!myfile)
    {
        cerr << "Unable to open file";
        exit(EXIT_FAILURE); // 终止程序
    }

    int account;
    string name;
    double balance;

    while (myfile >> account >> name >> balance)
    {
        cout << account << " " << name << " " << balance << endl;
    }

    myfile.close(); // 关闭文件
}