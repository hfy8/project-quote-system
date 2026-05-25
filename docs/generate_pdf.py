#!/usr/bin/env python3
"""Generate PDF user manual for Project Quote System."""
import os, sys

FONT_PATH = "/home/rs8568/project-quote-system/backend/fonts/simhei.ttf"
FONT_NAME = "SimHei"

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Register font
try:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
    print(f"Font '{FONT_NAME}' registered OK")
except Exception as e:
    print(f"Font registration failed: {e}")
    FONT_NAME = "Helvetica"

# Colours
TEAL      = colors.HexColor("#0D9488")
TEAL_DARK = colors.HexColor("#0F766E")
GRAY_BG   = colors.HexColor("#F8FAFB")
GRAY_LINE = colors.HexColor("#E2E8F0")
TEXT_DARK = colors.HexColor("#1E293B")
TEXT_MID  = colors.HexColor("#475569")
WHITE     = colors.white

SC = "/home/rs8568/project-quote-system/screenshots"


def make_styles():
    def S(name, **kw):
        return ParagraphStyle(name, fontName=FONT_NAME, **kw)

    return {
        "cover_title": S("CoverTitle", fontSize=36, textColor=WHITE, alignment=TA_CENTER, leading=44, spaceAfter=12),
        "cover_sub":   S("CoverSub",  fontSize=16, textColor=colors.HexColor("#CCFBF1"), alignment=TA_CENTER, leading=22, spaceAfter=8),
        "cover_info":  S("CoverInfo",  fontSize=12, textColor=colors.HexColor("#99F6E4"), alignment=TA_CENTER, leading=18),
        "h1": S("H1",  fontSize=22, textColor=TEAL,      spaceAfter=10, spaceBefore=6,  leading=28),
        "h2": S("H2",  fontSize=16, textColor=TEAL_DARK,  spaceAfter=6,  spaceBefore=14, leading=22),
        "h3": S("H3",  fontSize=13, textColor=TEXT_DARK, spaceAfter=4,  spaceBefore=8,  leading=18),
        "body":      S("Body",      fontSize=10, textColor=TEXT_DARK, leading=16, spaceAfter=6),
        "body_mid":  S("BodyMid",  fontSize=10, textColor=TEXT_MID,  leading=15, spaceAfter=4),
        "caption":   S("Caption",   fontSize=9,  textColor=TEXT_MID,  alignment=TA_CENTER, leading=13, spaceAfter=10, spaceBefore=4),
        "table_hdr": S("TH", fontSize=9, textColor=WHITE, alignment=TA_CENTER, leading=13),
        "table_cell":S("TC", fontSize=9, textColor=TEXT_DARK, leading=13),
        "bullet":    S("Bullet", fontSize=10, textColor=TEXT_DARK, leading=15, leftIndent=16, spaceAfter=3, bulletIndent=6),
    }


def img(filename, width=15*cm):
    path = os.path.join(SC, filename)
    if not os.path.exists(path):
        return Paragraph(f"[图片不存在: {filename}]", make_styles()["body"])
    try:
        im = Image(path)
        im._restrictSize(width, 9*cm)
        return im
    except Exception as e:
        return Paragraph(f"[加载失败: {filename}]", make_styles()["body"])


def hr():
    return HRFlowable(width="100%", thickness=1, color=GRAY_LINE, spaceAfter=8, spaceBefore=8)


def sp(h=4*mm):
    return Spacer(1, h)


def section(title, styles):
    return [
        Spacer(1, 8*mm),
        Paragraph(title, styles["h1"]),
        hr(),
    ]


def subsection(title, styles):
    return [Paragraph(title, styles["h2"])]


def caption(text, styles):
    return Paragraph(f"\u25b2 {text}", styles["caption"])


def bullet(text, styles):
    return Paragraph(f"\u2022 {text}", styles["bullet"])


def tbl_style():
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  TEAL),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),  [WHITE, GRAY_BG]),
        ("GRID",          (0,0), (-1,-1),  0.5, GRAY_LINE),
        ("FONTNAME",      (0,0), (-1,-1),  FONT_NAME),
        ("FONTSIZE",      (0,0), (-1,-1),  9),
        ("TOPPADDING",    (0,0), (-1,-1),  5),
        ("BOTTOMPADDING", (0,0), (-1,-1),  5),
        ("LEFTPADDING",   (0,0), (-1,-1),  8),
        ("RIGHTPADDING",  (0,0), (-1,-1),  8),
        ("VALIGN",        (0,0), (-1,-1),  "MIDDLE"),
    ])


