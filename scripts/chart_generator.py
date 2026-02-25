#!/usr/bin/env python3
"""
Financial Chart Generator for Investment Reports
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import os

class ChartGenerator:
    def __init__(self, output_dir='generated_images'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Set style
        plt.style.use('default')
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['figure.dpi'] = 300

    def investment_trend(self, years, investments, title):
        """Create investment trend chart"""
        fig, ax = plt.subplots(figsize=(10, 6))

        colors = ['#2E86AB' if x >= 0 else '#E63946' for x in investments]
        bars = ax.bar(years, investments, color=colors, edgecolor='black', linewidth=0.5)

        # Add value labels
        for bar, value in zip(bars, investments):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${value:,.0f}M',
                   ha='center', va='bottom' if height >= 0 else 'top',
                   fontsize=9)

        ax.set_xlabel('Fiscal Year')
        ax.set_ylabel('Amount (USD Millions)')
        ax.set_title(title, fontweight='bold', pad=15)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.axhline(y=0, color='black', linewidth=0.8)

        # Add horizontal line for average
        avg = sum(investments) / len(investments)
        ax.axhline(y=avg, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.text(0.02, 0.98, f'Avg: ${avg:,.0f}M', transform=ax.transAxes,
               verticalalignment='top', fontsize=8, style='italic',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        plt.tight_layout()
        filename = title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        filepath = os.path.join(self.output_dir, f'{filename}.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Saved: {filepath}')

    def investment_type_breakdown(self, types, values, title):
        """Create investment type breakdown chart"""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Use different colors for positive vs negative
        colors = []
        for v in values:
            if v < 0:
                colors.append('#E63946')  # Red for outflows
            else:
                colors.append('#2E86AB')  # Blue for inflows

        bars = ax.barh(types, values, color=colors, edgecolor='black', linewidth=0.5)

        # Add value labels
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'${abs(value):,.0f}M',
                   ha='left' if width >= 0 else 'right',
                   va='center', fontsize=9)

        ax.set_xlabel('Amount (USD Millions)')
        ax.set_title(title, fontweight='bold', pad=15)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.axvline(x=0, color='black', linewidth=0.8)

        plt.tight_layout()
        filename = title.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        filepath = os.path.join(self.output_dir, f'{filename}.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Saved: {filepath}')
