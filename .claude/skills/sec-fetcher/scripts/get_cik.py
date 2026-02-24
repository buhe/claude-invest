"""
根据公司名称获取 SEC CIK

用法:
    python get_cik.py "Apple"
    python get_cik.py "Microsoft"
"""

import requests
import json
import pandas as pd
import sys

# === 重要：请替换为您的真实信息 ===
headers = {
    "User-Agent": "bear 81128054@qq.com"
}


def get_cik_by_company_name(company_name, headers=headers):
    """
    根据公司名称（支持部分匹配）获取SEC CIK
    返回：CIK字符串（10位，前导零），或None
    """
    url = "https://www.sec.gov/files/company_tickers.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"请求SEC数据失败：{e}")
        print("请检查网络或User-Agent是否正确设置。")
        return None

    # 构建DataFrame
    records = []
    for key, value in data.items():
        records.append({
            'cik': str(value['cik_str']).zfill(10),          # 补齐10位
            'ticker': value['ticker'].upper(),
            'company_name': value['title']
        })

    df = pd.DataFrame(records)

    # 模糊搜索：公司名称包含输入关键词（忽略大小写）
    mask = df['company_name'].str.lower().str.contains(company_name.lower(), na=False)
    results = df[mask]

    if results.empty:
        print(f"未找到包含 '{company_name}' 的公司。")
        print("提示：尝试输入更精确或更短的关键词，例如 'Apple'、'Microsoft'。")
        return None
    else:
        print(f"找到 {len(results)} 个匹配结果：")
        print(results[['cik', 'ticker', 'company_name']].to_string(index=False))
        print("\n返回第一个匹配的CIK（通常是最相关的）。")
        return results.iloc[0]['cik']  # 返回第一个匹配的CIK


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1].strip()
    else:
        company = input("请输入公司名称（例如 Apple、Microsoft、Tesla）：").strip()

    if company:
        cik = get_cik_by_company_name(company, headers)
        if cik:
            print(f"\n公司 '{company}' 的CIK 是：{cik}")
    else:
        print("请提供公司名称")
