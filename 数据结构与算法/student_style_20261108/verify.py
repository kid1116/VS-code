from pathlib import Path
import subprocess,os,json,re,random,collections,itertools,shutil

work=Path(__file__).resolve().parent
build=work/'build';build.mkdir(exist_ok=True)
files=sorted((work/'modified').rglob('*.cpp'))
sources={}
for i,p in enumerate(files):
    copy=build/f'p{i}.cpp';copy.write_text(p.read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
    sources[p.stem]=copy
old=build/'old_airport.cpp'
old.write_bytes((work/'original/实践作业/实践作业1.cpp').read_bytes())

maze_wrapper='''
#define main student_main
#include "SOURCE"
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
  cout<<"\\n";
 }
}
'''
extra=[]
for i,name in enumerate(['平时作业2-1','平时作业3-1','平时作业3-3']):
    wrapper=build/f'maze{i}.cpp';wrapper.write_text(maze_wrapper.replace('SOURCE',sources[name].name),encoding='utf-8');extra.append(wrapper)
stack_wrapper='''
#include <cassert>
#define main student_main
#include "SOURCE"
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
}cout<<"STACK CHECK PASSED\\n";}
'''
queue_wrapper='''
#include <cassert>
#define main student_main
#include "SOURCE"
#undef main
int main(){for(int n=0;n<=100;n++){
 Queue q,a,b;for(int i=1;i<=n;i++)q.enqueue(i);
 q.split(a,b);int x;assert(!q.dequeue(x));q.enqueue(99);assert(q.dequeue(x)&&x==99);
 for(int i=1;i<=n;i+=2)assert(a.dequeue(x)&&x==i);
 for(int i=2;i<=n;i+=2)assert(b.dequeue(x)&&x==i);
 assert(!a.dequeue(x)&&!b.dequeue(x));
 a.enqueue(10);b.enqueue(20);assert(a.dequeue(x)&&x==10&&b.dequeue(x)&&x==20);
}cout<<"QUEUE CHECK PASSED\\n";}
'''
for name,body,label in [('平时作业1',stack_wrapper,'stack'),('平时作业3-2',queue_wrapper,'queue')]:
    p=build/(label+'.cpp');p.write_text(body.replace('SOURCE',sources[name].name),encoding='utf-8');extra.append(p)
bat=['@echo off','call "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat" -arch=x64 >nul']
for src in list(sources.values())+[old]+extra:
    bat += [f'cl /nologo /utf-8 /std:c++17 /EHsc /W4 "{src}" /Fo:"{src.with_suffix(".obj")}" /Fe:"{src.with_suffix(".exe")}"','if errorlevel 1 exit /b 1']
(build/'compile.bat').write_text('\r\n'.join(bat)+'\r\n',encoding='utf-8')
r=subprocess.run(['cmd','/c',str(build/'compile.bat')],capture_output=True)
(build/'compile.log').write_bytes(r.stdout+r.stderr)
assert r.returncode==0,(r.stdout+r.stderr).decode(errors='replace')
print('Compiled all 7 revised sources and verification programs.')

def run(exe,data='',args=()):
    r=subprocess.run([str(exe),*args],input=data.encode('utf-8'),capture_output=True,timeout=20)
    assert r.returncode==0,(exe,r.returncode,r.stderr.decode(errors='replace'))
    return r.stdout.decode('utf-8').replace('\r\n','\n')
for label in ['stack','queue']:
    print(run(build/(label+'.exe')).strip())
for name,source in sources.items():
    text=run(source.with_suffix('.exe'),'0\n' if name=='实践作业1' else '')
    (build/(name+'-output.txt')).write_text(text,encoding='utf-8')

# Exhaustive 3x3 mazes: independent BFS reference determines reachability and shortest length.
cases=[]
for mask in range(512):
    a=[[int(bool(mask & (1<<(r*3+c)))) for c in range(3)] for r in range(3)]
    cases.append((a,(0,0),(2,2)))
rng=random.Random(20261108)
for i in range(100):
    a=[[rng.randrange(3)==0 for c in range(7)] for r in range(5)]
    cases.append((a,(rng.randrange(5),rng.randrange(7)),(rng.randrange(5),rng.randrange(7))))
cases += [([[0]],(0,0),(0,0)),([[1]],(0,0),(0,0)),([[0]],(-1,0),(0,0))]
data=str(len(cases))+'\n'
distances=[]
for a,start,goal in cases:
    n,m=len(a),len(a[0]);data+=f'{n} {m}\n'+' '.join(str(int(x)) for row in a for x in row)+'\n'+' '.join(map(str,start+goal))+'\n'
    distance=-1
    if 0<=start[0]<n and 0<=start[1]<m and not a[start[0]][start[1]] and not a[goal[0]][goal[1]]:
        q=collections.deque([(start,0)]);seen={start}
        while q:
            p,d=q.popleft()
            if p==goal:distance=d;break
            for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr,nc=p[0]+dr,p[1]+dc
                if 0<=nr<n and 0<=nc<m and not a[nr][nc] and (nr,nc) not in seen:
                    seen.add((nr,nc));q.append(((nr,nc),d+1))
    distances.append(distance)
for index in range(3):
    rows=run(build/f'maze{index}.exe',data).splitlines();assert len(rows)==len(cases)
    for line,(a,start,goal),distance in zip(rows,cases,distances):
        values=list(map(int,line.split()));found,count=values[:2]
        assert found==(distance>=0)
        path=list(zip(values[2::2],values[3::2]));assert count==len(path)
        if found:
            assert path[0]==start and path[-1]==goal and len(set(path))==len(path)
            assert all(not a[r][c] for r,c in path)
            assert all(abs(x[0]-y[0])+abs(x[1]-y[1])==1 for x,y in zip(path,path[1:]))
            if index==1:assert count-1==distance
    print(f'Maze {index+1}: {len(cases)} cases passed.')

# Generate train output sequences by branching on legal push/pop operations.
def trains(n):
    result=set()
    def visit(next,stack,out):
        if len(out)==n:result.add(''.join(map(str,out)));return
        if next<=n:visit(next+1,stack+[next],out)
        if stack:visit(next,stack[:-1],out+[stack[-1]])
    visit(1,[],[]);return result
text=(build/'平时作业2-2-output.txt').read_text(encoding='utf-8')
for n,chunk in zip([3,4],text.split('n=')[1:]):
    yes=set(re.search(r'可能的顺序：(.*)',chunk)[1].split())
    no=set(re.search(r'不可能的顺序：(.*)',chunk)[1].split())
    assert yes==trains(n)
    assert yes|no=={''.join(map(str,p)) for p in itertools.permutations(range(1,n+1))}
    assert not yes&no
print('Train enumeration: all permutations for n=3 and n=4 passed.')

def old_events(text):
    time=-1;events=[]
    for line in text.splitlines():
        t=re.match(r'=== TIME (\d+) ===',line)
        if t:time=int(t[1])
        match=re.match(r'  R(\d): (LAND|TAKEOFF) (\d+) wait=(\d+)(?: fuel=(\d+))?(.*)',line)
        if match:events.append((time,int(match[1]),match[2],int(match[3]),int(match[4]),int(match[5]) if match[5] else None,'EMERGENCY' in match[6]))
    return events
def new_events(text):
    time=-1;events=[]
    for line in text.splitlines():
        t=re.match(r'===== 时间 (\d+) =====',line)
        if t:time=int(t[1])
        match=re.match(r'跑道(\d)：飞机(\d+)(降落|起飞)，等待=(\d+)(?:，剩余燃油=(\d+))?(.*)',line)
        if match:events.append((time,int(match[1]),'LAND' if match[3]=='降落' else 'TAKEOFF',int(match[2]),int(match[4]),int(match[5]) if match[5] else None,'紧急' in match[6]))
    return events
airport=sources['实践作业1'].with_suffix('.exe')
example=run(airport,'0\n');assert new_events(example)==old_events(run(old.with_suffix('.exe')))
inputcases=[[(0,[])],[(0,[5,3])],[(3,[0])],[(3,[0,0])],[(3,[0,0,0])],[(0,[1,1,1]),(0,[0,0,0])]]
for seed in range(50):
    r=random.Random(seed);inputcases.append([(r.randrange(4),[r.randrange(8) for j in range(r.randrange(4))]) for i in range(40)])
for rows in inputcases:
    data=str(len(rows))+'\n'+''.join(f'{d} {len(f)} '+ ' '.join(map(str,f))+'\n' for d,f in rows)
    newtext=run(airport,data);oldtext=run(old.with_suffix('.exe'),data,['--stdin'])
    assert new_events(newtext)==old_events(oldtext)
    totals=re.findall(r'STATS takeoff=(\d+) avgWait=([\d.]+); landed=(\d+) avgWait=([\d.]+) avgFuel=([\d.]+); zeroFuelLandings=(\d+); lost=(\d+)',oldtext)[-1]
    takeoff=re.findall(r'已起飞：(\d+)，平均等待：([\d.]+)',newtext)[-1]
    land=re.findall(r'已降落：(\d+)，平均等待：([\d.]+)，落地平均剩余燃油：([\d.]+)',newtext)[-1]
    emergency=re.findall(r'燃油为0时成功降落：(\d+)，失事：(\d+)',newtext)[-1]
    assert tuple(takeoff+land+emergency)==totals
print('Airport: demo and 56 scenarios match the original service events and statistics.')
for data in ['-1\n','1\n4 0\n','1\n0 1 -1\n','1\n0 2 5\n']:
    r=subprocess.run([str(airport)],input=data.encode(),capture_output=True,timeout=20);assert r.returncode==1
print('Invalid input checks passed. ALL CHECKS PASSED.')
