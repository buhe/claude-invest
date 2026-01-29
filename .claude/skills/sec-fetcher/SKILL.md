---
name: sec-fetcher
description: Download SEC 10-K annual reports for US public companies. Use when user needs to download company 10-K filings from SEC EDGAR database, get annual financial reports for a specific company, or fetch SEC filing data by company name. The skill automatically finds the company CIK and downloads the most recent 5 years of 10-K annual reports.
---

# SEC Fetcher

从 SEC EDGAR 数据库下载美国上市公司的 10-K 年度财报。

## Quick Start

使用 Python 脚本直接下载财报：

```bash
python scripts/fetch_10k.py "Apple Inc"
```

指定输出目录：

```bash
python scripts/fetch_10k.py "Microsoft Corporation" ./msft_filings
```

自定义年份（默认 5 年）：

```bash
python scripts/fetch_10k.py "Tesla Inc" ./tesla --years 3
```

## Workflow

1. **搜索公司 CIK**
   - 通过公司名称在 SEC 数据库中查找对应的 CIK（Central Index Key）
   - 如果找不到，请检查公司名称是否与 SEC 列表一致（例如 "Apple Inc" 而非 "Apple"）

2. **获取 10-K 列表**
   - 从 SEC Submissions API 获取公司最近的所有备案文件
   - 筛选 Form 10-K（年度财报）

3. **下载文件**
   - 按提交日期排序，获取最近 N 年的 10-K
   - 下载到 `{公司名}_10K_Files` 目录（或自定义目录）

## Script Details

`scripts/fetch_10k.py` 包含两个主要函数：

### `get_cik_by_company_name(company_name: str) -> str | None`

根据公司名称搜索 SEC Company API，返回 CIK（带前导零的 10 位数字）。

### `fetch_10k_filings(cik: str, company_name: str, output_dir: str = None, years: int = 5) -> list[str]`

下载指定公司的 10-K 文件。

**参数：**
- `cik`: 公司 CIK（有无前导零均可）
- `company_name`: 用于文件夹/文件命名
- `output_dir`: 输出目录（默认: `{公司名}_10K_Files`）
- `years`: 获取年数（默认: 5）

**返回：** 下载的文件路径列表

## User-Agent Requirement

SEC API 要求设置 User-Agent 头部。脚本中使用：

```python
HEADERS = {
    "User-Agent": "bear bugu1986@126.com"
}
```

建议用户修改为自己的姓名和邮箱。

## Resources

### scripts/
- `fetch_10k.py`: 完整的 10-K 下载脚本，包含 CIK 搜索和文件下载功能
