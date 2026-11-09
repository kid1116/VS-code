/*
题干：模拟有3条跑道的机场。1、2号跑道各有2个降落FIFO队列，3条跑道
各有1个起飞FIFO队列。每时间单位至多新增3架起飞、3架降落飞机；每条
跑道每单位至多处理1架。起飞分配连续偶数id，降落分配连续奇数id；新飞机
加入最短队列。燃油为0的飞机优先于一切其他请求，1架用3号跑道，多架时
动用其他跑道。3号跑道平时只起飞。输出全部事件、所有队列、已完成起降
的平均等待、已降落飞机的平均剩余燃油，以及燃油为0时成功降落的总数。
*/
#include <iostream>
#include <deque>
#include <vector>
#include <array>
#include <fstream>
#include <sstream>
#include <random>
#include <iomanip>
#include <stdexcept>
#include <cassert>
#include <algorithm>
#include <filesystem>
#include <codecvt>
#include <locale>
using namespace std;
struct Plane
{
    int id, arrive, fuel;
};
struct Input
{
    int departures = 0;
    vector<int> fuel;
};
struct Stats
{
    int takeoff = 0, landed = 0, zeroLandings = 0, lost = 0, createdD = 0, createdL = 0;
    long long waitD = 0, waitL = 0, remainingFuel = 0;
};
class Airport
{
    array<deque<Plane>, 4> landing;
    array<deque<Plane>, 3> departure;
    int nextOdd = 1, nextEven = 2;
    bool verbose;
    Stats stats;
    template <size_t N>
    static size_t shortest(const array<deque<Plane>, N> &queues)
    {
        size_t best = 0;
        for (size_t i = 1; i < N; ++i)
            if (queues[i].size() < queues[best].size())
                best = i;
        return best;
    }
    void say(const string &s) const
    {
        if (verbose)
            cout << s << '\n';
    }
    void complete(Plane p, int r, int t, bool isLanding, bool emergency)
    {
        assert(t >= p.arrive);
        if (isLanding)
        {
            assert(p.fuel >= 0);
            ++stats.landed;
            stats.waitL += t - p.arrive;
            stats.remainingFuel += p.fuel;
            if (p.fuel == 0)
                ++stats.zeroLandings;
        }
        else
        {
            ++stats.takeoff;
            stats.waitD += t - p.arrive;
        }
        ostringstream s;
        s << "  R" << r + 1 << ": " << (isLanding ? "LAND " : "TAKEOFF ") << p.id
          << " wait=" << t - p.arrive;
        if (isLanding)
            s << " fuel=" << p.fuel;
        if (emergency)
            s << " EMERGENCY";
        say(s.str());
    }
    // 普通降落只能取指定队列的队首，不允许按燃油给普通队列重排。
    void ordinary(int r, int t)
    {
        if (r == 2)
        {
            if (!departure[r].empty())
            {
                auto p = departure[r].front();
                departure[r].pop_front();
                complete(p, r, t, false, false);
            }
            else
                say("  R3: IDLE");
            return;
        }
        int q = 2 * r;
        if (landing[q + 1].size() > landing[q].size())
            ++q;
        if (!landing[q].empty() && landing[q].size() >= departure[r].size())
        {
            auto p = landing[q].front();
            landing[q].pop_front();
            complete(p, r, t, true, false);
        }
        else if (!departure[r].empty())
        {
            auto p = departure[r].front();
            departure[r].pop_front();
            complete(p, r, t, false, false);
        }
        else
            say("  R" + to_string(r + 1) + ": IDLE");
    }

public:
    explicit Airport(bool v = true) : verbose(v) {}
    const Stats &result() const { return stats; }
    bool empty() const
    {
        for (const auto &q : landing)
            if (!q.empty())
                return false;
        for (const auto &q : departure)
            if (!q.empty())
                return false;
        return true;
    }
    void check() const
    {
        int l = 0, d = 0;
        for (const auto &q : landing)
        {
            int previous = -1;
            for (auto p : q)
            {
                assert(p.id % 2 == 1 && p.fuel >= 0 && p.id > previous);
                previous = p.id;
                ++l;
            }
        }
        for (const auto &q : departure)
        {
            int previous = -1;
            for (auto p : q)
            {
                assert(p.id % 2 == 0 && p.id > previous);
                previous = p.id;
                ++d;
            }
        }
        // 7路归并检查全局唯一编号，队列数为常数，检查时间也是O(Q)。
        array<const deque<Plane> *, 7> queues{};
        array<size_t, 7> pos{};
        for (int i = 0; i < 4; ++i)
            queues[i] = &landing[i];
        for (int i = 0; i < 3; ++i)
            queues[i + 4] = &departure[i];
        int last = -1;
        while (true)
        {
            int best = -1;
            for (int i = 0; i < 7; ++i)
                if (pos[i] < queues[i]->size() &&
                    (best < 0 || (*queues[i])[pos[i]].id < (*queues[best])[pos[best]].id))
                    best = i;
            if (best < 0)
                break;
            int id = (*queues[best])[pos[best]++].id;
            assert(id > last);
            last = id;
        }
        assert(stats.createdL == stats.landed + stats.lost + l);
        assert(stats.createdD == stats.takeoff + d);
    }
    void report(int t, const string &phase) const
    {
        if (!verbose)
            return;
        cout << "  QUEUES " << phase << " at t=" << t << " (front -> rear)\n";
        for (int i = 0; i < 4; ++i)
        {
            cout << "    L" << i + 1 << "@R" << i / 2 + 1 << ": [";
            for (auto p : landing[i])
                cout << p.id << "(f=" << p.fuel << ",a=" << p.arrive << ") ";
            cout << "]\n";
        }
        for (int i = 0; i < 3; ++i)
        {
            cout << "    D" << i + 1 << "@R" << i + 1 << ": [";
            for (auto p : departure[i])
                cout << p.id << "(a=" << p.arrive << ") ";
            cout << "]\n";
        }
        cout << fixed << setprecision(2) << "  STATS takeoff=" << stats.takeoff << " avgWait="
             << (stats.takeoff ? double(stats.waitD) / stats.takeoff : 0.0)
             << "; landed=" << stats.landed << " avgWait=" << (stats.landed ? double(stats.waitL) / stats.landed : 0.0)
             << " avgFuel=" << (stats.landed ? double(stats.remainingFuel) / stats.landed : 0.0)
             << "; zeroFuelLandings=" << stats.zeroLandings << "; lost=" << stats.lost << '\n';
    }
    void step(int t, const Input &input)
    {
        if (input.departures < 0 || input.departures > 3 || input.fuel.size() > 3)
            throw invalid_argument("arrival counts must be 0..3");
        for (int f : input.fuel)
            if (f < 0)
                throw invalid_argument("fuel must be nonnegative");
        say("=== TIME " + to_string(t) + " ===");
        for (int i = 0; i < input.departures; ++i)
        {
            size_t q = shortest(departure);
            Plane p{nextEven, t, 0};
            nextEven += 2;
            departure[q].push_back(p);
            ++stats.createdD;
            say("  ARRIVE TAKEOFF " + to_string(p.id) + " -> D" + to_string(q + 1));
        }
        for (int fuel : input.fuel)
        {
            size_t q = shortest(landing);
            Plane p{nextOdd, t, fuel};
            nextOdd += 2;
            landing[q].push_back(p);
            ++stats.createdL;
            say("  ARRIVE LAND " + to_string(p.id) + " fuel=" + to_string(fuel) + " -> L" + to_string(q + 1));
        }
        check();
        report(t, "before service");
        // 同时紧急的飞机按到达先后(id)服务，先使用3号再1号、2号跑道。
        vector<Plane> urgent;
        // 一次遍历摘出紧急飞机，其余节点依次保留，避免重复在deque中间erase。
        for (auto &q : landing)
        {
            deque<Plane> keep;
            for (auto p : q)
            {
                if (p.fuel == 0)
                    urgent.push_back(p);
                else
                    keep.push_back(p);
            }
            q.swap(keep);
        }
        // 最多救援3架，只需选出最早的3架，无需对所有候选排序。
        for (size_t i = 0; i < min(size_t(3), urgent.size()); ++i)
        {
            auto it = min_element(urgent.begin() + i, urgent.end(), [](Plane a, Plane b)
                                  { return a.id < b.id; });
            iter_swap(urgent.begin() + i, it);
        }
        const int order[] = {2, 0, 1};
        array<bool, 3> used{false, false, false};
        int operations = 0;
        for (size_t i = 0; i < urgent.size(); ++i)
        {
            Plane p = urgent[i];
            if (i < 3)
            {
                int r = order[i];
                used[r] = true;
                ++operations;
                complete(p, r, t, true, true);
            }
            else
            {
                ++stats.lost;
                say("  LOST " + to_string(p.id) + ": fuel=0, all 3 runways already allocated");
            }
        }
        for (int r = 0; r < 3; ++r)
            if (!used[r])
            {
                int before = stats.takeoff + stats.landed;
                ordinary(r, t);
                operations += stats.takeoff + stats.landed - before;
            }
        assert(operations <= 3);
        check();
        report(t, "after service");
        int pending = 0;
        for (auto &q : landing)
            for (auto &p : q)
            {
                assert(p.fuel > 0);
                --p.fuel;
                ++pending;
            }
        if (pending)
            say("  END: fuel -1 for " + to_string(pending) + " waiting landing planes");
        else
            say("  END: no landing planes waiting");
        check();
    }
    Stats run(const vector<Input> &input)
    {
        size_t t = 0;
        for (; t < input.size(); ++t)
            step((int)t, input[t]);
        while (!empty())
        {
            if (t > input.size() + 100000)
                throw runtime_error("drain limit exceeded");
            step((int)t++, {});
        }
        say("=== FINAL ===");
        report((int)t, "final");
        return stats;
    }
};
vector<Input> readInput(istream &in)
{
    int t;
    if (!(in >> t) || t < 0 || t > 10000)
        throw invalid_argument("T must be 0..10000");
    vector<Input> data;
    for (int i = 0; i < t; ++i)
    {
        Input row;
        int land;
        if (!(in >> row.departures >> land) || row.departures < 0 || row.departures > 3 || land < 0 || land > 3)
            throw invalid_argument("bad arrival counts at time " + to_string(i));
        for (int j = 0; j < land; ++j)
        {
            int f;
            if (!(in >> f) || f < 0)
                throw invalid_argument("missing/negative fuel");
            row.fuel.push_back(f);
        }
        data.push_back(row);
    }
    string extra;
    if (in >> extra)
        throw invalid_argument("unexpected extra input");
    return data;
}
vector<Input> randomInput(unsigned seed, int t)
{
    if (t < 0 || t > 10000)
        throw invalid_argument("duration must be 0..10000");
    mt19937 rng(seed);
    uniform_int_distribution<int> count(0, 3), fuel(0, 7);
    vector<Input> data;
    for (int i = 0; i < t; ++i)
    {
        Input row;
        row.departures = count(rng);
        int n = count(rng);
        for (int j = 0; j < n; ++j)
            row.fuel.push_back(fuel(rng));
        data.push_back(row);
    }
    return data;
}
void selfTest()
{
    {
        Airport a(false);
        auto s = a.run({});
        assert(s.takeoff == 0 && s.landed == 0);
    }
    {
        Airport a(false);
        auto s = a.run({Input{0, {5, 3}}});
        assert(s.landed == 2 && s.waitL == 1 && s.remainingFuel == 7 && s.lost == 0);
    }
    for (int n = 1; n <= 3; ++n)
    {
        Airport a(false);
        auto s = a.run({Input{3, vector<int>(n, 0)}});
        assert(s.zeroLandings == n && s.lost == 0 && s.takeoff == 3);
    }
    // t=0有3架普通飞机，剩1架在t=1变成紧急；再到3架燃油0飞机，共4架。
    {
        Airport a(false);
        auto s = a.run({Input{0, {1, 1, 1}}, Input{0, {0, 0, 0}}});
        assert(s.landed == 5 && s.zeroLandings == 3 && s.lost == 1);
    }
    // 同一队列中，紧急飞机允许越过非紧急队首，后者仍保留原顺序。
    {
        Airport a(false);
        a.run({Input{3, {5, 5, 5}}, Input{3, {5, 5, 5}}, Input{3, {0, 0, 0}}});
    }
    for (unsigned seed = 0; seed < 100; ++seed)
    {
        Airport a(false);
        auto s = a.run(randomInput(seed, 100));
        assert(s.createdL == s.landed + s.lost && s.createdD == s.takeoff);
    }
    for (string text : {"1 4 0", "1 0 1 -1", "1 0 2 4", "0 extra"})
    {
        istringstream in(text);
        bool rejected = false;
        try
        {
            readInput(in);
        }
        catch (const invalid_argument &)
        {
            rejected = true;
        }
        assert(rejected);
    }
    cout << "AIRPORT SELF-TEST PASSED: empty; 1/2/3 emergencies; overflow; FIFO invariants;\n"
         << "100 seeded random simulations x 100 arrivals periods; invalid input.\n";
}
int runMain(int argc, char *argv[])
{
    try
    {
        vector<Input> data;
        if (argc == 2 && string(argv[1]) == "--self-test")
        {
            selfTest();
            return 0;
        }
        if (argc == 2 && string(argv[1]) == "--stdin")
            data = readInput(cin);
        else if (argc == 3 && string(argv[1]) == "--input")
        {
            ifstream in(filesystem::u8path(argv[2]));
            if (!in)
                throw runtime_error("cannot open input file");
            data = readInput(in);
        }
        else if (argc == 4 && string(argv[1]) == "--random")
            data = randomInput((unsigned)stoul(argv[2]), stoi(argv[3]));
        else if (argc == 1)
            data = {{2, {5, 3}}, {1, {0}}, {0, {0, 0}}, {0, {0, 0, 0}}, {2, {5, 6, 5}}, {0, {}}, {0, {}}, {0, {}}};
        else
            throw invalid_argument("usage: airport [--input file | --stdin | --random seed T | --self-test]");
        cout << "AIRPORT SIMULATION | enqueue -> emergency -> ordinary -> fuel countdown\n";
        Airport airport;
        airport.run(data);
        return 0;
    }
    catch (const exception &e)
    {
        cerr << "INPUT ERROR: " << e.what() << '\n';
        return 1;
    }
}
#ifdef _WIN32
// Windows宽字符入口保留中文路径，再统一转为UTF-8交给主程序。
int wmain(int argc, wchar_t *argv[])
{
    wstring_convert<codecvt_utf8_utf16<wchar_t>> conv;
    vector<string> args;
    for (int i = 0; i < argc; ++i)
        args.push_back(conv.to_bytes(argv[i]));
    vector<char *> ptrs;
    for (auto &s : args)
        ptrs.push_back(s.data());
    return runMain(argc, ptrs.data());
}
#else
int main(int argc, char *argv[]) { return runMain(argc, argv); }
#endif
