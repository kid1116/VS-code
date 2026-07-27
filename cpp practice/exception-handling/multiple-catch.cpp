#include <iostream>
#include <stdexcept>
#include <new>
#include <string>

using namespace std;

// 自定义异常类，派生自标准异常层次结构
class NetworkException : public runtime_error
{
public:
    explicit NetworkException(const string& msg) : runtime_error(msg) {}
};

class TimeoutException : public NetworkException
{
public:
    explicit TimeoutException(const string& msg) : NetworkException(msg) {}
};

// 模拟网络请求的函数
void fetchData(int mode)
{
    switch (mode)
    {
    case 0:
        cout << "Fetching data successfully..." << endl;
        break;
    case 1:
        throw TimeoutException("Connection timed out after 30 seconds.");
    case 2:
        throw NetworkException("Unable to resolve hostname.");
    case 3:
        throw runtime_error("A general runtime error occurred.");
    case 4:
        throw bad_alloc();          // 内存分配失败
    case 5:
        throw 42;                   // 抛出非标准异常（int 类型）
    default:
        throw logic_error("Invalid mode specified.");
    }
}

int main()
{
    // 演示不同的异常类型和多个 catch 块
    for (int mode = 0; mode <= 6; ++mode)
    {
        cout << "\n=== Mode " << mode << " ===" << endl;

        try
        {
            fetchData(mode);
            cout << "Request completed successfully." << endl;
        }
        catch (const TimeoutException& e)            // 最派生 — 必须先捕获
        {
            cout << "[TimeoutException] " << e.what() << endl;
            cout << "  -> Tip: Check your network connection or increase timeout." << endl;
        }
        catch (const NetworkException& e)            // 基类 — 在派生类之后
        {
            cout << "[NetworkException] " << e.what() << endl;
            cout << "  -> Tip: Verify the URL and network settings." << endl;
        }
        catch (const bad_alloc& e)                   // 标准异常
        {
            cout << "[bad_alloc] Memory allocation failed: " << e.what() << endl;
        }
        catch (const runtime_error& e)               // 标准运行时异常
        {
            cout << "[runtime_error] " << e.what() << endl;
        }
        catch (const logic_error& e)                 // 标准逻辑异常
        {
            cout << "[logic_error] " << e.what() << endl;
        }
        catch (const exception& e)                   // 所有标准异常的基类
        {
            cout << "[exception] " << e.what() << endl;
        }
        catch (...)                                  // 捕获所有其他异常
        {
            cout << "[Unknown] Caught an exception of unknown type." << endl;
            cout << "  -> This handler catches everything, even non-std exceptions." << endl;
        }
    }

    cout << "\n=== All modes tested ===" << endl;
    return 0;
}
