#!/usr/bin/env python3
"""
Asset Composition Pie Chart Generator
Creates a pie chart showing various asset types composition
"""

import matplotlib.pyplot as plt
import os


def generate_asset_composition_chart(asset_data, year, output_dir='generated_images'):
    """
    Generate asset composition pie chart

    Args:
        asset_data: dict with asset names as keys and percentages/values as values
            Example: {'Current Assets': 45, 'Non-current Assets': 55}
        year: str, the fiscal year for the chart title
        output_dir: str, directory to save the chart
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract data
    segments = list(asset_data.keys())
    percentages = list(asset_data.values())

    # Color palette
    color_palette = ['#1E88E5', '#43A047', '#FF9800', '#7B1FA2', '#E91E63',
                    '#00BCD4', '#FFC107', '#8BC34A', '#9C27B0', '#607D8B']
    colors = color_palette[:len(segments)]

    # Explode the largest segment for emphasis
    explode = [0.08 if p == max(percentages) else 0.03 for p in percentages]

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(percentages, explode=explode, labels=segments, colors=colors,
                                       autopct='%1.0f%%', pctdistance=0.85,
                                       textprops={'fontsize': 11, 'fontweight': 'bold'},
                                       startangle=90, counterclock=False)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax.set_title(f'Asset Composition ({year})', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/asset_composition.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ Chart saved: {output_dir}/asset_composition.png")


if __name__ == '__main__':
    # Example usage
    example_data = {
        'Current Assets': 35,
        'Non-current Assets': 65
    }
    generate_asset_composition_chart(example_data, '2024')
