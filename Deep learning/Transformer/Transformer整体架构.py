'''  Encoder
        │
        ▼
Input Token
    │
    ▼
Embedding
    │
    ▼
Positional Encoding
    │
    ▼
┌──────────────────────┐
│   Encoder Layer × 6  │
│                      │
│  Multi-Head Attention│
│          ↓           │
│     Add & Norm       │
│          ↓           │
│        FFN           │
│          ↓           │
│     Add & Norm       │
└──────────────────────┘
    │
    ▼
Encoder Output
    │
    │
    │
    └──────────────────────────┐
                               ▼
                            Decoder
                               │
Target Token                   │
    │                          │
    ▼                          │
Embedding                      │
    │                          │
    ▼                          │
Positional Encoding            │
    │                          │
    ▼                          │
┌──────────────────────────────┐
│     Decoder Layer × 6        │
│                              │
│ Masked Self Attention        │
│          ↓                   │
│      Add & Norm              │
│          ↓                   │
│ Cross Attention ← Encoder ───┤
│          ↓                   │
│      Add & Norm              │
│          ↓                   │
│          FFN                 │
│          ↓                   │
│      Add & Norm              │
└──────────────────────────────┘
    │
    ▼
Linear Projection
    │
    ▼
7个词的概率'''
import torch
import torch.nn as nn
import math


# ============================================================
# 1. 参数
# ============================================================

src_vab = {'P': 0, 'ich': 1, 'mochte': 2, 'ein': 3, 'bier': 4}
src_vocab_size = len(src_vab)

tgt_vocab = {'P': 0, 'i': 1, 'want': 2, 'a': 3, 'beer': 4, 'S': 5, 'E': 6}
tgt_vocab_size = len(tgt_vocab)

src_len = 5
tgt_len = 5

d_model = 512
d_ff = 2048
d_k = d_v = 64

n_layers = 6
n_heads = 8


# ============================================================
# 2. Padding Mask
# ============================================================

def get_attn_pad_mask(seq_q, seq_k):
    """
    seq_q: [batch_size, len_q]
    seq_k: [batch_size, len_k]

    返回：
    pad_attn_mask: [batch_size, len_q, len_k]

    True  -> 这个位置需要被 mask
    False -> 正常参与 attention
    """

    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()

    # 找出 seq_k 中哪些位置是 PAD
    pad_attn_mask = seq_k.eq(0)

    # [batch, len_k]
    # ->
    # [batch, len_q, len_k]
    pad_attn_mask = pad_attn_mask.unsqueeze(1).expand(
        batch_size,
        len_q,
        len_k
    )

    return pad_attn_mask


# ============================================================
# 3. Decoder 的 Subsequence Mask
# ============================================================

def get_attn_subsequence_mask(seq):
    """
    防止 decoder 偷看未来信息

    seq: [batch_size, tgt_len]

    返回：
    [batch_size, tgt_len, tgt_len]
    """

    batch_size, tgt_len = seq.size()

    # 上三角矩阵
    # 例如 tgt_len = 5

    # [[0, 1, 1, 1, 1],
    #  [0, 0, 1, 1, 1],
    #  [0, 0, 0, 1, 1],
    #  [0, 0, 0, 0, 1],
    #  [0, 0, 0, 0, 0]]

    mask = torch.triu(
        torch.ones((tgt_len, tgt_len), dtype=torch.bool),
        diagonal=1
    )

    mask = mask.unsqueeze(0).expand(
        batch_size,
        tgt_len,
        tgt_len
    )

    return mask


# ============================================================
# 4. Positional Encoding
# ============================================================

