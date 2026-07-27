#include <iostream>
#include <stdexcept>

class TestException : public std::runtime_error {
public:
    explicit TestException(const std::string& message) : std::runtime_error(message) {}
};

int main()
{
    try 
    {
        throw TestException("This is a test exception.");
    } 
    catch (const TestException& e) 
    {
        std::cout<<"Exception occurred: "<<e.what()<<std::endl;
        throw;
    }
}