const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';  // 13.3" x 7.5"
pres.author = '项目组';
pres.title = '项目报价系统开发计划与模块设计';
pres.subject = '汇报演示';

// 配色方案 - Teal Trust 清新商务风
const COLORS = {
  primary: "0D9488",      // 主色 - 青色
  secondary: "14B8A6",    // 辅助色
  accent: "F59E0B",       // 强调色 - 琥珀
  dark: "1E293B",         // 深色文字
  light: "F8FAFC",        // 浅色背景
  white: "FFFFFF",
  gray: "64748B",
  lightGray: "E2E8F0",
  tealLight: "CCFBF1"
};

// 工厂函数避免对象复用问题
const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

// ============================================
// Slide 1: 封面
// ============================================
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

// 装饰圆形
slide1.addShape(pres.shapes.OVAL, {
  x: -1.5, y: -1.5, w: 4, h: 4,
  fill: { color: COLORS.secondary, transparency: 50 }
});
slide1.addShape(pres.shapes.OVAL, {
  x: 10.5, y: 5, w: 4, h: 4,
  fill: { color: COLORS.secondary, transparency: 50 }
});

// 标题
slide1.addText("项目报价系统", {
  x: 0.5, y: 2.2, w: 12.3, h: 1.2,
  fontSize: 54, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});

slide1.addText("开发计划与模块设计", {
  x: 0.5, y: 3.5, w: 12.3, h: 0.7,
  fontSize: 28, fontFace: "Microsoft YaHei",
  color: COLORS.tealLight, align: "center"
});

// 分隔线
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 5, y: 4.4, w: 3.3, h: 0.05,
  fill: { color: COLORS.accent }
});

slide1.addText("项目汇报", {
  x: 0.5, y: 5, w: 12.3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei",
  color: COLORS.white, align: "center"
});

// ============================================
// Slide 2: 目录
// ============================================
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.light };

slide2.addText("目录", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 36, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 1.2, h: 0.06,
  fill: { color: COLORS.primary }
});

const tocItems = [
  { num: "01", title: "项目背景与目标" },
  { num: "02", title: "系统功能规划" },
  { num: "03", title: "技术架构设计" },
  { num: "04", title: "数据模型设计" },
  { num: "05", title: "开发计划与里程碑" },
  { num: "06", title: "预期成果" }
];

tocItems.forEach((item, i) => {
  const y = 1.6 + i * 0.85;
  const col = i < 3 ? 0 : 1;
  const x = col === 0 ? 0.8 : 7;

  // 编号圆形
  slide2.addShape(pres.shapes.OVAL, {
    x: x, y: y, w: 0.6, h: 0.6,
    fill: { color: COLORS.primary }
  });
  slide2.addText(item.num, {
    x: x, y: y, w: 0.6, h: 0.6,
    fontSize: 14, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  slide2.addText(item.title, {
    x: x + 0.8, y: y, w: 4, h: 0.6,
    fontSize: 20, fontFace: "Microsoft YaHei",
    color: COLORS.dark, valign: "middle"
  });
});

// ============================================
// Slide 3: 项目背景
// ============================================
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.light };

// 顶部色带
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide3.addText("项目背景与目标", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 左侧卡片 - 背景
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 5.8, h: 3.8,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.4, w: 0.08, h: 3.8,
  fill: { color: COLORS.primary }
});

