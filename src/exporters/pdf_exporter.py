"""
PDF експортер для звітів аналізу диску
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors


def export_to_pdf(data, output_file):
    """
    Експортувати дані аналізу в PDF формат

    Args:
        data: Словник з даними аналізу
        output_file: Шлях до вихідного PDF файлу
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = data.get('title', 'Disk Analysis Report')
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 0.5*inch))

    # Summary section
    if 'summary' in data:
        story.append(Paragraph('Summary', styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))

        for key, value in data['summary'].items():
            text = f"<b>{key}:</b> {value}"
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

        story.append(Spacer(1, 0.3*inch))

    # Usage section
    if 'usage' in data:
        story.append(Paragraph('Disk Usage', styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))

        usage = data['usage']
        usage_data = [
            ['Metric', 'Value'],
            ['Total', f"{usage.get('total', 0)} bytes"],
            ['Used', f"{usage.get('used', 0)} bytes"],
            ['Free', f"{usage.get('free', 0)} bytes"]
        ]

        usage_table = Table(usage_data)
        usage_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(usage_table)
        story.append(Spacer(1, 0.3*inch))

    # Largest files section
    if 'largest_files' in data:
        story.append(Paragraph('Largest Files', styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))

        files_data = [['Path', 'Size (bytes)']]
        for file_info in data['largest_files']:
            files_data.append([
                file_info.get('path', ''),
                str(file_info.get('size', 0))
            ])

        files_table = Table(files_data)
        files_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(files_table)

    # Build PDF
    doc.build(story)
