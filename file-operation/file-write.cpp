#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

int main()
{
    ofstream myfile;
    myfile.open("example.txt", ios::app);
    if (!myfile)
    {
        cerr << "Unable to open file";
        exit(EXIT_FAILURE); // 终止程序
    }

    cout << "Enter the account,name and balance: " << endl
         << "Enter end-of-file to end input.\n?";

    int account;
    string name;
    double balance;

    while (cin >> account >> name >> balance)
    {
        myfile << account << " " << name << " " << balance << endl;
        cout << "?"; // 提示用户输入下一行数据
    }

    myfile.close(); // 关闭文件
    cout << "Data saved to file.";
}