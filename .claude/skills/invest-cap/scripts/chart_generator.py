#!/usr/bin/env python3
"""
Investment Report Chart Generator
Generates professional financial charts for investment research reports using matplotlib.
All charts use English labels and titles, saved at 300 DPI to generated_images/ directory.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Union
import os

# Try relative import first, fall back to absolute import
try:
    from . import CHART_DIVIDEND_GROWTH, CHART_SHARE_COUNT_TREND, CHART_CAPITAL_ALLOCATION_BREAKDOWN
except ImportError:
    # When running as standalone script
    CHART_DIVIDEND_GROWTH = "dividend_growth.png"
    CHART_SHARE_COUNT_TREND = "share_count_trend.png"
    CHART_CAPITAL_ALLOCATION_BREAKDOWN = "capital_allocation_breakdown.png"


class ChartGenerator:
    """Generate financial charts for investment research reports."""

    def __init__(self, output_dir: str = "generated_images"):
        """
        Initialize chart generator with output directory.

        Args:
            output_dir: Output directory path (relative to current working directory)
        """
        # Use absolute path based on current working directory to avoid
        # accidentally creating files in the script's own directory
        output_path = Path(output_dir)
        if output_path.is_absolute():
            self.output_dir = output_path
        else:
            # Resolve relative path from current working directory, not script location
            self.output_dir = Path.cwd() / output_path

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set matplotlib style for professional business charts
        plt.style.use('default')

    def _format_currency(self, value: float, prefix: str = "$") -> str:
        """Format value as currency string."""
        if abs(value) >= 1e9:
            return f"{prefix}{value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"{prefix}{value/1e6:.2f}M"
        else:
            return f"{prefix}{value:.2f}"

    def share_count_trend(
        self,
        years: List[str],
        share_counts: List[int],
        title: str = "Share Count Trend",
        split_year: Optional[int] = None,
        split_ratio: float = 1.0
    ) -> str:
        """
        Chart 6: Share Count Trend (Line Chart)

        Handles stock splits by normalizing data. If a stock split occurred,
        all pre-split data is adjusted to post-split basis for consistent visualization.

        Args:
            years: List of years (e.g., ['2019', '2020', '2021', '2022', '2023', '2024'])
            share_counts: List of share counts matching years (actual reported values)
            title: Chart title
            split_year: Year when stock split occurred (e.g., 2021 for 4:1 split in 2021)
            split_ratio: Split ratio (e.g., 4.0 for 4:1 split, 1.0 if no split)

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        # Normalize for stock split - adjust pre-split shares to post-split basis
        normalized_shares = []
        split_occurred = split_year is not None and split_ratio > 1.0

        for i, year in enumerate(years):
            year_int = int(year)
            if split_occurred and year_int < split_year:
                # Adjust pre-split shares upward by split ratio
                normalized_shares.append(share_counts[i] * split_ratio)
            else:
                normalized_shares.append(share_counts[i])

        # Convert to millions for display
        shares_millions = [s / 1e6 for s in normalized_shares]

        ax.plot(years, shares_millions, color='#E53935', linewidth=2.5, marker='o', markersize=6)

        # Add stock split annotation if applicable
        if split_occurred:
            split_idx = next((i for i, y in enumerate(years) if int(y) >= split_year), None)
            if split_idx is not None and split_idx < len(years):
                ax.axvline(x=split_idx - 0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
                ax.annotate(f'{int(split_ratio)}:1 Stock Split',
                           xy=(split_idx - 0.5, max(shares_millions) * 0.9),
                           xytext=(split_idx, max(shares_millions) * 0.95),
                           fontsize=10, color='gray', ha='center',
                           arrowprops=dict(arrowstyle='->', color='gray', lw=1))

        # Add data labels (skip extreme values for cleaner display)
        for i, (year, value) in enumerate(zip(years, shares_millions)):
            if i == 0 or i == len(years) - 1 or len(shares_millions) <= 6:
                ax.text(i, value + max(shares_millions) * 0.02,
                       f'{value:.0f}M', ha='center', va='bottom',
                       fontsize=9, color='#E53935', fontweight='bold')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Fiscal Year', fontsize=12)
        ax.set_ylabel('Share Count (Millions)', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set reasonable y-axis limits to prevent extreme aspect ratios
        y_min = min(shares_millions) * 0.95
        y_max = max(shares_millions) * 1.05
        ax.set_ylim(y_min, y_max)

        plt.tight_layout()
        output_path = self.output_dir / CHART_SHARE_COUNT_TREND
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def dividend_growth(
        self,
        years: List[str],
        dividends: List[float],
        title: str = "Dividend Per Share Growth (Last 10 Years)"
    ) -> str:
        """
        Chart 7: Dividend Growth Trend (Bar Chart)

        Args:
            years: List of years
            dividends: List of dividend per share values in dollars
            title: Chart title

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(years, dividends, color='#1E88E5', width=0.7)

        for i, v in enumerate(dividends):
            ax.text(i, v + max(dividends) * 0.02, f'${v:.2f}',
                   ha='center', va='bottom', fontsize=9, color='#1E88E5', fontweight='bold')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Fiscal Year', fontsize=12)
        ax.set_ylabel('Dividend Per Share ($)', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / CHART_DIVIDEND_GROWTH
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def capital_allocation_breakdown(
        self,
        years: List[str],
        dividends: List[float],
        repurchases: List[float],
        title: Optional[str] = None
    ) -> str:
        """
        Chart 10: Capital Allocation Breakdown (Stacked Bar Chart)

        Args:
            years: List of years (typically last 5 years)
            dividends: List of dividend amounts in billions
            repurchases: List of share repurchase amounts in billions
            title: Chart title (auto-generated if None)

        Returns:
            Path to saved chart image
        """
        if title is None:
            title = f"Capital Allocation Breakdown ({years[0]}-{years[-1]})"

        fig, ax = plt.subplots(figsize=(10, 6))

        dividends_arr = np.array(dividends)
        repurchases_arr = np.array(repurchases)

        bars1 = ax.bar(years, dividends_arr, label='Dividends', color='#42A5F5', width=0.6)
        bars2 = ax.bar(years, repurchases_arr, bottom=dividends_arr,
                      label='Share Repurchases', color='#66BB6A', width=0.6)

        # Add data labels
        for i in range(len(years)):
            ax.text(i, dividends_arr[i]/2, f'${dividends_arr[i]:.1f}B',
                   ha='center', va='center', fontsize=9, color='white', fontweight='bold')
            ax.text(i, dividends_arr[i] + repurchases_arr[i]/2,
                   f'${repurchases_arr[i]:.1f}B', ha='center', va='center',
                   fontsize=9, color='white', fontweight='bold')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Fiscal Year', fontsize=12)
        ax.set_ylabel('Amount ($ Billions)', fontsize=12)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / CHART_CAPITAL_ALLOCATION_BREAKDOWN
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def revenue_trend(
        self,
        years: List[str],
        revenues: List[float],
        title: str = "Revenue Trend"
    ) -> str:
        """
        Generate revenue trend line chart.

        Args:
            years: List of years
            revenues: List of revenue values in billions
            title: Chart title

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(years, revenues, color='#43A047', linewidth=2.5, marker='o', markersize=6)

        for i, (year, value) in enumerate(zip(years, revenues)):
            ax.text(i, value + max(revenues) * 0.01, f'${value:.1f}B',
                   ha='center', va='bottom', fontsize=9, color='#43A047', fontweight='bold')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Fiscal Year', fontsize=12)
        ax.set_ylabel('Revenue ($ Billions)', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output_path = self.output_dir / 'revenue_trend.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def revenue_segment_breakdown(
        self,
        segments: List[str],
        values: List[float],
        title: str = "Revenue by Segment"
    ) -> str:
        """
        Generate revenue segment breakdown pie or bar chart.

        Args:
            segments: List of segment names
            values: List of revenue values
            title: Chart title

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#42A5F5', '#66BB6A', '#FFA726', '#AB47BC', '#EF5350',
                 '#26C6DA', '#D4E157', '#FF7043']

        wedges, texts, autotexts = ax.pie(
            values, labels=segments, autopct='%1.1f%%',
            colors=colors[:len(segments)], startangle=90
        )

        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
            autotext.set_color('white')

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        output_path = self.output_dir / 'revenue_segment_breakdown.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)

    def profit_margins(
        self,
        years: List[str],
        gross_margins: List[float],
        operating_margins: List[float],
        net_margins: List[float],
        title: str = "Profit Margins Trend"
    ) -> str:
        """
        Generate profit margins trend line chart.

        Args:
            years: List of years
            gross_margins: List of gross margin percentages
            operating_margins: List of operating margin percentages
            net_margins: List of net margin percentages
            title: Chart title

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(years, gross_margins, label='Gross Margin', color='#43A047',
               linewidth=2.5, marker='o', markersize=5)
        ax.plot(years, operating_margins, label='Operating Margin', color='#1E88E5',
               linewidth=2.5, marker='s', markersize=5)
        ax.plot(years, net_margins, label='Net Margin', color='#E53935',
               linewidth=2.5, marker='^', markersize=5)

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Fiscal Year', fontsize=12)
        ax.set_ylabel('Margin (%)', fontsize=12)
        ax.legend(loc='lower left')
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add percentage y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

        plt.tight_layout()
        output_path = self.output_dir / 'profit_margins.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        return str(output_path)


def main():
    """Example usage of ChartGenerator."""
    generator = ChartGenerator()

    # Example: Share count trend
    generator.share_count_trend(
        years=['2019', '2020', '2021', '2022', '2023', '2024'],
        share_counts=[1000000000, 980000000, 960000000, 950000000, 940000000, 930000000]
    )

    print("Example chart generated in generated_images/ directory")


if __name__ == "__main__":
    main()
