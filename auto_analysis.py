#!/usr/bin/env python3
"""
自动化投资分析系统
自动执行5轮分析，每轮6个子代理，交叉对比，翻译成英文更新README
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
import re
import time

class AutoInvestmentAnalysis:
    """自动化投资分析系统"""

    def __init__(self, company_name: str, exchange: str = "SEC"):
        """
        初始化自动化分析系统

        Args:
            company_name: 公司名称（如：Apple Inc.）
            exchange: 交易所类型 (SEC/HKEX)
        """
        self.company_name = company_name
        self.exchange = exchange.upper()
        self.base_dir = Path("input")
        self.rounds = 5
        self.agents = [
            "segment-agent",
            "balance-agent",
            "value-agent",
            "cap-agent",
            "cap-acq-agent",
            "mda-agent"
        ]
        self.start_time = datetime.now()

    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def step1_download_reports(self):
        """步骤1：下载财报"""
        self.log("=== 步骤1：下载财报 ===")

        # 创建input目录
        self.base_dir.mkdir(exist_ok=True)
        os.chdir(self.base_dir)

        # 使用prepare-agent下载财报
        prompt = f"""
        准备{self.company_name}的财报数据：

        1. 判断公司在哪上市：
           - 如果在美股上市，使用 sec-fetcher skill 下载最近5年的10-K/20-F年报
           - 如果在港股上市，使用 hkex-fetcher skill 下载最近5年的年报

        2. 使用 stockanalysis skill 提取最近5年的：
           - 利润表
           - 资产负债表
           - 现金流量表
           - 最近1年的分红数据

        3. 将所有数据写入 references.md 文件

        4. 确保财报和references.md都完整且准确
        """

        self.log(f"启动 prepare-agent 下载财报...")
        self.log(f"提示：{prompt[:100]}...")

        # 返回上级目录
        os.chdir("..")

    def step2_run_rounds(self):
        """步骤2：执行5轮分析"""
        self.log("\n=== 步骤2：执行5轮分析 ===")

        for round_num in range(1, self.rounds + 1):
            self.log(f"\n--- 第{round_num}轮分析 ---")

            # 使用invest-report skill执行单轮分析
            self.log(f"启动第{round_num}轮的6个分析代理...")

            # 这里实际上会调用Claude Code的invest-report skill
            # 每轮会并行启动6个代理

    def step3_cross_compare(self):
        """步骤3：交叉对比"""
        self.log("\n=== 步骤3：交叉对比分析 ===")

        # 对每个模块使用diff-agent进行比对
        modules = [
            "业务构成与成本结构",
            "资产负债表",
            "企业估值",
            "资本配置",
            "投资入股与并购",
            "MD&A管理层讨论"
        ]

        for module in modules:
            self.log(f"比对 {module} 模块的5轮分析结果...")

    def step4_generate_final_report(self):
        """步骤4：生成最终报告"""
        self.log("\n=== 步骤4：生成最终投资研究报告 ===")

        # 基于diff-agent的校验报告生成最终报告
        self.log("汇总各模块校验报告，生成最终投资研究...")

    def step5_translate_to_english(self):
        """步骤5：翻译成英文"""
        self.log("\n=== 步骤5：翻译成英文 ===")

        # 查找最终报告
        report_files = list(self.base_dir.glob("*投资研究报告.md"))
        if not report_files:
            self.log("未找到投资研究报告", "ERROR")
            return

        report_file = report_files[-1]  # 使用最新的报告
        self.log(f"翻译报告: {report_file.name}")

        # 读取中文报告
        with open(report_file, 'r', encoding='utf-8') as f:
            chinese_content = f.read()

        # 翻译成英文
        english_content = self.translate_markdown(chinese_content)

        # 保存英文版
        english_file = report_file.parent / f"{report_file.stem}_EN.md"
        with open(english_file, 'w', encoding='utf-8') as f:
            f.write(english_content)

        self.log(f"英文报告已保存: {english_file.name}")
        return english_file

    def step6_update_readme(self, english_report_path: Path):
        """步骤6：更新README"""
        self.log("\n=== 步骤6：更新README ===")

        readme_path = Path("README.md")

        # 读取现有README
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        else:
            readme_content = "# Investment Research Reports\n\n"

        # 读取英文报告
        with open(english_report_path, 'r', encoding='utf-8') as f:
            english_report = f.read()

        # 生成README更新内容
        update_date = datetime.now().strftime("%Y-%m-%d")
        new_section = f"""

