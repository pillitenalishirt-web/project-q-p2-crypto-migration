
from pathlib import Path
from html import escape
import textwrap


def bar_chart_svg(values, title, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1000, 500
    left, right, top, bottom = 90, 35, 65, 145
    plot_width = width - left - right
    plot_height = height - top - bottom
    maximum = max([float(value) for _, value in values] + [1.0])
    spacing = 24
    bar_width = (plot_width - spacing * (len(values) - 1)) / max(1, len(values))
    baseline = top + plot_height
    elements = []

    for index, (label, value) in enumerate(values):
        numeric_value = float(value)
        bar_height = numeric_value / maximum * (plot_height - 30)
        x = left + index * (bar_width + spacing)
        y = baseline - bar_height
        center = x + bar_width / 2

        elements.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" '
            f'height="{bar_height:.2f}" fill="#4178be" rx="3"/>'
        )
        elements.append(
            f'<text x="{center:.2f}" y="{y - 10:.2f}" '
            f'text-anchor="middle" font-size="13" fill="#222">'
            f'{escape(f"{numeric_value:,.4g}")}</text>'
        )

        lines = textwrap.wrap(str(label), width=20, break_long_words=False)
        label_start_y = baseline + 25

        elements.append(
            f'<text x="{center:.2f}" y="{label_start_y}" '
            f'text-anchor="middle" font-size="12" fill="#222">'
        )

        for line_index, line in enumerate(lines):
            dy = 0 if line_index == 0 else 15
            elements.append(
                f'<tspan x="{center:.2f}" dy="{dy}">'
                f'{escape(line)}</tspan>'
            )

        elements.append('</text>')

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="32" text-anchor="middle" '
        f'font-size="19" font-weight="bold" fill="#222">'
        f'{escape(title)}</text>',
        f'<line x1="{left}" y1="{baseline}" x2="{width - right}" '
        f'y2="{baseline}" stroke="#333"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" '
        f'y2="{baseline}" stroke="#333"/>',
        *elements,
        '</svg>',
    ]

    path.write_text('\n'.join(svg), encoding='utf-8')
    return str(path)
