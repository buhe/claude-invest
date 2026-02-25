"""
下载公司最近5年的年度财报

用法:
    python fetch_10k.py "0000320193"  # Apple的CIK (美国公司，下载10-K)
    python fetch_10k.py "0000789019"  # Microsoft的CIK (美国公司，下载10-K)

说明:
    - 美国本土公司下载 10-K
    - 外国公司下载 20-F (自动检测)
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
    "User-Agent": "bear bugu1986@gmail.com"
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


def get_form_type(df):
    """
    自动检测公司应该下载的报表类型 (10-K 或 20-F)

    返回: '10-K' 或 '20-F'
    """
    # 统计可用的 10-K 和 20-F 数量
    tenk_count = len(df[df['form'] == '10-K'])
    twentyf_count = len(df[df['form'] == '20-F'])

    # 优先使用有数据的类型，如果都有，10-K 优先（美国公司）
    if tenk_count > 0:
        return '10-K'
    elif twentyf_count > 0:
        return '20-F'
    else:
        return '10-K'  # 默认


def fetch_10k_filings(cik, years=5, output_dir=None, delay=2, work_dir=None):
    """
    下载公司最近N年的年度财报文件 (10-K 或 20-F)

    参数:
        cik: SEC CIK (10位，带前导零)
        years: 下载最近几年的财报 (默认5年)
        output_dir: 输出目录 (默认为工作目录下的 {公司名}_10K_Files)
        delay: 每个文件下载之间的延迟秒数 (默认2秒)
        work_dir: 工作目录，用于解析相对路径 (默认为当前工作目录)

    说明:
        - 美国本土公司自动下载 10-K
        - 外国公司自动下载 20-F
    """
    # 获取工作目录（优先使用传入的 work_dir，否则使用当前工作目录）
    cwd = work_dir if work_dir is not None else os.getcwd()

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

    # 确定输出目录（相对于工作目录）
    if output_dir is None:
        # 直接在工作目录下保存文件，不创建子文件夹
        output_dir = cwd

    # 如果提供了相对路径，转换为绝对路径（相对于工作目录）
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(cwd, output_dir)

    # 解析recent filings
    filings = data['filings']['recent']
    df = pd.DataFrame(filings)
    df['filingDate'] = pd.to_datetime(df['filingDate'])

    # 自动检测报表类型 (10-K 或 20-F)
    form_type = get_form_type(df)

    # 筛选指定类型的报表并排序
    if form_type == '20-F':
        filtered_df = df[df['form'] == '20-F'].sort_values('filingDate', ascending=False).head(years)
        print(f"检测到外国公司，将下载 20-F 报表\n")
    else:
        filtered_df = df[df['form'] == '10-K'].sort_values('filingDate', ascending=False).head(years)
        print(f"检测到美国本土公司，将下载 10-K 报表\n")

    if filtered_df.empty:
        print(f"未找到CIK {cik} 的 {form_type} 文件")
        return False

    # 创建下载文件夹
    os.makedirs(output_dir, exist_ok=True)

    # CIK 无前导零
    cik_no_zero = str(data['cik'])

    # 根据报表类型设置文件名前缀
    form_prefix = "20F" if form_type == "20-F" else "10K"

    print(f"开始下载最近{len(filtered_df)}年 {form_type}：\n")
    for idx, row in filtered_df.iterrows():
        accession = row['accessionNumber']
        acc_no_dash = accession.replace("-", "")
        primary_doc = row['primaryDocument']
        report_date = str(row.get('reportDate', 'Unknown'))[:4]  # 财年

        doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_no_zero}/{acc_no_dash}/{primary_doc}"

        filename = f"{company_name_clean}_{form_prefix}_{report_date}_{primary_doc}"
        filepath = os.path.join(output_dir, filename)

        print(f"下载 {report_date} 财年 {form_type} ({row['filingDate'].date()})：{doc_url}")

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
        if idx < len(filtered_df) - 1:
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
        print("用法: python fetch_10k.py <CIK> [年数] [输出目录] [工作目录]")
        print("示例: python fetch_10k.py 0000320193 5")
        print("示例: python fetch_10k.py 0000320193 5 . /path/to/work/dir")
        sys.exit(1)

    cik = sys.argv[1].strip()
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    work_dir = sys.argv[4] if len(sys.argv) > 4 else None

    fetch_10k_filings(cik, years, output_dir, work_dir=work_dir)
