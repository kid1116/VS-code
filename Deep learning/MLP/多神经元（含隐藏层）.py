import numpy as np

# 输入 
X = np.array([0.5, -0.3])  # 形状 (2,)
y_true = np.array([1.0])  # 形状 (1,)

# 参数初始化
W1 = np.random.randn(2, 4) * 0.1  # 输入2维 → 隐藏层4个神经元
b1 = np.zeros(4)                  # 每个隐藏神经元自带一个偏置

W2 = np.random.randn(4, 1) * 0.1  # 隐藏层4维 → 输出1个神经元
b2 = np.zeros(1)

for epoch in range(100):
# 前向传播
    z1 = X @ W1 + b1      # 形状 (4,)
    a1 = np.maximum(0, z1) # ReLU激活函数
    z2 = a1 @ W2 + b2     # 形状 (1,) 
    y_pred = z2

# 假设 y_true = 1.0，用 MSE
    loss = (y_pred - y_true)**2
    print(f"Epoch {epoch}, Loss: {loss}")
    d_loss = 2 * (y_pred - y_true)  # 总指挥信号，形状 (1,)

# --- 第2层（输出层）反向传播
    dloss_dz2 = d_loss                 # 形状 (1,)
    dloss_dW2 = a1.reshape(4, 1) @ dloss_dz2.reshape(1, 1)  # 矩阵形式：(4,1) @ (1,1) = (4,1)
    dloss_db2 = dloss_dz2              # 形状 (1,)

# 把误差继续往上传（传给隐藏层）
    dloss_da1 = dloss_dz2 @ W2.T      # 形状 (4,)

# --- 第1层（隐藏层）反向传播（穿过ReLU激活函数）---
# ReLU 的导数：输入 > 0 时为1，否则为0
    drelu = (z1 > 0).astype(float)     # 形状 (4,)
    dloss_dz1 = dloss_da1 * drelu      # 形状 (4,)

    dloss_dW1 = X.reshape(2, 1) @ dloss_dz1.reshape(1, 4)  # (2,4)
    dloss_db1 = dloss_dz1              # 形状 (4,)

    lr = 0.01
    W1 -= lr * dloss_dW1
    b1 -= lr * dloss_db1
    W2 -= lr * dloss_dW2
    b2 -= lr * dloss_db2