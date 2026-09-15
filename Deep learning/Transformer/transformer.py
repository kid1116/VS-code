import torch
import torch.nn as nn
import encoder
import decoder

#定义超参数：
d_model = 512  # 词向量维度
tgt_vocab_size = 10000  # 目标词汇表大小

#核心架构分为三部分：编码层，解码层，输出层
class Transformer(nn.Module):
    def __init__(self):
        super(Transformer, self).__init__()
        self.encoder = encoder.Encoder()  # 编码层
        self.decoder = decoder.Decoder()  # 解码层
        self.projection = nn.Linear(
            d_model, 
            tgt_vocab_size,
            bias=False
        )  # 输出层

    def forward(self,enc_inputs,dec_inputs):

        # 1.编码层
        enc_outputs = self.encoder(enc_inputs)

        # 2.解码层
        dec_outputs = self.decoder(dec_inputs,enc_outputs)

        # 3.输出层
        dec_logits = self.projection(dec_outputs)

        return dec_logits

        