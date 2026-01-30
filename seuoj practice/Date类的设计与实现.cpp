#include <iostream>
using namespace std;

class Date
{
public:
    int month, day, year;
};

int main()
{
    int cnt = 1;
    while (cnt <= 2)
    {
        Date d;
        cin >> d.month >> d.day >> d.year;
        if (d.month < 1 || d.month > 12)
            d.month = 1;
        cout << "Date " << cnt << ": " << d.month << "/" << d.day << "/" << d.year << endl;
        cnt++;
    }
    return 0;
}