slide3.addText("项目背景", {
  x: 0.8, y: 1.6, w: 5.2, h: 0.5,
  fontSize: 20, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide3.addText([
  { text: "企业报价管理现状：", options: { bold: true, breakLine: true } },
  { text: "• 报价流程分散，效率低下", options: { breakLine: true } },
  { text: "• 物料价格难以统一管理", options: { breakLine: true } },
  { text: "• 版本管理混乱，追溯困难", options: { breakLine: true } },
  { text: "• 审批流程不规范", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "亟需一套统一的报价管理系统", options: { bold: true, color: COLORS.accent } }
], {
  x: 0.8, y: 2.2, w: 5.2, h: 2.8,
  fontSize: 15, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// 右侧卡片 - 目标
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 1.4, w: 6, h: 3.8,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 1.4, w: 0.08, h: 3.8,
  fill: { color: COLORS.secondary }
});

slide3.addText("项目目标", {
  x: 7.1, y: 1.6, w: 5.4, h: 0.5,
  fontSize: 20, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.secondary
});

slide3.addText([
  { text: "核心目标：", options: { bold: true, breakLine: true } },
  { text: "✓ 建立统一的报价管理平台", options: { breakLine: true } },
  { text: "✓ 实现物料标准化管理", options: { breakLine: true } },
  { text: "✓ 支持版本管理与追溯", options: { breakLine: true } },
  { text: "✓ 规范变更审批流程", options: { breakLine: true } },
  { text: "✓ 提升团队协作效率", options: { breakLine: true } },
  { text: "", options: { breakLine: true } },
  { text: "预期效果：报价周期缩短 50%", options: { bold: true, color: COLORS.primary } }
], {
  x: 7.1, y: 2.2, w: 5.4, h: 2.8,
  fontSize: 15, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// ============================================
// Slide 4: 系统功能规划
// ============================================
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.light };

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide4.addText("系统功能规划", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 功能模块网格 2x3
const modules = [
  { icon: "📋", title: "报价单管理", desc: "创建、编辑、归档\n版本历史追踪" },
  { icon: "📦", title: "物料管理", desc: "物料库维护\n分类检索" },
  { icon: "💰", title: "费用管理", desc: "厂内/厂外费用\n费用类型配置" },
  { icon: "🔄", title: "变更申请", desc: "变更审批流程\n状态追踪" },
  { icon: "📊", title: "数据报表", desc: "费用系数配置\n汇率管理" },
  { icon: "🔔", title: "消息通知", desc: "实时推送\n变更提醒" }
];

modules.forEach((mod, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  const x = 0.6 + col * 4.2;
  const y = 1.4 + row * 2.4;

  // 卡片
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 3.9, h: 2.1,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // 图标圆形背景
  slide4.addShape(pres.shapes.OVAL, {
    x: x + 0.25, y: y + 0.3, w: 0.8, h: 0.8,
    fill: { color: COLORS.tealLight }
  });

  slide4.addText(mod.icon, {
    x: x + 0.25, y: y + 0.3, w: 0.8, h: 0.8,
    fontSize: 24, align: "center", valign: "middle"
  });

  slide4.addText(mod.title, {
    x: x + 1.2, y: y + 0.35, w: 2.4, h: 0.5,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark
  });

  slide4.addText(mod.desc, {
    x: x + 1.2, y: y + 0.9, w: 2.4, h: 1,
    fontSize: 12, fontFace: "Microsoft YaHei",
    color: COLORS.gray
  });
});

// ============================================
// Slide 5: 业务流程
// ============================================
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.light };

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide5.addText("核心业务流程", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
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

const stepWidth = 1.9;
const startX = 0.7;

steps.forEach((step, i) => {
  const x = startX + i * 2.1;

  // 圆形编号
  slide5.addShape(pres.shapes.OVAL, {
    x: x + 0.55, y: 1.5, w: 0.7, h: 0.7,
    fill: { color: COLORS.primary }
  });
  slide5.addText(step.num, {
    x: x + 0.55, y: 1.5, w: 0.7, h: 0.7,
    fontSize: 20, fontFace: "Arial", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  // 连接箭头
  if (i < steps.length - 1) {
    slide5.addShape(pres.shapes.RECTANGLE, {
      x: x + 1.35, y: 1.8, w: 0.65, h: 0.06,
      fill: { color: COLORS.lightGray }
    });
    slide5.addText("→", {
      x: x + 1.75, y: 1.55, w: 0.4, h: 0.5,
      fontSize: 16, color: COLORS.primary, align: "center"
    });
  }

  // 标题和描述
  slide5.addText(step.title, {
    x: x, y: 2.4, w: stepWidth, h: 0.5,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });
  slide5.addText(step.desc, {
    x: x, y: 2.9, w: stepWidth, h: 0.4,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: COLORS.gray, align: "center"
  });
});

// 底部说明卡片
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.8, w: 12.3, h: 2.3,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide5.addText("系统特点", {
  x: 0.8, y: 4, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide5.addText([
  { text: "模块化设计：", options: { bold: true } },
  { text: "报价单下可创建多个模块，每个模块独立管理物料和费用", options: { breakLine: true } },
  { text: "版本控制：", options: { bold: true } },
  { text: "每次重要操作自动生成版本快照，支持版本回退", options: { breakLine: true } },
  { text: "权限管理：", options: { bold: true } },
  { text: "基于角色的权限控制，确保数据安全", options: { breakLine: true } },
  { text: "消息驱动：", options: { bold: true } },
  { text: "变更申请实时通知相关人员" }
], {
  x: 0.8, y: 4.5, w: 11.5, h: 1.5,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// ============================================
// Slide 6: 技术架构
// ============================================
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.light };

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide6.addText("技术架构设计", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 三层架构
const layers = [
  { title: "前端层", tech: "Vue 3 + Element Plus + Vite", color: COLORS.primary, y: 1.4 },
  { title: "后端层", tech: "Flask + SQLAlchemy + JWT", color: COLORS.secondary, y: 3.3 },
  { title: "数据层", tech: "PostgreSQL + SQL Server", color: COLORS.accent, y: 5.2 }
];

layers.forEach((layer) => {
  // 层背景
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 8, h: 1.5,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  // 左侧色条
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: layer.y, w: 0.1, h: 1.5,
    fill: { color: layer.color }
  });

  slide6.addText(layer.title, {
    x: 0.8, y: layer.y + 0.2, w: 3, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
    color: layer.color
  });

  slide6.addText(layer.tech, {
    x: 0.8, y: layer.y + 0.7, w: 7, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: COLORS.dark
  });
});

// 右侧技术栈详情
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 9, y: 1.4, w: 3.8, h: 5.3,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide6.addText("技术栈详情", {
  x: 9.2, y: 1.6, w: 3.4, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide6.addText([
  { text: "前端", options: { bold: true, color: COLORS.primary, breakLine: true } },
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
  { text: "数据库", options: { bold: true, color: COLORS.accent, breakLine: true } },
  { text: "PostgreSQL 主库", options: { breakLine: true } },
  { text: "SQL Server 数据同步" }
], {
  x: 9.2, y: 2.2, w: 3.4, h: 4.2,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// ============================================
// Slide 7: 数据模型
// ============================================
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.light };

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide7.addText("数据模型设计", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 核心实体
const entities = [
  { name: "用户", fields: "username, password\nrole, permissions", x: 0.5, y: 1.3 },
  { name: "报价单", fields: "name, status\ntax_rate, version", x: 3.2, y: 1.3 },
  { name: "模块", fields: "name, code\nbusiness_lead\ntechnician_lead", x: 5.9, y: 1.3 },
  { name: "物料", fields: "code, name\nunit_price\ncategory", x: 8.6, y: 1.3 },
  { name: "费用", fields: "fee_type\nlocation\namount", x: 11.3, y: 1.3 }
];

entities.forEach((ent) => {
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.4, h: 2.0,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: ent.x, y: ent.y, w: 2.4, h: 0.5,
    fill: { color: COLORS.primary }
  });
  slide7.addText(ent.name, {
    x: ent.x, y: ent.y, w: 2.4, h: 0.5,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });
  slide7.addText(ent.fields, {
    x: ent.x + 0.1, y: ent.y + 0.6, w: 2.2, h: 1.3,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center", valign: "top"
  });
});

// 关系线
slide7.addShape(pres.shapes.LINE, {
  x: 2.9, y: 2.3, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 5.6, y: 2.3, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 8.3, y: 2.3, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});
slide7.addShape(pres.shapes.LINE, {
  x: 11.0, y: 2.3, w: 0.3, h: 0,
  line: { color: COLORS.primary, width: 2 }
});

// 底部说明
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.6, w: 12.3, h: 2.5,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide7.addText("关系说明", {
  x: 0.8, y: 3.8, w: 3, h: 0.5,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary
});

slide7.addText([
  { text: "用户 ", options: { bold: true, color: COLORS.primary } },
  { text: "——< 报价单 >——< 模块 >——< 物料 >", options: { breakLine: true } },
  { text: "       ", options: {} },
  { text: "          │                    │", options: { breakLine: true } },
  { text: "       参与人                数量/单价", options: { breakLine: true } },
  { text: "                        │", options: { breakLine: true } },
  { text: "                     费用", options: {} },
  { text: "", options: { breakLine: true } },
  { text: "版本快照：", options: { bold: true, color: COLORS.secondary } },
  { text: "每次操作自动记录版本，支持回退和对比", options: {} }
], {
  x: 0.8, y: 4.3, w: 11.5, h: 1.6,
  fontSize: 12, fontFace: "Consolas",
  color: COLORS.dark, valign: "top"
});

// ============================================
// Slide 8: 模块详细设计
// ============================================
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.light };

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide8.addText("核心模块详细设计", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 四个模块卡片
const detailModules = [
  {
    title: "报价单模块",
    features: ["创建/编辑/删除报价单", "报价单状态流转", "参与人员管理", "归档/撤销归档"],
    x: 0.5
  },
  {
    title: "模块管理",
    features: ["创建/编辑/删除模块", "成员任务分配", "业务/技术负责人", "物料选入"],
    x: 3.7
  },
  {
    title: "物料管理",
    features: ["物料库 CRUD", "分类管理（大/普通/其他）", "批量导入功能", "启用/禁用状态"],
    x: 6.9
  },
  {
    title: "变更申请",
    features: ["创建变更申请", "审批流程", "批准/拒绝操作", "消息通知"],
    x: 10.1
  }
];

detailModules.forEach((mod) => {
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: mod.x, y: 1.3, w: 2.9, h: 3.8,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: mod.x, y: 1.3, w: 2.9, h: 0.6,
    fill: { color: COLORS.primary }
  });
  slide8.addText(mod.title, {
    x: mod.x, y: 1.3, w: 2.9, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.white, align: "center", valign: "middle"
  });

  slide8.addText(
    mod.features.map((f, i) => ({
      text: "• " + f,
      options: { breakLine: i < mod.features.length - 1 }
    })),
    {
      x: mod.x + 0.15, y: 2.1, w: 2.6, h: 2.8,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: COLORS.dark, valign: "top"
    }
  );
});

// 底部备注
slide8.addText("所有模块均支持操作日志记录，支持版本回退", {
  x: 0.5, y: 5.3, w: 12.3, h: 0.4,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.gray, align: "center"
});

// ============================================
// Slide 9: 开发计划
// ============================================
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.light };

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide9.addText("开发计划与里程碑", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
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
    x: x + 0.8, y: 1.5, w: 0.5, h: 0.5,
    fill: { color: COLORS.primary }
  });

  // 连接线
  if (i < milestones.length - 1) {
    slide9.addShape(pres.shapes.RECTANGLE, {
      x: x + 1.3, y: 1.72, w: 2, h: 0.06,
      fill: { color: COLORS.lightGray }
    });
  }

  // 周数
  slide9.addText(m.week, {
    x: x, y: 2.1, w: 2.2, h: 0.4,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.primary, align: "center"
  });

  // 标题
  slide9.addText(m.title, {
    x: x, y: 2.5, w: 2.2, h: 0.5,
    fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
    color: COLORS.dark, align: "center"
  });

  // 任务卡片
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 3.1, w: 2.2, h: 2.0,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });
  slide9.addText(m.tasks, {
    x: x + 0.1, y: 3.2, w: 2.0, h: 1.8,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center", valign: "middle"
  });
});

// 底部总结
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.4, w: 12.3, h: 0.6,
  fill: { color: COLORS.tealLight }
});
slide9.addText("预计总工期：10周 | 团队规模：3-4人 | 目标：完成 P0 所有功能", {
  x: 0.5, y: 5.4, w: 12.3, h: 0.6,
  fontSize: 13, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.primary, align: "center", valign: "middle"
});