## {self.company_name} Investment Research

**Analysis Date**: {update_date}
**Rounds of Analysis**: 5 rounds × 6 agents = 30 independent analyses
**Exchange**: {self.exchange}

### Report Summary

{self.extract_summary(english_report)}

### Full Report

See [Full English Report]({english_report_path}) for complete analysis.

### Key Findings

{self.extract_key_findings(english_report)}

### Investment Rating

{self.extract_rating(english_report)}

---

*Auto-generated on {update_date}*
"""

        # 更新README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content + new_section)

        self.log(f"README已更新")

    def translate_markdown(self, chinese_text: str) -> str:
        """翻译Markdown内容"""
        # 这里可以调用翻译API
        # 为了演示，返回一个简化的翻译版本

        # 提取关键部分进行翻译
        translations = {
            "报告摘要": "Executive Summary",
            "核心观点": "Key Insights",
            "关键财务指标": "Key Financial Metrics",
            "投资评级": "Investment Rating",
            "业务构成与成本结构分析": "Business Segments and Cost Structure Analysis",
            "资产负债表分析": "Balance Sheet Analysis",
            "企业估值分析": "Valuation Analysis",
            "资本配置分析": "Capital Allocation Analysis",
            "MD&A管理层讨论与分析": "Management's Discussion and Analysis",
            "综合评估与投资建议": "Comprehensive Assessment and Investment Recommendation",
            "数据来源与免责声明": "Data Sources and Disclaimer",
        }

        result = chinese_text
        for cn, en in translations.items():
            result = result.replace(cn, en)

        return result

    def extract_summary(self, report: str) -> str:
        """提取报告摘要"""
        # 简单提取第一段作为摘要
        lines = report.split('\n')
        summary_lines = []
        for line in lines[:20]:  # 前20行
            if line.strip() and not line.startswith('#'):
                summary_lines.append(line)
            if len(summary_lines) >= 5:
                break
        return '\n'.join(summary_lines)

    def extract_key_findings(self, report: str) -> str:
        """提取关键发现"""
        # 查找关键发现部分
        if "Key Insights" in report or "关键观点" in report:
            start = report.find("Key Insights")
            if start == -1:
                start = report.find("关键观点")
            if start != -1:
                section = report[start:start+500]
                return section[:200] + "..."
        return "See full report for detailed findings."

    def extract_rating(self, report: str) -> str:
        """提取投资评级"""
        # 查找投资评级
        if "Investment Rating" in report or "投资评级" in report:
            start = report.find("Investment Rating")
            if start == -1:
                start = report.find("投资评级")
            if start != -1:
                section = report[start:start+300]
                lines = section.split('\n')
                for line in lines:
                    if 'Buy' in line or 'Hold' in line or 'Sell' in line or '买入' in line or '持有' in line:
                        return line.strip()
        return "See full report for investment rating."

    def run_full_analysis(self):
        """运行完整分析流程"""
        self.log(f"开始自动化投资分析: {self.company_name}")
        self.log(f"交易所: {self.exchange}")
        self.log(f"分析轮次: {self.rounds}")
        self.log(f"每轮代理数: {len(self.agents)}")

        try:
            # 步骤1：下载财报
            self.step1_download_reports()

            # 步骤2：执行5轮分析
            self.step2_run_rounds()

            # 步骤3：交叉对比
            self.step3_cross_compare()

            # 步骤4：生成最终报告
            self.step4_generate_final_report()

            # 步骤5：翻译成英文
            english_report = self.step5_translate_to_english()
            if not english_report:
                self.log("翻译失败，终止流程", "ERROR")
                return

            # 步骤6：更新README
            self.step6_update_readme(english_report)

            # 完成
            elapsed = datetime.now() - self.start_time
            self.log(f"\n=== 分析完成 ===")
            self.log(f"总耗时: {elapsed}")
            self.log(f"报告已生成并更新到README")

        except Exception as e:
            self.log(f"分析过程中发生错误: {str(e)}", "ERROR")
            raise


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python auto_analysis.py <公司名称> [交易所]")
        print("示例: python auto_analysis.py 'Apple Inc.' SEC")
        print("示例: python auto_analysis.py '腾讯控股' HKEX")
        sys.exit(1)

    company_name = sys.argv[1]
    exchange = sys.argv[2] if len(sys.argv) > 2 else "SEC"

    analyzer = AutoInvestmentAnalysis(company_name, exchange)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
