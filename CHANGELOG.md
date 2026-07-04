# 更新记录 · CHANGELOG

> 韩语音义体系地图的迭代记录。按「韩N」批次组织（每个批次 = 一次会话的一组改动）。

## 韩5 — 移植日语 UX 改进（2026-07-05）

从日语项目（日14~日20）选择性移植 6 项通用 UX 改进，保留韩语的初声辅音导航模型：

- **双击双向关联跳转**：双击词条 → 跳转到所属初声/词根 + 高亮 + 滚动；双击词根 → 选中首个词条 + 滚动。`dblClickEntry` 和 `dblClickRoot`。
- **搜索改进**：搜索时用 `highlightRoot` 高亮首命中词根；搜索结果左侧按初声分组展示命中词根；右侧直接展示搜索命中词条（不再只显示提示）；移除搜索时的 `scrollIntoView` 避免页面跳走。
- **`scrollToActiveItems`**：通用滚动工具，操作后自动跳转到选中词条/词根位置。
- **`clearAllFilters` + 清搜按钮**：清搜索 + 初声 + 词根 + 标签选中态；搜索栏旁加「清搜」按钮。
- **多端同步 verbose**：`pushToGist(verbose)` / `pullFromGist(verbose)` — 启动时提示同步结果、切回前台静默拉取（失败仍提示）、手动同步提供明确反馈。
- **`selectEntry` 轻量化**：点击词条只重绘 words-list + detail-panel，不触发全量 `render()`。
- state 新增 `highlightRoot` / `highlightLayer` / `rootCoreOverrides` 字段。

## 韩4 — 最近词汇列表 + 搜索跳转首个

- 最近添加词汇列表（按 createdAt 倒序，默认收起）。
- 搜索模式跳转到第一个匹配词条。

## 韩1–3 — 导航适配 + PWA + 多端同步 + 标签云

- 韩1-3：导航按钮区 wrap + max-height 500 容换行；谚文 pron 显示删除。
- 多端同步（GitHub Gist）+ PWA（manifest、service worker）。
- 标签云 UX 重设计：卡片网格 + inline 展开 + 紧凑排版。
- 标签重组升级：20 大类标准根 + 仅补漏智能重跑。
- 语言学字段全中文化 + 自动迁移 + POS 适用性硬过滤。
- AI 补全字段可配置 + LLM 双套配置。
- 扩展 11 个语法字段 + add-modal 折叠分区。
- 词性/阶称/敬语/派生/基本形 5 个语法字段。
- 添加 Google Gemini 作为 LLM provider。
