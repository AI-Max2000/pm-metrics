# 公式、边界与离线计算器

## 常用口径

| 指标 | 算法与适用条件 |
|---|---|
| 比例 | 分子 / 分母；分母为零时未定义。只有计数子集才要求分子不超过分母，NRR 等可超过 100% |
| 环比/同比增长 | (本期 − 基期) / 基期；基期为零或负数时不输出常规增长百分比，单列绝对变化和业务解释 |
| 百分点变化 | 两个百分率直接相减；相对变化另除以原百分率 |
| MRR | 活跃经常性合同按月归一，约定折扣/退款/税口径；一次性收入不计入 |
| MRR 桥接 | 期末 = 期初 + 新增 + 扩张 − 缩减 − 流失；各项同周期、互斥、不重复计入 |
| NRR | 同一期初客户群的 (期初收入 + 扩张 − 缩减 − 流失) / 期初收入；不含新客户，期初为零则未定义 |
| CAC | 约定范围的获客成本 / 对应新增付费客户；注明渠道、滞后和归因，不能混用销售线索数 |
| 简化 LTV | 同周期 ARPU × 毛利率 / 同周期客户流失率；仅为稳定模型近似，短历史/变化大/零流失时不外推无穷 LTV |
| 净现金消耗 | 月经营现金流出 − 月经营现金流入；不混用权责收入和现金支出 |
| 简化跑道 | 可用现金 / 正的月净现金消耗；依赖未来消耗稳定，债务到期/融资等另建现金预测 |

净消耗为零或负时，当前没有正的净消耗，不能给出负数跑道，也不能承诺“永远不会缺钱”。融资款与一次性现金变动不应混入稳定经营消耗来掩盖风险。

公式校核：[Stripe burn rate 说明](https://stripe.com/ie/resources/more/what-is-burn-rate-what-startups-need-to-know-about-this-key-metric)，查阅于 2026-10-04。财务计算仍需与用户定义、账期和现金口径一致；这里不提供统一融资或经营决策阈值。

## 调用方式

在本 Skill 文件夹内运行，输入 JSON 文件或通过标准输入传入 JSON：

```bash
python3 scripts/metric_math.py examples/cash-burn.json
python3 scripts/metric_math.py --help
```

脚本只读取输入并把结果写到标准输出，不联网、不修改输入。调用前确认输入真实含义、周期和币种一致。示例文件是合成算例。

| operation | 必需字段 | 输出 |
|---|---|---|
| ratio | numerator, denominator | ratio（小数）与 percent |
| growth | current, previous | absolute_change, growth_fraction, growth_percent |
| mrr_bridge | start, new, expansion, contraction, churn | end_mrr, net_new_mrr |
| nrr | start, expansion, contraction, churn | ending_cohort_revenue, nrr_fraction, nrr_percent |
| cash_runway | cash, monthly_cash_in, monthly_cash_out | net_monthly_burn, runway_months |

数值必须为有限 JSON 数字；不接受字符串、布尔、NaN 或 Infinity。输入的收入/现金/计数按非负值处理；损益转正等负基期场景需要单独定义，不能硬套本计算器。未知字段会报错，防止拼写错误被忽略。

`status=ok` 表示算式完成，不表示业务数据已核实；零分母/零基期返回 `status=undefined`；非正净消耗返回 `status=not_burning`、跑道 `null`。不合法输入返回错误并以非零状态退出。

## 核对算例

- 现金 360000，月经营流入 20000，流出 80000：净消耗 60000，简化跑道 6 个月。
- 同样现金，流入/流出均为 80000：净消耗 0，跑道不适用，不返回无穷大。
- 期初 MRR 100，新增 20，扩张 10，缩减 5，流失 15：期末 110；同一期初 cohort 的 NRR 为 90%，新增 20 不计入。

运行 [scripts/test_metric_math.py](../scripts/test_metric_math.py) 可复验边界行为；计算器没有实现显著性检验，不能用它证明 A/B 胜出。
