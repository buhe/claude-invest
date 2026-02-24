#!/usr/bin/env python3
"""
Long-term Debt Trend Line Chart Generator
Creates a line chart showing long-term debt trend over years
"""

import matplotlib.pyplot as plt
import os
from . import CHART_DEBT_TREND


def generate_debt_trend_chart(years, debt_values, output_dir='generated_images'):
    """
    Generate long-term debt trend line chart

    Args:
        years: list of str, fiscal years
            Example: ['2019', '2020', '2021', '2022', '2023', '2024']
        debt_values: list of float, debt values matching the years (in billions)
            Example: [100, 110, 105, 120, 115, 130]
        output_dir: str, directory to save the chart
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Validate input
    if len(years) != len(debt_values):
        raise ValueError("years and debt_values must have the same length")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(years, debt_values, marker='o', linewidth=2.5, markersize=8, color='#795548')

    # Add data labels
    for i, v in enumerate(debt_values):
        ax.text(i, v + (max(debt_values) * 0.02), f'${v:.1f}B',
                ha='center', va='bottom', fontsize=10, color='#795548', fontweight='bold')

    ax.set_title('Long-term Debt Trend', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Fiscal Year', fontsize=12)
    ax.set_ylabel('Debt ($ Billions)', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/{CHART_DEBT_TREND}', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[OK] Chart saved: {output_dir}/{CHART_DEBT_TREND}")


if __name__ == '__main__':
    # Example usage
    example_years = ['2019', '2020', '2021', '2022', '2023', '2024']
    example_debt = [100.5, 110.2, 105.8, 120.3, 115.7, 130.1]
    generate_debt_trend_chart(example_years, example_debt)
