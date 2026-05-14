"""导出功能模块 - 支持 Word/Excel/PDF 格式"""
from flask import Blueprint, send_file, jsonify, request
from io import BytesIO
from datetime import datetime

# Word 导出
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Excel 导出
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# PDF 导出 - 使用 fpdf2 支持中文
from fpdf import FPDF

# 中文字体路径
FONT_REGULAR = '/mnt/c/Windows/Fonts/simhei.ttf'  # 黑体（支持中文）
FONT_BOLD = '/mnt/c/Windows/Fonts/simhei.ttf'      # 黑体（暂无粗体，用黑体代替）

from app.models.quotation import Quotation
from app.models.module import Module
from app.models.material import ModuleMaterial, Material
from app.models.fee import OtherFee
from app.models.fee_rate import FeeRate
from app.models.exchange_rate import ExchangeRate
from app.models.version import VersionSnapshot
from app.models.user import User

export_bp = Blueprint('exports', __name__)


def get_quotation_with_details(quotation_id):
    """获取报价单及其详细信息"""
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return None
    
    # 获取模块及物料
    modules = Module.query.filter_by(quotation_id=quotation_id).all()
    for module in modules:
        module.materials = ModuleMaterial.query.filter_by(module_id=module.id).all()
    
    # 获取其他费用
    fees = OtherFee.query.filter_by(quotation_id=quotation_id).all()
    
    return quotation, modules, fees


def calculate_totals_with_rates(quotation, modules, fees):
    """计算汇总数据（含费用系数和税率）"""
    # 分类统计物料
    category_totals = {'large': 0, 'standard': 0, 'other': 0}
    for module in modules:
        for mm in module.materials:
            if mm.material:
                cat = mm.material.category or 'standard'
                amount = float(mm.material.unit_price or 0) * mm.quantity
                category_totals[cat] = category_totals.get(cat, 0) + amount
    
    # 获取费用系数
    fee_rates = {fr.category: float(fr.rate) for fr in FeeRate.query.all()}
    rate_large = fee_rates.get('large', 1.0)
    rate_standard = fee_rates.get('standard', 1.0)
    rate_other = fee_rates.get('other', 1.0)
    
    # 计算物料含系数小计
    material_with_rates = (
        category_totals.get('large', 0) * rate_large +
        category_totals.get('standard', 0) * rate_standard +
        category_totals.get('other', 0) * rate_other
    )
    
    material_total = sum(category_totals.values())
    fees_total = sum(float(fee.amount or 0) for fee in fees)
    subtotal = material_with_rates + fees_total
    
    # 获取税率
    tax_rate = float(quotation.tax_rate) if quotation.tax_rate else 0.13
    tax_amount = subtotal * tax_rate
    grand_total = subtotal + tax_amount
    
    return {
        'material_total': material_total,
        'material_total_with_rates': material_with_rates,
        'fees_total': fees_total,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'category_totals': category_totals,
        'fee_rates': fee_rates
    }


def convert_currency(amount, to_currency, exchange_rates):
    """汇率转换"""
    if to_currency == 'CNY':
        return amount
    # rate 是 "1 目标货币 = X CNY"
    rate = exchange_rates.get(to_currency, 1)
    return amount / rate


