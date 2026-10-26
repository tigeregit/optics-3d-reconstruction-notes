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
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=7, color="#888")
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
    for name, r0, r1, z0, z1, c in items:
        ax.add_patch(plt.Rectangle((z0, r0), z1 - z0, r1 - r0, fc=c, alpha=0.25, ec=c, lw=1.5))
        ax.text(np.sqrt(z0 * z1), np.sqrt(r0 * r1), name, ha="center", va="center", fontsize=11, color=c)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(5e-4, 3e4); ax.set_ylim(5e-4, 1e2)
    ax.set_xlabel("深度量程 / 工作范围（mm）"); ax.set_ylabel("深度分辨率（mm）")
    ax.set_title("深度传感方式：分辨率 vs 量程（数量级示意）", fontsize=11)
    ax.grid(alpha=0.3, which="both")
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=7, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-sensor-compare.pdf", bbox_inches="tight"); plt.close(fig)


def fig_error_budget_map():
    fig, ax = plt.subplots(figsize=(12, 5.0))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    stages = [
        ("光源/投影", "第5、7章", "伽马、同步\n光谱、散斑"),
        ("场景", "第5、7章", "高反、散射\n偏振、互反射"),
        ("镜头", "第2、3、4、9章", "PSF/MTF\n畸变、景深"),
        ("传感器", "第6章", "光子/读出噪声\n饱和、非线性"),
        ("相位/匹配", "第4、7章", "σ_φ、展开\n伽马谐波"),
        ("三角测量", "第3、8章", "Z²/(B f_x)\n标定误差"),
        ("点云", "", "拼接、滤波\n运动"),
    ]
    w = 1.7
    for i, (n, ch, err) in enumerate(stages):
        x = 0.3 + i * 1.95
        ax.add_patch(FancyBboxPatch((x, 3.2), w, 1.2, boxstyle="round,pad=0.05", fc="#E3F2FD", ec="#1565C0"))
        ax.text(x + w / 2, 3.95, n, ha="center", fontsize=10, weight="bold")
        ax.text(x + w / 2, 3.45, ch, ha="center", fontsize=8, color="#555")
        ax.text(x + w / 2, 2.4, err, ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round", fc="#FFF8E1", ec="#E65100"))
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + 1.95, 3.8), xytext=(x + w, 3.8), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax.text(7, 5.2, "从光子到点云：每一环都向误差预算贡献随机项与系统项", ha="center", fontsize=12)
    ax.text(7, 1.0, "随机项：可平均（多帧、更高 SNR）    系统项：不可平均，需建模、标定或改设计",
            ha="center", fontsize=9, color="#333")
    fig.text(0.5, 0.01, NOTE, ha="center", fontsize=7, color="#888")
    fig.savefig(OUT / "fig-error-budget-map.pdf", bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_mtf_curve(); fig_sensor_compare(); fig_error_budget_map(); print("done")
