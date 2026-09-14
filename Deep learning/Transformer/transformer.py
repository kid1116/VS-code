import torch
import torch.nn as nn

#核心架构分为三部分：编码层，解码层，输出层
class Transformer(nn.Module):
    def __init__(self):
        super(Transformer, self).__init__()
        self.encoder = Encoder()  # 编码层
        self.decoder = Decoder()  # 解码层
        self.projection = nn.Linear(d_model, tgt_vocab_size,bias=False)  # 输出层
    def forward(self,enc_inputs,dec_inputs):
        