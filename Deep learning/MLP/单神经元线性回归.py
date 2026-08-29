import numpy as np

x,y_true = 3.0,5.0
w,b = 0,0 #自定义权重，残差
lr = 0.01 #学习率

for _ in range(200):
    # forward
    y_pred = w * x + b
    #MSE损失函数 loss = (y_pred - y_true) ** 2 
    #MAE损失函数 loss = np.abs(y_pred - y_true)
    #Huber 损失函数 
    delta = 1.0
    e=y_pred - y_true

    # backward 
    print(f"error: {np.abs(e):.4f}, w: {w:.4f}, b: {b:.4f}")

    if(np.abs(e) <= delta):
        d_loss = e
    else:
        d_loss = delta * np.sign(e)

    dypred_dw = x #loss 对 w 的梯度
    dypred_db = 1 #loss 对 b 的梯度

    dloss_dw = d_loss * dypred_dw
    dloss_db = d_loss * dypred_db

    #update
    w -= lr * dloss_dw
    b -= lr * dloss_db  