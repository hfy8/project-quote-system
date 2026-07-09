#!/usr/bin/env python3
"""
项目报价系统操作手册 - Markdown → PDF 生成器

使用 reportlab + wqy-zenhei 中文字体
"""
import sys
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

CJK_FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

def register_font():
    pdfmetrics.registerFont(TTFont('WQY', CJK_FONT))
    pdfmetrics.registerFont(TTFont('WQY-Bold', CJK_FONT))

def parse_inline(text, base_font='WQY'):
    """处理行内格式: **bold** / `code` / ![alt](path)"""
    # 图片 ![alt](path)
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    parts = []
    last_end = 0
    for m in img_pattern.finditer(text):
        if m.start() > last_end:
            parts.append(('text', text[last_end:m.start()]))
        parts.append(('img', m.group(2), m.group(1)))
        last_end = m.end()
    if last_end < len(text):
        parts.append(('text', text[last_end:]))

    # 处理每个 text 段的 bold / code
    result = []
    for part in parts:
        if part[0] == 'img':
            result.append(part)
        else:
            text = part[1]
            # 先处理 code (`...`)
            code_pattern = re.compile(r'`([^`]+)`')
            code_parts = []
            last_end = 0
            for m in code_pattern.finditer(text):
                if m.start() > last_end:
                    code_parts.append(('text', text[last_end:m.start()]))
                code_parts.append(('code', m.group(1)))
                last_end = m.end()
            if last_end < len(text):
                code_parts.append(('text', text[last_end:]))

            # 再处理 bold (**...**)
            for cp in code_parts:
                if cp[0] == 'code':
                    result.append(('code', cp[1]))
                else:
                    text2 = cp[1]
                    bold_pattern = re.compile(r'\*\*([^*]+)\*\*')
                    last_end = 0
                    for m in bold_pattern.finditer(text2):
                        if m.start() > last_end:
                            result.append(('text', text2[last_end:m.start()]))
                        result.append(('bold', m.group(1)))
                        last_end = m.end()
                    if last_end < len(text2):
                        result.append(('text', text2[last_end:]))
    return result

