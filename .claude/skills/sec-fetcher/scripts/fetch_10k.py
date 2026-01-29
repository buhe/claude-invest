"""
下载公司最近5年的10-K年度财报

用法:
    python fetch_10k.py "0000320193"  # Apple的CIK
    python fetch_10k.py "0000789019"  # Microsoft的CIK
"""

import requests
import json
import os
import pandas as pd
from datetime import datetime

headers = {
    "User-Agent": "bear bugu1986@126.com"
}


def fetch_10k_filings(cik, years=5, output_dir=None):
    """
    下载公司最近N年的10-K文件

    参数:
        cik: SEC CIK (10位，带前导零)
        years: 下载最近几年的10-K (默认5年)
        output_dir: 输出目录 (默认为 {公司名}_10K_Files)
    """
    # 获取公司所有filing数据
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("请求失败！请检查CIK是否正确或User-Agent是否设置。")
        return False

    data = response.json()

    # 获取公司名称用于文件夹命名
    company_name_clean = "Company"  # 默认值
    company_name = data.get('filings', {}).get('recent', {}).get('companyName', [None])[0]
    if company_name:
        # 清理公司名称用于文件夹
        company_name_clean = company_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        if output_dir is None:
            output_dir = f"{company_name_clean}_10K_Files"
    else:
        if output_dir is None:
            output_dir = "10K_Files"

    # 解析recent filings
    filings = data['filings']['recent']
    df = pd.DataFrame(filings)
    df['filingDate'] = pd.to_datetime(df['filingDate'])

    # 筛选10-K并排序
    tenk_df = df[df['form'] == '10-K'].sort_values('filingDate', ascending=False).head(years)

    if tenk_df.empty:
        print(f"未找到CIK {cik} 的10-K文件")
        return False

    # 创建下载文件夹
    os.makedirs(output_dir, exist_ok=True)

    # CIK 无前导零
    cik_no_zero = str(data['cik'])

    print(f"开始下载最近{len(tenk_df)}年10-K：\n")
    for idx, row in tenk_df.iterrows():
        accession = row['accessionNumber']
        acc_no_dash = accession.replace("-", "")
        primary_doc = row['primaryDocument']
        report_date = str(row.get('reportDate', 'Unknown'))[:4]  # 财年

        doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_no_zero}/{acc_no_dash}/{primary_doc}"

        filename = f"{company_name_clean}_10K_{report_date}_{primary_doc}"
        filepath = os.path.join(output_dir, filename)

        print(f"下载 {report_date} 财年 10-K ({row['filingDate'].date()})：{doc_url}")

        doc_resp = requests.get(doc_url, headers=headers)
        if doc_resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(doc_resp.content)
            print(f"   保存成功：{filepath}\n")
        else:
            print(f"   下载失败 (状态码: {doc_resp.status_code})\n")

    print(f"所有下载完成！文件保存在 {output_dir} 文件夹。")
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python fetch_10k.py <CIK> [年数] [输出目录]")
        print("示例: python fetch_10k.py 0000320193 5")
        sys.exit(1)

    cik = sys.argv[1].strip()
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    fetch_10k_filings(cik, years, output_dir)
