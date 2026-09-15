'''            Decoder Layer
                     │
                     ▼
               Decoder输入 X
                     │
                     ▼
        Masked Self-Attention
                     │
                     ▼
               Add & Norm
                     │
                     ▼
              Cross-Attention
                     ▲
                     │
               Encoder输出
                     │
                     ▼
               Add & Norm
                     │
                     ▼
                   FFN
                     │
                     ▼
               Add & Norm
                     │
                     ▼
                  输出'''

import torch
import torch.nn as nn

#超参数
d_model = 512  # 词向量维度
src_vocab_size = 10000  # 源词汇表大小
num_layers = 6  # 解码层数量
n_heads = 8  # 多头注意力头数
d_ff = 2048  # 前馈网络隐藏层维度
dropout = 0.1  # Dropout概率

class Decoder(nn.Module):
    def __init__(self):
        super(Decoder, self).__init__()

        self.embedding = nn.Embedding(src_vocab_size, d_model)  # 词嵌入层

        self.layers = nn.ModuleList([DecoderLayer() for _ in range(num_layers)])  # 解码层堆叠

    def forward(self, enc_inputs):
        # 1.词嵌入
        dec_outputs = self.embedding(enc_inputs)

        # 2.解码层堆叠
        for layer in self.layers:
            dec_outputs = layer(dec_outputs)

        return dec_outputs
    
class DecoderLayer(nn.Module):
    def __init__(self,d_model,num_heads,d_ff,dropout):
        super(DecoderLayer, self).__init__()

        self.self_attn =nn.MultiHeadAttention(
            d_model,num_heads)

        self.cross_attn = nn.MultiHeadAttention(
            d_model,num_heads)

        self.feed_forward = nn.Sequential(
            nn.Linear(d_model,d_ff),
            nn.ReLU(),
            nn.Linear(d_ff,d_model)
        )

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_outputs, self_mask=None, cross_mask=None):
        self_attn_output, _ = self.self_attn(
            x, x, x,self_mask
        )
        x = self.norm1(x + self_attn_output)

        cross_attn_output= self.cross_attn(
            x, enc_outputs, enc_outputs, cross_mask
        )
        x = self.norm2(x + cross_attn_output)

        ffn_output = self.feed_forward(x)
        x = self.norm3(x + ffn_output)

        return x
        