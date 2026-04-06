"""
HTML експортер для звітів аналізу диску
"""

from typing import Dict, Any


def export_to_html(data: Dict[str, Any], output_file: str) -> None:
    """
    Експортувати дані у HTML файл

    Args:
        data: Словник з даними для експорту
        output_file: Шлях до вихідного HTML файлу

    Returns:
        None
    """
    # Отримуємо дані
    title = data.get('title', 'Disk Analysis Report')
    directory = data.get('directory', '')
    summary = data.get('summary', {})

    # Генеруємо HTML
    html_content = f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .info {{
            margin: 20px 0;
        }}
        .info-item {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
"""

    if directory:
        html_content += f"""        <div class="info">
            <div class="info-item">
                <strong>Directory:</strong> {directory}
            </div>
        </div>
"""

    if summary:
        html_content += """        <div class="info">
            <h2>Summary</h2>
"""
        for key, value in summary.items():
            html_content += f"""            <div class="info-item">
                <strong>{key}:</strong> {value}
            </div>
"""
        html_content += """        </div>
"""

    html_content += """    </div>
</body>
</html>"""

    # Записуємо у файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
