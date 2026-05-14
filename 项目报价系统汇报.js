const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = '项目组';
pres.title = '项目报价系统开发计划与模块设计';
pres.subject = '汇报演示';

// 配色 - 蓝色商务风（参考日报系统）
const COLORS = {
  primary: "1F4E79",      // 深蓝主色
  secondary: "2E75B6",    // 中蓝
  accent: "4472C4",       // 亮蓝
  white: "FFFFFF",
  light: "F5F7FA",
  dark: "2C3E50",
  gray: "7F8C8D",
  lightGray: "ECF0F1",
  orange: "ED7D31",       // 橙色强调
  green: "70AD47"         // 绿色
};

// 工厂函数
const makeShadow = () => ({ type: "outer", blur: 4, offset: 2, angle: 135, color: "000000", opacity: 0.1 });

// ============================================
// Slide 1: 封面
// ============================================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.white };

// 顶部深蓝色块
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 1.2,
  fill: { color: COLORS.primary }
});

// 左侧装饰条
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 1.2, w: 0.15, h: 6.3,
  fill: { color: COLORS.orange }
});

// 主标题
slide1.addText("项目报价系统", {
  x: 0.8, y: 1.8, w: 11.5, h: 1,
  fontSize: 48, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary, align: "center"
});

// 副标题
slide1.addText("开发计划与模块设计", {
  x: 0.8, y: 2.9, w: 11.5, h: 0.6,
  fontSize: 24, fontFace: "Microsoft YaHei",
  color: COLORS.secondary, align: "center"
});

// 分隔线
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 4.5, y: 3.7, w: 4.3, h: 0.04,
  fill: { color: COLORS.orange }
});

// 底部信息
slide1.addText("项目汇报", {
  x: 0.8, y: 4.2, w: 11.5, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei",
  color: COLORS.gray, align: "center"
});

// 右下角装饰
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 11, y: 5.5, w: 2.3, h: 0.08,
  fill: { color: COLORS.orange }
});

// ============================================
// Slide 2: 目录
// ============================================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.light };

