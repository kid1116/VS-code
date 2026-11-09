
#define main student_main
#include "p6.cpp"
#undef main
int main(){
 int count;cin>>count;
 while(count--){
  int sx,sy,ex,ey;cin>>n>>m;
  for(int i=0;i<n;i++)for(int j=0;j<m;j++){cin>>maze[i][j];visited[i][j]=false;}
  cin>>sx>>sy>>ex>>ey;path.clear();
  bool found=legal(sx,sy)&&legal(ex,ey)&&solve(sx,sy,ex,ey);
  cout<<found<<" "<<path.size();
  for(int i=0;i<(int)path.size();i++)cout<<" "<<path[i].x<<" "<<path[i].y;
  cout<<"\n";
 }
}
