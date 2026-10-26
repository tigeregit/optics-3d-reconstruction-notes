# OWNERS

| 角色 | 职责 | 寿命 |
|------|------|------|
| Manager | 大纲、STYLE/OWNERS、合稿、编译、派工与清扫 | 长期 |
| 讲义·审核 | 只写 `reviews/**`；Notation Lock、教学法、blocking | 长期（跨书复用，至多 1） |
| 写手 / 配图（executor 或临时） | 章 stub→正文、图 PDF | 临时 / 后台任务 |

写手可写：`chapters/chXX.tex`（派工指定）、`figures/` 下锁定文件名、必要时补 `refs/book.bib` 真实条目。

写手勿改：已冻结 `docs/OUTLINE.md` 章结构、`STYLE.md` Notation Lock、他人章文件（除非合稿指令）。

首轮写章优先用 Manager 后台 executor，**不建**临时章 bot；复用长期「讲义·审核」。收工时若无临时 bot，删除清单为空。
