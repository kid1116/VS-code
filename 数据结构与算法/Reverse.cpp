struct Node
{
    int data;
    Node *next;
};

void moveRight(Node *&l, Node *&r, int n)
{
    while (n > 0 && r != nullptr)
    {
        Node *p = r;
        r = r->next;

        p->next = l;
        l = p;

        n--;
    }
}

void moveLeft(Node *&l, Node *&r, int n)
{
    while (n > 0 && l != nullptr)
    {
        Node *p = l;
        l = l->next;

        p->next = r;
        r = p;

        n--;
    }
}