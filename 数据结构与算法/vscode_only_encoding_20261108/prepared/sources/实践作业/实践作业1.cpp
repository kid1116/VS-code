/*
题干：模拟有3条跑道的机场。1、2号跑道各有2个降落队列，
每条跑道各有1个起飞队列。每个时间单位最多新增3架起飞飞机、
3架降落飞机，每条跑道最多处理1架飞机。
起飞飞机用连续偶数编号，降落飞机用连续奇数编号。
普通飞机按FIFO处理；燃油为0的飞机优先，先用3号跑道，
有多架时再用1、2号跑道。输出队列内容和起降统计信息。

输入：先输入时间单位数T；随后每期输入起飞数、降落数，
以及每架新降落飞机的燃油。输入0可以运行程序自带的例子。
*/
#include <iostream>
#include <deque>
#include <vector>
#include <iomanip>
using namespace std;

struct Plane
{
    int id;      // 飞机编号
    int arrive;  // 加入队列的时间
    int fuel;    // 剩余燃油，仅降落飞机使用
};

deque<Plane> landing[4];
deque<Plane> departure[3];
int oddId = 1, evenId = 2;
int landNum = 0, takeoffNum = 0, zeroNum = 0, lostNum = 0;
long long landWait = 0, takeoffWait = 0, fuelSum = 0;

// 找到同类队列中最短的一队，相同长度时选编号小的
int shortest(deque<Plane> q[], int n)
{
    int k = 0;
    for (int i = 1; i < n; i++)
        if (q[i].size() < q[k].size())
            k = i;
    return k;
}

bool allEmpty()
{
    for (int i = 0; i < 4; i++)
        if (!landing[i].empty())
            return false;
    for (int i = 0; i < 3; i++)
        if (!departure[i].empty())
            return false;
    return true;
}

void printQueues()
{
    cout << "队列内容（从队首到队尾）：" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "L" << i + 1 << "（跑道" << i / 2 + 1 << "）：";
        for (int j = 0; j < (int)landing[i].size(); j++)
            cout << landing[i][j].id << "(燃油=" << landing[i][j].fuel << ") ";
        cout << endl;
    }
    for (int i = 0; i < 3; i++)
    {
        cout << "D" << i + 1 << "（跑道" << i + 1 << "）：";
        for (int j = 0; j < (int)departure[i].size(); j++)
            cout << departure[i][j].id << " ";
        cout << endl;
    }
}

void printStats()
{
    double avgLandWait = 0, avgTakeoffWait = 0, avgFuel = 0;
    if (landNum > 0)
    {
        avgLandWait = (double)landWait / landNum;
        avgFuel = (double)fuelSum / landNum;
    }
    if (takeoffNum > 0)
        avgTakeoffWait = (double)takeoffWait / takeoffNum;

    cout << "已起飞：" << takeoffNum << "，平均等待：" << avgTakeoffWait << endl;
    cout << "已降落：" << landNum << "，平均等待：" << avgLandWait;
    cout << "，落地平均剩余燃油：" << avgFuel << endl;
    cout << "燃油为0时成功降落：" << zeroNum << "，失事：" << lostNum << endl;
}

void land(Plane p, int runway, int time, bool emergency)
{
    landNum++;
    landWait += time - p.arrive;
    fuelSum += p.fuel;
    if (p.fuel == 0)
        zeroNum++;
    cout << "跑道" << runway + 1 << "：飞机" << p.id << "降落";
    cout << "，等待=" << time - p.arrive << "，剩余燃油=" << p.fuel;
    if (emergency)
        cout << "（紧急）";
    cout << endl;
}

void takeoff(int runway, int time)
{
    Plane p = departure[runway].front();
    departure[runway].pop_front();
    takeoffNum++;
    takeoffWait += time - p.arrive;
    cout << "跑道" << runway + 1 << "：飞机" << p.id << "起飞";
    cout << "，等待=" << time - p.arrive << endl;
}

// 为一条未被紧急飞机占用的跑道安排普通起降
void ordinary(int runway, int time)
{
    if (runway == 2)
    {
        if (!departure[2].empty())
            takeoff(2, time);
        else
            cout << "跑道3：空闲" << endl;
        return;
    }

    int k = runway * 2;
    if (landing[k + 1].size() > landing[k].size())
        k++;
    // 先服务较长的队列；长度相同优先降落，始终取队首
    if (!landing[k].empty() && landing[k].size() >= departure[runway].size())
    {
        Plane p = landing[k].front();
        landing[k].pop_front();
        land(p, runway, time, false);
    }
    else if (!departure[runway].empty())
        takeoff(runway, time);
    else
        cout << "跑道" << runway + 1 << "：空闲" << endl;
}

