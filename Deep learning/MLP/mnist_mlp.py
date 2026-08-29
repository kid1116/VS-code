import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# 1. 固定随机种子
torch.manual_seed(42)

# 2. 超参数设置
batch_size = 64
learning_rate = 0.01
epochs = 10

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

# 4. 定义MLP模型（对比你的双层，这里升级为3层）
class MNIST_MLP(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入28x28=784维 -> 隐藏1(256) -> 隐藏2(128) -> 输出10类(0-9)
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # x形状: (batch_size, 1, 28, 28) -> 展平为 (batch_size, 784)
        x = x.view(-1, 784)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)  # 注意！这里不加Softmax，因为CrossEntropyLoss自带
        return x

# 5. 实例化模型、损失函数、优化器
model = MNIST_MLP()
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