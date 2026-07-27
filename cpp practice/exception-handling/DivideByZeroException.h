#include <stdexcept>

class DivideByZeroException : public std::runtime_error 
{
public:     
    DivideByZeroException() : std::runtime_error("Attempted to divide by zero.") {} //what() function output
};