// 标题栏
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide2.addText("目  录", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 28, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 目录项
const tocItems = [
  { num: "01", title: "项目背景与目标" },
  { num: "02", title: "系统功能规划" },
  { num: "03", title: "技术架构设计" },
  { num: "04", title: "数据模型设计" },
  { num: "05", title: "开发计划与里程碑" },
  { num: "06", title: "预期成果" }
];

tocItems.forEach((item, i) => {
  const col = i < 3 ? 0 : 1;
  const row = i % 3;
  const x = col === 0 ? 1.5 : 7.5;
  const y = 1.4 + row * 1.3;

  // 编号圆形
  slide2.addShape(pres.shapes.OVAL, {
    x: x, y: y, w: 0.7, h: 0.7,
    fill: { color: COLORS.primary }
  });
  slide2.addText(item.num, {
    x: x, y: y, w: 0.7, h: 0.7,
    fontSize: 16, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  // 标题
  slide2.addText(item.title, {
    x: x + 1, y: y, w: 4, h: 0.7,
    fontSize: 22, fontFace: "Microsoft YaHei",
    color: COLORS.dark, valign: "middle"
  });
});

// Footer
slide2.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide2.addText("2", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 3: 项目背景与目标
// ============================================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.light };

// 标题栏
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide3.addText("01  项目背景与目标", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 左侧卡片 - 项目背景
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 5.9, h: 4.5,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 5.9, h: 0.55,
  fill: { color: COLORS.secondary }
});
slide3.addText("项目背景", {
  x: 0.7, y: 1.25, w: 5.5, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide3.addText([
  { text: "企业报价管理现状：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "• 报价流程分散，效率低下", options: { breakLine: true } },
  { text: "• 物料价格难以统一管理", options: { breakLine: true } },
  { text: "• 版本管理混乱，追溯困难", options: { breakLine: true } },
  { text: "• 审批流程不规范", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "亟需建立统一的报价管理平台", options: { bold: true, color: COLORS.orange } }
], {
  x: 0.7, y: 1.9, w: 5.5, h: 3.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// 右侧卡片 - 项目目标
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 6.9, y: 1.2, w: 5.9, h: 4.5,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 6.9, y: 1.2, w: 5.9, h: 0.55,
  fill: { color: COLORS.accent }
});
slide3.addText("项目目标", {
  x: 7.1, y: 1.25, w: 5.5, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide3.addText([
  { text: "核心目标：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "✓ 建立统一的报价管理平台", options: { breakLine: true } },
  { text: "✓ 实现物料标准化管理", options: { breakLine: true } },
  { text: "✓ 支持版本管理与追溯", options: { breakLine: true } },
  { text: "✓ 规范变更审批流程", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "预期效果：报价周期缩短 50%", options: { bold: true, color: COLORS.green } }
], {
  x: 7.1, y: 1.9, w: 5.5, h: 3.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// Footer
slide3.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide3.addText("3", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 4: 系统功能规划
// ============================================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.light };

// 标题栏
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide4.addText("02  系统功能规划", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 功能模块 2x3
const modules = [
  { icon: "📋", title: "报价单管理", desc: "创建、编辑、归档\n版本历史追踪" },
  { icon: "📦", title: "物料管理", desc: "物料库维护\n分类检索" },
  { icon: "💰", title: "费用管理", desc: "厂内/厂外费用\n费用类型配置" },
  { icon: "🔄", title: "变更申请", desc: "变更审批流程\n状态追踪" },
  { icon: "📊", title: "数据配置", desc: "费用系数\n汇率管理" },
  { icon: "🔔", title: "消息通知", desc: "实时推送\n变更提醒" }
];

modules.forEach((mod, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.5 + col * 4.2;
  const y = 1.2 + row * 2.4;

  // 卡片
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 3.9, h: 2.1,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // 顶部色条
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 3.9, h: 0.08,
    fill: { color: COLORS.accent }
  });

  // 图标
  slide4.addText(mod.icon, {
    x: x + 0.2, y: y + 0.25, w: 0.7, h: 0.7,
    fontSize: 28, align: "center", valign: "middle"
  });

  // 标题
  slide4.addText(mod.title, {
    x: x + 1, y: y + 0.3, w: 2.6, h: 0.5,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary
  });

  // 描述
  slide4.addText(mod.desc, {
    x: x + 1, y: y + 0.9, w: 2.6, h: 1,
    fontSize: 12, fontFace: "Microsoft YaHei",
    color: COLORS.gray
  });
});

// Footer
slide4.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide4.addText("4", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 5: 核心业务流程
// ============================================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.light };

// 标题栏
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide5.addText("02  系统功能规划 - 核心业务流程", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 流程步骤
const steps = [
  { num: "1", title: "创建报价单", desc: "填写项目信息" },
  { num: "2", title: "创建模块", desc: "划分项目模块" },
  { num: "3", title: "选择物料", desc: "从物料库选入" },
  { num: "4", title: "配置费用", desc: "厂内/厂外费用" },
  { num: "5", title: "提交审批", desc: "变更申请流程" },
  { num: "6", title: "归档导出", desc: "生成报价文档" }
];

steps.forEach((step, i) => {
  const x = 0.7 + i * 2.1;

  // 圆形编号
  slide5.addShape(pres.shapes.OVAL, {
    x: x + 0.55, y: 1.3, w: 0.7, h: 0.7,
    fill: { color: COLORS.primary }
  });
  slide5.addText(step.num, {
    x: x + 0.55, y: 1.3, w: 0.7, h: 0.7,
    fontSize: 20, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  // 连接箭头
  if (i < steps.length - 1) {
    slide5.addText("→", {
      x: x + 1.35, y: 1.3, w: 0.6, h: 0.7,
      fontSize: 20, color: COLORS.orange, align: "center", valign: "middle"
    });
  }

  // 标题和描述
  slide5.addText(step.title, {
    x: x, y: 2.15, w: 1.9, h: 0.5,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });
  slide5.addText(step.desc, {
    x: x, y: 2.6, w: 1.9, h: 0.4,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: COLORS.gray, align: "center"
  });
});

// 底部说明卡片
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.4, w: 12.3, h: 3.1,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide5.addText("系统特点", {
  x: 0.8, y: 3.6, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide5.addText([
  { text: "模块化设计：", options: { bold: true, color: COLORS.primary } },
  { text: "报价单下可创建多个模块，每个模块独立管理物料和费用", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "版本控制：", options: { bold: true, color: COLORS.primary } },
  { text: "每次重要操作自动生成版本快照，支持版本回退", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "权限管理：", options: { bold: true, color: COLORS.primary } },
  { text: "基于角色的权限控制，确保数据安全", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "消息驱动：", options: { bold: true, color: COLORS.primary } },
  { text: "变更申请实时通知相关人员" }
], {
  x: 0.8, y: 4.1, w: 11.5, h: 2.2,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// Footer
slide5.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide5.addText("5", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 6: 技术架构设计
// ============================================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.light };

// 标题栏
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide6.addText("03  技术架构设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 三层架构
const layers = [
  { title: "前端层", tech: "Vue 3 + Element Plus + Vite", color: COLORS.accent, y: 1.2 },
  { title: "后端层", tech: "Flask + SQLAlchemy + JWT", color: COLORS.secondary, y: 3.1 },
  { title: "数据层", tech: "PostgreSQL + SQL Server", color: COLORS.orange, y: 5.0 }
];

layers.forEach((layer) => {
  // 层背景
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 8, h: 1.6,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // 左侧色条
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 0.1, h: 1.6,
    fill: { color: layer.color }
  });

  slide6.addText(layer.title, {
    x: 0.8, y: layer.y + 0.2, w: 3, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: layer.color
  });

  slide6.addText(layer.tech, {
    x: 0.8, y: layer.y + 0.8, w: 7, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: COLORS.dark
  });
});

// 右侧技术栈详情
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 9, y: 1.2, w: 3.8, h: 5.4,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 9, y: 1.2, w: 3.8, h: 0.5,
  fill: { color: COLORS.primary }
});
slide6.addText("技术栈详情", {
  x: 9.2, y: 1.25, w: 3.4, h: 0.45,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

slide6.addText([
  { text: "前端", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "Vue 3.4 + Composition API", options: { breakLine: true } },
  { text: "Element Plus 2.6", options: { breakLine: true } },
  { text: "Pinia 状态管理", options: { breakLine: true } },
  { text: "Vue Router 4", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "后端", options: { bold: true, color: COLORS.secondary, breakLine: true } },
  { text: "Flask 3.0", options: { breakLine: true } },
  { text: "SQLAlchemy 2.0 ORM", options: { breakLine: true } },
  { text: "Flask-JWT-Extended", options: { breakLine: true } },
  { text: "APScheduler 定时任务", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "数据库", options: { bold: true, color: COLORS.orange, breakLine: true } },
  { text: "PostgreSQL 主库", options: { breakLine: true } },
  { text: "SQL Server 数据同步" }
], {
  x: 9.2, y: 1.85, w: 3.4, h: 4.5,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// Footer
slide6.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide6.addText("6", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 7: 数据模型设计
// ============================================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.light };

// 标题栏
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide7.addText("04  数据模型设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 核心实体
const entities = [
  { name: "用户", fields: "username, password\nrole, permissions", x: 0.5, y: 1.2 },
  { name: "报价单", fields: "name, status\ntax_rate, version", x: 3.3, y: 1.2 },
  { name: "模块", fields: "name, code\nbusiness_lead\ntechnician_lead", x: 6.1, y: 1.2 },
  { name: "物料", fields: "code, name\nunit_price\ncategory", x: 8.9, y: 1.2 },
  { name: "费用", fields: "fee_type\nlocation\namount", x: 11.7, y: 1.2 }
];

entities.forEach((ent) => {
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.5, h: 1.8,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.5, h: 0.45,
    fill: { color: COLORS.accent }
  });
  slide7.addText(ent.name, {
    x: ent.x, y: ent.y, w: 2.5, h: 0.45,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });
  slide7.addText(ent.fields, {
    x: ent.x + 0.1, y: ent.y + 0.55, w: 2.3, h: 1.15,
    fontSize: 10, fontFace: "Consolas",
    color: COLORS.dark, align: "center", valign: "top"
  });
});

// 连接线
slide7.addShape(pres.shapes.LINE, {
  x: 3.0, y: 2.1, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 5.8, y: 2.1, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 8.6, y: 2.1, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 11.4, y: 2.1, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});

// 关系说明卡片
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.3, w: 12.3, h: 3.2,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide7.addText("关系说明", {
  x: 0.8, y: 3.5, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide7.addText([
  { text: "用户 ", options: { bold: true, color: COLORS.primary } },
  { text: "——< 报价单 >——< 模块 >——< 物料 >", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "核心关系：报价单包含多个模块，模块包含多个物料，支持费用独立配置", options: { color: COLORS.gray, breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "数据模型清单：", options: { bold: true, color: COLORS.primary, breakLine: true } },
  { text: "用户(User) | 报价单(Quotation) | 模块(Module) | 物料(Material) | 费用(Fee)", options: { breakLine: true } },
  { text: "费用类型(FeeType) | 费用系数(FeeRate) | 汇率(ExchangeRate) | 版本(Version)", options: { breakLine: true } },
  { text: "变更申请(ChangeRequest) | 消息(Message) | 操作日志(OperationLog)", options: {} }
], {
  x: 0.8, y: 4.0, w: 11.5, h: 2.3,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// Footer
slide7.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide7.addText("7", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 8: 核心模块详细设计
// ============================================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.light };

// 标题栏
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide8.addText("04  核心模块详细设计", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 四个模块卡片
const detailModules = [
  {
    title: "报价单模块",
    features: ["创建/编辑/删除报价单", "报价单状态流转", "参与人员管理", "归档/撤销归档", "版本快照管理"],
    x: 0.5
  },
  {
    title: "模块管理",
    features: ["创建/编辑/删除模块", "成员任务分配", "业务/技术负责人", "物料选入管理"],
    x: 3.5
  },
  {
    title: "物料管理",
    features: ["物料库 CRUD", "分类管理（大/普通/其他）", "批量导入功能", "启用/禁用状态"],
    x: 6.5
  },
  {
    title: "变更申请",
    features: ["创建变更申请", "审批流程", "批准/拒绝操作", "消息通知", "变更历史追踪"],
    x: 9.5
  }
];

detailModules.forEach((mod) => {
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: mod.x, y: 1.15, w: 2.8, h: 5.3,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: mod.x, y: 1.15, w: 2.8, h: 0.55,
    fill: { color: COLORS.accent }
  });
  slide8.addText(mod.title, {
    x: mod.x, y: 1.15, w: 2.8, h: 0.55,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  slide8.addText(
    mod.features.map((f, i) => ({
      text: "• " + f,
      options: { breakLine: i < mod.features.length - 1 }
    })),
    {
      x: mod.x + 0.15, y: 1.9, w: 2.5, h: 4.3,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: COLORS.dark, valign: "top"
    }
  );
});

// Footer
slide8.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide8.addText("8", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 9: 开发计划与里程碑
// ============================================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.light };

// 标题栏
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide9.addText("05  开发计划与里程碑", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 时间线
const milestones = [
  { week: "第1-2周", title: "基础框架搭建", tasks: "项目初始化\nAPI架构设计\n数据库设计" },
  { week: "第3-4周", title: "核心功能开发", tasks: "用户认证\n报价单管理\n物料管理" },
  { week: "第5-6周", title: "业务模块开发", tasks: "模块管理\n费用管理\n版本控制" },
  { week: "第7-8周", title: "高级功能开发", tasks: "变更申请\n消息通知\n权限管理" },
  { week: "第9-10周", title: "测试与优化", tasks: "功能测试\nBug修复\n文档编写" }
];

milestones.forEach((m, i) => {
  const x = 0.5 + i * 2.5;

  // 圆形节点
  slide9.addShape(pres.shapes.OVAL, {
    x: x + 0.85, y: 1.3, w: 0.5, h: 0.5,
    fill: { color: COLORS.primary }
  });

  // 连接线
  if (i < milestones.length - 1) {
    slide9.addShape(pres.shapes.RECTANGLE, {
      x: x + 1.35, y: 1.52, w: 2, h: 0.06,
      fill: { color: COLORS.lightGray }
    });
  }

  // 周数
  slide9.addText(m.week, {
    x: x, y: 1.95, w: 2.2, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary, align: "center"
  });

  // 标题
  slide9.addText(m.title, {
    x: x, y: 2.35, w: 2.2, h: 0.5,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });

  // 任务卡片
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 2.95, w: 2.2, h: 2.0,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide9.addText(m.tasks, {
    x: x + 0.1, y: 3.05, w: 2.0, h: 1.8,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center", valign: "middle"
  });
});

// 底部总结
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.2, w: 12.3, h: 1.3,
  fill: { color: COLORS.primary }
});
slide9.addText("预计总工期：10周  |  团队规模：3-4人  |  目标：完成 P0 所有功能", {
  x: 0.5, y: 5.35, w: 12.3, h: 0.5,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});
slide9.addText("P0 功能：报价单管理、物料管理、模块管理、费用管理、版本控制、变更申请、权限管理", {
  x: 0.5, y: 5.85, w: 12.3, h: 0.5,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.lightGray, align: "center"
});

// Footer
slide9.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide9.addText("9", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 10: 预期成果
// ============================================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.light };

// 标题栏
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.9,
  fill: { color: COLORS.primary }
});
slide10.addText("06  预期成果", {
  x: 0.5, y: 0.2, w: 12.3, h: 0.6,
  fontSize: 26, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, margin: 0
});

// 左侧装饰条
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.9, w: 0.12, h: 6.135,
  fill: { color: COLORS.orange }
});

// 成果指标
const results = [
  { metric: "50%", label: "报价周期缩短", icon: "⚡" },
  { metric: "100%", label: "流程规范化", icon: "📋" },
  { metric: "实时", label: "消息通知", icon: "🔔" },
  { metric: "追溯", label: "版本管理", icon: "🔙" }
];

results.forEach((r, i) => {
  const x = 0.6 + i * 3.1;

  slide10.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.2, w: 2.9, h: 2.2,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  slide10.addText(r.icon, {
    x: x, y: 1.4, w: 2.9, h: 0.6,
    fontSize: 28, align: "center"
  });

  slide10.addText(r.metric, {
    x: x, y: 2.0, w: 2.9, h: 0.6,
    fontSize: 26, fontFace: "Arial", bold: true,
    color: COLORS.primary, align: "center"
  });

  slide10.addText(r.label, {
    x: x, y: 2.6, w: 2.9, h: 0.5,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center"
  });
});

// 功能清单
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.65, w: 12.3, h: 2.8,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide10.addText("交付清单", {
  x: 0.8, y: 3.85, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide10.addText([
  { text: "✓ 前端 Vue 3 + Element Plus 系统", options: { breakLine: true } },
  { text: "✓ 后端 Flask RESTful API", options: { breakLine: true } },
  { text: "✓ PostgreSQL 数据库设计", options: { breakLine: true } },
  { text: "✓ 用户认证与权限管理", options: { breakLine: true } },
  { text: "✓ 操作日志与审计追踪" }
], {
  x: 0.8, y: 4.35, w: 5.5, h: 1.8,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

slide10.addText([
  { text: "✓ 报价单全生命周期管理", options: { breakLine: true } },
  { text: "✓ 版本控制与回退", options: { breakLine: true } },
  { text: "✓ 变更审批流程", options: { breakLine: true } },
  { text: "✓ 消息通知系统", options: { breakLine: true } },
  { text: "✓ 技术文档与使用手册" }
], {
  x: 6.8, y: 4.35, w: 5.5, h: 1.8,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// Footer
slide10.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.gray
});
slide10.addText("10", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.gray, align: "right"
});

// ============================================
// Slide 11: 结束页
// ============================================
let slide11 = pres.addSlide();
slide11.background = { color: COLORS.primary };

// 装饰
slide11.addShape(pres.shapes.OVAL, {
  x: -2, y: -2, w: 5, h: 5,
  fill: { color: COLORS.secondary, transparency: 60 }
});
slide11.addShape(pres.shapes.OVAL, {
  x: 10, y: 4.5, w: 4, h: 4,
  fill: { color: COLORS.secondary, transparency: 60 }
});

// 左侧装饰条
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.2, h: 7.125,
  fill: { color: COLORS.orange }
});

slide11.addText("感谢聆听", {
  x: 0.5, y: 2.3, w: 12.3, h: 1,
  fontSize: 48, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});

slide11.addText("Q & A", {
  x: 0.5, y: 3.4, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Arial",
  color: COLORS.lightGray, align: "center"
});

// 分隔线
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 4.2, w: 2.3, h: 0.04,
  fill: { color: COLORS.orange }
});

slide11.addText("项目报价系统开发计划与模块设计", {
  x: 0.5, y: 4.5, w: 12.3, h: 0.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.white, align: "center"
});

// Footer
slide11.addText("项目报价系统", {
  x: 0.5, y: 6.8, w: 4, h: 0.4,
  fontSize: 10, color: COLORS.lightGray
});
slide11.addText("11", {
  x: 12.3, y: 6.8, w: 0.5, h: 0.4,
  fontSize: 10, color: COLORS.lightGray, align: "right"
});

// 保存文件
pres.writeFile({ fileName: "/mnt/c/Users/rs8568/Desktop/Project/项目报价系统汇报.pptx" })
  .then(() => console.log("PPT 生成成功！"))
  .catch(err => console.error("生成失败:", err));
