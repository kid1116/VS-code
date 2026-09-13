import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
from torch.utils.data import DataLoader

# 1. 固定随机种子
torch.manual_seed(42)

# 2. 超参数设置
batch_size = 64
learning_rate = 0.01
epochs = 5

# 3. 数据加载（PyTorch自带MNIST）
transform = transforms.Compose([
    transforms.ToTensor(),  # 把图片(0-255)转为Tensor(0-1)
    transforms.Normalize((0.1307,), (0.3081,))  # 标准化（均值0.1307，标准差0.3081）
])

# 下载训练集和测试集
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, 
                                           download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, 
                                          download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 4. CNN模型定义（对比你的MLP，这里升级为卷积神经网络）
class MNIST_CNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        # ========== 1. CNN特征提取器（代替原来的 fc1+fc2） ==========
        # 输入: (batch, 1, 28, 28)
        # 参数: 输入通道1，输出通道32，卷积核3x3，填充1（保持尺寸不变）
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        
        # 输入: (batch, 32, 28, 28) -> 经过MaxPool变成 (batch, 32, 14, 14)
        # 参数: 输入通道32，输出通道64，卷积核3x3，填充1
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        # 注意：这里没有写池化层，而是在 forward 里直接调用 F.max_pool2d，更灵活
        
        # ========== 2. 全连接分类器（就是你熟悉的 MLP！） ==========
        # 经过两次池化（2x2），28 -> 14 -> 7
        # 最后一层特征图尺寸：64通道 * 7 * 7 = 3136
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 相当于你原来的隐藏层
        self.fc2 = nn.Linear(128, 10)          # 输出10类
        
        # 在类内部定义一个 Dropout 防过拟合（CNN 里很常用）
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        # ---------- 第一阶段：卷积提取特征 ----------
        # x 输入形状: (batch, 1, 28, 28)
        x = self.conv1(x)          # (batch, 32, 28, 28)
        x = F.relu(x)              # 激活（和你MLP的ReLU完全一样！）
        x = F.max_pool2d(x, 2)     # 2x2池化 -> (batch, 32, 14, 14)
        
        x = self.conv2(x)          # (batch, 64, 14, 14)
        x = F.relu(x)              
        x = F.max_pool2d(x, 2)     # 2x2池化 -> (batch, 64, 7, 7)  收工！
        
        # ---------- 第二阶段：拉直 + MLP分类（你完全懂的部分） ----------
        # 这一步就相当于你原来的 x.view(-1, 784)
        x = x.view(x.size(0), -1)  # 拉直成 (batch, 64*7*7=3136)
        
        x = self.fc1(x)            # 相当于你的第一层全连接 (3136 -> 128)
        x = F.relu(x)              
        x = self.dropout(x)        # 随机杀死25%的神经元（防止过拟合的小技巧）
        
        x = self.fc2(x)            # 输出 (128 -> 10)
        return x

# 5. 实例化模型、损失函数、优化器
model = MNIST_CNN()
criterion = nn.CrossEntropyLoss()  # 替换掉你的MSE
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# 6. 训练（5个Epoch）
print("开始训练...")
for epoch in range(epochs):
    running_loss = 0.0
    for images, labels in train_loader:
        # 前向传播
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}")

# 7. 测试（看准确率）
print("\n开始测试...")
correct = 0
total = 0
with torch.no_grad():  # 测试时不计算梯度，省内存
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)  # 取概率最大的类别
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"测试集准确率: {100 * correct / total:.2f}%")