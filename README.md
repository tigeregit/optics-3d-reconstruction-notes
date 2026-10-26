# 《光学讲义：三维重建与结构光》

副标题：面向相机 / 投影 / 干涉 / 条纹实践者

服务非物理系、从事 C++/CUDA 医学三维重建的读者：按主流光学教程习惯补齐「够用」光学，每章落到相机 / 投影 / 干涉 / 条纹里为什么要懂。

## 状态

大纲已确认（见 `docs/OUTLINE.md`）。Round~A（ch00–ch02）、Round~B（ch03–ch05）、Round~C（ch06–ch07）已写正文；ch08–ch10 仍为 stub。

## 结构

- `docs/OUTLINE.md` — 章目录与写章计划
- `STYLE.md` — 书定位、Notation Lock、写作约定
- `chapters/` — ch00–ch10 章 TeX
- `figures/` — 锁定文件名配图（见 `figures/README.md`）
- `refs/book.bib` — 文献
- `reviews/` — 讲义·审核产出

## 编译

```bash
./scripts/build.sh
# 或
/workspace/bin/tectonic -X compile book.tex
```

产出：`book.pdf`（需 Noto CJK SC）。

## 配图脚本

```bash
/workspace/engineering-cybernetics-harness/.venv/bin/python scripts/gen_figs_roundA.py
/workspace/engineering-cybernetics-harness/.venv/bin/python scripts/gen_figs_roundB.py
/workspace/engineering-cybernetics-harness/.venv/bin/python scripts/gen_figs_roundC.py
```
