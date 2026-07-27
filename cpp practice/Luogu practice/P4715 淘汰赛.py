n = int(input())
powers = list(map(int, input().split()))
# 记录每个国家的能力值和编号（编号从1开始）
countries = [(powers[i], i + 1) for i in range(len(powers))]

# 找到冠军（能力值最高的国家）
max_power = max(powers)
champion_idx = powers.index(max_power)
champion = countries[champion_idx]

# 确定冠军所在的半区范围
total = 2 ** n
half = total // 2 #除法取整
# 确定冠军所在的半区起点和终点
if champion_idx < half:
    # 冠军在前半区
    candidates = countries[half:]
else:
    # 冠军在后半区
    candidates = countries[:half]

# 在另外半区中找到能力值最高的国家（亚军）
second_max = -1
runner_up = -1
for power, idx in candidates:
    if power > second_max:
        second_max = power
        runner_up = idx

print(runner_up)