#include <iostream>
#include <stdexcept>

using namespace std;

class Item
{
public:
    int value;

    Item(int v) : value(v)
    {
        cout<<"Item "<< v <<" constructor called."<<endl;
        if (v == 3)
            throw runtime_error("An exception is thrown.");
        
    }
    ~Item()
    {
        cout<<"Item "<<value<<" destructor called."<<endl;
    }
};

int main()
{
    cout<<"Constructing an object of Item class."<<endl;
    try
    {
        Item item1(1);
        Item item2(2);
        Item item3(3);
        Item item4(4);
    }
    catch (const runtime_error& e)
    {
        cout << "Exception caught: " << e.what() << endl;
    }
}