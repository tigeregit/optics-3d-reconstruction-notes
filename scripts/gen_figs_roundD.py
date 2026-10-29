#!/usr/bin/env python3
"""Round D figures: MTF cascade, sensor comparison, error budget map."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "figures"
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42
NOTE = "概念草图，非精确工程图（数量级示意）"


def mtf_diff(x):
    x = np.clip(x, 0, 1)
    return 2 / np.pi * (np.arccos(x) - x * np.sqrt(1 - x ** 2))


def fig_mtf_curve():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    nu = np.linspace(0, 1, 400)  # normalized to diffraction cutoff
    d = mtf_diff(nu)
    defocus = np.abs(np.sinc(2.2 * nu))  # simple geometric-defocus proxy
    pix = np.abs(np.sinc(nu / 0.6))      # pixel aperture, Nyquist at 0.3
    ax = axes[0]
    ax.plot(nu, d, label="衍射限", lw=1.6)
    ax.plot(nu, defocus, label="离焦（示意）", lw=1.2)
    ax.plot(nu, pix, label="像元孔径", lw=1.2)
    ax.plot(nu, d * defocus * pix, "k", lw=2.2, label="级联 = 乘积")
    ax.axvline(0.3, color="#999", ls="--"); ax.text(0.31, 0.9, "奈奎斯特", fontsize=8, color="#666")
    ax.set_xlabel("空间频率（归一化到衍射截止）"); ax.set_ylabel("MTF")
    ax.set_title("MTF 级联", fontsize=11); ax.legend(fontsize=8); ax.grid(alpha=0.3)
    ax = axes[1]
    nf = np.linspace(0.02, 0.3, 200)
    m = mtf_diff(nf) * np.abs(np.sinc(2.2 * nf)) * np.abs(np.sinc(nf / 0.6))
    m2 = m ** 2  # projector chain * camera chain (similar optics)
    sig = (1 / nf) / np.maximum(m2, 1e-3)  # depth noise ∝ P/M
    sig /= sig.min()
    ax.plot(nf, m2, color="#1565C0", lw=2, label="投影×相机 链路 MTF")
    ax2 = ax.twinx()
    ax2.plot(nf, sig, color="#C62828", lw=2, label="相对深度噪声 ∝ P/M")
    ax2.set_ylim(0, 6); ax2.set_ylabel("相对深度噪声", color="#C62828")
    ax.set_xlabel("条纹空间频率（归一化）"); ax.set_ylabel("调制传递", color="#1565C0")
    ax.set_title("条纹周期选择：存在最优区间", fontsize=11); ax.grid(alpha=0.3)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper center")
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=10, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-mtf-curve.pdf", bbox_inches="tight"); plt.close(fig)


def fig_sensor_compare():
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    # 与正文表 tab:ch09-compare 一致（分辨率 mm, 量程 mm）
    items = [
        ("共聚焦", 1e-3, 2e-2, 1e-1, 2e1, "#1565C0"),
        ("OCT", 2e-3, 1e-2, 5e-1, 5e0, "#6A1B9A"),
        ("结构光", 3e-3, 5e-2, 1e0, 5e2, "#2E7D32"),
        ("立体", 1e-2, 1e0, 1e0, 2e4, "#E65100"),
        ("ToF", 1e0, 3e1, 1e2, 2e4, "#C62828"),
    ]
    # 共聚焦与 OCT 区域重叠：二者标签移到框外并用引线指向各自框
    offsets = {"共聚焦": (5e-3, 1.5e-3), "OCT": (5e-3, 8e-2)}
    anchors = {"共聚焦": (0.25, 1.6e-3), "OCT": (1.5, 5e-3)}
    for name, r0, r1, z0, z1, c in items:
        ax.add_patch(plt.Rectangle((z0, r0), z1 - z0, r1 - r0, fc=c, alpha=0.25, ec=c, lw=1.5))
        cx, cy = np.sqrt(z0 * z1), np.sqrt(r0 * r1)
        if name in offsets:
            tx, ty = offsets[name]
            ax.annotate(name, xy=anchors[name], xytext=(tx, ty), fontsize=11, color=c,
                        ha="center", va="center",
                        arrowprops=dict(arrowstyle="-", color=c, lw=1.0))
        else:
            ax.text(cx, cy, name, ha="center", va="center", fontsize=13, color=c)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(5e-4, 3e4); ax.set_ylim(5e-4, 1e2)
    ax.set_xlabel("深度量程 / 工作范围（mm）"); ax.set_ylabel("深度分辨率（mm）")
    ax.set_title("深度传感方式：分辨率 vs 量程（数量级示意）", fontsize=11)
    ax.grid(alpha=0.3, which="both")
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=10, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-sensor-compare.pdf", bbox_inches="tight"); plt.close(fig)


def fig_error_budget_map():
    # 两行布局：印刷时按版心宽缩放，框内字号保持 >= 约 8pt
    fig, ax = plt.subplots(figsize=(9, 6.6))
    ax.set_xlim(0, 9); ax.set_ylim(0, 6.6); ax.axis("off")
    stages = [
        ("光源/投影", "第六、八章", "伽马、同步\n光谱、散斑"),
        ("场景", "第六、八章", "高反、散射\n偏振、互反射"),
        ("镜头", "第二至五、十章", "PSF/MTF\n畸变、景深"),
        ("传感器", "第七章", "光子/读出噪声\n饱和、非线性"),
        ("相位/匹配", "第五、八章", r"$\sigma_\varphi$、展开" "\n伽马谐波"),
        ("三角测量", "第三、四、九章", r"$Z^2/(B f_x)$" "\n标定误差"),
        ("点云", "第十二章", "拼接、滤波\n运动"),
    ]
    w, h = 2.0, 2.05
    pos = [(0.2 + i * 2.2, 3.55) for i in range(4)] + [(1.3 + i * 2.2, 0.95) for i in range(3)]
    for i, ((n, ch, err), (x, y)) in enumerate(zip(stages, pos)):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc="#E3F2FD", ec="#1565C0"))
        ax.text(x + w / 2, y + h - 0.32, n, ha="center", va="center", fontsize=15, weight="bold")
        ax.text(x + w / 2, y + h - 0.72, ch, ha="center", va="center", fontsize=12, color="#333")
        ax.text(x + w / 2, y + 0.55, err, ha="center", va="center", fontsize=13, linespacing=1.3,
                bbox=dict(boxstyle="round,pad=0.25", fc="#FFF8E1", ec="#E65100"))
        if i in (0, 1, 2, 4, 5):
            ax.annotate("", xy=(x + 2.2, y + h / 2), xytext=(x + w, y + h / 2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.plot([6.6 + w / 2, 6.6 + w / 2, 2.3], [3.55, 3.28, 3.28], color="k", lw=1.5)
    ax.annotate("", xy=(2.3, 3.0), xytext=(2.3, 3.29), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(4.5, 6.3, "从光子到点云：每一环都贡献随机项与系统项", ha="center", fontsize=16)
    ax.text(4.5, 0.4, "随机项：可平均（多帧、更高 SNR）", ha="center", fontsize=13, color="#333")
    ax.text(4.5, 0.0, "系统项：不可平均，需建模、标定或改设计", ha="center", fontsize=13, color="#333")
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=10, color="#888")
    fig.savefig(OUT / "fig-error-budget-map.pdf", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_mtf_curve(); fig_sensor_compare(); fig_error_budget_map(); print("done")