def hdr_tbl_style():
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  TEAL_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),  [WHITE, GRAY_BG]),
        ("GRID",          (0,0), (-1,-1),  0.5, GRAY_LINE),
        ("FONTNAME",      (0,0), (-1,-1),  FONT_NAME),
        ("FONTSIZE",      (0,0), (-1,-1),  9),
        ("TOPPADDING",    (0,0), (-1,-1),  5),
        ("BOTTOMPADDING", (0,0), (-1,-1),  5),
        ("LEFTPADDING",   (0,0), (-1,-1),  8),
        ("RIGHTPADDING",  (0,0), (-1,-1),  8),
    ])


def make_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(tbl_style())
    return t


def make_hdr_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(hdr_tbl_style())
    return t


# ── Sections ────────────────────────────────────────────────────────────────

def build_cover(story, S):
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("项目报价系统", S["cover_title"]))
    story.append(Paragraph("使用说明书", S["cover_sub"]))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("User Guide", S["cover_sub"]))
    story.append(Spacer(1, 5*cm))

    meta = [
        ["系统地址", "http://10.60.100.1:9005"],
        ["默认账号", "admin  /  admin123"],
        ["版本",     "v1.0"],
        ["日期",     "2026年5月"],
    ]
    mt = Table(meta, colWidths=[5*cm, 12*cm])
    mt.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), FONT_NAME),
        ("FONTSIZE",  (0,0), (-1,-1), 11),
        ("TEXTCOLOR", (0,0), (-1,-1), WHITE),
        ("ALIGN",     (0,0), (0,-1), "RIGHT"),
        ("ALIGN",     (1,0), (1,-1), "LEFT"),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING",(0,0), (-1,-1), 12),
        ("LINEBELOW", (0,-1), (-1,-1), 0.5, colors.HexColor("#5EEAD4")),
        ("BACKGROUND", (0,0), (-1,-1), TEAL_DARK),
    ]))
    story.append(mt)
    story.append(PageBreak())


