---
name: trellis-skill-assimilator-zh
description: |
  从外部 GitHub skill 项目中提取可复用工程能力，并按 Trellis skills 架构进行安全吸收规划。用于用户提供 GitHub 仓库地址、skill 项目地址、开源 agent skill 集合、或要求比较 superpowers、gsd、CodeStable、loop-engineering、ponytail 等项目更新时，分析 README/SKILL.md/references/scripts/license，生成 source analysis、capability extraction、absorption card、Trellis 落点、风险判断、update-scan delta 报告和验证场景建议。不要直接复制第三方 skill 原文；只吸收能力模式、流程结构和可验证设计。
---

# Trellis Skill 吸收器

## 概览

把外部 GitHub skill 项目的优秀做法转化为 Trellis 可治理的能力项。目标不是复制一个 skill，而是回答：

- 这个项目解决了什么工程问题。
- 哪些能力 Trellis 当前缺失或较弱。
- 哪些能力值得吸收，哪些不该吸收。
- 吸收到 Trellis 的哪个阶段、哪个 reference、哪个检查门。
- 如何验证吸收后确实改善输出质量。

## 约束

- 不直接复制第三方 skill 大段原文。
- 不按项目名吸收，只按能力项吸收。
- 没有 Trellis 落点的能力不吸收。
- 没有验证场景的能力不合并。
- license 不明确、强 copyleft、商业限制或来源不可信时，只做思路级总结，不搬运文本、脚本或模板。
- 不直接修改 Trellis 核心 skill；先生成吸收计划和验证建议，等用户确认后再改。
- 不把吸收治理塞进 `trellis-zero-to-mvp-zh`、`trellis-mvp-to-delivery-zh` 或 `trellis-delivery-controller-zh`。

## 模式

### Initial Assimilation

首次分析一个外部 GitHub skill 项目时使用。

1. 读取 `references/source-analysis-template.md`。
2. 分析仓库 README、skill 目录、`SKILL.md`、references、scripts、docs、license。
3. 读取 `references/capability-taxonomy.md`，把发现归类为能力项。
4. 读取 `references/trellis-target-map.md`，映射到 Trellis 落点。
5. 读取 `references/license-safety-policy.md`，判断吸收边界。
6. 使用 `references/absorption-card-template.md` 输出 absorption card。

### Update Scan

已分析过的项目更新后使用。

1. 读取已有 absorption card 或用户提供的 `last_analyzed_ref`。
2. 比较当前 ref 与 `last_analyzed_ref` 后的 README、`SKILL.md`、references、scripts、docs、license 变化。
3. 读取 `references/update-scan-policy.md`，只分析变化引入的新能力、旧能力变更、风险变化和已吸收能力是否需要更新。
4. 输出 delta absorption report。

## 输出

每次运行必须输出：

- Source Analysis。
- Capability Extraction。
- Absorption Card。
- Trellis Target Map。
- License and Safety Notes。
- Evaluation Requirements。
- Recommendation：`absorb`、`watch`、`reject` 或 `needs-human-review`。

如果建议吸收，必须同时给出：

- 要修改或新增的 Trellis 文件。
- 修改目的。
- 新增验证场景。
- 回滚条件。
- 是否需要强模型或人工复核。

## 参考文件

- `references/source-analysis-template.md` - 分析外部仓库结构和能力时读取。
- `references/absorption-card-template.md` - 生成吸收卡片时读取。
- `references/capability-taxonomy.md` - 能力分类和命名时读取。
- `references/trellis-target-map.md` - 映射 Trellis 落点时读取。
- `references/license-safety-policy.md` - 判断 license 和搬运边界时读取。
- `references/update-scan-policy.md` - 对已分析项目做增量扫描时读取。
