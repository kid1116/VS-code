import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 创建画布和子图
fig, ax = plt.subplots(figsize=(10, 12), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')  # 隐藏坐标轴

# 定义绘制逻辑门的函数
def draw_gate(x, y, label, inner_text, has_bubble=False, is_compound=False):
    # 输入线
    if not is_compound:
        ax.plot([x-1, x], [y+0.3, y+0.3], 'k-', lw=1)
        ax.plot([x-1, x], [y-0.3, y-0.3], 'k-', lw=1)
    else:
        # 与或门/与或非门 4 输入
        ax.plot([x-1, x], [y+0.5, y+0.5], 'k-', lw=1)
        ax.plot([x-1, x], [y+0.2, y+0.2], 'k-', lw=1)
        ax.plot([x-1, x], [y-0.2, y-0.2], 'k-', lw=1)
        ax.plot([x-1, x], [y-0.5, y-0.5], 'k-', lw=1)
    
    # 门主体方框
    if not is_compound:
        rect = patches.Rectangle((x, y-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='white')
        ax.add_patch(rect)
        ax.text(x+0.5, y, inner_text, ha='center', va='center', fontsize=10)
        # 输出线
        if has_bubble:
            ax.plot([x+1, x+1.3], [y, y], 'k-', lw=1)
            circle = patches.Circle((x+1.3, y), 0.08, linewidth=1, edgecolor='k', facecolor='white')
            ax.add_patch(circle)
            ax.plot([x+1.38, x+1.8], [y, y], 'k-', lw=1)
        else:
            ax.plot([x+1, x+1.8], [y, y], 'k-', lw=1)
    else:
        # 复合门：与+或
        rect1 = patches.Rectangle((x, y-0.6), 0.8, 1.2, linewidth=1, edgecolor='k', facecolor='white')
        rect2 = patches.Rectangle((x+0.8, y-0.6), 0.8, 1.2, linewidth=1, edgecolor='k', facecolor='white')
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.text(x+0.4, y, '&', ha='center', va='center', fontsize=10)
        ax.text(x+1.2, y, '≥1', ha='center', va='center', fontsize=10)
        # 输出线
        if has_bubble:
            ax.plot([x+1.6, x+1.9], [y, y], 'k-', lw=1)
            circle = patches.Circle((x+1.9, y), 0.08, linewidth=1, edgecolor='k', facecolor='white')
            ax.add_patch(circle)
            ax.plot([x+1.98, x+2.4], [y, y], 'k-', lw=1)
        else:
            ax.plot([x+1.6, x+2.4], [y, y], 'k-', lw=1)
    
    # 标签
    ax.text(x-1.2, y, label, ha='right', va='center', fontsize=9)

# 逐个绘制逻辑门
gate_list = [
    ("非门", 10, "1", False, False),
    ("与门", 9, "&", False, False),
    ("或门", 8, "≥1", False, False),
    ("与非门", 7, "&", True, False),
    ("或非门", 6, "≥1", True, False),
    ("异或门", 5, "=1", False, False),
    ("同或门", 4, "=1", True, False),
    ("与或门", 2, "", False, True),
    ("与或非门", 1, "", True, True),
]

for i, (name, y, inner, bubble, compound) in enumerate(gate_list):
    draw_gate(2, y, name, inner, bubble, compound)

# 标题
ax.text(5, 11.5, "逻辑门国标符号汇总", ha='center', va='center', fontsize=14, weight='bold')

plt.tight_layout()
plt.savefig("logic_gates_summary.png", dpi=150, bbox_inches='tight')
plt.show()