def get_currency_symbol(currency):
    """获取币种符号"""
    symbols = {'CNY': '¥', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
    return symbols.get(currency, '¥')


def generate_version_files(quotation_id, version_no, snapshot_data, data=None):
    """为版本生成Word和PDF文件，返回文件路径字典"""
    import os
    import json
    
    # 创建版本文件存储目录
    base_dir = f'/mnt/c/Users/rs8568/Desktop/Project/project-quote-system/backend/versions/{quotation_id}'
    os.makedirs(base_dir, exist_ok=True)
    
    word_path = os.path.join(base_dir, f'v{version_no}.docx')
    pdf_path = os.path.join(base_dir, f'v{version_no}.pdf')
    
    # 获取报价单信息（包含币种）
    quotation = Quotation.query.get(quotation_id)
    
    if data is None:
        data = json.loads(snapshot_data) if isinstance(snapshot_data, str) else snapshot_data
    
    # 填充物料详细信息（与 get_version_snapshot_data 相同逻辑）
    for module in data.get('modules', []):
        for mm in module.get('materials', []):
            mat = Material.query.get(mm.get('material_id'))
            if mat:
                mm['name'] = mat.name or ''
                mm['brand'] = mat.brand or ''
                mm['spec'] = mat.spec or ''
                mm['unit_price'] = float(mat.unit_price or 0)
                mm['category'] = mat.category or 'standard'
    
    # 计算汇总
    totals = calculate_version_totals(data)
    
    # 生成 Word 文件
    _generate_version_word(word_path, quotation_id, version_no, data, totals, quotation)
    
    # 生成 PDF 文件
    _generate_version_pdf(pdf_path, quotation_id, version_no, data, totals, quotation)
    
    return {'word': word_path, 'pdf': pdf_path}


def _generate_version_word(word_path, quotation_id, version_no, data, totals, quotation=None):
    """生成版本 Word 文件"""
    doc = Document()
    title = doc.add_heading(f'{data.get("name", "报价单")}', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 基本信息
    doc.add_heading('基本信息', level=1)
    info_table = doc.add_table(rows=5, cols=2)
    info_table.style = 'Table Grid'
    business_owner_name = ''
    if data.get('business_owner_id'):
        owner = User.query.get(data.get('business_owner_id'))
        if owner:
            business_owner_name = owner.real_name
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    info_data = [
        ('项目名称', data.get('name', '')),
        ('方案编号', data.get('scheme_no', '')),
        ('业务负责人', business_owner_name),
        ('版本号', f'v{version_no}'),
        ('报价币种', currency)
    ]
    for i, (key, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = key
        info_table.rows[i].cells[1].text = str(value)
    
    doc.add_paragraph()
    
    # 整合表格
    doc.add_heading('物料及费用清单', level=1)
    
    module_groups = []
    for module in data.get('modules', []):
        items = []
        module_total = 0
        for mm in module.get('materials', []):
            item_total = float(mm.get('unit_price', 0) or 0) * float(mm.get('quantity', 0) or 0)
            module_total += item_total
            items.append({
                'item': mm.get('name', ''),
                'spec': mm.get('spec', ''),
                'category': mm.get('brand', ''),
                'unit_price': f'¥{float(mm.get("unit_price", 0) or 0):.2f}',
                'quantity': str(mm.get('quantity', 0)),
                'subtotal': f'¥{item_total:.2f}',
            })
        module_groups.append({
            'name': module.get('name', '未命名模块'),
            'items': items,
            'total': module_total
        })
    
    fees_total = sum(float(f.get('amount', 0)) for f in data.get('fees', []))
    fee_items = []
    for fee in data.get('fees', []):
        location_text = '厂内' if fee.get('location') == 'internal' else ('厂外' if fee.get('location') == 'external' else '')
        fee_items.append({
            'item': fee.get('fee_type', '') or fee.get('name', ''),
            'spec': location_text,
            'category': fee.get('fee_type', '') or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f'¥{float(fee.get("amount", 0)):.2f}',
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    if module_groups:
        combined_table = doc.add_table(rows=1, cols=8)
        combined_table.style = 'Table Grid'
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        for j, header in enumerate(headers):
            combined_table.rows[0].cells[j].text = header
        
        for group in module_groups:
            if not group['items']:
                row = combined_table.add_row()
                row.cells[0].text = group['name']
                row.cells[1].text = '（无物料）'
                continue
            
            first_row = combined_table.add_row()
            first_row.cells[0].text = group['name']
            first_row.cells[1].text = group['items'][0]['item']
            first_row.cells[2].text = group['items'][0]['spec']
            first_row.cells[3].text = group['items'][0]['category']
            first_row.cells[4].text = group['items'][0]['unit_price']
            first_row.cells[5].text = group['items'][0]['quantity']
            first_row.cells[6].text = group['items'][0]['subtotal']
            first_row.cells[7].text = f'¥{group["total"]:.2f}'
            
            if len(group['items']) > 1:
                module_cell = first_row.cells[0]
                for i in range(1, len(group['items'])):
                    next_row = combined_table.add_row()
                    next_row.cells[1].text = group['items'][i]['item']
                    next_row.cells[2].text = group['items'][i]['spec']
                    next_row.cells[3].text = group['items'][i]['category']
                    next_row.cells[4].text = group['items'][i]['unit_price']
                    next_row.cells[5].text = group['items'][i]['quantity']
                    next_row.cells[6].text = group['items'][i]['subtotal']
                    module_cell = module_cell.merge(next_row.cells[0])
                
                total_cell = first_row.cells[7]
                for i in range(1, len(group['items'])):
                    next_row_idx = len(combined_table.rows) - 1
                    total_cell = total_cell.merge(combined_table.rows[next_row_idx].cells[7])
    else:
        doc.add_paragraph('无物料及费用数据')
    
    doc.add_paragraph()
    
    # 汇总信息
    doc.add_heading('报价汇总', level=1)
    summary_table = doc.add_table(rows=7, cols=2)
    summary_table.style = 'Table Grid'
    summary_data = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
        (f'最终报价(CNY)', f'¥{totals["grand_total"]:.2f}')
    ]
    for i, (key, value) in enumerate(summary_data):
        summary_table.rows[i].cells[0].text = key
        summary_table.rows[i].cells[1].text = value
    
    doc.save(word_path)


def _generate_version_pdf(pdf_path, quotation_id, version_no, data, totals, quotation=None):
    """生成版本 PDF 文件（复用报价单PDF逻辑）"""
    # 获取币种和汇率
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    # 收集分组数据
    module_groups = []
    for module in data.get('modules', []):
        items = []
        module_total = 0
        for mm in module.get('materials', []):
            mat = Material.query.get(mm.get('material_id'))
            if mat:
                item_total = float(mat.unit_price or 0) * mm.get('quantity', 1)
                module_total += item_total
                items.append({
                    'item': mat.name or '',
                    'spec': mat.spec or '',
                    'category': mat.brand or '',
                    'unit_price': f'¥{float(mat.unit_price or 0):.2f}',
                    'quantity': str(mm.get('quantity', 1)),
                    'subtotal': f'¥{item_total:.2f}',
                })
        if items:
            module_groups.append({
                'name': module.get('name', '未命名模块'),
                'items': items,
                'total': module_total
            })
    
    fees_total = sum(float(f.get('amount', 0)) for f in data.get('fees', []))
    fee_items = []
    for fee in data.get('fees', []):
        location_text = '厂内' if fee.get('location') == 'internal' else ('厂外' if fee.get('location') == 'external' else '')
        fee_items.append({
            'item': fee.get('fee_type', '') or fee.get('name', ''),
            'spec': location_text,
            'category': fee.get('fee_type', '') or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f"¥{float(fee.get('amount', 0)):.2f}",
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    buffer = BytesIO()
    
    class PDF(FPDF):
        def header(self):
            pass
        def footer(self):
            pass
    
    pdf = PDF()
    pdf.add_font('SimHei', '', FONT_REGULAR, uni=True)
    pdf.add_font('SimHei', 'B', FONT_BOLD, uni=True)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 标题
    pdf.set_font('SimHei', 'B', 16)
    pdf.cell(0, 12, data.get('name', '报价单'), 0, 1, 'C')
    pdf.ln(5)
    
    # 基本信息
    pdf.set_font('SimHei', 'B', 11)
    pdf.cell(0, 8, '基本信息', 0, 1)
    pdf.set_font('SimHei', '', 10)
    
    business_owner_name = ''
    if data.get('business_owner_id'):
        owner = User.query.get(data.get('business_owner_id'))
        if owner:
            business_owner_name = owner.real_name
    basic_info = [
        ('项目名称', data.get('name', '')),
        ('方案编号', data.get('scheme_no', '')),
        ('业务负责人', business_owner_name),
        ('版本号', f'v{version_no}'),
        ('报价币种', currency)
    ]
    for key, value in basic_info:
        pdf.set_font('SimHei', 'B', 9)
        pdf.cell(40, 6, key, 1)
        pdf.set_font('SimHei', '', 9)
        pdf.cell(0, 6, str(value), 1, 1)
    
    pdf.ln(5)
    
    # 物料及费用清单 (PDF)
    if module_groups:
        col_widths = [22, 38, 26, 20, 22, 12, 26, 24]  # 总约190
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        
        def draw_table_header():
            pdf.set_font('SimHei', 'B', 8)
            pdf.set_fill_color(68, 114, 196)
            pdf.set_text_color(255, 255, 255)
            pdf.set_x(pdf.l_margin if pdf.l_margin else 10)
            for i, h in enumerate(headers):
                pdf.cell(col_widths[i], 6, h, 1, 0, 'C', True)
            pdf.ln()
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('SimHei', '', 8)
        
        def draw_group(y_start, group):
            item_count = len(group['items'])
            row_h = 5
            y_bottom = y_start + item_count * row_h
            
            # 使用PDF实际的左边距（默认10）
            x_start = pdf.l_margin if pdf.l_margin else 10
            x_module = x_start
            x_data = x_start + col_widths[0]
            x_total = x_start + col_widths[0] + sum(col_widths[1:7])
            x_end = x_start + sum(col_widths)
            
            # 模块列外边框
            pdf.rect(x_module, y_start, col_widths[0], item_count * row_h)
            # 合计列外边框
            pdf.rect(x_total, y_start, col_widths[7], item_count * row_h)
            
            # 数据区域边框
            pdf.line(x_data, y_start, x_data, y_bottom)
            pdf.line(x_total, y_start, x_total, y_bottom)
            
            # 列竖向分割线
            x_cur = x_data
            for j in range(1, 7):
                x_line = x_cur + col_widths[j]
                pdf.line(x_line, y_start, x_line, y_bottom)
                x_cur += col_widths[j]
            
            # 行水平分割线
            for i in range(1, item_count):
                y_line = y_start + i * row_h
                pdf.line(x_data, y_line, x_total, y_line)
            
            # 顶边和底边
            pdf.line(x_data, y_start, x_total, y_start)
            pdf.line(x_data, y_bottom, x_total, y_bottom)
            
            # 文字
            pdf.set_xy(x_module, y_start + (item_count * row_h - 5) / 2)
            pdf.cell(col_widths[0], 5, group['name'], 0, 0, 'C')
            pdf.set_xy(x_total, y_start + (item_count * row_h - 5) / 2)
            pdf.cell(col_widths[7], 5, f'¥{group["total"]:.2f}', 0, 0, 'C')
            
            # 数据单元格内容
            for i, item in enumerate(group['items']):
                y_row = y_start + i * row_h
                x_cur = x_data
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[1], row_h, str(item['item'])[:17], 0)
                x_cur += col_widths[1]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[2], row_h, str(item['spec'])[:12], 0)
                x_cur += col_widths[2]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[3], row_h, str(item['category'])[:9], 0)
                x_cur += col_widths[3]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[4], row_h, str(item['unit_price']), 0, 0, 'R')
                x_cur += col_widths[4]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[5], row_h, str(item['quantity']), 0, 0, 'C')
                x_cur += col_widths[5]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[6], row_h, str(item['subtotal']), 0, 0, 'R')
            
            # 移动到下一行
            pdf.set_y(y_bottom)
            return y_bottom
        
        def check_page_break(y_current, item_count, row_h=5):
            """检查是否需要换页，留出足够空间给当前模块"""
            try:
                y_current = float(y_current) if y_current is not None else 0
            except (ValueError, TypeError):
                y_current = 0
            pdf_h = float(pdf.h) if pdf.h else 297.0
            pdf_bm = float(pdf.b_margin) if pdf.b_margin else 10.0
            page_height = pdf_h - pdf_bm
            needed_height = item_count * row_h + 10  # 10为表头高度
            if y_current + needed_height > page_height:
                pdf.add_page()
                draw_table_header()
                new_y = pdf.get_y()
                return float(new_y) if new_y is not None else (pdf_h - pdf_bm - 10)
            return y_current
        
        # 开始绘制表格
        pdf.ln(5)
        pdf.set_font('SimHei', 'B', 11)
        pdf.cell(0, 8, '物料及费用清单', 0, 1)
        draw_table_header()
        
        y_start = pdf.get_y()
        for group in module_groups:
            if not group['items']:
                pdf.cell(sum(col_widths), 5, f'{group["name"]} - （无物料）', 1, 1, 'L')
                y_start = pdf.get_y()
                continue
            
            item_count = len(group['items'])
            # 检查是否需要换页
            y_start = check_page_break(y_start, item_count)
            
            y_end = draw_group(y_start, group)
            if y_end is None:
                y_end = y_start + len(group['items']) * 5
            y_start = y_end
        
        # 移动到下一页
        if y_start + 10 > (pdf.h if pdf.h else 297) - (pdf.b_margin if pdf.b_margin else 10):
            pdf.add_page()
    else:
        pdf.set_font('SimHei', '', 9)
        pdf.cell(0, 5, '无物料及费用数据', 0, 1)
    
    pdf.ln(5)
    
    # 报价汇总
    pdf.set_font('SimHei', 'B', 11)
    pdf.cell(0, 8, '报价汇总', 0, 1)
    
    pdf.set_font('SimHei', 'B', 9)
    pdf.set_fill_color(68, 114, 196)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(100, 6, '项目', 1, 0, 'C', True)
    pdf.cell(0, 6, '金额', 1, 1, 'C', True)
    
    pdf.set_text_color(0, 0, 0)
    summary_items = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
    ]
    pdf.set_font('SimHei', '', 9)
    for label, value in summary_items:
        pdf.cell(100, 5, label, 1)
        pdf.cell(0, 5, value, 1, 1, 'R')
    
    # 最终报价（高亮）
    pdf.set_font('SimHei', 'B', 10)
    pdf.set_fill_color(226, 239, 218)
    pdf.cell(100, 7, f'最终报价({currency})', 1, 0, 'C', True)
    pdf.cell(0, 7, f'{currency_symbol}{grand_total_converted:.2f}', 1, 1, 'R', True)
    
    # 输出
    pdf.output(buffer)
    with open(pdf_path, 'wb') as f:
        f.write(buffer.getvalue())

