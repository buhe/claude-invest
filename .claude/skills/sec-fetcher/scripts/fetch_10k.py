"""
下载公司最近5年的10-K年度财报

用法:
    python fetch_10k.py "0000320193"  # Apple的CIK
    python fetch_10k.py "0000789019"  # Microsoft的CIK
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import pandas as pd
import time
from datetime import datetime

headers = {
    "User-Agent": "bear bugu1986@126.com"
}


def create_session_with_retry(retries=3, backoff_factor=1, timeout=30):
    """
    创建带有重试机制的 requests Session

    参数:
        retries: 最大重试次数
        backoff_factor: 重试间隔因子 (秒)
        timeout: 请求超时时间 (秒)
    """
    session = requests.Session()

    # 配置重试策略
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def fetch_10k_filings(cik, years=5, output_dir=None, delay=2):
    """
    下载公司最近N年的10-K文件

    参数:
        cik: SEC CIK (10位，带前导零)
        years: 下载最近几年的10-K (默认5年)
        output_dir: 输出目录 (默认为当前工作目录下的 {公司名}_10K_Files)
        delay: 每个文件下载之间的延迟秒数 (默认2秒)
    """
    # 获取当前工作目录（调用者所在的目录）
    cwd = os.getcwd()

    # 创建带重试的 session
    session = create_session_with_retry(retries=3, backoff_factor=1, timeout=60)

    # 获取公司所有filing数据
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = session.get(url, headers=headers, timeout=60)
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

    # 确定输出目录（相对于当前工作目录）
    if output_dir is None:
        # 使用简化的公司名称作为文件夹名
        folder_name = company_name_clean.replace(' ', '').replace('_', '')
        if not folder_name:
            folder_name = "Company"
        output_dir = os.path.join(cwd, folder_name)

    # 如果提供了相对路径，转换为绝对路径（相对于当前工作目录）
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(cwd, output_dir)

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

        try:
            doc_resp = session.get(doc_url, headers=headers, timeout=60)
            if doc_resp.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(doc_resp.content)
                print(f"   保存成功：{filepath}\n")
            else:
                print(f"   下载失败 (状态码: {doc_resp.status_code})\n")
        except requests.exceptions.SSLError as e:
            print(f"   SSL 错误: {e}")
            print(f"   跳过此文件，继续下一个...\n")
        except requests.exceptions.RequestException as e:
            print(f"   请求错误: {e}")
            print(f"   跳过此文件，继续下一个...\n")

        # 延迟，避免请求过快
        if idx < len(tenk_df) - 1:
            time.sleep(delay)

    # 显示保存的相对路径（更友好）
    if os.path.isabs(output_dir) and cwd:
        try:
            rel_path = os.path.relpath(output_dir, cwd)
            print(f"所有下载完成！文件保存在: {rel_path}/")
        except:
            print(f"所有下载完成！文件保存在: {output_dir}/")
    else:
        print(f"所有下载完成！文件保存在: {output_dir}/")
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