// ============================================
// Slide 10: 预期成果
// ============================================
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.light };

slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.3, h: 0.15,
  fill: { color: COLORS.primary }
});

slide10.addText("预期成果", {
  x: 0.5, y: 0.4, w: 12.3, h: 0.8,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.dark
});

// 成果指标
const results = [
  { metric: "50%", label: "报价周期缩短", icon: "⚡" },
  { metric: "100%", label: "流程规范化", icon: "📋" },
  { metric: "实时", label: "消息通知", icon: "🔔" },
  { metric: "追溯", label: "版本管理", icon: "🔙" }
];

results.forEach((r, i) => {
  const x = 0.7 + i * 3.1;

  slide10.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.3, w: 2.8, h: 2.2,
    fill: { color: COLORS.white },
    shadow: makeShadow()
  });

  slide10.addText(r.icon, {
    x: x, y: 1.5, w: 2.8, h: 0.7,
    fontSize: 32, align: "center"
  });

  slide10.addText(r.metric, {
    x: x, y: 2.2, w: 2.8, h: 0.6,
    fontSize: 28, fontFace: "Arial", bold: true,
    color: COLORS.primary, align: "center"
  });

  slide10.addText(r.label, {
    x: x, y: 2.8, w: 2.8, h: 0.5,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: COLORS.dark, align: "center"
  });
});

