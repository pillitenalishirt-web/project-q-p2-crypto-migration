from pathlib import Path


def bar_chart_svg(values, title, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 820, 430
    left, right, top, bottom = 90, 35, 65, 85
    plot_width = width - left - right
    plot_height = height - top - bottom
    maximum = max([float(v) for _, v in values] + [1.0])
    bars = []
    spacing = 16
    bar_width = max(18, (plot_width - spacing * (len(values) - 1)) / max(1, len(values)))
    for index, (label, value) in enumerate(values):
        bar_height = (float(value) / maximum) * (plot_height - 25)
        x = left + index * (bar_width + spacing)
        y = top + plot_height - bar_height
        bars.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" fill="#4178be"/>')
        bars.append(f'<text x="{x + bar_width/2:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-size="12">{float(value):.4g}</text>')
        bars.append(f'<text x="{x + bar_width/2:.2f}" y="{top + plot_height + 24}" text-anchor="middle" font-size="11">{label}</text>')
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="{width/2}" y="32" text-anchor="middle" font-size="19" font-weight="bold">{title}</text>', f'<line x1="{left}" y1="{top+plot_height}" x2="{width-right}" y2="{top+plot_height}" stroke="#333"/>', f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_height}" stroke="#333"/>'] + bars + ['</svg>']
    path.write_text('\n'.join(svg), encoding='utf-8')
    return str(path)
