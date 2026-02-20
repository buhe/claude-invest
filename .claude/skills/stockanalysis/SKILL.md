---
name: stockanalysis
description: 从 stockanalysis.com 获取公司财务数据。当 Claude 需要通过股票代码检索上市公司财务报表（利润表、资产负债表、现金流量表）、公司概览或关键财务指标（如收入、净利润、经营活动现金流、资本支出和自由现金流）时使用。
---

# Stockanalysis

## 概述

使用 agent-browser 从 [stockanalysis.com](https://stockanalysis.com/) 获取公司财务数据。可通过股票代码检索任何上市公司的财务报表和关键指标。
stockanalysis 可以查询美股、港股（先转换成代码，如，腾讯 > 0700 (港股其实目前只需要四位 stockanalysis 使用四位数字，是把查询到的第一个0去掉，如：00700 -> 0700 ) https://stockanalysis.com/quote/hkg/0700/financials/）、A股（先转换成代码，如，茅台 > 600519 https://stockanalysis.com/quote/sha/600519/financials/）等股票的财务数据。

## URL 模式

| 数据类型 | URL 模式 | 示例 |
|----------|----------|------|
| 公司概览 | `https://stockanalysis.com/stocks/{股票代码}/` | https://stockanalysis.com/stocks/aapl/ |
| 利润表 | `https://stockanalysis.com/stocks/{股票代码}/financials/` | https://stockanalysis.com/stocks/aapl/financials/ |
| 资产负债表 | `https://stockanalysis.com/stocks/{股票代码}/financials/balance-sheet/` | https://stockanalysis.com/stocks/aapl/financials/balance-sheet/ |
| 现金流量表 | `https://stockanalysis.com/stocks/{股票代码}/financials/cash-flow-statement/` | https://stockanalysis.com/stocks/aapl/financials/cash-flow-statement/ |
| 最近1年的分红 | `https://stockanalysis.com/stocks/{股票代码}/dividend/` | https://stockanalysis.com/stocks/aapl/dividend/ |

## 快速开始

### 基本公司数据

```bash
agent-browser open "https://stockanalysis.com/stocks/{股票代码}/"
agent-browser snapshot
```

### 财务报表

```bash
agent-browser open "https://stockanalysis.com/stocks/{股票代码}/financials/"
agent-browser open "https://stockanalysis.com/stocks/{股票代码}/financials/cash-flow-statement/"
```

## 数据提取

### 关键财务指标

| 指标 | 位置 | 描述 |
|------|------|------|
| 营业收入 | 利润表 | 运营产生的总收入 |
| 净利润 | 利润表 | 扣除所有费用和税费后的利润 |
| 经营活动现金流 | 现金流量表 | 核心业务活动产生的现金 |
| 资本支出 (CapEx) | 现金流量表 | 用于固定资产和设备的现金支出 |
| 自由现金流 (FCF) | 现金流量表 | 经营活动现金流 - 资本支出 |
| 总资产 | 资产负债表 | 公司拥有的所有资产 |
| 总负债 | 资产负债表 | 所有债务和义务 |

### 自由现金流计算

```
自由现金流 = 经营活动现金流 - 资本支出
```

## 工作流程

1. **构建 URL**：使用股票代码 `https://stockanalysis.com/stocks/{股票代码}/financials/`

2. **打开页面**：使用 agent-browser
   ```bash
   agent-browser open "https://stockanalysis.com/stocks/{股票代码}/financials/"
   ```

3. **截取快照**：捕获页面内容
   ```bash
   agent-browser snapshot
   ```

4. **提取数据**：从快照中提取，重点关注：
   - 表格标题（年份/季度）
   - 指标行（营业收入、净利润、经营活动现金流、资本支出、自由现金流）

5. **格式化输出**：以清晰的表格结构呈现
6. **详细命令** Run agent-browser --help to see available commands
7. **异常处理**：如果页面出现类似 references/nvda_cash_flow_full.png 的注册页面则关闭。

## 数据周期

StockAnalysis 提供多种数据格式：
- **年度**：财政年度数据（默认）
- **季度**：季度报告
- **TTM**：过去十二个月

使用页面上的导航按钮切换不同周期。

## 常见股票代码示例

| 公司 | 股票代码 |
|------|----------|
| 苹果 | AAPL |
| 微软 | MSFT |
| 谷歌/字母表 | GOOGL |
| 亚马逊 | AMZN |
| 特斯拉 | TSLA |
| 英伟达 | NVDA |
| Meta | META |
| 伯克希尔·哈撒韦 | BRK.B |
| 强生 | JNJ |
| 摩根大通 | JPM |
