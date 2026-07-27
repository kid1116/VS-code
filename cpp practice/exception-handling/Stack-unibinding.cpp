#include <iostream>
#include <stdexcept>

class Logger {
    std::string name;
public:
    Logger(const std::string& n) : name(n) {
        std::cout << "[" << name << "] construct\n";
    }
    ~Logger() {
        //throw std::runtime_error("throw in destructor"); // 在析构函数中抛出异常
        std::cout << "[" << name << "] destruct\n"; // 栈展开时自动调用
    }
};

void level3() {
    Logger log3("level3"); // 对象3
    throw std::runtime_error("throw in level3"); // 抛出异常，触发栈展开
    // 此行及之后代码不会执行
}

void level2() {
    Logger log2("level2"); // 对象2
    level3();              // 调用level3
}

void level1() {
    Logger log1("level1"); // 对象1
    level2();              // 调用level2
}

int main() 
{
    try {
        level1();
    } 
    catch (const std::exception& e) {
        std::cout << "catched exception: " << e.what() << "\n";
    }
    return 0;
}