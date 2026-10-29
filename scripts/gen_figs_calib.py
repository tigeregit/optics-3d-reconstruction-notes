#!/usr/bin/env python3
"""Calibration-chapter figures: pipeline, residual bowl, hand-eye."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT = Path(__file__).resolve().parents[1] / "figures"
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42
NOTE = "概念草图，非精确工程图（数量级示意）"


def fig_calib_pipeline():
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    ax.set_xlim(0, 9.2); ax.set_ylim(0, 3.4); ax.axis("off")
    steps = [
        (0.2, "拍多姿态\n标定板"),
        (1.7, "检角点\n亚像素"),
        (3.2, "单应初值\nZhang"),
        (4.7, "LM/BA\n精炼"),
        (6.2, "输出\n$K$、畸变、$R_i,t_i$"),
        (7.7, "金标准\n抽检"),
    ]
    for i, (x, lab) in enumerate(steps):
        ax.add_patch(FancyBboxPatch((x, 1.1), 1.35, 1.35, boxstyle="round,pad=0.04",
                                    fc="#E3F2FD", ec="#1565C0", lw=1.4))
        ax.text(x + 0.675, 1.78, lab, ha="center", va="center", fontsize=12, linespacing=1.35)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.55, 1.78), xytext=(x + 1.35, 1.78),
                        arrowprops=dict(arrowstyle="->", lw=1.6, color="#333"))
    ax.text(4.6, 3.05, "单目平面靶标定流程（Zhang → LM/BA）", ha="center", fontsize=14)
    ax.text(4.6, 0.45, "双目 / 相机–投影仪：在共享靶点上再估相对外参；手眼另见 AX=XB",
            ha="center", fontsize=11, color="#444")
    fig.text(0.5, 0.02, NOTE, ha="center", fontsize=9, color="#888")
    fig.savefig(OUT / "fig-calib-pipeline.pdf", bbox_inches="tight"); plt.close(fig)


def fig_reproj_bowl():
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    # Bowl-shaped cost landscape in (tx, k1) — schematic
    tx = np.linspace(-1.0, 1.0, 120)
    k1 = np.linspace(-1.0, 1.0, 120)
    TX, K1 = np.meshgrid(tx, k1)
    # Elongated valley: strong constraint on tx, weak on k1 (observability sketch)
    J = (TX - 0.15) ** 2 + 0.12 * (K1 + 0.3) ** 2 + 0.04 * TX * K1
    cs = ax.contourf(TX, K1, J, levels=18, cmap="YlOrBr")
    ax.contour(TX, K1, J, levels=10, colors="#5D4037", linewidths=0.5, alpha=0.5)
    ax.plot(0.15, -0.3, "o", color="#B71C1C", ms=8, label="真值附近")
    ax.plot([-0.6], [0.7], "s", color="#1565C0", ms=7, label="坏初值")
    ax.annotate("", xy=(0.05, -0.15), xytext=(-0.55, 0.65),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.5))
    ax.set_xlabel(r"平移参数 $t_x$（示意坐标）", fontsize=12)
    ax.set_ylabel(r"畸变 $k_1$（示意坐标）", fontsize=12)
    ax.set_title("重投影代价的碗形与狭长谷（可观性示意）", fontsize=13)
    ax.legend(loc="upper right", fontsize=10)
    fig.colorbar(cs, ax=ax, fraction=0.046, pad=0.04, label=r"$C=\sum\|e\|^2$")
    fig.text(0.5, 0.01, NOTE, ha="center", fontsize=9, color="#888")
    fig.savefig(OUT / "fig-reproj-bowl.pdf", bbox_inches="tight"); plt.close(fig)


def fig_handeye():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 7.2); ax.set_ylim(0, 4.6); ax.axis("off")
    # Probe body
    ax.add_patch(FancyBboxPatch((0.6, 1.6), 2.2, 1.4, boxstyle="round,pad=0.05",
                                fc="#ECEFF1", ec="#455A64", lw=1.5))
    ax.text(1.7, 2.7, "探头本体\n（手）", ha="center", va="center", fontsize=12)
    # Camera
    ax.add_patch(FancyBboxPatch((3.4, 2.55), 1.6, 0.95, boxstyle="round,pad=0.04",
                                fc="#E3F2FD", ec="#1565C0", lw=1.5))
    ax.text(4.2, 3.02, "相机\n（眼）", ha="center", va="center", fontsize=12)
    # Target
    ax.add_patch(Rectangle((5.2, 0.7), 1.5, 1.5, fill=False, ec="#E65100", lw=1.5, linestyle="--"))
    for i in range(4):
        for j in range(4):
            if (i + j) % 2 == 0:
                ax.add_patch(Rectangle((5.2 + i * 0.375, 0.7 + j * 0.375), 0.375, 0.375,
                                       fc="#FFECB3", ec="none"))
    ax.text(5.95, 0.35, "标定板（世界）", ha="center", fontsize=11)

    def arrow(x1, y1, x2, y2, text, color="#333"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.7, color=color))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, text, ha="center", fontsize=11, color=color)

    arrow(2.8, 2.3, 3.4, 2.85, r"$X_{\mathrm{he}}$", "#6A1B9A")
    # Relative motions A_i (eye), B_i (hand) for one motion segment
    # Draw two poses of probe+camera as dashed ghosts, arrows for relative A_i, B_i
    ax.add_patch(FancyBboxPatch((0.35, 0.55), 1.5, 0.85, boxstyle="round,pad=0.03",
                                fc="#FAFAFA", ec="#90A4AE", lw=1.0, linestyle="--"))
    ax.text(1.1, 0.97, "手$_{i}$", ha="center", va="center", fontsize=10, color="#607D8B")
    ax.add_patch(FancyBboxPatch((2.55, 0.85), 1.1, 0.65, boxstyle="round,pad=0.03",
                                fc="#E8F5E9", ec="#81C784", lw=1.0, linestyle="--"))
    ax.text(3.1, 1.17, "眼$_{i}$", ha="center", va="center", fontsize=10, color="#2E7D32")
    # B_i: hand_i -> hand_{i+1}
    ax.annotate("", xy=(1.5, 1.6), xytext=(1.1, 1.4),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#455A64"))
    ax.text(0.55, 1.55, r"$B_i$（手相对）", fontsize=11, color="#455A64")
    # A_i: eye_i -> eye_{i+1}
    ax.annotate("", xy=(3.5, 2.55), xytext=(3.1, 1.5),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="#1565C0"))
    ax.text(3.7, 1.85, r"$A_i$（眼相对）", fontsize=11, color="#1565C0")
    ax.text(3.6, 4.25, r"手眼：$A_i X_{\mathrm{he}} = X_{\mathrm{he}} B_i$（相对运动，$A_i,B_i$ 同段）",
            ha="center", fontsize=13)
    ax.text(3.6, 3.85, r"口扫：多段相对运动求固定手眼变换 $X_{\mathrm{he}}$",
            ha="center", fontsize=11, color="#444")
    fig.text(0.5, 0.02, NOTE, ha="center", fontsize=9, color="#888")
    fig.savefig(OUT / "fig-handeye.pdf", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_calib_pipeline(); fig_reproj_bowl(); fig_handeye()
    print("done")
