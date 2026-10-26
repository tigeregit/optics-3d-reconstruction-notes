#!/usr/bin/env python3
"""Generate Round A conceptual PDFs (Chinese labels): pinhole/thinlens, DoF/CoC, distortion."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42


def fig_pinhole_thinlens():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))

    # Left: pinhole
    ax = axes[0]
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-3.2, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("针孔成像（概念）", fontsize=12, pad=6)

    # object arrow at x=1
    ax.annotate("", xy=(1.0, 1.6), xytext=(1.0, -0.2),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=2))
    ax.text(0.55, 0.7, "物", fontsize=9, color="#1565C0", ha="center")
    ax.plot([1.0], [0.0], "o", color="#333", ms=3)

    # pinhole plane
    ax.plot([5.0, 5.0], [-2.6, 2.6], color="#333", lw=1.5)
    ax.plot(5.0, 0.0, "o", color="#C62828", ms=6, zorder=5)
    ax.text(5.0, 2.85, "针孔", fontsize=9, ha="center", color="#C62828")

    # image plane
    ax.plot([8.5, 8.5], [-2.6, 2.6], color="#2E7D32", lw=1.8)
    ax.text(8.5, 2.85, "像面 $(u,v)$", fontsize=9, ha="center", color="#2E7D32")

    # rays through pinhole (inverted image)
    ax.plot([1.0, 5.0, 8.5], [1.6, 0.0, -1.35], color="#555", lw=1.2, ls="-")
    ax.plot([1.0, 5.0, 8.5], [-0.2, 0.0, 0.15], color="#888", lw=0.9, ls="--")
    ax.annotate("", xy=(8.5, -1.35), xytext=(8.5, 0.15),
                arrowprops=dict(arrowstyle="->", color="#2E7D32", lw=1.8))
    ax.text(9.15, -0.55, "倒立像", fontsize=8, color="#2E7D32")

    ax.text(5.0, -3.05, "几何：直线过光心；无透镜焦距概念\n医学扫描中作投影模型起点",
            ha="center", fontsize=8, color="#444",
            bbox=dict(boxstyle="round", facecolor="#FAFAFA", edgecolor="#BBB", lw=0.6))

    # Right: thin lens
    ax = axes[1]
    ax.set_xlim(-0.8, 11.2)
    ax.set_ylim(-3.4, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("薄透镜成像（概念）", fontsize=12, pad=6)

    # object
    ax.annotate("", xy=(1.2, 1.8), xytext=(1.2, 0.0),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=2))
    ax.text(0.55, 0.9, "物距 $s$", fontsize=8, color="#1565C0", rotation=90, va="center")
    ax.annotate("", xy=(1.2, -0.35), xytext=(5.5, -0.35),
                arrowprops=dict(arrowstyle="<->", color="#1565C0", lw=1.0))
    ax.text(3.3, -0.75, "$s$", fontsize=9, color="#1565C0", ha="center")

    # lens
    lens_x = 5.5
    theta = np.linspace(-np.pi / 2.2, np.pi / 2.2, 40)
    r = 2.4
    ax.plot(lens_x + 0.35 * np.cos(theta), r * 0.85 * np.sin(theta), color="#6A1B9A", lw=2)
    ax.plot(lens_x - 0.35 * np.cos(theta), r * 0.85 * np.sin(theta), color="#6A1B9A", lw=2)
    ax.plot([lens_x, lens_x], [-2.2, 2.2], color="#6A1B9A", lw=1.0, ls=":")
    ax.text(lens_x, 2.55, "薄透镜 $f$", fontsize=9, ha="center", color="#6A1B9A")

    # optical axis
    ax.plot([-0.3, 11.0], [0, 0], color="#999", lw=0.8, ls="-")

    # image
    ax.annotate("", xy=(9.3, -1.35), xytext=(9.3, 0.0),
                arrowprops=dict(arrowstyle="->", color="#2E7D32", lw=2))
    ax.annotate("", xy=(5.5, -0.35), xytext=(9.3, -0.35),
                arrowprops=dict(arrowstyle="<->", color="#2E7D32", lw=1.0))
    ax.text(7.4, -0.75, "$s'$", fontsize=9, color="#2E7D32", ha="center")
    ax.text(9.95, -0.7, "像距 $s'$", fontsize=8, color="#2E7D32")

    # chief rays sketch
    ax.plot([1.2, lens_x, 9.3], [1.8, 1.8, -1.35], color="#555", lw=1.0)
    ax.plot([1.2, lens_x, 9.3], [1.8, 0.0, -1.35], color="#888", lw=1.0, ls="--")

    ax.text(5.5, -2.95,
            r"薄透镜公式：$\frac{1}{s}+\frac{1}{s'}=\frac{1}{f}$（$f$=焦距，非频率）"
            "\n旁轴、单色、薄透镜假设",
            ha="center", fontsize=8, color="#444",
            bbox=dict(boxstyle="round", facecolor="#F3E5F5", edgecolor="#8E24AA", lw=0.6))

    fig.suptitle("概念草图，非精确工程图", fontsize=8, color="#888", y=0.02)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(OUT / "fig-pinhole-thinlens.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "fig-pinhole-thinlens.pdf")


def fig_dof_coc():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-3.0, 3.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("景深与弥散圆（Circle of Confusion）", fontsize=12, pad=8)

    # optical axis
    ax.plot([0, 12.2], [0, 0], color="#999", lw=0.9)

    # lens
    lx = 5.0
    theta = np.linspace(-np.pi / 2.3, np.pi / 2.3, 50)
    ax.plot(lx + 0.4 * np.cos(theta), 2.0 * np.sin(theta), color="#6A1B9A", lw=2.2)
    ax.plot(lx - 0.4 * np.cos(theta), 2.0 * np.sin(theta), color="#6A1B9A", lw=2.2)
    ax.text(lx, 2.35, "透镜 / 光瞳", fontsize=9, ha="center", color="#6A1B9A")

    # sensor plane
    sx = 9.5
    ax.plot([sx, sx], [-2.2, 2.2], color="#2E7D32", lw=2)
    ax.text(sx, 2.45, "像面", fontsize=9, ha="center", color="#2E7D32")

    # in-focus object -> sharp point on sensor
    ax.plot([1.5], [1.4], "o", color="#1565C0", ms=7)
    ax.text(1.5, 1.75, "对焦物面", fontsize=8, color="#1565C0", ha="center")
    ax.plot([1.5, lx, sx], [1.4, 0.9, 0.0], color="#1565C0", lw=1.1)
    ax.plot([1.5, lx, sx], [1.4, -0.9, 0.0], color="#1565C0", lw=1.1)
    ax.plot(sx, 0.0, "o", color="#1565C0", ms=5)
    ax.text(sx + 0.35, 0.15, "清晰点", fontsize=8, color="#1565C0")

    # defocused object -> CoC
    ax.plot([0.6], [-1.5], "o", color="#E65100", ms=7)
    ax.text(0.6, -1.95, "离焦物点", fontsize=8, color="#E65100", ha="center")
    ax.plot([0.6, lx, sx], [-1.5, 1.1, 1.1], color="#E65100", lw=1.0, ls="-")
    ax.plot([0.6, lx, sx], [-1.5, -1.1, -1.1], color="#E65100", lw=1.0, ls="-")
    # CoC disk on sensor
    coc = Circle((sx, 0.0), 1.1, fill=False, edgecolor="#E65100", lw=1.8, linestyle="--")
    # Actually CoC should be centered where the cone intersects sensor - use mid
    # Draw a disk at intersection: cone from lens to points at y=±1.1 on sensor through focus behind
    # Simpler: show CoC as vertical segment / circle at sensor for defocused ray bundle
    coc2 = Circle((sx, 0.0), 1.05, fill=True, facecolor="#FFE0B2", edgecolor="#E65100",
                  lw=1.5, alpha=0.55, zorder=2)
    # reposition: defocused rays hit at ±1.1, so CoC center at 0 with radius ~1.1 is ok for sketch
    # But in-focus point is also at 0 - better offset CoC for the defocused case
    # Redraw: put defocused image slightly below
    ax.patches.clear() if False else None
    # Draw CoC as ellipse/circle centered at (sx, -0.0) with note — keep simple vertical bar
    ax.plot([sx, sx], [-1.1, 1.1], color="#E65100", lw=4, solid_capstyle="round",
            alpha=0.45, zorder=2)
    ax.add_patch(Circle((sx, 0.0), 1.05, fill=False, edgecolor="#E65100", lw=1.6, ls="--", zorder=3))
    ax.text(sx + 0.55, -1.55, "弥散圆\n直径 $c$", fontsize=8, color="#E65100")

    # depth of field bracket on object side
    ax.annotate("", xy=(0.3, 1.4), xytext=(2.8, 1.4),
                arrowprops=dict(arrowstyle="<->", color="#00695C", lw=1.4))
    ax.text(1.55, 2.55, "可接受清晰的物距范围 → 景深相关量 $Z_d$",
            fontsize=9, color="#00695C", ha="center",
            bbox=dict(boxstyle="round", facecolor="#E0F2F1", edgecolor="#00695C", lw=0.7))

    ax.text(6.0, -2.7,
            "容许弥散圆越大 → 表观景深越大；孔径越大、焦距越长 → 景深越窄（旁轴近似）\n"
            "符号：$Z_d$ 表景深相关量，勿与世界坐标 $Z$ 混用而不加下标",
            ha="center", fontsize=8, color="#333",
            bbox=dict(boxstyle="round", facecolor="#FFFDE7", edgecolor="#F9A825", lw=0.7))
    ax.text(6.0, -3.35, "概念草图，非精确工程图", ha="center", fontsize=7, color="#888")

    fig.tight_layout()
    fig.savefig(OUT / "fig-dof-coc.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "fig-dof-coc.pdf")


def fig_distortion():
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.8))

    def draw_grid(ax, warp_fn, title, color):
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=11, color=color, pad=6)
        n = 7
        xs = np.linspace(-1.0, 1.0, n)
        for x in xs:
            ys = np.linspace(-1.0, 1.0, 80)
            pts = np.array([warp_fn(x, y) for y in ys])
            ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.0, alpha=0.85)
        for y in xs:
            xs_line = np.linspace(-1.0, 1.0, 80)
            pts = np.array([warp_fn(x, y) for x in xs_line])
            ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.0, alpha=0.85)
        # unit circle reference
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(th), np.sin(th), color="#BBB", lw=0.8, ls=":")

    def identity(x, y):
        return x, y

    def barrel(x, y):
        r2 = x * x + y * y
        k1 = -0.22
        s = 1 + k1 * r2
        return s * x, s * y

    def pincushion(x, y):
        r2 = x * x + y * y
        k1 = 0.22
        s = 1 + k1 * r2
        return s * x, s * y

    draw_grid(axes[0], identity, "理想（无畸变）网格", "#37474F")
    draw_grid(axes[1], barrel, "桶形畸变（$k_1<0$ 示意）", "#C62828")
    draw_grid(axes[2], pincushion, "枕形畸变（$k_1>0$ 示意）", "#1565C0")

    fig.suptitle(
        "径向畸变使直线弯曲；标定需在投影模型中显式建模（概念草图，非精确工程图）",
        fontsize=9, color="#555", y=0.02,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(OUT / "fig-distortion.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "fig-distortion.pdf")


if __name__ == "__main__":
    fig_pinhole_thinlens()
    fig_dof_coc()
    fig_distortion()
    print("done")
