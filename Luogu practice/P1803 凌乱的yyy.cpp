#include <iostream>
#include <algorithm>
using namespace std;

struct Game
{
    int a;
    int b;
} arr[1000001];

int main()
{
    int n;
    cin >> n;
    int a, b;
    for (int i = 0; i < n; i++)
    {
        cin >> a >> b;
        arr[i].a = a;
        arr[i].b = b;
    }

    int count = 0;
    sort(arr, arr + n, [](Game a, Game b)
         { return a.b < b.b; });

    int finish = 0;
    for (int i = 0; i < n; i++)
    {
        if (finish <= arr[i].a)
        {
            count++;
            finish = arr[i].b;
        }
    }

    cout << count << endl;
    return 0;
}