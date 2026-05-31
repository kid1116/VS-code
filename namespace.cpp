#include <iostream>
using namespace std;

namespace A {
    int a = 10;
    void display() {
        cout << "A::a = " << a << endl;
    }
}

namespace B {
    int a = 20;
    void display() {
        cout << "B::a = " << a << endl;
    }
    namespace C {
        int a = 30;
        void display() {
            cout << "B::C::a = " << a << endl;
        }
    }
}

int a=40;
void display() {
    cout << "a = " << a << endl;
}

int main() {
    A::display(); 
    B::display(); 
    B::C::display();
    display();
    ::display(); //"::"表示全局作用域
    return 0; 
}