def render_inline(text, styles, base_size=10):
    """渲染行内格式为 Paragraph XML"""
    parts = parse_inline(text)
    xml_parts = []
    for part in parts:
        if part[0] == 'img':
            xml_parts.append(f'<font color="blue">[图片: {part[1]}]</font>')
        elif part[0] == 'bold':
            xml_parts.append(f'<b>{part[1]}</b>')
        elif part[0] == 'code':
            xml_parts.append(f'<font face="Courier" color="#d6336c">{part[1]}</font>')
        else:
            xml_parts.append(part[1].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    return ''.join(xml_parts)

def md_to_pdf(md_path, pdf_path, title='项目报价系统操作手册'):
    register_font()

    # 读取 markdown
    md_text = Path(md_path).read_text(encoding='utf-8')

    # 样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontName='WQY', fontSize=22, leading=28,
                                  textColor=HexColor('#0d9488'), alignment=TA_LEFT,
                                  spaceAfter=20)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
                              fontName='WQY-Bold', fontSize=18, leading=24,
                              textColor=HexColor('#0d9488'),
                              spaceBefore=20, spaceAfter=10,
                              pageBreakBefore=True)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                              fontName='WQY-Bold', fontSize=14, leading=20,
                              textColor=HexColor('#0f766e'),
                              spaceBefore=14, spaceAfter=8)
    h3_style = ParagraphStyle('H3', parent=styles['Heading3'],
                              fontName='WQY-Bold', fontSize=12, leading=16,
                              textColor=HexColor('#115e59'),
                              spaceBefore=10, spaceAfter=6)
    h4_style = ParagraphStyle('H4', parent=styles['Heading4'],
                              fontName='WQY-Bold', fontSize=11, leading=14,
                              textColor=HexColor('#134e4a'),
                              spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontName='WQY', fontSize=10, leading=14,
                                 spaceAfter=6, alignment=TA_LEFT)
    code_style = ParagraphStyle('Code', parent=styles['Code'],
                                 fontName='Courier', fontSize=8, leading=10,
                                 backColor=HexColor('#f1f5f9'),
                                 borderPadding=4, leftIndent=8,
                                 spaceAfter=8)

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm,
                            title=title, author='Hermes Agent')

    elements = []

    # 处理 markdown 行
    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_buffer = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 代码块
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_buffer = []
            else:
                in_code_block = False
                if code_buffer:
                    code_text = '\n'.join(code_buffer)
                    elements.append(Preformatted(code_text, code_style))
            i += 1
            continue
        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # 标题
        if stripped.startswith('# '):
            text = stripped[2:].strip()
            elements.append(Paragraph(text, title_style))
            i += 1
            continue
        if stripped.startswith('## '):
            text = stripped[3:].strip()
            # 跳过第一个 H2 (目录), 后续都加分页
            if len([e for e in elements if isinstance(e, Paragraph)]) > 0:
                elements.append(PageBreak())
            elements.append(Paragraph(text, h1_style))
            i += 1
            continue
        if stripped.startswith('### '):
            text = stripped[4:].strip()
            elements.append(Paragraph(text, h2_style))
            i += 1
            continue
        if stripped.startswith('#### '):
            text = stripped[5:].strip()
            elements.append(Paragraph(text, h3_style))
            i += 1
            continue

        # 水平线
        if stripped == '---':
            elements.append(Spacer(1, 8))
            i += 1
            continue

        # 表格
        if '|' in stripped and i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|', lines[i+1]):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            if len(table_lines) >= 2:
                # 解析表格
                rows = []
                for tl in table_lines:
                    if re.match(r'^\s*\|[\s\-:|]+\|', tl):
                        continue
                    cells = [c.strip() for c in tl.strip('|').split('|')]
                    rows.append(cells)
                if rows:
                    col_count = max(len(r) for r in rows)
                    # 补齐
                    for r in rows:
                        while len(r) < col_count:
                            r.append('')
                    # 创建 Table
                    data = []
                    for r_idx, row in enumerate(rows):
                        row_data = []
                        for cell in row:
                            inline_xml = render_inline(cell, styles)
                            row_data.append(Paragraph(inline_xml, body_style))
                        data.append(row_data)
                    col_widths = [165 * col_count / col_count * mm / col_count] * col_count
                    # 计算列宽
                    avail_width = 180 * mm
                    col_widths = [avail_width / col_count] * col_count
                    table = Table(data, colWidths=col_widths, repeatRows=1)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0d9488')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), white),
                        ('FONTNAME', (0, 0), (-1, 0), 'WQY-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e1')),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8fafc')]),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                        ('LEFTPADDING', (0, 0), (-1, -1), 4),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 6))
            continue

        # 图片
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            img_path = img_match.group(2)
            # 处理相对路径
            md_dir = Path(md_path).parent
            full_path = md_dir / img_path
            if full_path.exists():
                try:
                    img = Image(str(full_path), width=160*mm, height=90*mm,
                                kind='proportional')
                    elements.append(img)
                    elements.append(Spacer(1, 4))
                except Exception as e:
                    elements.append(Paragraph(f'[图片加载失败: {img_path}]', body_style))
            else:
                elements.append(Paragraph(f'[图片不存在: {full_path}]', body_style))
            i += 1
            continue

        # 列表
        if stripped.startswith('- ') or stripped.startswith('* '):
            content = stripped[2:]
            inline_xml = render_inline(content, styles)
            elements.append(Paragraph(f'• {inline_xml}', body_style))
            i += 1
            continue
        if re.match(r'^\d+\.\s', stripped):
            m = re.match(r'^(\d+)\.\s(.*)$', stripped)
            num, content = m.group(1), m.group(2)
            inline_xml = render_inline(content, styles)
            elements.append(Paragraph(f'{num}. {inline_xml}', body_style))
            i += 1
            continue

        # 普通段落
        if stripped:
            inline_xml = render_inline(stripped, styles)
            elements.append(Paragraph(inline_xml, body_style))

        i += 1

    doc.build(elements)
    print(f"✅ PDF 已生成: {pdf_path}")

if __name__ == '__main__':
    md_to_pdf(
        '/home/rs8568/project-quote-system/docs/OPERATION_MANUAL.md',
        '/home/rs8568/project-quote-system/docs/项目报价系统操作手册.pdf',
        title='项目报价系统 — 操作手册'
    )