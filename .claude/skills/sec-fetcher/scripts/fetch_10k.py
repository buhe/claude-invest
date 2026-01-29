#!/usr/bin/env python3
"""
Download SEC 10-K filings for a company.
Usage: python fetch_10k.py <company_name> [output_dir]
"""

import requests
import json
import os
import sys
import argparse
from datetime import datetime

# SEC API requires a User-Agent header
HEADERS = {
    "User-Agent": "bear bugu1986@126.com"
    # Users should modify this to their own name and email
}


def get_cik_by_company_name(company_name: str) -> str | None:
    """
    Get CIK for a company by searching SEC's company API.

    Args:
        company_name: Company name to search for

    Returns:
        CIK as a string (with leading zeros) or None if not found
    """
    # SEC company search API
    url = "https://edata.sec.gov/subs/GetCIKs"
    params = {"company": company_name, "type": "", "cik": "", "sic": "", "owner": "exclude"}

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return None

    results = response.json()
    if not results or "companies" not in results or not results["companies"]:
        return None

    # Return the first match's CIK
    cik = results["companies"][0]["cik_str"]
    # Pad to 10 digits with leading zeros
    return cik.zfill(10)


def fetch_10k_filings(cik: str, company_name: str, output_dir: str = None, years: int = 5) -> list[str]:
    """
    Download the most recent 10-K filings for a company.

    Args:
        cik: Company CIK (with or without leading zeros)
        company_name: Name used for folder/file naming
        output_dir: Directory to save files (default: {company_name}_10K_Files)
        years: Number of years to fetch (default: 5)

    Returns:
        List of downloaded file paths
    """
    # Remove leading zeros for URL construction
    cik_no_zero = cik.lstrip("0") or "0"

    # Get company filings
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch filings for CIK {cik}")

    data = response.json()

    # Parse recent filings
    filings = data["filings"]["recent"]

    # Create output directory
    if output_dir is None:
        output_dir = f"{company_name.replace(' ', '_')}_10K_Files"
    os.makedirs(output_dir, exist_ok=True)

    # Filter for 10-K forms and get recent ones
    tenk_filings = []
    for i in range(len(filings["form"])):
        if filings["form"][i] == "10-K":
            tenk_filings.append({
                "accessionNumber": filings["accessionNumber"][i],
                "filingDate": filings["filingDate"][i],
                "reportDate": filings.get("reportDate", [{}] * len(filings["form"]))[i] if "reportDate" in filings else "Unknown",
                "primaryDocument": filings["primaryDocument"][i],
            })

    # Sort by filing date and get most recent
    tenk_filings.sort(key=lambda x: x["filingDate"], reverse=True)
    tenk_filings = tenk_filings[:years]

    downloaded_files = []
    print(f"开始下载最近 {len(tenk_filings)} 份 10-K 报告：\n")

    for filing in tenk_filings:
        accession = filing["accessionNumber"]
        acc_no_dash = accession.replace("-", "")
        primary_doc = filing["primaryDocument"]
        report_date = str(filing["reportDate"])[:4] if filing["reportDate"] != "Unknown" else "Unknown"
        filing_date = filing["filingDate"][:10]

        doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_no_zero}/{acc_no_dash}/{primary_doc}"

        filename = f"{company_name.replace(' ', '_')}_10K_{report_date}_{primary_doc}"
        filepath = os.path.join(output_dir, filename)

        print(f"下载 {report_date} 财年 10-K (提交日期: {filing_date})")
        print(f"  URL: {doc_url}")

        doc_resp = requests.get(doc_url, headers=HEADERS)
        if doc_resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(doc_resp.content)
            print(f"  保存成功: {filepath}\n")
            downloaded_files.append(filepath)
        else:
            print(f"  下载失败 (HTTP {doc_resp.status_code})\n")

    print(f"完成！共下载 {len(downloaded_files)} 份文件，保存在 {output_dir} 目录。")
    return downloaded_files


def main():
    parser = argparse.ArgumentParser(
        description="Download SEC 10-K filings for a company",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fetch_10k.py "Apple Inc"
  python fetch_10k.py "Microsoft Corporation" ./msft_filings
  python fetch_10k.py "Tesla Inc" ./tesla --years 3
        """
    )
    parser.add_argument("company", help="Company name (as listed with SEC)")
    parser.add_argument("output_dir", nargs="?", help="Output directory (optional)")
    parser.add_argument("--years", type=int, default=5, help="Number of years to fetch (default: 5)")

    args = parser.parse_args()

    # Get CIK
    print(f"搜索公司: {args.company}")
    cik = get_cik_by_company_name(args.company)
    if not cik:
        print(f"未找到公司 '{args.company}'，请检查公司名称是否正确。")
        sys.exit(1)
    print(f"找到 CIK: {cik}\n")

    # Fetch filings
    try:
        fetch_10k_filings(cik, args.company, args.output_dir, args.years)
    except RuntimeError as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
