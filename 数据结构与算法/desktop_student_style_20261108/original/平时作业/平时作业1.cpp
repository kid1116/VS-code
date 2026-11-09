/* 题干：为栈ADT增加输出、分裂和合并函数。分裂后的第一个栈包含原栈
   下半部分，另一个包含剩余元素；合并时第二个栈放在第一个栈之上。
*/
#include <iostream>
#include <vector>
#include <stdexcept>
#include <cassert>
using namespace std;

class Stack
{
    vector<int> a;

public:
    void push(int x) { a.push_back(x); }
    int pop()
    {
        if (a.empty())
            throw underflow_error("empty stack");
        int x = a.back();
        a.pop_back();
        return x;
    }
    const vector<int> &values() const { return a; }
    void print() const
    {
        cout << "bottom [";
        for (int x : a)
            cout << x << ' ';
        cout << "] top\n";
    }
    // 返回两个新栈，原栈不变；奇数时下半部分取floor(n/2)。
    pair<Stack, Stack> split() const
    {
        Stack low, high;
        size_t mid = a.size() / 2;
        low.a.assign(a.begin(), a.begin() + mid);
        high.a.assign(a.begin() + mid, a.end());
        return {low, high};
    }
    static Stack merge(const Stack &first, const Stack &second)
    {
        Stack ans;
        ans.a = first.a;
        ans.a.insert(ans.a.end(), second.a.begin(), second.a.end());
        return ans;
    }
};

int main()
{
    for (int n : {0, 1, 4, 5})
    {
        Stack s;
        for (int i = 1; i <= n; ++i)
            s.push(i);
        cout << "n=" << n << " original: ";
        s.print();
        auto parts = s.split();
        cout << "lower: ";
        parts.first.print();
        cout << "upper: ";
        parts.second.print();
        auto joined = Stack::merge(parts.first, parts.second);
        assert(joined.values() == s.values());
        cout << "merged: ";
        joined.print();
    }
    Stack s;
    s.push(7);
    assert(s.pop() == 7);
    try
    {
        s.pop();
        assert(false);
    }
    catch (const underflow_error &)
    {
        cout << "empty pop: rejected\n";
    }
    cout << "ALL STACK TESTS PASSED\n";
}