class PositionalEncoding(nn.Module):

    def __init__(
        self,
        d_model,
        dropout=0.1,
        max_len=5000
    ):
        super(PositionalEncoding, self).__init__()

        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)

        position = torch.arange(
            0,
            max_len,
            dtype=torch.float
        ).unsqueeze(1)

        # 注意：
        # 这里必须是负号
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float()
            * (-math.log(10000.0) / d_model)
        )

        # 偶数维度使用 sin
        pe[:, 0::2] = torch.sin(position * div_term)

        # 奇数维度使用 cos
        pe[:, 1::2] = torch.cos(position * div_term)

        # [max_len, d_model]
        # ->
        # [max_len, 1, d_model]
        pe = pe.unsqueeze(1)

        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        x: [seq_len, batch_size, d_model]
        """

        x = x + self.pe[:x.size(0)]

        return self.dropout(x)


# ============================================================
# 5. Scaled Dot-Product Attention
# ============================================================

class ScaledDotProductAttention(nn.Module):

    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()

    def forward(self, Q, K, V, attn_mask):
        """
        Q: [batch, heads, len_q, d_k]
        K: [batch, heads, len_k, d_k]
        V: [batch, heads, len_k, d_v]

        attn_mask:
        [batch, len_q, len_k]
        """

        # ----------------------------------------------------
        # 第一步：Q × K^T
        # ----------------------------------------------------

        scores = torch.matmul(
            Q,
            K.transpose(-1, -2)
        )

        # ----------------------------------------------------
        # 第二步：除以 sqrt(d_k)
        # ----------------------------------------------------

        scores = scores / math.sqrt(d_k)

        # ----------------------------------------------------
        # 第三步：Mask
        # ----------------------------------------------------

        # [batch, len_q, len_k]
        #
        # ->
        #
        # [batch, 1, len_q, len_k]

        attn_mask = attn_mask.unsqueeze(1)

        scores = scores.masked_fill(
            attn_mask,
            -1e9
        )

        # ----------------------------------------------------
        # 第四步：Softmax
        # ----------------------------------------------------

        attn = torch.softmax(
            scores,
            dim=-1
        )

        # ----------------------------------------------------
        # 第五步：Attention × V
        # ----------------------------------------------------

        context = torch.matmul(
            attn,
            V
        )

        return context, attn


# ============================================================
# 6. Multi-Head Attention
# ============================================================

class MultiHeadAttention(nn.Module):

    def __init__(self):
        super(MultiHeadAttention, self).__init__()

        self.W_Q = nn.Linear(
            d_model,
            d_k * n_heads,
            bias=False
        )

        self.W_K = nn.Linear(
            d_model,
            d_k * n_heads,
            bias=False
        )

        self.W_V = nn.Linear(
            d_model,
            d_v * n_heads,
            bias=False
        )

        self.fc = nn.Linear(
            n_heads * d_v,
            d_model,
            bias=False
        )

    def forward(self, Q, K, V, attn_mask):
        """
        Q/K/V:
        [batch, seq_len, d_model]

        输出：
        context: [batch, seq_len, d_model]
        """

        batch_size = Q.size(0)

        residual = Q

        # ----------------------------------------------------
        # 1. 线性变换得到 Q K V
        # ----------------------------------------------------

        q_s = self.W_Q(Q)
        k_s = self.W_K(K)
        v_s = self.W_V(V)

        # ----------------------------------------------------
        # 2. 拆成多个 head
        # ----------------------------------------------------

        q_s = q_s.view(
            batch_size,
            -1,
            n_heads,
            d_k
        ).transpose(1, 2)

        k_s = k_s.view(
            batch_size,
            -1,
            n_heads,
            d_k
        ).transpose(1, 2)

        v_s = v_s.view(
            batch_size,
            -1,
            n_heads,
            d_v
        ).transpose(1, 2)

        # 现在：
        #
        # Q:
        # [batch, heads, len_q, d_k]
        #
        # K:
        # [batch, heads, len_k, d_k]
        #
        # V:
        # [batch, heads, len_k, d_v]

        # ----------------------------------------------------
        # 3. Scaled Dot-Product Attention
        # ----------------------------------------------------

        context, attn = ScaledDotProductAttention()(
            q_s,
            k_s,
            v_s,
            attn_mask
        )

        # context:
        # [batch, heads, len_q, d_v]

        # ----------------------------------------------------
        # 4. 把多个 head 拼回来
        # ----------------------------------------------------

        context = context.transpose(
            1,
            2
        ).contiguous().view(
            batch_size,
            -1,
            n_heads * d_v
        )

        # ----------------------------------------------------
        # 5. 线性映射
        # ----------------------------------------------------

        output = self.fc(context)

        # ----------------------------------------------------
        # 6. 残差连接 + LayerNorm
        # ----------------------------------------------------

        output = nn.LayerNorm(d_model).to(output.device)(
            output + residual
        )

        return output, attn


# ============================================================
# 7. Feed Forward Network
# ============================================================

class PoswiseFeedForwardNet(nn.Module):

    def __init__(self):
        super(PoswiseFeedForwardNet, self).__init__()

        self.fc = nn.Sequential(

            nn.Linear(
                d_model,
                d_ff,
                bias=False
            ),

            nn.ReLU(),

            nn.Linear(
                d_ff,
                d_model,
                bias=False
            )
        )

    def forward(self, x):

        return self.fc(x)


# ============================================================
# 8. Encoder Layer
# ============================================================

class EncoderLayer(nn.Module):

    def __init__(self):
        super(EncoderLayer, self).__init__()

        self.enc_self_attn = MultiHeadAttention()

        self.pos_ffn = PoswiseFeedForwardNet()

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, enc_inputs, enc_self_attn_mask):

        # ====================================================
        # 第一部分：Self Attention
        # ====================================================

        residual = enc_inputs

        enc_outputs, attn = self.enc_self_attn(
            enc_inputs,
            enc_inputs,
            enc_inputs,
            enc_self_attn_mask
        )

        enc_outputs = self.norm1(
            enc_outputs
        )

        # ====================================================
        # 第二部分：FFN
        # ====================================================

        residual = enc_outputs

        ffn_outputs = self.pos_ffn(
            enc_outputs
        )

        enc_outputs = self.norm2(
            ffn_outputs + residual
        )

        return enc_outputs, attn


# ============================================================
# 9. Encoder
# ============================================================

class Encoder(nn.Module):

    def __init__(self):
        super(Encoder, self).__init__()

        self.src_emb = nn.Embedding(
            src_vocab_size,
            d_model
        )

        self.pos_emb = PositionalEncoding(
            d_model
        )

        self.layers = nn.ModuleList(
            [
                EncoderLayer()
                for _ in range(n_layers)
            ]
        )

    def forward(self, enc_inputs):

        # ----------------------------------------------------
        # 1. 词嵌入
        # ----------------------------------------------------

        enc_outputs = self.src_emb(
            enc_inputs
        )

        # enc_outputs:
        # [batch, src_len, d_model]

        # ----------------------------------------------------
        # 2. 变成 [seq_len, batch, d_model]
        # ----------------------------------------------------

        enc_outputs = enc_outputs.transpose(
            0,
            1
        )

        # ----------------------------------------------------
        # 3. 位置编码
        # ----------------------------------------------------

        enc_outputs = self.pos_emb(
            enc_outputs
        )

        # ----------------------------------------------------
        # 4. 再变回 [batch, seq_len, d_model]
        # ----------------------------------------------------

        enc_outputs = enc_outputs.transpose(
            0,
            1
        )

        # ----------------------------------------------------
        # 5. Padding Mask
        # ----------------------------------------------------

        enc_self_attn_mask = get_attn_pad_mask(
            enc_inputs,
            enc_inputs
        )

        enc_self_attns = []

        # ----------------------------------------------------
        # 6. 经过 6 个 Encoder Layer
        # ----------------------------------------------------

        for layer in self.layers:

            enc_outputs, enc_self_attn = layer(
                enc_outputs,
                enc_self_attn_mask
            )

            enc_self_attns.append(
                enc_self_attn
            )

        return enc_outputs, enc_self_attns


# ============================================================
# 10. Decoder Layer
# ============================================================

class DecoderLayer(nn.Module):

    def __init__(self):
        super(DecoderLayer, self).__init__()

        # Decoder Self Attention

        self.dec_self_attn = MultiHeadAttention()

        # Encoder-Decoder Attention

        self.dec_enc_attn = MultiHeadAttention()

        self.pos_ffn = PoswiseFeedForwardNet()

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)

    def forward(
        self,
        dec_inputs,
        enc_outputs,
        dec_self_attn_mask,
        dec_enc_attn_mask
    ):

        # ====================================================
        # 1. Decoder Self Attention
        # ====================================================

        residual = dec_inputs

        dec_outputs, dec_self_attn = self.dec_self_attn(
            dec_inputs,
            dec_inputs,
            dec_inputs,
            dec_self_attn_mask
        )

        dec_outputs = self.norm1(
            dec_outputs
        )

        # ====================================================
        # 2. Cross Attention
        # ====================================================

        residual = dec_outputs

        dec_outputs, dec_enc_attn = self.dec_enc_attn(
            dec_outputs,
            enc_outputs,
            enc_outputs,
            dec_enc_attn_mask
        )

        dec_outputs = self.norm2(
            dec_outputs
        )

        # ====================================================
        # 3. Feed Forward
        # ====================================================

        residual = dec_outputs

        ffn_outputs = self.pos_ffn(
            dec_outputs
        )

        dec_outputs = self.norm3(
            ffn_outputs + residual
        )

        return (
            dec_outputs,
            dec_self_attn,
            dec_enc_attn
        )


# ============================================================
# 11. Decoder
# ============================================================

class Decoder(nn.Module):

    def __init__(self):
        super(Decoder, self).__init__()

        self.tgt_emb = nn.Embedding(
            tgt_vocab_size,
            d_model
        )

        self.pos_emb = PositionalEncoding(
            d_model
        )

        self.layers = nn.ModuleList(
            [
                DecoderLayer()
                for _ in range(n_layers)
            ]
        )

    def forward(
        self,
        dec_inputs,
        enc_inputs,
        enc_outputs
    ):

        # ----------------------------------------------------
        # 1. Target Embedding
        # ----------------------------------------------------

        dec_outputs = self.tgt_emb(
            dec_inputs
        )

        # [batch, tgt_len, d_model]

        # ----------------------------------------------------
        # 2. Position Encoding
        # ----------------------------------------------------

        dec_outputs = dec_outputs.transpose(
            0,
            1
        )

        dec_outputs = self.pos_emb(
            dec_outputs
        )

        dec_outputs = dec_outputs.transpose(
            0,
            1
        )

        # ----------------------------------------------------
        # 3. Decoder Self Attention Mask
        # ----------------------------------------------------

        dec_self_attn_pad_mask = get_attn_pad_mask(
            dec_inputs,
            dec_inputs
        )

        dec_self_attn_subsequence_mask = get_attn_subsequence_mask(
            dec_inputs
        )

        # 两个 Mask 合并
        dec_self_attn_mask = (
            dec_self_attn_pad_mask
            |
            dec_self_attn_subsequence_mask
        )

        # ----------------------------------------------------
        # 4. Cross Attention Mask
        # ----------------------------------------------------

        dec_enc_attn_mask = get_attn_pad_mask(
            dec_inputs,
            enc_inputs
        )

        dec_self_attns = []
        dec_enc_attns = []

        # ----------------------------------------------------
        # 5. 经过 6 个 Decoder Layer
        # ----------------------------------------------------

        for layer in self.layers:

            dec_outputs, dec_self_attn, dec_enc_attn = layer(
                dec_outputs,
                enc_outputs,
                dec_self_attn_mask,
                dec_enc_attn_mask
            )

            dec_self_attns.append(
                dec_self_attn
            )

            dec_enc_attns.append(
                dec_enc_attn
            )

        return (
            dec_outputs,
            dec_self_attns,
            dec_enc_attns
        )


# ============================================================
# 12. Transformer
# ============================================================

class Transformer(nn.Module):

    def __init__(self):

        super(Transformer, self).__init__()

        self.encoder = Encoder()

        self.decoder = Decoder()

        self.projection = nn.Linear(
            d_model,
            tgt_vocab_size,
            bias=False
        )

    def forward(
        self,
        enc_inputs,
        dec_inputs
    ):

        # ====================================================
        # Encoder
        # ====================================================

        enc_outputs, enc_self_attns = self.encoder(
            enc_inputs
        )

        # ====================================================
        # Decoder
        # ====================================================

        dec_outputs, dec_self_attns, dec_cross_attns = self.decoder(
            dec_inputs,
            enc_inputs,
            enc_outputs
        )

        # ====================================================
        # Projection
        # ====================================================

        dec_logits = self.projection(
            dec_outputs
        )

        # [batch, tgt_len, vocab_size]
        #
        # ->
        #
        # [batch*tgt_len, vocab_size]

        return (
            dec_logits.view(-1, dec_logits.size(-1)),
            enc_self_attns,
            dec_self_attns,
            dec_cross_attns
        )


# ============================================================
# 13. 测试
# ============================================================

if __name__ == '__main__':

    sentences = [
        ['ich', 'mochte', 'ein', 'bier', 'P'],
        ['S', 'i', 'want', 'a', 'beer'],
        ['i', 'want', 'a', 'beer', 'E']
    ]

    # -----------------------------------------
    # Encoder 输入
    # -----------------------------------------

    enc_inputs = torch.tensor([
        [
            src_vab['ich'],
            src_vab['mochte'],
            src_vab['ein'],
            src_vab['bier'],
            src_vab['P']
        ]
    ])

    # -----------------------------------------
    # Decoder 输入
    # S i want a beer
    # -----------------------------------------

    dec_inputs = torch.tensor([
        [
            tgt_vocab['S'],
            tgt_vocab['i'],
            tgt_vocab['want'],
            tgt_vocab['a'],
            tgt_vocab['beer']
        ]
    ])

    # -----------------------------------------
    # 创建 Transformer
    # -----------------------------------------

    model = Transformer()

    # -----------------------------------------
    # 前向传播
    # -----------------------------------------

    dec_logits, enc_self_attns, dec_self_attns, dec_cross_attns = model(
        enc_inputs,
        dec_inputs
    )
    
    #softmax
    dec_probs = torch.softmax(dec_logits, dim=-1)
    print("dec_probs.shape:")
    print(dec_probs.shape)

    print("概率：")
    print(dec_probs)
    