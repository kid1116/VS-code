#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cstdlib>

using namespace std;

enum RequestType
{
  ZERO_BALANCE = 1,
  CREDIT_BALANCE,
  DEBIT_BALANCE,
  END
};
int getRequest();
bool shouldDisplay(int, double);
void outputLine(int, const string &, double);

int main()
{
  ifstream inClientFile("D:\\VS code\\file\\clients.txt", ios::in);

  if (!inClientFile)
  {
    cerr << "File could not be opened." << endl;
    exit(EXIT_FAILURE);
  }

  int account;
  string name;
  double balance;

  int request = getRequest();

  while (request != END)
  {
    switch (request)
    {
    case ZERO_BALANCE:
      cout << "\nAccounts with zero balances:" << endl;
      break;
    case CREDIT_BALANCE:
      cout << "\nAccounts with credit balances:" << endl;
      break;
    case DEBIT_BALANCE:
      cout << "\nAccounts with debit balances:" << endl;
      break;
    default:
      cout << "Invalid request." << endl;
      break;
    }

    while (inClientFile >> account >> name >> balance)
    {
      if (shouldDisplay(request, balance))
        outputLine(account, name, balance);
    }

    inClientFile.clear();  // 清除EOF状态
    inClientFile.seekg(0); // 将文件读取指针重新定位到文件开头（偏移0字节）
    request = getRequest();
  }
  cout << "End of run." << endl;
}

int getRequest()
{
  int request;

  cout << "\nEnter request" << endl
       << "1-List accounts with zero balances" << endl
       << "2-List accounts with credit balances" << endl
       << "3-List accounts with debit balances" << endl
       << "4-End" << fixed << showpoint;

  do
  {
    cout << "\n?";
    cin >> request;
  } while (request < ZERO_BALANCE || request > END);
  return request;
}

bool shouldDisplay(int type, double balance)
{
  if (type == ZERO_BALANCE && balance == 0)
    return true;
  else if (type == CREDIT_BALANCE && balance < 0)
    return true;
  else if (type == DEBIT_BALANCE && balance > 0)
    return true;
  else
    return false;
}

void outputLine(int account, const string &name, double balance)
{
  cout << left << setw(10) << account
       << setw(13) << name
       << setw(7) << setprecision(2) << right << balance << endl;
}