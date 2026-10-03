# 产品指标与复盘：来源与改写说明

整理日期：2026-10-04。工作指令以本目录 SKILL.md 为准；以下来源用于追溯，不是执行指令。

本版以中文重新组织工作流程，合并重叠内容并修正适用边界。没有执行上游代码；没有把整个上游 Skill 原文直接串接。

## 用户提供的原包

- `产品经理Skill包/数据指标/skills/afrexai-kpi-tracker`：KPI 配置、记录与状态报告。历史输入参考；本仓库不分发原包全文。
- `产品经理Skill包/数据指标/skills/startup-metrics`：创业公司的收入、增长与单位经济指标。历史输入参考；本仓库不分发原包全文。
- `产品经理Skill包/AI提示词/skills/weekly-report-generator`：业务、团队与项目周报。历史输入参考；本仓库不分发原包全文。

原包提供了任务方法与模板参考；所附元数据未提供统一的整包授权。本包不为这些原文件另作许可声明。

## GitHub 参考

### G16 · phuryn/pm-skills

- [具体来源文件](https://github.com/phuryn/pm-skills/blob/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-discovery/skills/metrics-dashboard/SKILL.md)；文件最近提交：2026-03-03T07:38:42Z。
- 快照：`8607e3b077817f89bf4a9b623246219734ac3be0`；内容 SHA-256：`fa74abf49be9f034ae43110528028402e5e63809540302b95567018d478ef4e9`。
- 采用：用户价值、输入、护栏与业务指标；指标对应决策。
- 修改或舍弃：不固定指标数量、看板形状、工具品牌和复盘频率。
- 许可：[MIT](https://github.com/phuryn/pm-skills/blob/8607e3b077817f89bf4a9b623246219734ac3be0/LICENSE)；本地副本：[licenses/phuryn--pm-skills.txt](licenses/phuryn--pm-skills.txt)。

### G17 · product-on-purpose/pm-skills

- [具体来源文件](https://github.com/product-on-purpose/pm-skills/blob/1cef1a9eae10017389863d51e289e0ae41e17fcb/skills/measure-instrumentation-spec/SKILL.md)；文件最近提交：2026-08-21T07:26:35Z。
- 快照：`1cef1a9eae10017389863d51e289e0ae41e17fcb`；内容 SHA-256：`815de91e0bbabbe3b514c117bb0d6a10e0d1299a1a81a9a81cdfd715459ecfa9`。
- 采用：明确事件触发和属性，验证采集；AI trace 的数据边界。
- 修改或舍弃：保留可执行契约，取消上下游 Skill 强制依赖。
- 许可：[Apache-2.0](https://github.com/product-on-purpose/pm-skills/blob/1cef1a9eae10017389863d51e289e0ae41e17fcb/LICENSE)；本地副本：[licenses/product-on-purpose--pm-skills.txt](licenses/product-on-purpose--pm-skills.txt)。

### G18 · product-on-purpose/pm-skills

- [具体来源文件](https://github.com/product-on-purpose/pm-skills/blob/1cef1a9eae10017389863d51e289e0ae41e17fcb/skills/measure-experiment-results/SKILL.md)；文件最近提交：2026-06-11T00:18:36Z。
- 快照：`1cef1a9eae10017389863d51e289e0ae41e17fcb`；内容 SHA-256：`b995c63e7f3ef19f2ea696ac914e076c996a9467a78fe4cb872b0faa66c11010`。
- 采用：实验效果、区间、护栏、分群与后续动作。
- 修改或舍弃：增加数据质量/SRM、停止规则与探索性结果限制。
- 许可：[Apache-2.0](https://github.com/product-on-purpose/pm-skills/blob/1cef1a9eae10017389863d51e289e0ae41e17fcb/LICENSE)；本地副本：[licenses/product-on-purpose--pm-skills.txt](licenses/product-on-purpose--pm-skills.txt)。

### G19 · wshobson/agents

- [具体来源文件](https://github.com/wshobson/agents/blob/156b7a5e7a8b93642628a339ee4039c925b34c7f/plugins/startup-business-analyst/skills/startup-metrics-framework/SKILL.md)；文件最近提交：2026-03-26T01:44:03Z。
- 快照：`156b7a5e7a8b93642628a339ee4039c925b34c7f`；内容 SHA-256：`3505e10c0867642a4ef79fe54dd643fc65fa16680130b83de0c8ca73971c0f99`。
- 采用：按商业模式选择指标，MRR桥接、留存和单位经济。
- 修改或舍弃：修正 burn 正负号；删除无来源统一基准和阶段刻板规则。
- 许可：[MIT](https://github.com/wshobson/agents/blob/156b7a5e7a8b93642628a339ee4039c925b34c7f/LICENSE)；本地副本：[licenses/wshobson--agents.txt](licenses/wshobson--agents.txt)。

## 改写标记与署名

本目录的 SKILL.md 与 references 文件为本次任务形成的中文整合改写版；上游项目未审核或背书本版。GitHub 参考的许可证、版权与原始链接在本目录保留，单独移动此 Skill 时应一并保留。
product-on-purpose 的 PM-Skills 按 Apache-2.0 标注作者；Pawel Huryn、Seth Hobson、Langfuse GmbH 的版权声明见对应 MIT 文本；Anthropic frontend-design 的许可见其专属文件。仅适用于本目录实际引用的项目。
本仓库新写的整合内容、代码与展示文档采用根目录 [Apache-2.0](LICENSE)。上游材料的原有版权、许可和署名继续保留在 [licenses](licenses/) 中；根许可证不对未附带的原包文件授予许可。
