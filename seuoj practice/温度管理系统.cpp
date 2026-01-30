#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

class Temperaturemanager
{
private:
    string date[101];
    double temperature[101];
    int cnt;

public:
    Temperaturemanager() // 初始化
    {
        cnt = 0;
    }

    void addrecord(string d, double t) // 添加记录
    {
        if (cnt < 100)
        {
            date[cnt] = d;
            temperature[cnt] = t;
            cnt++;
        }
        else
        {
            cout << "记录已到上限100条,无法添加更多记录" << endl;
        }
    }
    void printrecords() // 打印记录
    {
        cout << "所有温度记录：" << endl;
        for (int i = 0; i < cnt; i++)
        {
            cout << "\t日期:" << date[i] << ",温度：" << fixed << setprecision(1) << temperature[i] << "°C" << endl;
        }
    }
    void findmaxrecord() // 查找最高温度记录
    {
        cout << "统计结果：" << endl;
        double max = temperature[0];
        string date_max = date[0];
        for (int i = 0; i < cnt; i++)
        {
            if (temperature[i] > max)
            {
                max = temperature[i];
                date_max = date[i];
            }
        }
        cout << "\t最高温度:" << max << "°C" << "(日期:" << date_max << ")" << endl;
    }
    void findminrecord() // 查找最低温度记录
    {
        double min = temperature[0];
        string date_min = date[0];
        for (int i = 0; i < cnt; i++)
        {
            if (temperature[i] < min)
            {
                min = temperature[i];
                date_min = date[i];
            }
        }
        cout << "\t最低温度:" << min << "°C" << "(日期:" << date_min << ")" << endl;
    }
    void averagerecord() // 计算平均温度
    {
        double sum = 0;
        for (int i = 0; i < cnt; i++)
        {
            sum += temperature[i];
        }
        cout << "\t平均温度:" << fixed << setprecision(2) << sum / cnt << "°C" << endl;
    }
};

int main()
{
    string date;
    double temperature;

    Temperaturemanager tm;
    cout << "请输入日期(MM/DD)和温度记录,输入'0/0'结束输入" << endl;
    while (true)
    {
        cin >> date >> temperature;
        if (date == "0/0")
            break;
        tm.addrecord(date, temperature);
    }
    cout << "=== 温度管理系统 ===\n"
         << endl;
    tm.printrecords();
    cout << endl;
    tm.findmaxrecord();
    tm.findminrecord();
    tm.averagerecord();
    return 0;
}
