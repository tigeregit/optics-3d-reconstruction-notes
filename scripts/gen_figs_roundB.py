#!/usr/bin/env python3
"""Round B figures: interference, diffraction/PSF, polarization, radiometry."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Arc, Wedge, Rectangle
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42


def box(ax, xy, w, h, text, fc="#E8F1FA", ec="#2C5F8A", fs=9):
    x, y = xy
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                       facecolor=fc, edgecolor=ec, linewidth=1.3)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color="#1a1a1a")


def fig_interference_twobeam():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))

    # Left: Young / two-beam geometry
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 6.5)
    ax.axis("off")
    ax.set_title("双光束干涉（概念）", fontsize=12, pad=6)
    # source
    ax.plot(1.0, 3.2, "o", color="#1565C0", ms=10)
    ax.text(1.0, 3.85, "准单色源", fontsize=9, ha="center", color="#1565C0")
    # two slits
    ax.plot([3.5, 3.5], [1.5, 5.0], color="#333", lw=1.5)
    ax.plot(3.5, 4.2, "o", color="#C62828", ms=7)
    ax.plot(3.5, 2.2, "o", color="#C62828", ms=7)
    ax.text(3.5, 5.35, "双缝 / 双路", fontsize=9, ha="center", color="#C62828")
    ax.text(2.55, 4.2, "$S_1$", fontsize=9, color="#C62828", ha="right")
    ax.text(2.55, 2.2, "$S_2$", fontsize=9, color="#C62828", ha="right")
    # screen
    ax.plot([8.2, 8.2], [0.8, 5.6], color="#2E7D32", lw=2)
    ax.text(8.2, 6.05, "观察屏 / 传感器", fontsize=9, ha="center", color="#2E7D32")
    # rays
    for y_s, y_e in [(4.2, 5.0), (4.2, 3.2), (4.2, 1.5), (2.2, 5.0), (2.2, 3.2), (2.2, 1.5)]:
        ax.plot([3.5, 8.2], [y_s, y_e], color="#888", lw=0.8, alpha=0.7)
    ax.annotate("", xy=(8.2, 3.2), xytext=(1.0, 3.2),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.2, connectionstyle="arc3,rad=0"))
    # fringe sketch on screen
    ys = np.linspace(1.0, 5.4, 40)
    for i, y in enumerate(ys):
        inten = 0.3 + 0.7 * (0.5 * (1 + np.cos(2 * np.pi * (y - 3.2) / 0.9)))
        ax.plot([8.2, 8.2 + 0.55 * inten], [y, y], color="#2E7D32", lw=2.2, solid_capstyle="butt")
    ax.text(9.35, 3.2, "条纹\n$I(\\varphi)$", fontsize=8, color="#2E7D32", va="center")
    ax.text(5.0, 0.15, r"光程差 $\mathrm{OPD}$（或 $\delta$）$\leftrightarrow$ 相位 $\varphi=2\pi\,\delta/\lambda$",
            ha="center", fontsize=8.5,
            bbox=dict(boxstyle="round", facecolor="#E8F5E9", edgecolor="#2E7D32", lw=0.7))

    # Right: I vs phase
    ax = axes[1]
    phi = np.linspace(0, 4 * np.pi, 400)
    V = 0.75
    I0 = 1.0
    I = I0 * (1 + V * np.cos(phi))
    ax.plot(phi, I, color="#1565C0", lw=2)
    ax.fill_between(phi, I0 * (1 - V), I0 * (1 + V), color="#BBDEFB", alpha=0.35)
    ax.axhline(I0, color="#999", ls="--", lw=0.9)
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(0, 2.2)
    ax.set_xlabel(r"相位 $\varphi$（弧度）", fontsize=10)
    ax.set_ylabel(r"强度 $I$（相对）", fontsize=10)
    ax.set_title(r"$I = I_0(1+V\cos\varphi)$", fontsize=11)
    ax.text(2 * np.pi, 1.95, r"可见度 $V=\dfrac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}$",
            ha="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="#FFF8E1", edgecolor="#F9A825", lw=0.7))
    ax.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])
    ax.grid(True, alpha=0.3)
    ax.text(0.5, -0.18, "概念草图，非精确工程图", ha="center", fontsize=7, color="#888",
            transform=ax.transAxes)

    fig.tight_layout()
    fig.savefig(OUT / "fig-interference-twobeam.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig-interference-twobeam.pdf")


def fig_diffraction_psf():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))

    # Left: Airy sketch
    ax = axes[0]
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("衍射极限与艾里斑（概念）", fontsize=12, pad=6)
    # radial Airy-like intensity as rings
    for r, a in [(0.35, 0.95), (0.9, 0.35), (1.45, 0.18), (2.0, 0.1), (2.55, 0.06)]:
        circ = Circle((0, 0), r, fill=True, facecolor="#1565C0", alpha=a * 0.45,
                      edgecolor="#0D47A1", lw=0.8)
        ax.add_patch(circ)
    ax.add_patch(Circle((0, 0), 0.9, fill=False, edgecolor="#C62828", lw=1.8, ls="--"))
    ax.annotate("", xy=(0.9, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color="#C62828", lw=1.5))
    ax.text(0.45, 0.25, r"$r_{\mathrm{Airy}}$", fontsize=10, color="#C62828", ha="center")
    ax.text(0, -2.85, r"圆孔远场：中心亮斑 + 环；半角 $\sim 1.22\,\lambda/D$"
            "\n数值孔径越大，斑越小，但景深越窄",
            ha="center", fontsize=8, color="#333",
            bbox=dict(boxstyle="round", facecolor="#E3F2FD", edgecolor="#1565C0", lw=0.7))

    # Right: PSF / MTF curves
    ax = axes[1]
    x = np.linspace(-4, 4, 500)
    # approximate PSF envelope
    psf = np.exp(-0.5 * (x / 0.55) ** 2) + 0.08 * np.exp(-0.5 * ((x - 2.1) / 0.35) ** 2)
    psf = psf / psf.max()
    ax.plot(x, psf, color="#6A1B9A", lw=2, label=r"$\mathrm{PSF}$ 截面 $h$")
    ax.fill_between(x, 0, psf, color="#E1BEE7", alpha=0.4)
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel("像面径向位置（任意单位）", fontsize=9)
    ax.set_ylabel("相对强度", fontsize=9)
    ax.set_title(r"点扩散 $\mathrm{PSF}$；高频被 $\mathrm{MTF}$ 衰减", fontsize=11)
    # inset-like MTF curve
    freq = np.linspace(0, 1, 200)
    mtf = np.clip(1 - 1.15 * freq, 0, 1) ** 1.2
    ax2 = ax.inset_axes([0.52, 0.52, 0.44, 0.42])
    ax2.plot(freq, mtf, color="#E65100", lw=1.8)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel("空间频率", fontsize=7)
    ax2.set_ylabel("MTF", fontsize=7)
    ax2.tick_params(labelsize=6)
    ax2.set_title("MTF 示意", fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8, frameon=True)
    ax.text(0, -0.18, "概念草图：离焦使 PSF 更宽、MTF 更早截止 → 条纹对比度下降",
            ha="center", fontsize=8, color="#444", transform=ax.get_xaxis_transform())

    fig.tight_layout()
    fig.savefig(OUT / "fig-diffraction-psf.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig-diffraction-psf.pdf")


def fig_polarization_projector():
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("投影–场景–相机偏振路径（概念）", fontsize=12, pad=8)

    box(ax, (0.3, 1.8), 2.2, 1.4, "投影仪\n（可含偏振\n光学）", fc="#FFF3E0", ec="#EF6C00")
    box(ax, (3.2, 2.0), 1.6, 1.0, "起偏/\n分光", fc="#E8EAF6", ec="#3949AB", fs=8)
    box(ax, (5.6, 1.6), 2.4, 1.8, "场景表面\n高反 / 漫反\n次表面散射", fc="#E8F5E9", ec="#2E7D32")
    box(ax, (8.8, 2.0), 1.8, 1.0, "检偏片\n（可选）", fc="#FCE4EC", ec="#C2185B", fs=8)
    box(ax, (11.2, 1.8), 2.3, 1.4, "相机\n传感器", fc="#E3F2FD", ec="#1565C0")

    for x1, x2 in [(2.5, 3.2), (4.8, 5.6), (8.0, 8.8), (10.6, 11.2)]:
        ax.annotate("", xy=(x2, 2.5), xytext=(x1, 2.5),
                    arrowprops=dict(arrowstyle="->", color="#333", lw=1.6))

    # polarization marks
    ax.text(4.0, 3.35, "线偏光 / 部分偏光", fontsize=8, ha="center", color="#3949AB")
    ax.text(6.8, 3.75, "镜面反射常保偏\n漫射趋向退偏", fontsize=8, ha="center", color="#2E7D32")
    ax.text(9.7, 3.35, "抑镜面高光", fontsize=8, ha="center", color="#C2185B")

    ax.text(7.0, 0.55,
            "部分相干光源 → 干涉可见度受限于相干长度；粗糙面 + 相干照明 → 散斑\n"
            "牙面/金属高反：偏振片可抬有效条纹对比度，但会损失通量、影响 SNR",
            ha="center", fontsize=8.5, color="#333",
            bbox=dict(boxstyle="round", facecolor="#FAFAFA", edgecolor="#999", lw=0.7))
    ax.text(7.0, 0.08, "概念草图，非精确工程图", ha="center", fontsize=7, color="#888")

    fig.tight_layout()
    fig.savefig(OUT / "fig-polarization-projector.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig-polarization-projector.pdf")


def fig_radiometry_camera():
    fig, ax = plt.subplots(figsize=(10.6, 4.2))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title("辐射度量 → 相机响应（概念）", fontsize=12, pad=8)

    boxes = [
        (0.2, 2.2, 2.0, 1.3, r"通量 $\Phi$" + "\n(W)", "#FFF8E1", "#F9A825"),
        (2.8, 2.2, 2.2, 1.3, r"辐亮度 $L$" + "\n(W/m²/sr)", "#E8F5E9", "#2E7D32"),
        (5.6, 2.2, 2.2, 1.3, r"像面辐照度 $E$" + "\n(W/m²)", "#E3F2FD", "#1565C0"),
        (8.4, 2.2, 2.0, 1.3, "曝光·增益\n·响应曲线", "#F3E5F5", "#6A1B9A"),
        (10.8, 2.2, 1.5, 1.3, "灰度\nDN", "#FFEBEE", "#C62828"),
    ]
    for x, y, w, h, text, fc, ec in boxes:
        box(ax, (x, y), w, h, text, fc=fc, ec=ec, fs=8)
    for x1, x2 in [(2.2, 2.8), (5.0, 5.6), (7.8, 8.4), (10.4, 10.8)]:
        ax.annotate("", xy=(x2, 2.85), xytext=(x1, 2.85),
                    arrowprops=dict(arrowstyle="->", color="#333", lw=1.5))

    ax.text(6.2, 4.55, r"灰度 $\neq$ 辐照度 $E$：中间夹着光圈、快门、ISO/增益、gamma、暗电流与量化",
            ha="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="#FFFDE7", edgecolor="#F9A825", lw=0.8))

    # noise note
    ax.text(6.2, 0.7,
            r"光子噪声 / 读出噪声 / 量化 → 信噪比 $\mathrm{SNR}$"
            "\n自动曝光会改 E→灰度映射，破坏多帧光度一致性（相位/立体匹配需警惕）",
            ha="center", fontsize=8.5, color="#333",
            bbox=dict(boxstyle="round", facecolor="#FAFAFA", edgecolor="#999", lw=0.7))
    ax.text(6.2, 0.12, "概念草图，非精确工程图", ha="center", fontsize=7, color="#888")

    fig.tight_layout()
    fig.savefig(OUT / "fig-radiometry-camera.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig-radiometry-camera.pdf")


if __name__ == "__main__":
    fig_interference_twobeam()
    fig_diffraction_psf()
    fig_polarization_projector()
    fig_radiometry_camera()
    print("done")
