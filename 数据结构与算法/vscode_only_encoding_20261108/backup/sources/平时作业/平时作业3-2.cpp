/*
题干：把一个队列拆成两个队列，第一个存放原队列第1、3、5……个元素，
第二个存放剩下的元素，保持相对顺序，并分析复杂度。
思路：用链式队列，把原队列的节点交替接到两个结果队列的队尾。
时间复杂度O(n)，复用原来的节点，额外空间O(1)。
*/
#ifdef _WIN32
#include <windows.h>
#endif
#include <iostream>
using namespace std;

struct Node
{
    int data;
    Node *next;
};

class Queue
{
private:
    Node *head, *tail;

public:
    Queue()
    {
        head = tail = NULL;
    }

    ~Queue()
    {
        while (head != NULL)
        {
            Node *p = head;
            head = head->next;
            delete p;
        }
    }

    void enqueue(int x)
    {
        Node *p = new Node;
        p->data = x;
        p->next = NULL;
        if (tail == NULL)
            head = p;
        else
            tail->next = p;
        tail = p;
    }

    bool dequeue(int &x)
    {
        if (head == NULL)
            return false;
        Node *p = head;
        x = p->data;
        head = head->next;
        if (head == NULL)
            tail = NULL;
        delete p;
        return true;
    }

    void print()
    {
        cout << "队首 [ ";
        for (Node *p = head; p != NULL; p = p->next)
            cout << p->data << " ";
        cout << "] 队尾" << endl;
    }

    // q1、q2应当是两个不同的空队列，也不能是原队列
    void split(Queue &q1, Queue &q2)
    {
        if (this == &q1 || this == &q2 || &q1 == &q2 ||
            q1.head != NULL || q2.head != NULL)
        {
            cout << "请使用两个不同的空队列存放结果" << endl;
            return;
        }
        int pos = 1;
        while (head != NULL)
        {
            Node *p = head;
            head = head->next;
            p->next = NULL;

            // 先判断交给哪一个队列，再接到该队列的队尾
            Queue *q;
            if (pos % 2 == 1)
                q = &q1;
            else
                q = &q2;
            if (q->tail == NULL)
                q->head = p;
            else
                q->tail->next = p;
            q->tail = p;
            pos++;
        }
        tail = NULL;
    }
};

int main()
{
#ifdef _WIN32
    // Windows控制台统一使用UTF-8，避免中文乱码
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

    int num[] = {0, 1, 5, 6};
    for (int i = 0; i < 4; i++)
    {
        Queue q, q1, q2;
        for (int j = 1; j <= num[i]; j++)
            q.enqueue(j);
        cout << "原队列：";
        q.print();
        q.split(q1, q2);
        cout << "奇数位置：";
        q1.print();
        cout << "偶数位置：";
        q2.print();
        cout << endl;
    }
    return 0;
}
