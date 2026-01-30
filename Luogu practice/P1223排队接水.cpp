#include <iostream>
#include <algorithm>
#include <iomanip>
using namespace std;

struct task
{
    int num;
    int t;
} T[1000];

bool cmp(task a, task b)
{
    return a.t < b.t;
}

int main()
{
    int n;
    cin >> n;
    for (int i = 0; i < n; i++)
    {
        cin >> T[i].t;
        T[i].num = i + 1;
    }
    sort(T + 0, T + n, cmp);
    double sum = 0;
    for (int i = 0; i < n; i++)
    {
        cout << T[i].num << ' ';
        sum += T[i].t * (n - i - 1);
    }
    cout << endl;
    cout << fixed << setprecision(2) << sum / n;
    return 0;
}