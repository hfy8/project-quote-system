const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = '项目组';
pres.title = '项目报价系统系统设计';

// 配色
const COLORS = {
  primary: "1F4E79",
  secondary: "2E75B6",
  accent: "4472C4",
  white: "FFFFFF",
  light: "F5F7FA",
  dark: "2C3E50",
  gray: "7F8C8D",
  lightGray: "ECF0F1",
  orange: "ED7D31",
  green: "70AD47"
};

const makeShadow = () => ({ type: "outer", blur: 4, offset: 2, angle: 135, color: "000000", opacity: 0.1 });

// ============================================
// Slide 1: 项目背景与目标
// ============================================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.light };

slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide1.addText("ALL---项目报价系统---项目背景与目标", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 左侧卡片
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.15, w: 5.9, h: 5.45,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.15, w: 5.9, h: 0.55,
  fill: { color: COLORS.secondary }
});
slide1.addText("项目背景", {
  x: 0.7, y: 1.2, w: 5.5, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide1.addText([
  { text: "企业报价管理现状：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "• 报价流程分散，效率低下", options: { breakLine: true } },
  { text: "• 物料价格难以统一管理", options: { breakLine: true } },
  { text: "• 版本管理混乱，追溯困难", options: { breakLine: true } },
  { text: "• 审批流程不规范", options: { breakLine: true } },
  { text: "• 变更记录无法追踪", options: { breakLine: true } },
  { text: "• 报价数据难以复用", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "亟需建立统一的报价管理平台", options: { bold: true, color: COLORS.orange } }
], {
  x: 0.7, y: 1.85, w: 5.5, h: 4.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// 右侧卡片
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 6.9, y: 1.15, w: 5.9, h: 5.45,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 6.9, y: 1.15, w: 5.9, h: 0.55,
  fill: { color: COLORS.accent }
});
slide1.addText("项目目标", {
  x: 7.1, y: 1.2, w: 5.5, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide1.addText([
  { text: "核心目标：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "✓ 建立统一的报价管理平台", options: { breakLine: true } },
  { text: "✓ 实现物料标准化管理", options: { breakLine: true } },
  { text: "✓ 支持版本管理与追溯", options: { breakLine: true } },
  { text: "✓ 规范变更审批流程", options: { breakLine: true } },
  { text: "✓ 提升团队协作效率", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "预期效果：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "• 报价周期缩短 50%", options: { breakLine: true } },
  { text: "• 数据追溯率 100%", options: { breakLine: true } },
  { text: "• 审批效率提升 80%", options: { color: COLORS.green } }
], {
  x: 7.1, y: 1.85, w: 5.5, h: 4.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide1.addText("ALL---项目报价系统---项目背景与目标", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide1.addText("3", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 2: 系统功能规划
// ============================================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.light };

slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide2.addText("ALL---项目报价系统---系统功能规划", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const modules = [
  { icon: "📋", title: "报价单管理", features: ["创建/编辑/删除报价单", "状态流转（草稿→审批→归档）", "参与人员管理", "版本快照与回退"] },
  { icon: "📦", title: "物料管理", features: ["物料库 CRUD 操作", "分类管理（大/普通/其他）", "批量导入/导出", "启用/禁用状态控制"] },
  { icon: "💰", title: "费用管理", features: ["厂内费用配置", "厂外费用配置", "费用类型管理", "费用系数设置"] },
  { icon: "🔄", title: "变更申请", features: ["创建变更申请", "审批流程控制", "批准/拒绝操作", "变更历史追踪"] },
  { icon: "⚙️", title: "系统配置", features: ["汇率管理", "税率配置", "用户权限管理", "操作日志审计"] },
  { icon: "🔔", title: "消息通知", features: ["实时消息推送", "变更申请提醒", "审批结果通知", "版本更新通知"] }
];

modules.forEach((mod, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 4.2;
  const y = 1.15 + row * 2.7;

  slide2.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 3.9, h: 2.45,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 3.9, h: 0.5,
    fill: { color: COLORS.accent }
  });
  slide2.addText(mod.icon + " " + mod.title, {
    x: x + 0.15, y: y + 0.05, w: 3.6, h: 0.45,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, margin: 0
  });

  slide2.addText(
    mod.features.map((f, idx) => ({
      text: (idx + 1) + "、" + f,
      options: { breakLine: idx < mod.features.length - 1 }
    })),
    {
      x: x + 0.15, y: y + 0.6, w: 3.6, h: 1.7,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: COLORS.dark, valign: "top"
    }
  );
});

slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide2.addText("ALL---项目报价系统---系统功能规划", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide2.addText("4", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 3: 核心业务流程
// ============================================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.light };

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide3.addText("ALL---项目报价系统---核心业务流程", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const steps = [
  { num: "1", title: "创建报价单", desc: "填写项目名称\n客户信息" },
  { num: "2", title: "创建模块", desc: "划分项目模块\n分配负责人" },
  { num: "3", title: "选择物料", desc: "从物料库选入\n配置数量" },
  { num: "4", title: "配置费用", desc: "厂内/厂外\n费用系数" },
  { num: "5", title: "提交审批", desc: "发起变更申请\n等待审批" },
  { num: "6", title: "归档导出", desc: "审批通过归档\n导出 Word/Excel" }
];

steps.forEach((step, i) => {
  const x = 0.6 + i * 2.1;

  slide3.addShape(pres.shapes.OVAL, {
    x: x + 0.55, y: 1.2, w: 0.7, h: 0.7,
    fill: { color: COLORS.primary }
  });
  slide3.addText(step.num, {
    x: x + 0.55, y: 1.2, w: 0.7, h: 0.7,
    fontSize: 20, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  if (i < steps.length - 1) {
    slide3.addText("→", {
      x: x + 1.35, y: 1.2, w: 0.6, h: 0.7,
      fontSize: 22, color: COLORS.orange, align: "center", valign: "middle"
    });
  }

  slide3.addText(step.title, {
    x: x, y: 2.05, w: 1.9, h: 0.5,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });
  slide3.addText(step.desc, {
    x: x, y: 2.55, w: 1.9, h: 0.8,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: COLORS.gray, align: "center"
  });
});

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.55, w: 12.3, h: 3.05,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide3.addText("核心概念说明", {
  x: 0.8, y: 3.75, w: 4, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide3.addText([
  { text: "报价单 (Quotation)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "项目报价的顶层容器，包含多个模块，支持版本管理", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "模块 (Module)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "报价单下的子项目，可分配业务/技术负责人", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "物料 (Material)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "标准化的产品/服务项，从物料库选择", options: {} }
], {
  x: 0.8, y: 4.25, w: 5.5, h: 2.1,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide3.addText([
  { text: "费用 (Fee)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "厂内/厂外费用，支持费用系数计算", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "版本 (Version)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "每次重要操作自动生成快照，支持回退", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "变更申请 (ChangeRequest)", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "审批流程的核心，追踪变更历史", options: {} }
], {
  x: 6.8, y: 4.25, w: 5.5, h: 2.1,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide3.addText("ALL---项目报价系统---核心业务流程", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide3.addText("5", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 4: 技术架构设计
// ============================================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.light };

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide4.addText("ALL---项目报价系统---技术架构设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const layers = [
  { title: "前端层 Frontend", tech: "Vue 3 + Element Plus + Vite", color: COLORS.accent, y: 1.15 },
  { title: "后端层 Backend", tech: "Flask + SQLAlchemy + JWT", color: COLORS.secondary, y: 2.95 },
  { title: "数据层 Data", tech: "PostgreSQL + SQL Server", color: COLORS.orange, y: 4.75 }
];

layers.forEach((layer) => {
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 8, h: 1.55,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 0.1, h: 1.55,
    fill: { color: layer.color }
  });
  slide4.addText(layer.title, {
    x: 0.8, y: layer.y + 0.2, w: 7, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: layer.color
  });
  slide4.addText(layer.tech, {
    x: 0.8, y: layer.y + 0.8, w: 7, h: 0.5,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: COLORS.dark
  });
});

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 9, y: 1.15, w: 3.8, h: 5.35,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 9, y: 1.15, w: 3.8, h: 0.5,
  fill: { color: COLORS.primary }
});
slide4.addText("技术栈详情", {
  x: 9.2, y: 1.2, w: 3.4, h: 0.45,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide4.addText([
  { text: "前端技术", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "Vue 3.4 + Composition API", options: { breakLine: true } },
  { text: "Element Plus 2.6", options: { breakLine: true } },
  { text: "Pinia 状态管理", options: { breakLine: true } },
  { text: "Vue Router 4", options: { breakLine: true } },
  { text: "Axios HTTP 客户端", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "后端技术", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "Flask 3.0", options: { breakLine: true } },
  { text: "SQLAlchemy 2.0 ORM", options: { breakLine: true } },
  { text: "Flask-JWT-Extended", options: { breakLine: true } },
  { text: "Flask-CORS 跨域支持", options: { breakLine: true } },
  { text: "APScheduler 定时任务", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "数据库", options: { bold: true, color: COLORS.orange, breakLine: true } },
  { text: "PostgreSQL 主库", options: { breakLine: true } },
  { text: "SQL Server 数据同步" }
], {
  x: 9.2, y: 1.8, w: 3.4, h: 4.5,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide4.addText("ALL---项目报价系统---技术架构设计", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide4.addText("6", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 5: 数据模型设计
// ============================================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.light };

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide5.addText("ALL---项目报价系统---数据模型设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const entities = [
  { name: "用户", nameEn: "User", fields: "username\npassword\nrole", x: 0.5, y: 1.15 },
  { name: "报价单", nameEn: "Quotation", fields: "name\nstatus\ntax_rate", x: 3.3, y: 1.15 },
  { name: "模块", nameEn: "Module", fields: "name\ncode", x: 6.1, y: 1.15 },
  { name: "物料", nameEn: "Material", fields: "code\nname\nunit_price", x: 8.9, y: 1.15 },
  { name: "费用", nameEn: "Fee", fields: "fee_type\nlocation", x: 11.7, y: 1.15 }
];

entities.forEach((ent) => {
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.5, h: 1.9,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide5.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.5, h: 0.5,
    fill: { color: COLORS.accent }
  });
  slide5.addText(ent.name, {
    x: ent.x, y: ent.y, w: 2.5, h: 0.35,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });
  slide5.addText(ent.nameEn, {
    x: ent.x, y: ent.y + 0.28, w: 2.5, h: 0.22,
    fontSize: 8, fontFace: "Arial",
    color: COLORS.white, align: "center", valign: "middle"
  });
  slide5.addText(ent.fields, {
    x: ent.x + 0.1, y: ent.y + 0.6, w: 2.3, h: 1.2,
    fontSize: 10, fontFace: "Consolas",
    color: COLORS.dark, align: "center", valign: "top"
  });
});

[2.9, 5.7, 8.5, 11.3].forEach((x) => {
  slide5.addShape(pres.shapes.LINE, {
    x: x, y: 2.1, w: 0.4, h: 0,
    line: { color: COLORS.primary, width: 2 }
  });
});

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.3, w: 12.3, h: 3.3,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide5.addText("数据模型清单（共 17 个模型）", {
  x: 0.8, y: 3.5, w: 6, h: 0.5,
  fontSize: 15, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide5.addText([
  { text: "• User - 用户", options: { breakLine: true } },
  { text: "• Quotation - 报价单", options: { breakLine: true } },
  { text: "• Module - 模块", options: { breakLine: true } },
  { text: "• Material - 物料", options: { breakLine: true } },
  { text: "• MaterialCategory - 物料分类", options: { breakLine: true } },
  { text: "• Fee - 费用", options: { breakLine: true } },
  { text: "• FeeType - 费用类型", options: { breakLine: true } },
  { text: "• FeeRate - 费用系数", options: { breakLine: true } },
  { text: "• ExchangeRate - 汇率", options: {} }
], {
  x: 0.8, y: 4.0, w: 4, h: 2.4,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide5.addText([
  { text: "• Version - 版本快照", options: { breakLine: true } },
  { text: "• ChangeRequest - 变更申请", options: { breakLine: true } },
  { text: "• ChangeRequestItem - 变更项", options: { breakLine: true } },
  { text: "• Message - 消息", options: { breakLine: true } },
  { text: "• OperationLog - 操作日志", options: { breakLine: true } },
  { text: "• Role - 角色", options: { breakLine: true } },
  { text: "• Permission - 权限", options: { breakLine: true } },
  { text: "• Department - 部门（同步）", options: { breakLine: true } },
  { text: "• Position - 职位（同步）", options: {} }
], {
  x: 5, y: 4.0, w: 4.5, h: 2.4,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide5.addText("ALL---项目报价系统---数据模型设计", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide5.addText("7", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 6: 核心模块详细设计
// ============================================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.light };

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide6.addText("ALL---项目报价系统---核心模块详细设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const detailModules = [
  {
    title: "报价单模块",
    features: ["创建/编辑/删除报价单", "报价单状态流转", "参与人员管理", "归档/撤销归档", "版本快照管理", "复制报价单", "导出 Word/Excel/PDF"]
  },
  {
    title: "模块管理",
    features: ["创建/编辑/删除模块", "成员任务分配", "业务负责人配置", "技术负责人配置", "物料选入管理", "费用配置"]
  },
  {
    title: "物料管理",
    features: ["物料库 CRUD", "分类管理（大/普通/其他）", "批量导入功能", "启用/禁用状态", "物料参数配置", "价格维护"]
  },
  {
    title: "变更申请",
    features: ["创建变更申请", "审批流程控制", "批准/拒绝操作", "变更历史追踪", "消息通知相关人", "变更项管理"]
  }
];

detailModules.forEach((mod, i) => {
  const x = 0.5 + i * 3.15;
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.15, w: 3.0, h: 5.45,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.15, w: 3.0, h: 0.55,
    fill: { color: COLORS.accent }
  });
  slide6.addText(mod.title, {
    x: x, y: 1.15, w: 3.0, h: 0.55,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  slide6.addText(
    mod.features.map((f, idx) => ({
      text: (idx + 1) + "、" + f,
      options: { breakLine: idx < mod.features.length - 1 }
    })),
    {
      x: x + 0.1, y: 1.85, w: 2.8, h: 4.5,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: COLORS.dark, valign: "top"
    }
  );
});

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide6.addText("ALL---项目报价系统---核心模块详细设计", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide6.addText("8", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 7: API 接口设计
// ============================================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.light };

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide7.addText("ALL---项目报价系统---API 接口设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.15, w: 12.3, h: 5.45,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide7.addText("主要 API 模块（共 17 个接口文件）", {
  x: 0.8, y: 1.35, w: 6, h: 0.5,
  fontSize: 15, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide7.addText([
  { text: "认证模块", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "POST /api/auth/login - 登录", options: { breakLine: true } },
  { text: "POST /api/auth/logout - 登出", options: { breakLine: true } },
  { text: "PUT /api/auth/change-password - 修改密码", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "报价单模块", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET/POST /api/quotations - 列表/创建", options: { breakLine: true } },
  { text: "GET/PUT/DELETE /api/quotations/:id", options: { breakLine: true } },
  { text: "POST /api/quotations/:id/archive", options: { breakLine: true } },
  { text: "POST /api/quotations/:id/copy", options: { breakLine: true } },
  { text: "GET /api/quotations/:id/versions", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "模块管理", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET/POST /api/modules - 列表/创建", options: { breakLine: true } },
  { text: "GET/PUT/DELETE /api/modules/:id", options: { breakLine: true } },
  { text: "POST /api/modules/:id/materials", options: { breakLine: true } },
  { text: "POST /api/modules/:id/fees", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "物料管理", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET/POST /api/materials - 列表/创建", options: { breakLine: true } },
  { text: "POST /api/materials/import - 导入", options: {} }
], {
  x: 0.8, y: 1.9, w: 5.5, h: 4.5,
  fontSize: 10, fontFace: "Consolas",
  color: COLORS.dark, valign: "top"
});

slide7.addText([
  { text: "费用管理", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET/POST /api/fees - 列表/创建", options: { breakLine: true } },
  { text: "GET/PUT/DELETE /api/fees/:id", options: { breakLine: true } },
  { text: "GET/POST /api/fee-types", options: { breakLine: true } },
  { text: "GET/POST /api/fee-rates", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "变更申请", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET/POST /api/change-requests", options: { breakLine: true } },
  { text: "PUT /api/change-requests/:id/approve", options: { breakLine: true } },
  { text: "PUT /api/change-requests/:id/reject", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "版本管理", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET /api/versions/:id", options: { breakLine: true } },
  { text: "POST /api/versions/:id/rollback", options: { breakLine: true } },
  { text: "GET /api/versions/:id/compare/:other_id", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "其他模块", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "GET /api/exchange-rates", options: { breakLine: true } },
  { text: "GET /api/logs", options: { breakLine: true } },
  { text: "GET /api/messages", options: { breakLine: true } },
  { text: "GET /api/users, /api/departments", options: {} }
], {
  x: 6.5, y: 1.9, w: 6, h: 4.5,
  fontSize: 10, fontFace: "Consolas",
  color: COLORS.dark, valign: "top"
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide7.addText("ALL---项目报价系统---API 接口设计", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide7.addText("9", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 8: 开发计划与里程碑
// ============================================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.light };

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide8.addText("ALL---项目报价系统---开发计划与里程碑", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const milestones = [
  { week: "第1-2周", title: "基础框架搭建", tasks: "1. 项目初始化配置\n2. API 架构设计\n3. 数据库设计\n4. 认证模块开发" },
  { week: "第3-4周", title: "核心功能开发", tasks: "1. 报价单管理\n2. 模块管理\n3. 物料管理\n4. 费用管理" },
  { week: "第5-6周", title: "高级功能开发", tasks: "1. 版本控制\n2. 变更申请\n3. 消息通知\n4. 权限管理" },
  { week: "第7-8周", title: "系统集成", tasks: "1. 数据同步\n2. 导出功能\n3. 界面优化\n4. 性能优化" },
  { week: "第9-10周", title: "测试与上线", tasks: "1. 功能测试\n2. Bug 修复\n3. 文档编写\n4. 部署上线" }
];

milestones.forEach((m, i) => {
  const x = 0.5 + i * 2.5;

  slide8.addShape(pres.shapes.OVAL, {
    x: x + 0.85, y: 1.2, w: 0.5, h: 0.5,
    fill: { color: COLORS.primary }
  });

  if (i < milestones.length - 1) {
    slide8.addShape(pres.shapes.RECTANGLE, {
      x: x + 1.35, y: 1.42, w: 2, h: 0.06,
      fill: { color: COLORS.lightGray }
    });
  }

  slide8.addText(m.week, {
    x: x, y: 1.85, w: 2.2, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary, align: "center"
  });

  slide8.addText(m.title, {
    x: x, y: 2.25, w: 2.2, h: 0.45,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });

  slide8.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 2.8, w: 2.2, h: 2.6,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide8.addText(m.tasks, {
    x: x + 0.1, y: 2.9, w: 2.0, h: 2.4,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "left", valign: "top"
  });
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.6, w: 12.3, h: 1.0,
  fill: { color: COLORS.primary }
});
slide8.addText("预计总工期：10周  |  团队规模：3-4人  |  目标：完成 P0 所有功能并上线", {
  x: 0.5, y: 5.7, w: 12.3, h: 0.4,
  fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});
slide8.addText("P0：报价单管理 | 物料管理 | 模块管理 | 费用管理 | 版本控制 | 变更申请 | 权限管理", {
  x: 0.5, y: 6.1, w: 12.3, h: 0.4,
  fontSize: 10, fontFace: "Microsoft YaHei",
  color: COLORS.lightGray, align: "center"
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide8.addText("ALL---项目报价系统---开发计划与里程碑", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide8.addText("10", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 9: 预期成果
// ============================================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.light };

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide9.addText("ALL---项目报价系统---预期成果", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

const results = [
  { metric: "50%", label: "报价周期缩短", icon: "⚡" },
  { metric: "100%", label: "流程规范化", icon: "📋" },
  { metric: "实时", label: "消息通知", icon: "🔔" },
  { metric: "追溯", label: "版本管理", icon: "🔙" }
];

results.forEach((r, i) => {
  const x = 0.55 + i * 3.1;

  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.15, w: 2.95, h: 1.8,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  slide9.addText(r.icon, {
    x: x, y: 1.3, w: 2.95, h: 0.5,
    fontSize: 24, align: "center"
  });

  slide9.addText(r.metric, {
    x: x, y: 1.8, w: 2.95, h: 0.55,
    fontSize: 24, fontFace: "Arial", bold: true,
    color: COLORS.primary, align: "center"
  });

  slide9.addText(r.label, {
    x: x, y: 2.35, w: 2.95, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center"
  });
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.2, w: 12.3, h: 3.4,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide9.addText("交付清单", {
  x: 0.8, y: 3.4, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide9.addText([
  { text: "✓ 前端 Vue 3 + Element Plus 系统", options: { breakLine: true } },
  { text: "✓ 后端 Flask RESTful API", options: { breakLine: true } },
  { text: "✓ PostgreSQL 数据库设计", options: { breakLine: true } },
  { text: "✓ 用户认证与权限管理", options: { breakLine: true } },
  { text: "✓ 操作日志与审计追踪", options: { breakLine: true } },
  { text: "✓ 报价单全生命周期管理", options: { breakLine: true } },
  { text: "✓ 版本控制与回退", options: {} }
], {
  x: 0.8, y: 3.9, w: 5.5, h: 2.4,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide9.addText([
  { text: "✓ 变更审批流程", options: { breakLine: true } },
  { text: "✓ 消息通知系统", options: { breakLine: true } },
  { text: "✓ Word/Excel/PDF 导出", options: { breakLine: true } },
  { text: "✓ 数据同步功能", options: { breakLine: true } },
  { text: "✓ 响应式界面设计", options: { breakLine: true } },
  { text: "✓ 技术文档与使用手册", options: { breakLine: true } },
  { text: "✓ 培训与上线支持", options: {} }
], {
  x: 6.8, y: 3.9, w: 5.5, h: 2.4,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.primary }
});
slide9.addText("ALL---项目报价系统---预期成果", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide9.addText("11", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// ============================================
// Slide 10: 结束页
// ============================================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.primary };

slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.2, h: 7.125,
  fill: { color: COLORS.orange }
});

slide10.addShape(pres.shapes.OVAL, {
  x: -2, y: -2, w: 5, h: 5,
  fill: { color: COLORS.secondary, transparency: 60 }
});
slide10.addShape(pres.shapes.OVAL, {
  x: 10, y: 4.5, w: 4, h: 4,
  fill: { color: COLORS.secondary, transparency: 60 }
});

slide10.addText("感谢聆听", {
  x: 0.5, y: 2.5, w: 12.3, h: 1,
  fontSize: 48, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});

slide10.addText("Q & A", {
  x: 0.5, y: 3.6, w: 12.3, h: 0.6,
  fontSize: 28, fontFace: "Arial",
  color: COLORS.lightGray, align: "center"
});

slide10.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 4.4, w: 2.3, h: 0.05,
  fill: { color: COLORS.orange }
});

slide10.addText("项目报价系统开发计划与模块设计", {
  x: 0.5, y: 4.7, w: 12.3, h: 0.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.white, align: "center"
});

slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 6.9, w: 13.3, h: 0.225,
  fill: { color: COLORS.secondary }
});
slide10.addText("ALL---项目报价系统", {
  x: 0.5, y: 6.9, w: 5, h: 0.225,
  fontSize: 9, color: COLORS.white, valign: "middle", margin: 0
});
slide10.addText("12", {
  x: 12.3, y: 6.9, w: 0.5, h: 0.225,
  fontSize: 9, color: COLORS.white, align: "right", valign: "middle", margin: 0
});

// 保存文件 - 续页（从第3页开始，共10页）
pres.writeFile({ fileName: "/mnt/c/Users/rs8568/Desktop/Project/项目报价系统_内容续页.pptx" })
  .then(() => console.log("续页PPT生成成功！"))
  .catch(err => console.error("生成失败:", err));
