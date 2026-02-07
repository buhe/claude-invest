---
name: sec-fetcher
description: 根据公司名称获取 SEC CIK 并下载公司年度 10-K 财报文件。当用户需要以下操作时使用：(1) 根据公司名获取 SEC CIK，(2) 下载公司的 10-K 年度财报文件，(3) 获取 SEC EDGAR 系统中的公司 filing 数据，或请求美国上市公司的年报文件
---

# SEC Fetcher

## Overview

通过 SEC EDGAR 系统获取美国上市公司的 CIK（Central Index Key）和年度 10-K 财报文件。

## Quick Start

### 获取公司 CIK

根据公司名称（支持模糊匹配）获取 SEC CIK：

```bash
python scripts/get_cik.py "Apple"
python scripts/get_cik.py "Microsoft"
```

脚本会显示所有匹配结果并返回第一个 CIK（10位，带前导零）。

### 下载 10-K 财报

使用 CIK 下载最近 5 年的 10-K 文件：

```bash
python scripts/fetch_10k.py "0000320193"        # Apple，保存到当前目录
python scripts/fetch_10k.py "0000320193" 5     # 指定年数
python scripts/fetch_10k.py "0000320193" 5 "output_dir"  # 指定输出目录
python scripts/fetch_10k.py "0000320193" 5 "output_dir" "/path/to/work/dir"  # 指定工作目录
```

**重要说明**：
- 默认情况下，文件会保存到**当前工作目录**（不是脚本所在目录）
- 通过 `work_dir` 参数可以指定工作目录，用于解析相对路径
- 在 skill 执行时，应传递工作目录以确保文件下载到正确的位置

## 完整工作流

下载公司财报的完整流程：

1. **获取 CIK**：运行 `get_cik.py` 获取公司的 CIK
2. **下载财报**：使用 CIK 运行 `fetch_10k.py` 下载 10-K 文件

示例：

```bash
# 步骤1：获取 Apple 的 CIK
cik=$(python scripts/get_cik.py "Apple" | tail -1)

# 步骤2：下载财报到当前目录
python scripts/fetch_10k.py "$cik"

# 或指定工作目录（推荐在 skill 执行时使用）
python scripts/fetch_10k.py "$cik" 5 "." "/path/to/input/dir"
```

## API 说明

### SEC Company Tickers API

- **URL**: `https://www.sec.gov/files/company_tickers.json`
- **用途**: 获取所有上市公司的 CIK、股票代码和公司名称
- **更新**: 每个交易日更新

### SEC Submissions API

- **URL**: `https://data.sec.gov/submissions/CIK{cik}.json`
- **参数**: CIK（10位，带前导零）
- **返回**: 公司的所有 filing 数据，包括 10-K、10-Q、8-K 等

## 注意事项

1. **User-Agent**: SEC 要求请求必须包含有效的 User-Agent 头部，格式为 `姓名 邮箱`
2. **请求限制**: SEC 建议请求频率不超过每秒 10 次
3. **CIK 格式**: SEC API 中 CIK 必须是 10 位数字，不足需补前导零
4. **文件格式**: 下载的 10-K 文件通常是 HTML 或 PDF 格式
5. **SSL 错误**：如果出现 SSL 错误，尝试更换其中的邮箱，待选，bugu1986@126.com gubu1986@126.com 81128054@qq.com 

## Resources

### scripts/get_cik.py

根据公司名称获取 SEC CIK 的脚本。支持模糊匹配，返回最相关的结果。

**功能**：
- 从 SEC 获取完整公司列表
- 支持公司名称模糊搜索
- 返回 10 位 CIK（带前导零）

### scripts/fetch_10k.py

下载公司最近 N 年的 10-K 年度财报。

**功能**：
- 根据 CIK 获取公司的所有 filings
- 筛选并下载最近 N 年的 10-K 文件
- 自动创建以公司名命名的文件夹
- 支持自定义下载年数和输出目录
