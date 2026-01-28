#!/usr/bin/env python3
"""
Chart Generation Script for Investment Research Reports
Generates professional business charts using matplotlib

All charts must:
- Use 300 DPI resolution
- Use English labels and titles (even for Chinese reports)
- Save to generated_images/ directory
- Display data labels for clarity
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from pathlib import Path

# Set style for professional business presentation
plt.style.use('seaborn-v0_8-whitegrid')

# Professional color palette
COLOR_PALETTE = ['#1E88E5', '#43A047', '#FF9800', '#7B1FA2', '#E91E63',
                 '#00BCD4', '#FFC107', '#8BC34A', '#9C27B0', '#607D8B']

def ensure_output_dir():
    """Ensure generated_images directory exists"""
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def create_business_segments_pie(segments, percentages, year):
    """
    Create business segments revenue breakdown pie chart

    Args:
        segments: List of business segment names (in English)
        percentages: List of revenue percentages matching segments
        year: The fiscal year for the chart title
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Explode the largest segment for emphasis
    explode = [0.08 if p == max(percentages) else 0.03 for p in percentages]

    colors = COLOR_PALETTE[:len(segments)]

    wedges, texts, autotexts = ax.pie(
        percentages,
        explode=explode,
        labels=segments,
        colors=colors,
        autopct='%1.0f%%',
        pctdistance=0.85,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        startangle=90,
        counterclock=False
    )

    # Style percentage labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax.set_title(f'Business Segments Revenue Breakdown ({year})',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    output_dir = ensure_output_dir()
    filepath = output_dir / 'business_segments.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated: {filepath}")
    return str(filepath)


def create_geographic_segments_pie(regions, percentages, year):
    """
    Create geographic segments revenue breakdown pie chart

    Args:
        regions: List of geographic region names (in English)
        percentages: List of revenue percentages matching regions
        year: The fiscal year for the chart title
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Explode the largest segment for emphasis
    explode = [0.08 if p == max(percentages) else 0.03 for p in percentages]

    colors = COLOR_PALETTE[:len(regions)]

    wedges, texts, autotexts = ax.pie(
        percentages,
        explode=explode,
        labels=regions,
        colors=colors,
        autopct='%1.0f%%',
        pctdistance=0.85,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        startangle=90,
        counterclock=False
    )

    # Style percentage labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax.set_title(f'Geographic Revenue Breakdown ({year})',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    output_dir = ensure_output_dir()
    filepath = output_dir / 'geographic_segments.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated: {filepath}")
    return str(filepath)


def create_cost_structure_pie(cost_categories, percentages, year):
    """
    Create cost structure breakdown pie chart

    Args:
        cost_categories: List of cost category names (in English)
        percentages: List of cost percentages matching categories
        year: The fiscal year for the chart title
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Explode the largest segment for emphasis
    explode = [0.08 if p == max(percentages) else 0.03 for p in percentages]

    colors = COLOR_PALETTE[:len(cost_categories)]

    wedges, texts, autotexts = ax.pie(
        percentages,
        explode=explode,
        labels=cost_categories,
        colors=colors,
        autopct='%1.0f%%',
        pctdistance=0.85,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        startangle=90,
        counterclock=False
    )

    # Style percentage labels
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax.set_title(f'Cost Structure Breakdown ({year})',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    output_dir = ensure_output_dir()
    filepath = output_dir / 'cost_structure.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated: {filepath}")
    return str(filepath)


def create_revenue_trend_line(years, revenues, company_name):
    """
    Create revenue trend line chart (16:9 aspect ratio)

    Args:
        years: List of fiscal years (as strings)
        revenues: List of revenue values matching years
        company_name: Name of the company for title
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot line
    ax.plot(years, revenues, marker='o', linewidth=2.5,
            markersize=8, color=COLOR_PALETTE[0])

    # Add data labels
    for i, (year, revenue) in enumerate(zip(years, revenues)):
        ax.annotate(f'{revenue:.1f}',
                    xy=(i, revenue),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    ax.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue (Billions USD)', fontsize=12, fontweight='bold')
    ax.set_title(f'{company_name} Revenue Trend', fontsize=14, fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    output_dir = ensure_output_dir()
    filepath = output_dir / 'revenue_trend.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated: {filepath}")
    return str(filepath)


def create_debt_equity_bar(years, debt, equity, company_name):
    """
    Create debt vs equity comparison bar chart (16:9 aspect ratio)

    Args:
        years: List of fiscal years (as strings)
        debt: List of total debt values matching years
        equity: List of total equity values matching years
        company_name: Name of the company for title
    """
    import numpy as np

    x = np.arange(len(years))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))

    bars1 = ax.bar(x - width/2, debt, width, label='Total Debt',
                   color=COLOR_PALETTE[2])
    bars2 = ax.bar(x + width/2, equity, width, label='Total Equity',
                   color=COLOR_PALETTE[1])

    # Add data labels
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amount (Billions USD)', fontsize=12, fontweight='bold')
    ax.set_title(f'{company_name} Debt vs Equity', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_dir = ensure_output_dir()
    filepath = output_dir / 'debt_equity.png'
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Generated: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    # Example usage (for testing)
    print("Chart generation script loaded. Import functions to generate charts.")
