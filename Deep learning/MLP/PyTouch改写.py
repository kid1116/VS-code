import torch

# 设置随机种子，保证和你的 Numpy 实验初始值一致（方便对比）
torch.manual_seed(42)  # 注意：PyTorch 的随机种子和 Numpy 分开

# ---------- 1. 数据（完全照搬） ----------
X = torch.tensor([0.5, -0.3])          # 形状 (2,)
y_true = torch.tensor([1.0])           # 形状 (1,)

# ---------- 2. 参数（必须开启梯度追踪） ----------
# 之前的 W1 = np.random.randn(2,4)*0.1
W1 = torch.randn(2, 4) * 0.1 
W1.requires_grad_(True) 
b1 = torch.zeros(4, requires_grad=True)           

# 之前的 W2 = np.random.randn(4,1)*0.1
W2 = torch.randn(4, 1) * 0.1  
W2.requires_grad_(True)
b2 = torch.zeros(1, requires_grad=True)           

# ---------- 3. 前向传播（和 Numpy 写法 99% 相同） ----------
z1 = X @ W1 + b1          # 形状 (4,)
a1 = torch.relu(z1)       # 等价于 np.maximum(0, z1)
z2 = a1 @ W2 + b2         # 形状 (1,)
y_pred = z2

for _ in range(100):  # 训练 10 次
    # 前向传播
    z1 = X @ W1 + b1
    a1 = torch.relu(z1)
    z2 = a1 @ W2 + b2
    y_pred = z2
# 损失函数（MSE）
    loss = (y_pred - y_true).pow(2).sum()  # 因为只有一个样本，sum 和 mean 等价
    print(f"loss: {loss.item():.4f}")  # loss.item() 可以得到 Python float

# ---------- 4. 反向传播（告别手写公式！） ----------
    loss.backward()  # 这一行，自动计算了 dloss_dW1, dloss_db1, dloss_dW2, dloss_db2

# ---------- 5. 参数更新（梯度下降） ----------
    lr = 0.01
    with torch.no_grad():  # 重要！更新参数时，必须暂停梯度追踪
     W1 -= lr * W1.grad
     b1 -= lr * b1.grad
     W2 -= lr * W2.grad
     b2 -= lr * b2.grad
    
    # 清空梯度（否则下一轮反向传播会累加）
     W1.grad.zero_()
     b1.grad.zero_()
     W2.grad.zero_()
     b2.grad.zero_()

