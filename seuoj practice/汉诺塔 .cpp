#include <iostream>
using namespace std;

void tower(int n, char A, char B, char C)
{
    if (n == 1)
        cout << A << " -> " << C << endl;
    else
    {
        tower(n - 1, A, C, B);
        cout << A << " -> " << C << endl;
        tower(n - 1, B, A, C);
    }
}

int main()
{
    int n;
    cin >> n;
    tower(n, 'A', 'B', 'C');

    return 0;
}