def build_toc(story, S):
    story.extend(section("目录", S))
    items = [
        ("1",  "登录系统",           "3"),
        ("2",  "首页仪表盘",         "4"),
        ("3",  "报价单管理",         "6"),
        ("4",  "新建/编辑报价单",     "8"),
        ("5",  "我的分配",           "12"),
        ("6",  "变更审核",           "13"),
        ("7",  "原材料库",           "14"),
        ("8",  "费用类型",           "16"),
        ("9",  "费用系数",           "17"),
        ("10", "汇率配置",           "18"),
        ("11", "用户管理",           "19"),
        ("12", "角色管理",           "20"),
        ("13", "参与人权限",         "21"),
        ("14", "操作日志",           "22"),
        ("15", "修改密码与退出",     "23"),
        ("16", "PDF 导出功能",       "24"),
    ]
    data = [[Paragraph("章节", S["table_hdr"]), Paragraph("内容", S["table_hdr"]), Paragraph("页码", S["table_hdr"])]]
    for n, t, p in items:
        data.append([Paragraph(n, S["table_cell"]), Paragraph(t, S["table_cell"]), Paragraph(p, S["table_cell"])])
    t = Table(data, colWidths=[1.8*cm, 13*cm, 2.2*cm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(PageBreak())


def build_login(story, S):
    story.extend(section("1. 登录系统", S))
    story.append(img("01_login.png", 15*cm))
    story.append(caption("图 1-1  登录页面", S))
    story.append(sp())
    story.append(Paragraph("打开浏览器，访问系统地址 <b>http://10.60.100.1:9005</b>，显示登录页面（如图 1-1）。", S["body"]))
    story.append(sp(3*mm))
    story.append(Paragraph("<b>登录步骤：</b>", S["body"]))
    for s in [
        "在「用户名」输入框中填写账号（默认账号为 <b>admin</b>）；",
        "在「密码」输入框中填写密码（默认密码为 <b>admin123</b>）；",
        "点击「<b>登录</b>」按钮，进入系统首页。",
    ]:
        story.append(bullet(s, S))
    story.append(sp(3*mm))
    story.append(Paragraph("首次登录后请立即修改默认密码，密码安全责任由使用者自行承担。", S["body_mid"]))
    story.append(PageBreak())


def build_dashboard(story, S):
    story.extend(section("2. 首页仪表盘", S))
    story.append(img("02_dashboard.png", 15*cm))
    story.append(caption("图 2-1  首页仪表盘", S))
    story.append(sp())
    story.append(Paragraph("登录成功后进入首页，显示欢迎信息、快捷操作区、最近报价单列表。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>侧边栏导航说明：</b>", S["h3"]))
    data = [
        [Paragraph("图标", S["table_hdr"]), Paragraph("菜单", S["table_hdr"]), Paragraph("功能说明", S["table_hdr"])],
        [Paragraph("\U0001f4e6", S["table_cell"]), Paragraph("报价系统", S["table_cell"]), Paragraph("系统 Logo，点击可回到首页", S["table_cell"])],
        [Paragraph("\U0001f3e0", S["table_cell"]), Paragraph("首页", S["table_cell"]), Paragraph("系统首页仪表盘", S["table_cell"])],
        [Paragraph("\U0001f4cb", S["table_cell"]), Paragraph("报价单管理", S["table_cell"]), Paragraph("查看/管理所有报价单", S["table_cell"])],
        [Paragraph("\U0001f4cc", S["table_cell"]), Paragraph("我的分配", S["table_cell"]), Paragraph("当前用户被分配的报价单", S["table_cell"])],
        [Paragraph("\U0001f4e4", S["table_cell"]), Paragraph("变更审核", S["table_cell"]), Paragraph("审核报价单变更申请", S["table_cell"])],
        [Paragraph("\U0001f4e6", S["table_cell"]), Paragraph("原材料库", S["table_cell"]), Paragraph("物料品名、规格、品牌、价格管理", S["table_cell"])],
        [Paragraph("\U0001f4b0", S["table_cell"]), Paragraph("费用类型", S["table_cell"]), Paragraph("费用项目分类（人力/物流等）", S["table_cell"])],
        [Paragraph("\U0001f4ca", S["table_cell"]), Paragraph("费用系数", S["table_cell"]), Paragraph("各项费用的计算系数", S["table_cell"])],
        [Paragraph("\U0001f4b1", S["table_cell"]), Paragraph("汇率配置", S["table_cell"]), Paragraph("系统适用汇率管理", S["table_cell"])],
        [Paragraph("\U0001f464", S["table_cell"]), Paragraph("用户管理", S["table_cell"]), Paragraph("用户账号管理", S["table_cell"])],
        [Paragraph("\U0001f465", S["table_cell"]), Paragraph("角色管理", S["table_cell"]), Paragraph("角色及权限分配", S["table_cell"])],
        [Paragraph("\U0001f510", S["table_cell"]), Paragraph("参与人权限", S["table_cell"]), Paragraph("项目参与人数据权限设置", S["table_cell"])],
        [Paragraph("\U0001f4dd", S["table_cell"]), Paragraph("操作日志", S["table_cell"]), Paragraph("所有操作行为记录", S["table_cell"])],
        [Paragraph("\U0001f511", S["table_cell"]), Paragraph("修改密码", S["table_cell"]), Paragraph("修改当前账号密码", S["table_cell"])],
        [Paragraph("\U0001f6aa", S["table_cell"]), Paragraph("退出登录", S["table_cell"]), Paragraph("退出系统返回登录页", S["table_cell"])],
    ]
    t = Table(data, colWidths=[2*cm, 3.5*cm, 11.5*cm])
    t.setStyle(tbl_style())
    story.append(t)
    story.append(sp(3*mm))
    story.append(Paragraph("<b>快捷操作区：</b>", S["h3"]))
    story.append(Paragraph("首页中间的快捷操作卡片，点击可快速跳转至对应功能模块，减少菜单层级操作。", S["body"]))
    story.append(PageBreak())


def build_quotation_list(story, S):
    story.extend(section("3. 报价单管理", S))
    story.append(img("03_quotation_list.png", 15*cm))
    story.append(caption("图 3-1  报价单列表", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>报价单管理</b>」进入报价单列表页，支持按状态、类型筛选，支持项目名称关键字搜索。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>功能按钮说明：</b>", S["h3"]))
    data = [[Paragraph("按钮", S["table_hdr"]), Paragraph("功能说明", S["table_hdr"])]]
    for btn, desc in [
        ("+ 新建报价单", "创建新的报价单，填写项目信息/物料明细/费用明细后提交审核。"),
        ("状态筛选",    "下拉选择「全部/草稿/审批中/已通过/已归档」，快速过滤列表。"),
        ("类型筛选",    "下拉选择「全部/线体/项目/备件」，按业务类型过滤。"),
        ("搜索",        "输入项目名称关键字，点击「搜索」按钮进行模糊匹配。"),
    ]:
        data.append([Paragraph(btn, S["table_cell"]), Paragraph(desc, S["table_cell"])])
    story.append(make_table(data, [4*cm, 13*cm]))
    story.append(sp(3*mm))
    story.append(Paragraph("<b>列表操作：</b>", S["h3"]))
    for op in [
        "归档：点击「归档」按钮，将报价单归档封存；",
        "编辑：点击「编辑」按钮，进入报价单编辑页面修改内容；",
        "删除：点击「删除」按钮，弹出确认提示后删除（不可恢复，请谨慎操作）。",
    ]:
        story.append(bullet(op, S))
    story.append(PageBreak())


def build_new_quotation(story, S):
    story.extend(section("4. 新建/编辑报价单", S))
    story.append(img("04_new_quotation.png", 15*cm))
    story.append(caption("图 4-1  新建报价单页面", S))
    story.append(sp())
    story.append(Paragraph("点击报价单列表的「<b>+ 新建报价单</b>」按钮，或在已有报价单上点击「<b>编辑</b>」，进入报价单编辑页面。", S["body"]))
    story.append(sp(2*mm))

    story.extend(subsection("\U0001f4cc 项目信息", S))
    data = [[Paragraph("字段", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for f, d in [
        ("项目名称", "填写项目的名称（必填）"),
        ("方案号",   "系统自动生成，格式为 CSXXXXX"),
        ("客户名称", "填写客户公司/个人名称"),
        ("类型",     "下拉选择「线体/项目/备件」"),
        ("负责人",   "下拉选择系统用户"),
        ("币种",     "下拉选择「人民币/美元/欧元/港币」"),
        ("汇率",     "所选币种对人民币汇率（基准货币人民币 = 1.0000）"),
    ]:
        data.append([Paragraph(f, S["table_cell"]), Paragraph(d, S["table_cell"])])
    story.append(make_hdr_table(data, [3*cm, 14*cm]))
    story.append(sp(3*mm))

    story.extend(subsection("\U0001f4e6 报价明细", S))
    story.append(Paragraph("点击「<b>+ 添加物料</b>」从原材料库选择物料，自动带出规格、品牌、分类、单位和单价。", S["body"]))
    for s in [
        "物料名称：从下拉列表选择原材料库中已有物料；",
        "规格/品牌/分类：自动填充，支持修改；",
        "单价：自动填充原材料库中的单价，支持手动调整；",
        "数量：手动填写；",
        "小计：系统自动计算 = 单价 × 数量；",
        "操作列：点击「删除」移除该行物料。",
    ]:
        story.append(bullet(s, S))
    story.append(sp(2*mm))

    story.extend(subsection("\U0001f4b0 费用明细", S))
    story.append(Paragraph("点击「<b>+ 添加费用</b>」增加费用项目。", S["body"]))
    for s in [
        "费用名称：手动填写费用描述；",
        "费用类型：从下拉列表选择系统已定义的类型（人力费用/物流费用/包装费用/安装费用/其他费用）；",
        "系数：系统自动填入费用类型的默认系数，支持修改；",
        "金额：手动填写；",
        "操作：点击「删除」移除该行费用。",
    ]:
        story.append(bullet(s, S))
    story.append(sp(3*mm))

    story.extend(subsection("\U0001f4ca 金额计算规则", S))
    data = [[Paragraph("计算项", S["table_hdr"]), Paragraph("公式", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for row in [
        ("物料小计", "SUM(单价 × 数量)", "所有物料行小计之和"),
        ("费用小计", "SUM(金额)",        "所有费用行金额之和"),
        ("合计",     "物料小计 + 费用小计", "未税合计金额"),
        ("税额",     "合计 × 税率",      "税率由「费用系数」配置（默认 10%）"),
        ("报价总计", "(物料小计 + 费用小计) × (1 + 税率)", "含税总报价"),
    ]:
        data.append([Paragraph(x, S["table_cell"]) for x in row])
    story.append(make_table(data, [3.5*cm, 6*cm, 7.5*cm]))
    story.append(sp(3*mm))

    story.extend(subsection("\U0001f6b8 操作按钮", S))
    for s in [
        "保存草稿：保存当前填写内容，报价单状态变为「草稿」，可随时继续编辑。",
        "提交审核：提交后报价单状态变为「审批中」，进入审核流程。",
    ]:
        story.append(bullet(s, S))
    story.append(PageBreak())


def build_my_tasks(story, S):
    story.extend(section("5. 我的分配", S))
    story.append(Paragraph("点击侧边栏「<b>\U0001f4cc 我的分配</b>」进入，显示当前登录用户被分配负责的报价单列表。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("功能与「报价单管理」类似，可查看、编辑、导出所负责的报价单。列表中仅显示与当前用户相关的记录，便于快速定位工作内容。", S["body"]))
    story.append(PageBreak())


def build_audit(story, S):
    story.extend(section("6. 变更审核", S))
    story.append(Paragraph("点击侧边栏「<b>\U0001f4e4 变更审核</b>」进入，显示需要当前用户审核的报价单变更申请列表。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("当报价单被提交审核后，审核人会收到通知，可在「变更审核」页面处理。", S["body"]))
    story.append(sp(2*mm))
    data = [[Paragraph("操作", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for op, desc in [
        ("查看", "点击查看变更前后内容对比，了解变更详情"),
        ("通过", "同意变更，报价单更新为新内容"),
        ("驳回", "拒绝变更，报价单维持原内容不变"),
    ]:
        data.append([Paragraph(op, S["table_cell"]), Paragraph(desc, S["table_cell"])])
    story.append(make_table(data, [3*cm, 14*cm]))
    story.append(PageBreak())


def build_materials(story, S):
    story.extend(section("7. 原材料库", S))
    story.append(img("05_materials.png", 15*cm))
    story.append(caption("图 7-1  原材料库管理页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f4e6 原材料库</b>」进入物料管理页面，管理报价单可引用的物料清单。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>物料分类标签（左侧边栏）：</b>", S["h3"]))
    for cat, desc in [
        ("\U0001f4cb 全部",    "显示所有物料（共 22 种）"),
        ("\U0001f4e6 大件",   "大型设备类物料（当前 0 种）"),
        ("\0001f4da 普通件", "普通物料（当前 3 种）"),
        ("\U0001f4ce 其他件", "其他类物料（当前 7 种）"),
    ]:
        story.append(bullet(f"<b>{cat}</b>：{desc}", S))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>功能按钮说明：</b>", S["h3"]))
    data = [[Paragraph("按钮", S["table_hdr"]), Paragraph("功能说明", S["table_hdr"])]]
    for btn, desc in [
        ("+ 新增物料",   "弹出新增物料表单，填写品名/规格/品牌/分类/单位/单价后保存。"),
        ("\U0001f565 批量导入", "下载 Excel 模板，填写后上传批量导入物料数据。"),
        ("\U0001f50d 搜索",    "输入品名/规格/品牌关键字，点击「搜索」快速查找。"),
        ("编辑",         "点击「编辑」修改物料信息；"),
        ("删除",         "点击「删除」移除物料（请确认无报价单引用该物料后再删除）。"),
    ]:
        data.append([Paragraph(btn, S["table_cell"]), Paragraph(desc, S["table_cell"])])
    story.append(make_table(data, [4*cm, 13*cm]))
    story.append(sp(3*mm))
    story.append(Paragraph("<b>物料字段说明：</b>", S["h3"]))
    data = [[Paragraph("字段", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for f, d in [
        ("品名", "物料的名称，如「静电手环」「交换机 8口」"),
        ("规格", "规格型号，如「防静电-S」「SG-8P」"),
        ("品牌", "品牌/厂商，如「3M」「TP-Link」「山泽」"),
        ("分类", "物料分类：大件/普通件/其他件"),
        ("单位", "计量单位：个/盒/卷/套/包/台/根 等"),
        ("单价", "单价（元），人民币"),
    ]:
        data.append([Paragraph(f, S["table_cell"]), Paragraph(d, S["table_cell"])])
    story.append(make_hdr_table(data, [2.5*cm, 14.5*cm]))
    story.append(PageBreak())


def build_cost_types(story, S):
    story.extend(section("8. 费用类型", S))
    story.append(img("06_cost_types.png", 15*cm))
    story.append(caption("图 8-1  费用类型管理页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f4b0 费用类型</b>」进入，管理报价单「费用明细」中可选择的费用项目分类。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("新建报价单时，选择费用类型后系统会自动填入该类型的默认费用系数。", S["body"]))
    story.append(sp(2*mm))
    data = [
        [Paragraph("费用名称", S["table_hdr"]), Paragraph("英文名称 (name_en)", S["table_hdr"]), Paragraph("默认系数", S["table_hdr"])],
        [Paragraph("人力费用", S["table_cell"]), Paragraph("labor_cost", S["table_cell"]), Paragraph("1.00", S["table_cell"])],
        [Paragraph("物流费用", S["table_cell"]), Paragraph("logistics_cost", S["table_cell"]), Paragraph("1.00", S["table_cell"])],
        [Paragraph("包装费用", S["table_cell"]), Paragraph("packaging_cost", S["table_cell"]), Paragraph("1.00", S["table_cell"])],
        [Paragraph("安装费用", S["table_cell"]), Paragraph("installation_cost", S["table_cell"]), Paragraph("1.00", S["table_cell"])],
        [Paragraph("其他费用", S["table_cell"]), Paragraph("other_cost", S["table_cell"]), Paragraph("1.00", S["table_cell"])],
    ]
    story.append(make_table(data, [4*cm, 7*cm, 6*cm]))
    story.append(sp(3*mm))
    for s in ["+ 新增费用类型：新增自定义费用项目；", "编辑：修改费用名称/英文名称/默认系数；", "删除：删除费用类型（已被使用的类型不可删除）。"]:
        story.append(bullet(s, S))
    story.append(PageBreak())


def build_cost_coefficients(story, S):
    story.extend(section("9. 费用系数", S))
    story.append(img("07_cost_coefficients.png", 15*cm))
    story.append(caption("图 9-1  费用系数管理页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f4ca 费用系数</b>」进入，管理系统中各项费用的计算系数。", S["body"]))
    story.append(sp(2*mm))
    data = [
        [Paragraph("系数名称", S["table_hdr"]), Paragraph("英文标识", S["table_hdr"]), Paragraph("系数值", S["table_hdr"]), Paragraph("说明", S["table_hdr"])],
        [Paragraph("税率",     S["table_cell"]), Paragraph("tax_rate",     S["table_cell"]), Paragraph("0.10", S["table_cell"]), Paragraph("10% 税率",     S["table_cell"])],
        [Paragraph("利润率",   S["table_cell"]), Paragraph("profit_rate",  S["table_cell"]), Paragraph("0.15", S["table_cell"]), Paragraph("15% 利润率",   S["table_cell"])],
        [Paragraph("管理费率", S["table_cell"]), Paragraph("admin_rate",   S["table_cell"]), Paragraph("0.05", S["table_cell"]), Paragraph("5% 管理费",    S["table_cell"])],
    ]
    story.append(make_table(data, [3.5*cm, 4*cm, 3*cm, 6.5*cm]))
    story.append(sp(3*mm))
    for s in ["+ 新增系数：添加新的费用系数；", "编辑：修改系数值和说明；", "删除：删除费用系数（系统核心系数不可删除）。"]:
        story.append(bullet(s, S))
    story.append(PageBreak())


def build_exchange_rate(story, S):
    story.extend(section("10. 汇率配置", S))
    story.append(img("08_exchange_rate.png", 15*cm))
    story.append(caption("图 10-1  汇率配置页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f4b1 汇率配置</b>」进入，管理报价系统的适用汇率，支持多币种报价。", S["body"]))
    story.append(sp(2*mm))
    data = [
        [Paragraph("币种名称", S["table_hdr"]), Paragraph("币种代码", S["table_hdr"]), Paragraph("汇率", S["table_hdr"]), Paragraph("备注", S["table_hdr"])],
        [Paragraph("人民币", S["table_cell"]), Paragraph("CNY", S["table_cell"]), Paragraph("1.0000", S["table_cell"]), Paragraph("基准货币", S["table_cell"])],
        [Paragraph("美元",   S["table_cell"]), Paragraph("USD", S["table_cell"]), Paragraph("7.2500",  S["table_cell"]), Paragraph("—", S["table_cell"])],
        [Paragraph("欧元",   S["table_cell"]), Paragraph("EUR", S["table_cell"]), Paragraph("7.8500",  S["table_cell"]), Paragraph("—", S["table_cell"])],
        [Paragraph("港币",   S["table_cell"]), Paragraph("HKD", S["table_cell"]), Paragraph("0.9200",  S["table_cell"]), Paragraph("—", S["table_cell"])],
    ]
    story.append(make_table(data, [3.5*cm, 3.5*cm, 4*cm, 6*cm]))
    story.append(sp(3*mm))
    for s in [
        "人民币（CNY）固定为基准货币，汇率为 1.0000，不可修改；",
        "+ 新增币种：添加新的币种配置；",
        "编辑：修改币种名称和汇率值（注意：修改汇率会影响所有使用该币种的新报价单）；",
        "删除：删除非基准币种。",
    ]:
        story.append(bullet(s, S))
    story.append(PageBreak())


def build_user_management(story, S):
    story.extend(section("11. 用户管理", S))
    story.append(img("09_user_management.png", 15*cm))
    story.append(caption("图 11-1  用户管理页面（共 261 个用户）", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f464 用户管理</b>」进入，管理报价系统用户账号。用户数据与 SQL Server 同步，自动拉取员工部门/职位信息。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>功能说明：</b>", S["h3"]))
    for btn, desc in [
        ("+ 新增用户",  "管理员手动添加系统用户（独立于 SQL Server 同步）；"),
        ("角色筛选",   "点击「全部/管理员/业务员/项目/普通用户」标签快速筛选；"),
        ("\U0001f50d 搜索", "输入姓名或工号关键字搜索；"),
        ("编辑",       "修改用户角色或状态；"),
        ("重置",       "重置用户密码为默认密码（admin123），用户需自行修改。"),
    ]:
        story.append(bullet(f"<b>{btn}</b>：{desc}", S))
    story.append(sp(3*mm))
    story.append(Paragraph("<b>用户字段说明：</b>", S["h3"]))
    data = [[Paragraph("字段", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for f, d in [
        ("工号",     "员工工号（来自 SQL Server 同步）"),
        ("姓名",     "员工姓名（来自 SQL Server 同步）"),
        ("部门",     "员工部门（来自 SQL Server 同步）"),
        ("职位",     "员工职位（来自 SQL Server 同步）"),
        ("角色",     "系统角色：管理员/业务员/项目/普通用户"),
        ("状态",     "在职/离职"),
        ("创建时间", "用户创建时间"),
    ]:
        data.append([Paragraph(f, S["table_cell"]), Paragraph(d, S["table_cell"])])
    story.append(make_hdr_table(data, [2.5*cm, 14.5*cm]))
    story.append(PageBreak())


def build_role_management(story, S):
    story.extend(section("12. 角色管理", S))
    story.append(img("10_role_management.png", 15*cm))
    story.append(caption("图 12-1  角色管理页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f465 角色管理</b>」进入，管理角色及权限分配。", S["body"]))
    story.append(sp(2*mm))
    data = [
        [Paragraph("角色名称", S["table_hdr"]), Paragraph("英文标识", S["table_hdr"]), Paragraph("权限说明", S["table_hdr"])],
        [Paragraph("管理员", S["table_cell"]), Paragraph("admin",           S["table_cell"]), Paragraph("全部功能（增删改查、审核、导出、用户管理、系统配置）", S["table_cell"])],
        [Paragraph("报价员", S["table_cell"]), Paragraph("quotation_staff",  S["table_cell"]), Paragraph("报价单增删改查、提交审核、导出 PDF", S["table_cell"])],
        [Paragraph("审核员", S["table_cell"]), Paragraph("reviewer",         S["table_cell"]), Paragraph("审核报价单变更申请", S["table_cell"])],
        [Paragraph("查看者", S["table_cell"]), Paragraph("viewer",           S["table_cell"]), Paragraph("仅查看报价单，无编辑权限", S["table_cell"])],
    ]
    story.append(make_table(data, [3*cm, 4.5*cm, 9.5*cm]))
    story.append(sp(3*mm))
    for s in ["+ 新增角色：创建自定义角色并配置权限；", "编辑：修改角色名称和权限；", "删除：删除自定义角色（系统内置角色不可删除）。"]:
        story.append(bullet(s, S))
    story.append(PageBreak())


def build_participant_permissions(story, S):
    story.extend(section("13. 参与人权限", S))
    story.append(Paragraph("点击侧边栏「<b>\U0001f510 参与人权限</b>」进入，设置项目中各参与人的数据访问权限。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("管理员可为每个项目指定：", S["body"]))
    for s in [
        "哪些用户可以查看该项目报价单；",
        "哪些用户可以编辑该项目报价单内容；",
        "哪些用户可以审核该项目的变更申请。",
    ]:
        story.append(bullet(s, S))
    story.append(sp(2*mm))
    story.append(Paragraph("通过参与人权限，可以实现项目级数据隔离，确保不同部门/人员只能看到自己负责的项目报价单。", S["body"]))
    story.append(PageBreak())


def build_operation_logs(story, S):
    story.extend(section("14. 操作日志", S))
    story.append(img("11_operation_logs.png", 15*cm))
    story.append(caption("图 14-1  操作日志页面", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏「<b>\U0001f4dd 操作日志</b>」进入，记录所有用户在系统中的操作行为，便于审计追溯。", S["body"]))
    story.append(sp(2*mm))
    data = [[Paragraph("字段", S["table_hdr"]), Paragraph("说明", S["table_hdr"])]]
    for f, d in [
        ("操作时间", "操作发生的具体时间（精确到分钟）"),
        ("用户",     "操作用户的账号"),
        ("操作类型", "操作类型：登录/创建/编辑/删除/导出/审核 等"),
        ("详情",     "操作的具体内容，如「新建报价单 CS00001」「导出 PDF」"),
        ("IP 地址",  "操作用户来源 IP 地址"),
    ]:
        data.append([Paragraph(f, S["table_cell"]), Paragraph(d, S["table_cell"])])
    story.append(make_table(data, [3*cm, 14*cm]))
    story.append(sp(3*mm))
    story.append(Paragraph("日志永久保留，不可删除或修改，可按时间范围和操作类型进行筛选查询。", S["body"]))
    story.append(PageBreak())


def build_password_change(story, S):
    story.extend(section("15. 修改密码与退出", S))
    story.append(img("12_change_password.png", 12*cm))
    story.append(caption("图 15-1  修改密码弹窗", S))
    story.append(sp())
    story.append(Paragraph("点击侧边栏底部「<b>\U0001f511 修改密码</b>」弹出修改密码弹窗。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>操作步骤：</b>", S["body"]))
    for i, s in enumerate([
        "输入当前密码进行验证；",
        "输入新密码（建议 8 位以上，包含字母和数字）；",
        "再次输入新密码确认；",
        "点击「确认修改」保存。",
    ], 1):
        story.append(bullet(f"{i}. {s}", S))
    story.append(sp(4*mm))
    story.append(Paragraph("点击侧边栏底部「<b>\U0001f6aa 退出登录</b>」退出系统，返回登录页面。", S["body"]))
    story.append(PageBreak())


def build_pdf_export(story, S):
    story.extend(section("16. PDF 导出功能", S))
    story.append(Paragraph("在报价单列表或报价单详情页面，点击「<b>导出 PDF</b>」按钮，系统自动生成并下载 PDF 格式报价单文件。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("<b>PDF 内容包含：</b>", S["h3"]))
    for s in [
        "项目名称、方案号、客户名称、负责人；",
        "报价明细（物料清单：品名/规格/品牌/分类/单位/单价/数量/小计）；",
        "费用明细（费用名称/类型/系数/金额）；",
        "物料合计、费用合计、税率、报价总计；",
        "报价时间、有效期（如有）。",
    ]:
        story.append(bullet(s, S))
    story.append(sp(3*mm))
    story.append(Paragraph("<b>语言切换：</b>", S["h3"]))
    story.append(Paragraph("导出时点击语言切换下拉菜单，可选择 <b>中文</b> 或 <b>English</b>，PDF 内容随语言变化，所有中文名称自动翻译为英文。", S["body"]))
    story.append(sp(2*mm))
    story.append(Paragraph("如 PDF 中出现中文乱码，请联系系统管理员安装中文字体支持。", S["body_mid"]))


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    out_pdf = "/home/rs8568/project-quote-system/docs/项目报价系统使用说明书.pdf"
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)

    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm,  bottomMargin=1.5*cm,
        title="项目报价系统 使用说明书",
        author="Project Quote System",
    )

    S = make_styles()
    story = []

    build_cover(story, S)
    build_toc(story, S)
    build_login(story, S)
    build_dashboard(story, S)
    build_quotation_list(story, S)
    build_new_quotation(story, S)
    build_my_tasks(story, S)
    build_audit(story, S)
    build_materials(story, S)
    build_cost_types(story, S)
    build_cost_coefficients(story, S)
    build_exchange_rate(story, S)
    build_user_management(story, S)
    build_role_management(story, S)
    build_participant_permissions(story, S)
    build_operation_logs(story, S)
    build_password_change(story, S)
    build_pdf_export(story, S)

    # Flatten any remaining nested lists
    flat_story = []
    for item in story:
        if isinstance(item, list):
            flat_story.extend(item)
        else:
            flat_story.append(item)

    doc.build(flat_story)
    size_kb = os.path.getsize(out_pdf) / 1024
    print(f"PDF 生成完成：{out_pdf}")
    print(f"文件大小：{size_kb:.0f} KB ({int(size_kb//1024)} MB)")


if __name__ == "__main__":
    main()