@export_bp.route('/quotations/<int:quotation_id>/export/word', methods=['GET'])
def export_word(quotation_id):
    """导出 Word 格式"""
    data = get_quotation_with_details(quotation_id)
    if not data:
        return jsonify({'error': 'Quotation not found'}), 404
    
    quotation, modules, fees = data
    totals = calculate_totals_with_rates(quotation, modules, fees)
    
    # 使用报价单的币种
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    
    # 获取汇率
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    
    # 转换最终报价
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    doc = Document()
    doc = Document()
    
    # 设置文档标题
    title = doc.add_heading('报价单', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 基本信息
    doc.add_heading('基本信息', level=1)
    info_table = doc.add_table(rows=5, cols=2)
    info_table.style = 'Table Grid'
    info_data = [
        ('项目名称', quotation.name or ''),
        ('方案编号', quotation.scheme_no or ''),
        ('业务负责人', quotation.business_owner.real_name if quotation.business_owner else ''),
        ('创建时间', quotation.created_at.strftime('%Y-%m-%d %H:%M') if quotation.created_at else ''),
        ('报价币种', currency)
    ]
    for i, (key, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = key
        info_table.rows[i].cells[1].text = str(value)
    
    doc.add_paragraph()
    
    # 整合表格：模块及物料 + 其他费用
    doc.add_heading('物料及费用清单', level=1)
    
    # 收集分组数据
    module_groups = []
    
    # 按模块分组
    for module in modules:
        items = []
        module_total = 0
        if module.materials:
            for mm in module.materials:
                mat = mm.material
                if mat:
                    item_total = float(mat.unit_price or 0) * mm.quantity
                    module_total += item_total
                    items.append({
                        'item': mat.name or '',
                        'spec': mat.spec or '',
                        'category': mat.brand or '',
                        'unit_price': f'¥{float(mat.unit_price or 0):.2f}',
                        'quantity': str(mm.quantity),
                        'subtotal': f'¥{item_total:.2f}',
                    })
        module_groups.append({
            'name': module.name,
            'items': items,
            'total': module_total
        })
    
    # 费用单独一组
    fees_total = sum(float(f.amount or 0) for f in fees)
    fee_items = []
    for fee in fees:
        location_text = '厂内' if fee.location == 'internal' else ('厂外' if fee.location == 'external' else fee.location or '')
        fee_items.append({
            'item': fee.fee_type or '',
            'spec': location_text,
            'category': fee.fee_type or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f'¥{float(fee.amount or 0):.2f}',
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    if module_groups:
        # 创建整合表格：模块|项目|规格|分类/品牌|单价|数量|小计|合计
        combined_table = doc.add_table(rows=1, cols=8)
        combined_table.style = 'Table Grid'
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        for j, header in enumerate(headers):
            combined_table.rows[0].cells[j].text = header
        
        for group in module_groups:
            if not group['items']:
                row = combined_table.add_row()
                row.cells[0].text = group['name']
                row.cells[1].text = '（无物料）'
                continue
            
            # 第一行用于合并模块和合计
            first_row = combined_table.add_row()
            first_row.cells[0].text = group['name']
            first_row.cells[1].text = group['items'][0]['item']
            first_row.cells[2].text = group['items'][0]['spec']
            first_row.cells[3].text = group['items'][0]['category']
            first_row.cells[4].text = group['items'][0]['unit_price']
            first_row.cells[5].text = group['items'][0]['quantity']
            first_row.cells[6].text = group['items'][0]['subtotal']
            first_row.cells[7].text = f'¥{group["total"]:.2f}'
            
            # 合并模块列 (垂直合并)
            if len(group['items']) > 1:
                # 合并模块列
                module_cell = first_row.cells[0]
                for i in range(1, len(group['items'])):
                    next_row = combined_table.add_row()
                    next_row.cells[1].text = group['items'][i]['item']
                    next_row.cells[2].text = group['items'][i]['spec']
                    next_row.cells[3].text = group['items'][i]['category']
                    next_row.cells[4].text = group['items'][i]['unit_price']
                    next_row.cells[5].text = group['items'][i]['quantity']
                    next_row.cells[6].text = group['items'][i]['subtotal']
                    # 合并模块列
                    module_cell = module_cell.merge(next_row.cells[0])
                
                # 合并合计列
                total_cell = first_row.cells[7]
                for i in range(1, len(group['items'])):
                    next_row_idx = len(combined_table.rows) - 1
                    total_cell = total_cell.merge(combined_table.rows[next_row_idx].cells[7])
    else:
        doc.add_paragraph('无物料及费用数据')
    
    doc.add_paragraph()
    
    # 费用系数说明
    doc.add_heading('费用系数', level=1)
    rate_info = [
        f"大件系数: {totals['fee_rates'].get('large', 1.0)}x",
        f"普通件系数: {totals['fee_rates'].get('standard', 1.0)}x",
        f"其他件系数: {totals['fee_rates'].get('other', 1.0)}x"
    ]
    for info in rate_info:
        doc.add_paragraph(info)
    
    doc.add_paragraph()
    
    # 汇总信息
    doc.add_heading('报价汇总', level=1)
    summary_table = doc.add_table(rows=7, cols=2)
    summary_table.style = 'Table Grid'
    summary_data = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
        (f'最终报价({currency})', f'{currency_symbol}{grand_total_converted:.2f}')
    ]
    for i, (key, value) in enumerate(summary_data):
        summary_table.rows[i].cells[0].text = key
        summary_table.rows[i].cells[1].text = value
    
    # 保存文件
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    filename = f'quotation_{quotation_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.docx'
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/quotations/<int:quotation_id>/export/excel', methods=['GET'])
def export_excel(quotation_id):
    """导出 Excel 格式"""
    data = get_quotation_with_details(quotation_id)
    if not data:
        return jsonify({'error': 'Quotation not found'}), 404
    
    quotation, modules, fees = data
    totals = calculate_totals_with_rates(quotation, modules, fees)
    
    # 使用报价单的币种
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    
    # 获取汇率
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    
    # 转换最终报价
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    doc = Document()
    
    # 样式定义
    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center')
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Sheet 1: 基本信息
    ws1 = wb.active
    ws1.title = '基本信息'
    
    ws1.append(['报价单基本信息'])
    ws1.merge_cells('A1:D1')
    ws1['A1'].font = Font(bold=True, size=14)
    ws1['A1'].alignment = Alignment(horizontal='center')
    
    ws1.append([])
    basic_info = [
        ('项目名称', quotation.name or ''),
        ('方案编号', quotation.scheme_no or ''),
        ('业务负责人', quotation.business_owner.real_name if quotation.business_owner else ''),
        ('创建时间', quotation.created_at.strftime('%Y-%m-%d %H:%M') if quotation.created_at else ''),
        ('报价币种', currency)
    ]
    for key, value in basic_info:
        ws1.append([key, value])
    
    ws1.append([])
    ws1.append(['费用系数'])
    ws1.merge_cells(f'A{ws1.max_row}:B{ws1.max_row}')
    ws1[f'A{ws1.max_row}'].font = Font(bold=True)
    
    rate_info = [
        ('大件系数', f"{totals['fee_rates'].get('large', 1.0)}x"),
        ('普通件系数', f"{totals['fee_rates'].get('standard', 1.0)}x"),
        ('其他件系数', f"{totals['fee_rates'].get('other', 1.0)}x")
    ]
    for key, value in rate_info:
        ws1.append([key, value])
    
    ws1.append([])
    ws1.append(['报价汇总'])
    ws1.merge_cells(f'A{ws1.max_row}:B{ws1.max_row}')
    ws1[f'A{ws1.max_row}'].font = Font(bold=True)
    
    summary = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
        (f'最终报价({currency})', f'{currency_symbol}{grand_total_converted:.2f}')
    ]
    for key, value in summary:
        ws1.append([key, value])
    
    # 调整列宽
    ws1.column_dimensions['A'].width = 18
    ws1.column_dimensions['B'].width = 30
    
    # Sheet 2: 整合物料及费用清单
    ws2 = wb.create_sheet('物料及费用清单')
    
    # 添加表头 - 8列
    headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
    ws2.append(headers)
    for cell in ws2[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    row_num = 2
    merge_info = []  # 记录需要合并的信息：(start_row, end_row, col_letter)
    
    for group in module_groups:
        if not group['items']:
            ws2.append([group['name'], '（无物料）', '', '', '', '', '', ''])
            for cell in ws2[row_num]:
                cell.border = thin_border
            row_num += 1
            continue
        
        start_row = row_num
        for i, item in enumerate(group['items']):
            ws2.append([
                group['name'] if i == 0 else '',
                item['item'],
                item['spec'],
                item['category'],
                float(item['unit_price'].replace('¥', '')) if item['unit_price'] else 0,
                int(item['quantity']),
                float(item['subtotal'].replace('¥', '')) if item['subtotal'] else 0,
                group['total'] if i == 0 else ''
            ])
            for cell in ws2[row_num]:
                cell.border = thin_border
            row_num += 1
        
        # 记录合并信息
        if len(group['items']) > 1:
            merge_info.append((start_row, row_num - 1, 'A'))  # 模块列
            merge_info.append((start_row, row_num - 1, 'H'))  # 合计列
    
    # 执行合并
    for start, end, col in merge_info:
        if start < end:
            ws2.merge_cells(f'{col}{start}:{col}{end}')
            # 居中对齐
            cell = ws2[f'{col}{start}']
            cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # 调整列宽
    col_widths = [16, 24, 18, 14, 12, 8, 12, 16]
    for i, width in enumerate(col_widths):
        ws2.column_dimensions[get_column_letter(i + 1)].width = width
    
    # 保存文件
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    filename = f'quotation_{quotation_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/quotations/<int:quotation_id>/export/pdf', methods=['GET'])
def export_pdf(quotation_id):
    """导出 PDF 格式"""
    data = get_quotation_with_details(quotation_id)
    if not data:
        return jsonify({'error': 'Quotation not found'}), 404
    
    quotation, modules, fees = data
    totals = calculate_totals_with_rates(quotation, modules, fees)
    
    # 使用报价单的币种
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    
    # 获取汇率
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    
    # 转换最终报价
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    doc = Document()
    module_groups = []
    for module in modules:
        items = []
        module_total = 0
        if module.materials:
            for mm in module.materials:
                mat = mm.material
                if mat:
                    item_total = float(mat.unit_price or 0) * mm.quantity
                    module_total += item_total
                    items.append({
                        'item': mat.name or '',
                        'spec': mat.spec or '',
                        'category': mat.brand or '',
                        'unit_price': f'¥{float(mat.unit_price or 0):.2f}',
                        'quantity': str(mm.quantity),
                        'subtotal': f'¥{item_total:.2f}',
                    })
        module_groups.append({
            'name': module.name,
            'items': items,
            'total': module_total
        })
    
    fees_total = sum(float(f.amount or 0) for f in fees)
    fee_items = []
    for fee in fees:
        location_text = '厂内' if fee.location == 'internal' else ('厂外' if fee.location == 'external' else fee.location or '')
        fee_items.append({
            'item': fee.fee_type or '',
            'spec': location_text,
            'category': fee.fee_type or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f'¥{float(fee.amount or 0):.2f}',
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    buffer = BytesIO()
    
    class PDF(FPDF):
        def header(self):
            pass
        def footer(self):
            pass
    
    pdf = PDF()
    pdf.add_font('SimHei', '', FONT_REGULAR, uni=True)
    pdf.add_font('SimHei', 'B', FONT_BOLD, uni=True)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 标题
    pdf.set_font('SimHei', 'B', 16)
    pdf.cell(0, 12, '报价单', 0, 1, 'C')
    pdf.ln(5)
    
    # 基本信息
    pdf.set_font('SimHei', 'B', 11)
    pdf.cell(0, 8, '基本信息', 0, 1)
    pdf.set_font('SimHei', '', 10)
    
    basic_info = [
        ('项目名称', quotation.name or ''),
        ('方案编号', quotation.scheme_no or ''),
        ('业务负责人', quotation.business_owner.real_name if quotation.business_owner else ''),
        ('创建时间', quotation.created_at.strftime('%Y-%m-%d %H:%M') if quotation.created_at else ''),
        ('报价币种', currency)
    ]
    for key, value in basic_info:
        pdf.set_font('SimHei', 'B', 9)
        pdf.cell(40, 6, key, 1)
        pdf.set_font('SimHei', '', 9)
        pdf.cell(0, 6, str(value), 1, 1)
    
    pdf.ln(5)
    
    # 物料及费用清单 (PDF)
    if module_groups:
        col_widths = [22, 38, 26, 20, 22, 12, 26, 24]  # 总约190
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        
        def draw_table_header():
            pdf.set_font('SimHei', 'B', 8)
            pdf.set_fill_color(68, 114, 196)
            pdf.set_text_color(255, 255, 255)
            pdf.set_x(pdf.l_margin if pdf.l_margin else 10)
            for i, h in enumerate(headers):
                pdf.cell(col_widths[i], 6, h, 1, 0, 'C', True)
            pdf.ln()
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('SimHei', '', 8)
        
        def draw_group(y_start, group):
            item_count = len(group['items'])
            row_h = 5
            y_bottom = y_start + item_count * row_h
            
            # 使用PDF实际的左边距（默认10）
            x_start = pdf.l_margin if pdf.l_margin else 10
            x_module = x_start
            x_data = x_start + col_widths[0]
            x_total = x_start + col_widths[0] + sum(col_widths[1:7])
            x_end = x_start + sum(col_widths)
            
            # 模块列外边框
            pdf.rect(x_module, y_start, col_widths[0], item_count * row_h)
            # 合计列外边框
            pdf.rect(x_total, y_start, col_widths[7], item_count * row_h)
            
            # 数据区域边框
            pdf.line(x_data, y_start, x_data, y_bottom)
            pdf.line(x_total, y_start, x_total, y_bottom)
            
            # 列竖向分割线
            x_cur = x_data
            for j in range(1, 7):
                x_line = x_cur + col_widths[j]
                pdf.line(x_line, y_start, x_line, y_bottom)
                x_cur += col_widths[j]
            
            # 行水平分割线
            for i in range(1, item_count):
                y_line = y_start + i * row_h
                pdf.line(x_data, y_line, x_total, y_line)
            
            # 顶边和底边
            pdf.line(x_data, y_start, x_total, y_start)
            pdf.line(x_data, y_bottom, x_total, y_bottom)
            
            # 文字
            pdf.set_xy(x_module, y_start + (item_count * row_h - 5) / 2)
            pdf.cell(col_widths[0], 5, group['name'], 0, 0, 'C')
            pdf.set_xy(x_total, y_start + (item_count * row_h - 5) / 2)
            pdf.cell(col_widths[7], 5, f'¥{group["total"]:.2f}', 0, 0, 'C')
            
            # 数据单元格内容
            for i, item in enumerate(group['items']):
                y_row = y_start + i * row_h
                x_cur = x_data
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[1], row_h, str(item['item'])[:17], 0)
                x_cur += col_widths[1]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[2], row_h, str(item['spec'])[:12], 0)
                x_cur += col_widths[2]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[3], row_h, str(item['category'])[:9], 0)
                x_cur += col_widths[3]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[4], row_h, str(item['unit_price']), 0, 0, 'R')
                x_cur += col_widths[4]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[5], row_h, str(item['quantity']), 0, 0, 'C')
                x_cur += col_widths[5]
                pdf.set_xy(x_cur, y_row)
                pdf.cell(col_widths[6], row_h, str(item['subtotal']), 0, 0, 'R')
            
            # 移动到下一行
            pdf.set_y(y_bottom)
            return y_bottom
        
        def check_page_break(y_current, item_count, row_h=5):
            """检查是否需要换页，留出足够空间给当前模块"""
            try:
                y_current = float(y_current) if y_current is not None else 0
            except (ValueError, TypeError):
                y_current = 0
            pdf_h = float(pdf.h) if pdf.h else 297.0
            pdf_bm = float(pdf.b_margin) if pdf.b_margin else 10.0
            page_height = pdf_h - pdf_bm
            needed_height = item_count * row_h + 10  # 10为表头高度
            if y_current + needed_height > page_height:
                pdf.add_page()
                draw_table_header()
                new_y = pdf.get_y()
                return float(new_y) if new_y is not None else (pdf_h - pdf_bm - 10)
            return y_current
        
        # 开始绘制表格
        pdf.ln(5)
        pdf.set_font('SimHei', 'B', 11)
        pdf.cell(0, 8, '物料及费用清单', 0, 1)
        draw_table_header()
        
        y_start = pdf.get_y()
        for group in module_groups:
            if not group['items']:
                pdf.cell(sum(col_widths), 5, f'{group["name"]} - （无物料）', 1, 1, 'L')
                y_start = pdf.get_y()
                continue
            
            item_count = len(group['items'])
            # 检查是否需要换页
            y_start = check_page_break(y_start, item_count)
            
            y_end = draw_group(y_start, group)
            if y_end is None:
                y_end = y_start + len(group['items']) * 5
            y_start = y_end
        
        # 移动到下一页
        if y_start + 10 > (pdf.h if pdf.h else 297) - (pdf.b_margin if pdf.b_margin else 10):
            pdf.add_page()
    else:
        pdf.set_font('SimHei', '', 9)
        pdf.cell(0, 5, '无物料及费用数据', 0, 1)
    
    pdf.ln(5)
    
    # 报价汇总
    pdf.set_font('SimHei', 'B', 11)
    pdf.cell(0, 8, '报价汇总', 0, 1)
    
    pdf.set_font('SimHei', 'B', 9)
    pdf.set_fill_color(68, 114, 196)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(100, 6, '项目', 1, 0, 'C', True)
    pdf.cell(0, 6, '金额', 1, 1, 'C', True)
    
    pdf.set_text_color(0, 0, 0)
    summary_items = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
    ]
    pdf.set_font('SimHei', '', 9)
    for label, value in summary_items:
        pdf.cell(100, 5, label, 1)
        pdf.cell(0, 5, value, 1, 1, 'R')
    
    # 最终报价（高亮）
    pdf.set_font('SimHei', 'B', 10)
    pdf.set_fill_color(226, 239, 218)
    pdf.cell(100, 7, f'最终报价({currency})', 1, 0, 'C', True)
    pdf.cell(0, 7, f'{currency_symbol}{grand_total_converted:.2f}', 1, 1, 'R', True)
    
    # 输出
    pdf.output(buffer)
    buffer.seek(0)
    buffer.seek(0)
    
    filename = f'quotation_{quotation_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )


