
#include <cassert>
#define main student_main
#include "p5.cpp"
#undef main
int main(){for(int n=0;n<=100;n++){
 Queue q,a,b;for(int i=1;i<=n;i++)q.enqueue(i);
 q.split(a,b);int x;assert(!q.dequeue(x));q.enqueue(99);assert(q.dequeue(x)&&x==99);
 for(int i=1;i<=n;i+=2)assert(a.dequeue(x)&&x==i);
 for(int i=2;i<=n;i+=2)assert(b.dequeue(x)&&x==i);
 assert(!a.dequeue(x)&&!b.dequeue(x));
 a.enqueue(10);b.enqueue(20);assert(a.dequeue(x)&&x==10&&b.dequeue(x)&&x==20);
}cout<<"QUEUE CHECK PASSED\n";}
