#!/usr/bin/env python3
"""
Generate financial charts for valuation reports.
All chart labels, titles, and text are in ENGLISH.
"""

import matplotlib.pyplot as plt
import os
from pathlib import Path
from typing import List, Dict


def ensure_output_dir(output_dir: str = "generated_images") -> None:
    """Create output directory if it doesn't exist."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def create_line_chart(
    years: List[str],
    values: List[float],
    title: str,
    ylabel: str,
    filename: str,
    color: str,
    output_dir: str = "generated_images",
    value_format: str = "${:.0f}B"
) -> None:
    """
    Create a professional line chart with data labels.

    Args:
        years: List of year strings
        values: List of corresponding values
        title: Chart title
        ylabel: Y-axis label
        filename: Output filename
        color: Line color in hex format
        output_dir: Output directory
        value_format: Format string for data labels
    """
    ensure_output_dir(output_dir)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(years, values, marker='o', linewidth=2.5, markersize=8, color=color)

    # Add data labels
    for i, v in enumerate(values):
        ax.text(i, v + (max(values) - min(values)) * 0.02,
                value_format.format(v),
                ha='center', va='bottom', fontsize=10, color=color, fontweight='bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Fiscal Year', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/{filename}", dpi=300, bbox_inches='tight')
    plt.close()


def create_revenue_trend_chart(
    years: List[str],
    revenue: List[float],
    output_dir: str = "generated_images"
) -> None:
    """Create revenue trend line chart."""
    create_line_chart(
        years=years,
        values=revenue,
        title="Revenue Trend (Last 10 Years)",
        ylabel="Revenue ($ Billions)",
        filename="revenue_trend.png",
        color="#1E88E5",
        output_dir=output_dir
    )


def create_net_income_trend_chart(
    years: List[str],
    net_income: List[float],
    output_dir: str = "generated_images"
) -> None:
    """Create net income trend line chart."""
    create_line_chart(
        years=years,
        values=net_income,
        title="Net Income Trend (Last 10 Years)",
        ylabel="Net Income ($ Billions)",
        filename="net_income_trend.png",
        color="#43A047",
        output_dir=output_dir
    )


def create_fcf_trend_chart(
    years: List[str],
    fcf: List[float],
    output_dir: str = "generated_images"
) -> None:
    """Create free cash flow trend line chart."""
    create_line_chart(
        years=years,
        values=fcf,
        title="Free Cash Flow Trend (Last 10 Years)",
        ylabel="Free Cash Flow ($ Billions)",
        filename="fcf_trend.png",
        color="#8E24AA",
        output_dir=output_dir
    )


def generate_all_charts(
    financial_data: Dict[str, List],
    output_dir: str = "generated_images"
) -> None:
    """
    Generate all three required financial trend charts.

    Args:
        financial_data: Dictionary with keys:
            - 'years': List of year strings
            - 'revenue': List of revenue values
            - 'net_income': List of net income values
            - 'fcf': List of free cash flow values
        output_dir: Output directory for charts
    """
    years = financial_data['years']

    create_revenue_trend_chart(years, financial_data['revenue'], output_dir)
    create_net_income_trend_chart(years, financial_data['net_income'], output_dir)
    create_fcf_trend_chart(years, financial_data['fcf'], output_dir)


if __name__ == "__main__":
    # Example usage
    sample_data = {
        'years': ['2019', '2020', '2021', '2022', '2023', '2024'],
        'revenue': [100, 110, 125, 140, 155, 170],
        'net_income': [20, 22, 25, 28, 31, 35],
        'fcf': [18, 20, 23, 26, 29, 32]
    }
    generate_all_charts(sample_data)