# ==================== 版本导出 ====================

def get_version_snapshot_data(quotation_id, version_no):
    """获取版本快照数据并重建完整结构"""
    version = VersionSnapshot.query.filter_by(
        quotation_id=quotation_id,
        version_no=version_no
    ).first()
    if not version:
        return None
    
    import json
    data = json.loads(version.snapshot_data)
    
    # 重建物料信息（从快照的material_id查询完整物料数据）
    for module in data.get('modules', []):
        materials = module.get('materials', [])
        for mm in materials:
            mat = Material.query.get(mm.get('material_id'))
            if mat:
                mm['name'] = mat.name or ''
                mm['brand'] = mat.brand or ''
                mm['spec'] = mat.spec or ''
                mm['unit_price'] = mat.unit_price or 0
                mm['category'] = mat.category or 'standard'
    
    # 重建费用信息
    for fee in data.get('fees', []):
        fee['name'] = fee.get('fee_type', '') or fee.get('name', '')
        fee['amount'] = float(fee.get('amount', 0))
        fee['location'] = fee.get('position', 'internal')
    
    return data


def calculate_version_totals(data):
    """计算版本数据的汇总"""
    modules = data.get('modules', [])
    fees = data.get('fees', [])
    
    # 分类统计物料
    category_totals = {'large': 0, 'standard': 0, 'other': 0}
    for module in modules:
        for mm in module.get('materials', []):
            cat = mm.get('category', 'standard')
            amount = float(mm.get('unit_price', 0) or 0) * float(mm.get('quantity', 0) or 0)
            category_totals[cat] = category_totals.get(cat, 0) + amount
    
    # 获取费用系数
    fee_rates = {fr.category: float(fr.rate) for fr in FeeRate.query.all()}
    rate_large = fee_rates.get('large', 1.0)
    rate_standard = fee_rates.get('standard', 1.0)
    rate_other = fee_rates.get('other', 1.0)
    
    material_with_rates = (
        category_totals.get('large', 0) * rate_large +
        category_totals.get('standard', 0) * rate_standard +
        category_totals.get('other', 0) * rate_other
    )
    
    material_total = sum(category_totals.values())
    fees_total = sum(float(fee.get('amount', 0)) for fee in fees)
    subtotal = material_with_rates + fees_total
    
    tax_rate = float(data.get('tax_rate', 0)) if data.get('tax_rate') else 0.13
    tax_amount = subtotal * tax_rate
    grand_total = subtotal + tax_amount
    
    return {
        'material_total': material_total,
        'material_total_with_rates': material_with_rates,
        'fees_total': fees_total,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'fee_rates': fee_rates
    }


