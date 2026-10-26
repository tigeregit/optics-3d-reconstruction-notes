# 《光学讲义：三维重建与结构光》

副标题：面向相机 / 投影 / 干涉 / 条纹实践者

服务非物理系、从事 C++/CUDA 医学三维重建的读者：按主流光学教程习惯补齐「够用」光学，每章落到相机 / 投影 / 干涉 / 条纹里为什么要懂。

## 状态

**大纲待用户确认**（见 `docs/OUTLINE.md`）。确认前仅有章 stub（标题 + 节骨架 + 习题占位），**不写**完整章正文。

## 结构

- `docs/OUTLINE.md` — 章目录与写章计划（冻结候选）
- `STYLE.md` — 书定位、Notation Lock、写作约定
- `chapters/` — ch00–ch10 章 TeX stub
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