// 功能清单
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.8, w: 12.3, h: 2.2,
  fill: { color: COLORS.white },
  shadow: makeShadow()
});

slide10.addText("交付清单", {
  x: 0.8, y: 4, w: 3, h: 0.5,
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
  x: 0.8, y: 4.5, w: 5.5, h: 1.4,
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
  x: 6.5, y: 4.5, w: 5.5, h: 1.4,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: COLORS.dark, valign: "top"
});

// ============================================
// Slide 11: 结束页
// ============================================
let slide11 = pres.addSlide();
slide11.background = { color: COLORS.primary };

// 装饰
slide11.addShape(pres.shapes.OVAL, {
  x: -2, y: -2, w: 5, h: 5,
  fill: { color: COLORS.secondary, transparency: 50 }
});
slide11.addShape(pres.shapes.OVAL, {
  x: 10, y: 4.5, w: 4, h: 4,
  fill: { color: COLORS.secondary, transparency: 50 }
});

slide11.addText("感谢聆听", {
  x: 0.5, y: 2.5, w: 12.3, h: 1,
  fontSize: 48, fontFace: "Microsoft YaHei", bold: true,
  color: COLORS.white, align: "center"
});

slide11.addText("Q & A", {
  x: 0.5, y: 3.6, w: 12.3, h: 0.6,
  fontSize: 24, fontFace: "Arial",
  color: COLORS.tealLight, align: "center"
});

slide11.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 4.3, w: 2.3, h: 0.05,
  fill: { color: COLORS.accent }
});

slide11.addText("项目报价系统开发计划与模块设计", {
  x: 0.5, y: 4.6, w: 12.3, h: 0.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: COLORS.white, align: "center"
});

// 保存文件
pres.writeFile({ fileName: "/mnt/c/Users/rs8568/Desktop/Project/项目报价系统开发计划.pptx" })
  .then(() => console.log("PPT 生成成功！"))
  .catch(err => console.error("生成失败:", err));