@export_bp.route('/quotations/<int:quotation_id>/versions/<int:version_no>/export/word', methods=['GET'])
def export_version_word(quotation_id, version_no):
    """导出版本 Word 格式（直接下载预生成文件）"""
    version = VersionSnapshot.query.filter_by(
        quotation_id=quotation_id,
        version_no=version_no
    ).first()
    if not version:
        return jsonify({'error': 'Version not found'}), 404
    
    # 如果有预生成的文件，直接返回
    if version.word_file:
        import os
        if os.path.exists(version.word_file):
            # snapshot_data 是 JSON 字符串
            import json
            name = '报价单'
            if version.snapshot_data:
                try:
                    data = json.loads(version.snapshot_data) if isinstance(version.snapshot_data, str) else version.snapshot_data
                    name = data.get('name', '报价单')
                except:
                    pass
            filename = f'{name}_v{version_no}.docx'
            return send_file(
                version.word_file,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=filename
            )
    
    # 如果没有预生成文件，动态生成
    data = get_version_snapshot_data(quotation_id, version_no)
    if not data:
        return jsonify({'error': 'Version data not found'}), 404
    
    # 获取报价单信息（包含币种）
    quotation = Quotation.query.get(quotation_id)
    
    totals = calculate_version_totals(data)
    # 使用报价单的币种
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    doc = Document()
    title = doc.add_heading(f'{data.get("name", "报价单")}', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 基本信息
    doc.add_heading('基本信息', level=1)
    info_table = doc.add_table(rows=5, cols=2)
    info_table.style = 'Table Grid'
    business_owner_name = ''
    if data.get('business_owner_id'):
        owner = User.query.get(data.get('business_owner_id'))
        if owner:
            business_owner_name = owner.real_name
    info_data = [
        ('项目名称', data.get('name', '')),
        ('方案编号', data.get('scheme_no', '')),
        ('业务负责人', business_owner_name),
        ('版本号', f'v{version_no}'),
        ('报价币种', currency)
    ]
    for i, (key, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = key
        info_table.rows[i].cells[1].text = str(value)
    
    doc.add_paragraph()
    
    # 整合表格：模块及物料 + 其他费用
    doc.add_heading('物料及费用清单', level=1)
    
    module_groups = []
    
    # 按模块分组
    for module in data.get('modules', []):
        items = []
        module_total = 0
        for mm in module.get('materials', []):
            item_total = float(mm.get('unit_price', 0) or 0) * float(mm.get('quantity', 0) or 0)
            module_total += item_total
            items.append({
                'item': mm.get('name', ''),
                'spec': mm.get('spec', ''),
                'category': mm.get('brand', ''),
                'unit_price': f'¥{float(mm.get("unit_price", 0) or 0):.2f}',
                'quantity': str(mm.get('quantity', 0)),
                'subtotal': f'¥{item_total:.2f}',
            })
        module_groups.append({
            'name': module.get('name', '未命名模块'),
            'items': items,
            'total': module_total
        })
    
    # 费用单独一组
    fees_total = sum(float(f.get('amount', 0)) for f in data.get('fees', []))
    fee_items = []
    for fee in data.get('fees', []):
        location_text = '厂内' if fee.get('location') == 'internal' else ('厂外' if fee.get('location') == 'external' else '')
        fee_items.append({
            'item': fee.get('fee_type', '') or fee.get('name', ''),
            'spec': location_text,
            'category': fee.get('fee_type', '') or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f'¥{float(fee.get("amount", 0)):.2f}',
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    if module_groups:
        combined_table = doc.add_table(rows=1, cols=8)
        combined_table.style = 'Table Grid'
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        for j, header in enumerate(headers):
            combined_table.rows[0].cells[j].text = header
        
        for group in module_groups:
            if not group['items']:
                row = combined_table.add_row()
                row.cells[0].text = group['name']
                row.cells[1].text = '（无物料）'
                continue
            
            first_row = combined_table.add_row()
            first_row.cells[0].text = group['name']
            first_row.cells[1].text = group['items'][0]['item']
            first_row.cells[2].text = group['items'][0]['spec']
            first_row.cells[3].text = group['items'][0]['category']
            first_row.cells[4].text = group['items'][0]['unit_price']
            first_row.cells[5].text = group['items'][0]['quantity']
            first_row.cells[6].text = group['items'][0]['subtotal']
            first_row.cells[7].text = f'¥{group["total"]:.2f}'
            
            if len(group['items']) > 1:
                module_cell = first_row.cells[0]
                for i in range(1, len(group['items'])):
                    next_row = combined_table.add_row()
                    next_row.cells[1].text = group['items'][i]['item']
                    next_row.cells[2].text = group['items'][i]['spec']
                    next_row.cells[3].text = group['items'][i]['category']
                    next_row.cells[4].text = group['items'][i]['unit_price']
                    next_row.cells[5].text = group['items'][i]['quantity']
                    next_row.cells[6].text = group['items'][i]['subtotal']
                    module_cell = module_cell.merge(next_row.cells[0])
                
                total_cell = first_row.cells[7]
                for i in range(1, len(group['items'])):
                    next_row_idx = len(combined_table.rows) - 1
                    total_cell = total_cell.merge(combined_table.rows[next_row_idx].cells[7])
    else:
        doc.add_paragraph('无物料及费用数据')
    
    doc.add_paragraph()
    
    # 费用系数说明
    doc.add_heading('费用系数', level=1)
    rate_info = [
        f"大件系数: {totals['fee_rates'].get('large', 1.0)}x",
        f"普通件系数: {totals['fee_rates'].get('standard', 1.0)}x",
        f"其他件系数: {totals['fee_rates'].get('other', 1.0)}x"
    ]
    for info in rate_info:
        doc.add_paragraph(info)
    
    doc.add_paragraph()
    
    # 汇总信息
    doc.add_heading('报价汇总', level=1)
    summary_table = doc.add_table(rows=7, cols=2)
    summary_table.style = 'Table Grid'
    summary_data = [
        ('物料合计', f'¥{totals["material_total"]:.2f}'),
        ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
        ('费用合计', f'¥{totals["fees_total"]:.2f}'),
        ('小计', f'¥{totals["subtotal"]:.2f}'),
        ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
        ('税额', f'¥{totals["tax_amount"]:.2f}'),
        (f'最终报价({currency})', f'{currency_symbol}{grand_total_converted:.2f}')
    ]
    for i, (key, value) in enumerate(summary_data):
        summary_table.rows[i].cells[0].text = key
        summary_table.rows[i].cells[1].text = value
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    filename = f'{data.get("name", "报价单")}_v{version_no}_{datetime.now().strftime("%Y%m%d%H%M%S")}.docx'
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name=filename
    )


@export_bp.route('/quotations/<int:quotation_id>/versions/<int:version_no>/export/pdf', methods=['GET'])
def export_version_pdf(quotation_id, version_no):
    """导出版本 PDF 格式（直接下载预生成文件）"""
    version = VersionSnapshot.query.filter_by(
        quotation_id=quotation_id,
        version_no=version_no
    ).first()
    if not version:
        return jsonify({'error': 'Version not found'}), 404
    
    # 如果有预生成的文件，直接返回
    if version.pdf_file:
        import os
        if os.path.exists(version.pdf_file):
            # snapshot_data 是 JSON 字符串
            import json
            name = '报价单'
            if version.snapshot_data:
                try:
                    data = json.loads(version.snapshot_data) if isinstance(version.snapshot_data, str) else version.snapshot_data
                    name = data.get('name', '报价单')
                except:
                    pass
            filename = f'{name}_v{version_no}.pdf'
            return send_file(
                version.pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
    
    # 如果没有预生成文件，动态生成
    data = get_version_snapshot_data(quotation_id, version_no)
    if not data:
        return jsonify({'error': 'Version data not found'}), 404
    
    # 获取报价单信息（包含币种）
    quotation = Quotation.query.get(quotation_id)
    
    totals = calculate_version_totals(data)
    
    # 使用报价单的币种
    currency = quotation.currency if quotation and quotation.currency else 'CNY'
    exchange_rates = {er.currency: float(er.rate) for er in ExchangeRate.query.all()}
    currency_symbol = get_currency_symbol(currency)
    grand_total_converted = convert_currency(totals['grand_total'], currency, exchange_rates)
    
    # 收集分组数据
    module_groups = []
    for module in data.get('modules', []):
        items = []
        module_total = 0
        for mm in module.get('materials', []):
            item_total = float(mm.get('unit_price', 0) or 0) * float(mm.get('quantity', 0) or 0)
            module_total += item_total
            items.append({
                'item': mm.get('name', ''),
                'spec': mm.get('spec', ''),
                'category': mm.get('brand', ''),
                'unit_price': f'¥{float(mm.get("unit_price", 0) or 0):.2f}',
                'quantity': str(mm.get('quantity', 0)),
                'subtotal': f'¥{item_total:.2f}',
            })
        module_groups.append({
            'name': module.get('name', '未命名'),
            'items': items,
            'total': module_total
        })
    
    fees_total = sum(float(f.get('amount', 0)) for f in data.get('fees', []))
    fee_items = []
    for fee in data.get('fees', []):
        location_text = '厂内' if fee.get('location') == 'internal' else ('厂外' if fee.get('location') == 'external' else '')
        fee_items.append({
            'item': fee.get('fee_type', '') or fee.get('name', ''),
            'spec': location_text,
            'category': fee.get('fee_type', '') or '',
            'unit_price': '',
            'quantity': '1',
            'subtotal': f'¥{float(fee.get("amount", 0)):.2f}',
        })
    if fee_items:
        module_groups.append({
            'name': '其他费用',
            'items': fee_items,
            'total': fees_total
        })
    
    buffer = BytesIO()
    
    class PDF(FPDF):
        def header(self):
            pass
        def footer(self):
            pass
    
    pdf = PDF()
    pdf.add_font('SimHei', '', FONT_REGULAR, uni=True)
    pdf.add_font('SimHei', 'B', FONT_BOLD, uni=True)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 标题
    pdf.set_font('SimHei', 'B', 16)
    pdf.cell(0, 12, data.get('name', '报价单'), 0, 1, 'C')
    pdf.ln(5)
    
    # 基本信息
    pdf.set_font('SimHei', 'B', 11)
    pdf.cell(0, 8, '基本信息', 0, 1)
    pdf.set_font('SimHei', '', 10)
    
    business_owner_name = ''
    if data.get('business_owner_id'):
        owner = User.query.get(data.get('business_owner_id'))
        if owner:
            business_owner_name = owner.real_name
    basic_info = [
        ('项目名称', data.get('name', '')),
        ('方案编号', data.get('scheme_no', '')),
        ('业务负责人', business_owner_name),
        ('版本号', f'v{version_no}'),
        ('报价币种', currency)
    ]
    for key, value in basic_info:
        pdf.set_font('SimHei', 'B', 9)
        pdf.cell(40, 6, key, 1)
        pdf.set_font('SimHei', '', 9)
        pdf.cell(0, 6, str(value), 1, 1)
    
    pdf.ln(5)
    
    # 物料及费用清单 (PDF)
    if module_groups:
        col_widths = [22, 38, 26, 20, 22, 12, 26, 24]  # 总约190
        headers = ['模块', '项目', '规格', '分类/品牌', '单价', '数量', '小计', '合计']
        
        def draw_table_header():
            pdf.set_font('SimHei', 'B', 8)
            pdf.set_fill_color(68, 114, 196)
            pdf.set_text_color(255, 255, 255)
            pdf.set_x(pdf.l_margin if pdf.l_margin else 10)
            for i, h in enumerate(headers):
                pdf.cell(col_widths[i], 6, h, 1, 0, 'C', True)
            pdf.ln()
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('SimHei', '', 8)
        
        def draw_group(y_start, group):
            item_count = len(group['items'])
            row_h = 5
            y_bottom = y_start + item_count * row_h
            
            x_start = pdf.l_margin if pdf.l_margin else 10
            x_module = x_start
            x_data = x_start + col_widths[0]
            x_total = x_start + col_widths[0] + sum(col_widths[1:7])
            x_end = x_start + sum(col_widths)
            
            pdf.rect(x_module, y_start, col_widths[0], item_count * row_h)
            pdf.rect(x_total, y_start, col_widths[7], item_count * row_h)
            
            pdf.line(x_data, y_start, x_data, y_bottom)
            pdf.line(x_total, y_start, x_total, y_bottom)
            
            x_cur = x_data
            for j in range(1, 7):
                x_line = x_cur + col_widths[j]
                pdf.line(x_line, y_start, x_line, y_bottom)
                x_cur += col_widths[j]
            
            pdf.line(x_start, y_bottom, x_end, y_bottom)
            
            for i, item in enumerate(group['items']):
                y_item = y_start + i * row_h
                pdf.set_x(x_start)
                pdf.cell(col_widths[0], row_h, group['name'] if i == 0 else '', 0, 0, 'C')
                pdf.cell(col_widths[1], row_h, item['item'][:12], 0, 0, 'L')
                pdf.cell(col_widths[2], row_h, item['spec'][:8], 0, 0, 'L')
                pdf.cell(col_widths[3], row_h, item['category'][:6], 0, 0, 'L')
                pdf.cell(col_widths[4], row_h, item['unit_price'][:7], 0, 0, 'R')
                pdf.cell(col_widths[5], row_h, item['quantity'], 0, 0, 'C')
                pdf.cell(col_widths[6], row_h, item['subtotal'][:8], 0, 0, 'R')
                pdf.cell(col_widths[7], row_h, f'¥{group["total"]:.2f}' if i == 0 else '', 0, 1, 'R')
            
            return y_bottom
        
        draw_table_header()
        y = pdf.get_y()
        for group in module_groups:
            if group['items']:
                y = draw_group(y, group)
        
        pdf.ln(3)
        
        # 费用系数说明
        pdf.set_font('SimHei', 'B', 10)
        pdf.cell(0, 7, '费用系数', 0, 1)
        pdf.set_font('SimHei', '', 9)
        rate_info = [
            f"大件系数: {totals['fee_rates'].get('large', 1.0)}x",
            f"普通件系数: {totals['fee_rates'].get('standard', 1.0)}x",
            f"其他件系数: {totals['fee_rates'].get('other', 1.0)}x"
        ]
        for info in rate_info:
            pdf.cell(0, 5, info, 0, 1)
        
        pdf.ln(3)
        
        # 汇总信息
        pdf.set_font('SimHei', 'B', 10)
        pdf.cell(0, 7, '报价汇总', 0, 1)
        pdf.set_font('SimHei', '', 9)
        
        summary_data = [
            ('物料合计', f'¥{totals["material_total"]:.2f}'),
            ('物料合计(含系数)', f'¥{totals["material_total_with_rates"]:.2f}'),
            ('费用合计', f'¥{totals["fees_total"]:.2f}'),
            ('小计', f'¥{totals["subtotal"]:.2f}'),
            ('税率', f'{totals["tax_rate"] * 100:.0f}%'),
            ('税额', f'¥{totals["tax_amount"]:.2f}'),
            (f'最终报价({currency})', f'{currency_symbol}{grand_total_converted:.2f}')
        ]
        for key, value in summary_data:
            pdf.set_font('SimHei', 'B', 9)
            pdf.cell(50, 6, key, 1)
            pdf.set_font('SimHei', '', 9)
            pdf.cell(0, 6, value, 1, 1, 'R')
    
    pdf.output(buffer)
    buffer.seek(0)
    
    filename = f'{data.get("name", "报价单")}_v{version_no}_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
