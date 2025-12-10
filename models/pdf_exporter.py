from datetime import datetime
from typing import Dict, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import sys

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу для работы в exe и разработке"""
    try:
        # PyInstaller создает временную папку в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

class PDFExporter:
    """Класс для экспорта результатов в PDF"""

    def __init__(self):
        self.font_name = 'Helvetica'
        self.font_bold = 'Helvetica-Bold'
        self._setup_fonts()

    def _setup_fonts(self):
        """Настройка шрифтов с правильными путями"""
        try:
            # Получаем базовый путь
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            font_dir = os.path.join(base_path, 'assets', 'fonts')

            regular_path = os.path.join(font_dir, 'Roboto-Regular.ttf')
            bold_path = os.path.join(font_dir, 'Roboto-Bold.ttf')

            print(f"PDF Exporter ищет шрифты в: {font_dir}")
            print(f"Regular: {regular_path}")
            print(f"Bold: {bold_path}")

            if os.path.isfile(regular_path) and os.path.isfile(bold_path):
                pdfmetrics.registerFont(TTFont('RobotoRegular', regular_path))
                pdfmetrics.registerFont(TTFont('RobotoBold', bold_path))
                self.font_name = 'RobotoRegular'
                self.font_bold = 'RobotoBold'
                print("✓ PDF шрифты загружены")
            else:
                print(f"✗ Шрифты для PDF не найдены. Используется Helvetica.")
                self.font_name = 'Helvetica'
                self.font_bold = 'Helvetica-Bold'

        except Exception as e:
            print(f"Ошибка загрузки PDF шрифтов: {e}")
            self.font_name = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'

    def export_results(self, filename: str, model_name: str, doctor_name: str,
                       input_values: Dict[str, Tuple[str, float]],
                       z_value: float, p_value: float,
                       conclusion: str, formula: str):
        """Экспорт результатов в PDF"""
        try:
            doc = SimpleDocTemplate(
                filename,
                pagesize=A4,
                rightMargin=20 * mm,
                leftMargin=20 * mm,
                topMargin=20 * mm,
                bottomMargin=20 * mm
            )
            story = []
            styles = getSampleStyleSheet()

            # === Стили с поддержкой Roboto / fallback на Helvetica ===
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=self.font_bold,
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                alignment=1  # центрирование
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontName=self.font_bold,
                fontSize=14,
                textColor=colors.HexColor('#4a90e2'),
                spaceAfter=6,
                spaceBefore=12
            )

            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=11,
                textColor=colors.HexColor('#2c3e50')
            )

            # === Заголовок ===
            story.append(Paragraph("Результаты медицинской диагностики", title_style))
            story.append(Spacer(1, 10 * mm))

            # === Основная информация ===
            story.append(Paragraph(f"<b>Модель диагностики:</b> {model_name}", normal_style))
            story.append(Spacer(1, 3 * mm))

            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            story.append(Paragraph(f"<b>Дата и время:</b> {current_time}", normal_style))
            story.append(Spacer(1, 3 * mm))

            if doctor_name:
                story.append(Paragraph(f"<b>Врач:</b> {doctor_name}", normal_style))
                story.append(Spacer(1, 3 * mm))

            story.append(Spacer(1, 5 * mm))

            # === Входные параметры (таблица) ===
            story.append(Paragraph("Входные параметры:", heading_style))
            table_data = [["Параметр", "Значение"]]
            for label, value in input_values.values():
                table_data.append([label, f"{value:.4f}"])

            table = Table(table_data, colWidths=[120 * mm, 50 * mm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), self.font_bold),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTNAME', (0, 1), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            story.append(table)
            story.append(Spacer(1, 8 * mm))

            story.append(Paragraph("Формула расчета:", heading_style))
            story.append(Paragraph(formula, normal_style))
            story.append(Spacer(1, 8 * mm))

            story.append(Paragraph("Результаты расчета:", heading_style))
            result_data = [
                ["Показатель", "Значение"],
                ["z-значение", f"{z_value:.4f}"],
                ["Вероятность (p)", f"{p_value:.4f} ({p_value*100:.2f}%)"]
            ]
            result_table = Table(result_data, colWidths=[120 * mm, 50 * mm])
            result_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), self.font_bold),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTNAME', (0, 1), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0'))
            ]))
            story.append(result_table)
            story.append(Spacer(1, 8 * mm))

            story.append(Paragraph("Заключение:", heading_style))
            is_high_risk = "высок" in conclusion.lower() or "диагностируется" in conclusion.lower()
            conclusion_color = colors.HexColor('#e74c3c') if is_high_risk else colors.HexColor('#27ae60')
            conclusion_style = ParagraphStyle(
                'Conclusion',
                parent=normal_style,
                fontSize=12,
                textColor=conclusion_color,
                spaceAfter=6
            )
            story.append(Paragraph(f"<b>{conclusion}</b>", conclusion_style))
            story.append(Spacer(1, 8 * mm))

            if doctor_name:
                story.append(Spacer(1, 15 * mm))
                story.append(Paragraph(f"____________________ {doctor_name}", normal_style))

            doc.build(story)

        except Exception as e:
            raise