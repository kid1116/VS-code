import time

for i in range(101): # 添加进度条图形和百分比
    bar = '[' + '-' * (i // 2) + ' ' * (50 - i // 2) + ']'
    print(f"\r{bar} {i:3}%", end='', flush=True)
    time.sleep(0.02)
print()