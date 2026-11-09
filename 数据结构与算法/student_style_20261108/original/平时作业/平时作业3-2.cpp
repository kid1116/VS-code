/* 题干：为Queue类增加拆分函数，第一队列含原队列第1、3、5...个元素，
   第二队列含其余元素，保持相对顺序，并分析复杂度。
   思路：链式队列逐个摘取队首节点，交替接到两个结果队尾，复用节点。
   时间O(n)，除两个结果队列的头尾指针及计数外，额外空间O(1)。
*/
#include <iostream>
#include <vector>
#include <cassert>
#include <stdexcept>
using namespace std;
class Queue
{
    struct Node
    {
        int data;
        Node *next;
    };
    Node *head = nullptr, *tail = nullptr;
    Node *detach()
    {
        Node *p = head;
        head = head->next;
        if (!head)
            tail = nullptr;
        p->next = nullptr;
        return p;
    }
    void append(Node *p)
    {
        if (tail)
            tail->next = p;
        else
            head = p;
        tail = p;
    }

public:
    Queue() = default;
    Queue(const Queue &) = delete;
    Queue &operator=(const Queue &) = delete;
    ~Queue()
    {
        while (head)
        {
            Node *p = detach();
            delete p;
        }
    }
    bool empty() const { return !head; }
    void enqueue(int x) { append(new Node{x, nullptr}); }
    int dequeue()
    {
        if (empty())
            throw underflow_error("empty queue");
        Node *p = detach();
        int x = p->data;
        delete p;
        return x;
    }
    vector<int> values() const
    {
        vector<int> a;
        for (Node *p = head; p; p = p->next)
            a.push_back(p->data);
        return a;
    }
    void split(Queue &first, Queue &second)
    {
        if (this == &first || this == &second || &first == &second || !first.empty() || !second.empty())
            throw invalid_argument("distinct empty destination queues required");
        bool odd = true;
        while (head)
        {
            Node *p = detach();
            (odd ? first : second).append(p);
            odd = !odd;
        }
    }
};
void show(const Queue &q)
{
    cout << "front [";
    for (int x : q.values())
        cout << x << ' ';
    cout << "] rear\n";
}
int main()
{
    for (int n : {0, 1, 5, 6})
    {
        Queue q, a, b;
        vector<int> va, vb;
        for (int i = 1; i <= n; ++i)
        {
            q.enqueue(i);
            (i % 2 ? va : vb).push_back(i);
        }
        cout << "n=" << n << " original: ";
        show(q);
        q.split(a, b);
        cout << "odd positions: ";
        show(a);
        cout << "even positions: ";
        show(b);
        assert(q.empty() && a.values() == va && b.values() == vb);
        for (int x : va)
            assert(a.dequeue() == x);
        for (int x : vb)
            assert(b.dequeue() == x);
    }
    Queue q, a;
    try
    {
        q.dequeue();
        assert(false);
    }
    catch (const underflow_error &)
    {
        cout << "empty dequeue: rejected\n";
    }
    try
    {
        q.split(q, a);
        assert(false);
    }
    catch (const invalid_argument &)
    {
        cout << "alias destinations: rejected\n";
    }
    cout << "ALL QUEUE TESTS PASSED\n";
}
