
#include <cassert>
#define main student_main
#include "p1.cpp"
#undef main
int main(){for(int n=0;n<=100;n++){
 Stack s,a,b,c;for(int i=1;i<=n;i++)s.push(i);
 s.split(a,b);c.merge(a,b);int x;
 for(int i=n;i>=1;i--){assert(c.pop(x)&&x==i);assert(s.pop(x)&&x==i);}
 assert(!c.pop(x)&&!s.pop(x));
 for(int i=n/2;i>=1;i--)assert(a.pop(x)&&x==i);
 assert(!a.pop(x));
 for(int i=n;i>n/2;i--)assert(b.pop(x)&&x==i);
 assert(!b.pop(x));
}cout<<"STACK CHECK PASSED\n";}