void schedule(int time)
{
    vector<Plane> urgent;
    bool used[3] = {false, false, false};
    int order[3] = {2, 0, 1};

    // 遍历各降落队列，取出燃油为0的飞机，其余保持原来的顺序
    for (int i = 0; i < 4; i++)
    {
        int n = (int)landing[i].size();
        for (int j = 0; j < n; j++)
        {
            Plane p = landing[i].front();
            landing[i].pop_front();
            if (p.fuel == 0)
                urgent.push_back(p);
            else
                landing[i].push_back(p);
        }
    }

    // 最多能救援3架，找出最早到达的3架，先用3号跑道
    for (int i = 0; i < 3 && i < (int)urgent.size(); i++)
    {
        int k = i;
        for (int j = i + 1; j < (int)urgent.size(); j++)
            if (urgent[j].id < urgent[k].id)
                k = j;
        Plane temp = urgent[i];
        urgent[i] = urgent[k];
        urgent[k] = temp;
        land(urgent[i], order[i], time, true);
        used[order[i]] = true;
    }
    // 超过3架同时耗尽燃油时，剩下的飞机无法再等待
    for (int i = 3; i < (int)urgent.size(); i++)
    {
        lostNum++;
        cout << "飞机" << urgent[i].id << "燃油耗尽，跑道不足，失事" << endl;
    }

    for (int i = 0; i < 3; i++)
        if (!used[i])
            ordinary(i, time);
}

int main()
{

    int T;
    cout << fixed << setprecision(2);
    cout << "请输入时间单位数T（输入0运行示例）：" << endl;
    if (!(cin >> T) || T < 0)
    {
        cout << "时间单位数输入错误" << endl;
        return 1;
    }
    bool example = (T == 0);
    int data[8][5] = {
        {2, 2, 5, 3, 0}, {1, 1, 0, 0, 0}, {0, 2, 0, 0, 0},
        {0, 3, 0, 0, 0}, {2, 3, 5, 6, 5}, {0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}
    };
    if (example)
        T = 8;

    // 输入结束后，如果仍有飞机等待，就继续调度直到队列清空
    for (int time = 0; time < T || !allEmpty(); time++)
    {
        int d = 0, l = 0, fuel[3] = {0, 0, 0};
        cout << endl << "===== 时间 " << time << " =====" << endl;
        if (time < T)
        {
            if (example)
            {
                d = data[time][0];
                l = data[time][1];
                for (int i = 0; i < l; i++)
                    fuel[i] = data[time][i + 2];
            }
            else
            {
                cout << "输入起飞数、降落数及各降落飞机的燃油：" << endl;
                if (!(cin >> d >> l) || d < 0 || d > 3 || l < 0 || l > 3)
                {
                    cout << "起飞数和降落数必须在0到3之间" << endl;
                    return 1;
                }
                for (int i = 0; i < l; i++)
                    if (!(cin >> fuel[i]) || fuel[i] < 0)
                    {
                        cout << "燃油输入错误" << endl;
                        return 1;
                    }
            }
        }

        for (int i = 0; i < d; i++)
        {
            int k = shortest(departure, 3);
            Plane p = {evenId, time, 0};
            evenId += 2;
            departure[k].push_back(p);
            cout << "新到起飞飞机" << p.id << "，进入D" << k + 1 << endl;
        }
        for (int i = 0; i < l; i++)
        {
            int k = shortest(landing, 4);
            Plane p = {oddId, time, fuel[i]};
            oddId += 2;
            landing[k].push_back(p);
            cout << "新到降落飞机" << p.id << "，燃油=" << p.fuel << "，进入L" << k + 1 << endl;
        }
        cout << "调度前" << endl;
        printQueues();
        schedule(time);
        cout << "调度后" << endl;
        printQueues();
        printStats();

        // 只有仍在等待降落的飞机需要继续消耗燃油
        int waiting = 0;
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < (int)landing[i].size(); j++)
            {
                landing[i][j].fuel--;
                waiting++;
            }
        cout << "本期结束，" << waiting << "架等待降落飞机的燃油减1" << endl;
    }
    cout << endl << "===== 最终统计 =====" << endl;
    printStats();
    return 0;
}
