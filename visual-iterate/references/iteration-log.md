# Iteration Log — 简化记录模板

仅当用户需要迭代记录、复盘或多轮自动执行时才外显；普通单轮生成无需附长表格。

```markdown
# Visual Iteration: <作品名称>
Intent: <目标受众 + 要完成的事情>
Artifact: <类型/媒介/阅读尺寸>
Invariants: <不得改变的内容与视觉决定>
Evidence: <给定资料、可观察事实与待验证假设>

## V<n>
Source: <真实文件/当前可访问图片；无则注明>
Critique: <八个维度分别 Strong/Fair/Weak，必要时说明 N/A>
Top issues:
- [dimension] Observation: ... | Reason: ...
- [dimension] Observation: ... | Reason: ...
Change plan: <本轮优先修复的 1–3 个问题与冻结项>
Artifact: <真实交付位置>
Re-evaluation:
- Improved: <证据>
- Regressed: <证据，或未观察到明显回退>
- Unchanged: <证据>
- Unproven: <需用户测试/外部数据/无法目视判断的项>
Next action: <停止 / 继续 + 原因>
```

## 评分表（可选）

| Dimension | Before | After | Evidence (visual observation) | Status |
|---|---|---|---|---|
| Function | Fair | Strong | 目标动作从模糊描述改为明确 CTA | 设计判断，用户理解仍待测 |
| Hierarchy | Fair | Strong | CTA 从低对比、远离标题，变为紧随主标题的高对比按钮 | 可观察的视觉改进 |
| Audience | Fair | Fair | 未提供受众访谈，视觉变化不足以支持升级 | 保持评分 |

表格是**示例格式**，不能复制为未经评审的事实；实际分数由实际图片证据决定。

## 回归门槛

- 若本轮新增信息让字号不可读、图像关系被改错、遗漏核心事实、删掉已确认要求，则优先修复回退；不要因为某项变 Strong 就忽略硬约束失败。
- 多次新增小卡片/长解释导致拥挤时，优先删除、重新组织或拆分，而不是继续缩小字体。
- 同一生成者自评出现“一切都变好”时，检查反证，并保留不变和未验证项目。
