#!/usr/bin/env python3
"""Round C figures: fringe/phase, DMD concept, stereo triangulation."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon

OUT = Path(__file__).resolve().parents[1] / "figures"
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42
NOTE = "概念草图，非精确工程图"


def fig_fringe_phase():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
    x = np.linspace(0, 1, 600)
    ax = axes[0]
    for k, c in zip(range(4), ["#1565C0", "#2E7D32", "#E65100", "#6A1B9A"]):
        ax.plot(x, 0.5 + 0.4 * np.cos(2 * np.pi * 4 * x + k * np.pi / 2), color=c, lw=1.3,
                label=f"第 {k+1} 帧（移相 {k}·π/2）")
    ax.set_title("四步相移条纹（截面）", fontsize=11)
    ax.set_xlabel("像面位置 u（归一化）")
    ax.set_ylabel("灰度（相对）")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_ylim(0, 1.15)

    ax = axes[1]
    phi = 2 * np.pi * 4 * x + 1.2 * np.sin(2 * np.pi * x)
    wrapped = np.angle(np.exp(1j * phi))
    ax.plot(x, wrapped, color="#C62828", lw=1.3)
    ax.set_title(r"包裹相位 $\varphi_w\in(-\pi,\pi]$", fontsize=11)
    ax.set_xlabel("u（归一化）")
    ax.set_yticks([-np.pi, 0, np.pi])
    ax.set_yticklabels([r"$-\pi$", "0", r"$\pi$"])

    ax = axes[2]
    ax.plot(x, phi, color="#2E7D32", lw=1.6, label=r"展开相位 $\varphi$")
    ax.plot(x, wrapped, color="#C62828", lw=0.8, alpha=0.5, label="包裹相位")
    ax.set_title(r"展开：$\varphi=\varphi_w+2\pi k$", fontsize=11)
    ax.set_xlabel("u（归一化）")
    ax.legend(fontsize=8)
    for a in axes:
        a.grid(alpha=0.3)
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=7, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-fringe-phase.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_dmd_concept():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title("DMD 微镜：±倾角二值开关", fontsize=11)
    for i in range(6):
        x0 = 1 + i * 1.3
        on = i % 2 == 0
        ang = 12 if on else -12
        t = np.deg2rad(ang)
        pts = [(x0 - 0.5 * np.cos(t), 2.5 - 0.5 * np.sin(t)), (x0 + 0.5 * np.cos(t), 2.5 + 0.5 * np.sin(t))]
        ax.plot(*zip(*pts), color="#1565C0" if on else "#999", lw=5)
        ax.text(x0, 1.6, "开" if on else "关", ha="center", fontsize=8)
    ax.annotate("", xy=(5, 2.9), xytext=(5, 5.3), arrowprops=dict(arrowstyle="->", lw=1.5, color="#E65100"))
    ax.text(5.2, 5.0, "照明", fontsize=9, color="#E65100")
    ax.text(5, 0.7, "“开”镜反射进投影镜头；“关”镜偏到吸收器\n灰度靠时间脉宽调制（PWM），相机需帧同步",
            ha="center", fontsize=8, bbox=dict(boxstyle="round", fc="#FAFAFA", ec="#999"))

    ax = axes[1]
    x = np.linspace(0, 2, 800)
    binary = (np.cos(2 * np.pi * 2 * x) > 0).astype(float)
    k = np.exp(-0.5 * (np.linspace(-0.15, 0.15, 121) / 0.05) ** 2); k /= k.sum()
    blurred = np.convolve(binary, k, mode="same")
    ax.plot(x, binary, color="#999", lw=1.0, label="二值条纹（投影面）")
    ax.plot(x, blurred, color="#2E7D32", lw=2, label="离焦后 ≈ 正弦")
    ax.set_ylim(-0.1, 1.3)
    ax.set_title("二值离焦成正弦", fontsize=11)
    ax.set_xlabel("投影仪坐标（周期）")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.3)
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=7, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-dmd-concept.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_stereo_triangulation():
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4))
    ax = axes[0]
    ax.set_xlim(-1, 11); ax.set_ylim(-1, 8); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("三角测量与交会角", fontsize=11)
    C1, C2, P = np.array([2, 0.5]), np.array([8, 0.5]), np.array([5, 6.5])
    for C, lab in [(C1, "相机"), (C2, "相机/投影仪")]:
        ax.add_patch(Rectangle((C[0] - 0.5, C[1] - 0.4), 1, 0.6, fc="#E3F2FD", ec="#1565C0"))
        ax.text(C[0], C[1] - 0.9, lab, ha="center", fontsize=9)
        ax.plot(*zip(C, P), color="#555", lw=1.2)
        d = (P - C) / np.linalg.norm(P - C); nrm = np.array([-d[1], d[0]])
        poly = [C, P + 0.45 * nrm, P - 0.45 * nrm]
        ax.add_patch(Polygon(poly, fc="#FFE0B2", ec="none", alpha=0.35))
    ax.plot(*P, "o", color="#C62828")
    ax.text(P[0], P[1] + 0.4, "物点 (X,Y,Z)", ha="center", fontsize=9, color="#C62828")
    ax.annotate("", xy=C2 + [0, -0.2], xytext=C1 + [0, -0.2], arrowprops=dict(arrowstyle="<->"))
    ax.text(5, 0.0, "基线 B", ha="center", fontsize=9)
    ax.text(5, 4.9, "交会角 θ", ha="center", fontsize=9, color="#6A1B9A")
    ax.text(5, 7.5, "橙色：像面误差 δu 张开的射线锥 → 交汇区即深度不确定", ha="center", fontsize=8)

    ax = axes[1]
    Z = np.linspace(10, 40, 200)
    for B, c in [(5, "#C62828"), (10, "#1565C0"), (20, "#2E7D32")]:
        ax.plot(Z, Z ** 2 / (B * 1500) * 0.2 * 1000, color=c, lw=2, label=f"B = {B} mm")
    ax.set_xlabel("工作距 Z（mm）")
    ax.set_ylabel("δZ（μm），f_x=1500 px，δu=0.2 px")
    ax.set_title(r"$\delta Z\approx Z^2\,\delta u/(B f_x)$", fontsize=11)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.text(0.5, 0.005, NOTE, ha="center", fontsize=7, color="#888")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-stereo-triangulation.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_fringe_phase(); fig_dmd_concept(); fig_stereo_triangulation(); print("done")
