'''              Encoder
                    │
              输入 token
                    ↓
              Token Embedding
                    ↓
           Positional Encoding
                    ↓
        ┌─────────────────────┐
        │   Encoder Layer     │
        │                     │
        │ Multi-Head Attention│
        │          ↓          │
        │    Add & Norm       │
        │          ↓          │
        │       FFN           │
        │          ↓          │
        │    Add & Norm       │
        └─────────────────────┘
                    ↓
              Encoder Layer
                    ↓
                   ...
                    ↓
              enc_outputs'''

import torch
import torch.nn as nn

#超参数
d_model = 512  # 词向量维度
src_vocab_size = 10000  # 源词汇表大小
num_layers = 6  # 编码层数量
n_heads = 8  # 多头注意力头数
d_ff = 2048  # 前馈网络隐藏层维度
dropout = 0.1  # Dropout概率

class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()

        self.embedding = nn.Embedding(src_vocab_size, d_model)  # 词嵌入层

        self.layers = nn.ModuleList([EncoderLayer() for _ in range(num_layers)])  # 编码层堆叠

    def forward(self, enc_inputs):
        # 1.词嵌入
        enc_outputs = self.embedding(enc_inputs)

        # 2.编码层堆叠
        for layer in self.layers:
            enc_outputs = layer(enc_outputs)

        return enc_outputs

class EncoderLayer(nn.Module):
    def __init__(self,d_model,n_heads,d_ff,dropout):
        super(EncoderLayer, self).__init__()

        # 多头自注意力机制  
        self.self_attn = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=n_heads,
            dropout=dropout,
            batch_first=True
        )

        # 前馈神经网络
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

        #两个层归一化
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        # Dropout层
        self.dropout = nn.Dropout(dropout)

    def forward(self,x,mask=None):

        # 1.多头自注意力机制
        attn_output,_ = self.self_attn(
            x,
            x,
            x,
            attn_mask=mask
        )

        #Dropout，残差连接和归一化
        attn_output = self.dropout(attn_output)
        x = self.norm1(x + attn_output)

        # 2.前馈神经网络
        ffn_output = self.feed_forward(x)
        ffn_output = self.dropout(ffn_output)
        x = self.norm2(x + ffn_output)

        return x

x=torch.randn(2,5,512)
output=EncoderLayer(d_model, n_heads, d_ff, dropout).forward(x)
print(x.shape)
print(output.shape)