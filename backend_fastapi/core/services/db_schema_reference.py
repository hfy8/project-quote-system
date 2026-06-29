"""
数据库 Schema 参考（供 AI Agent 执行 SQL 时查阅）
共 33 个表（含 1 个多对多关联表）

用法：
    from core.services.db_schema_reference import SCHEMA_MAP, get_schema_text
    text = get_schema_text()  # 获取完整 schema 文本
"""
SCHEMA_MAP = {}


def _reg(name: str, comment: str, fields: str):
    SCHEMA_MAP[name] = {"comment": comment, "fields": fields}


_reg("quotations", "报价单（核心主表）", """
  id              Integer         PK
  name            String(100)     报价单名称
  type            String(20)      类型: single(单机)/line(线体)
  scheme_no       String(50)      方案号
  status          String(20)      状态: draft/approved
  business_owner_id Integer       FK->users.id 商务负责人
  creator_id      Integer         FK->users.id 创建人
  tax_rate        Float           税率, 默认0.13(13%增值税)
  profit_rate     Float           对外利润率=利润/成本, 如0.15=15%
  currency        String(10)      币种: CNY/USD/EUR, 默认CNY
  current_version Integer         当前版本号, 默认1
  parent_id       Integer         FK->quotations.id 父报价单(线体引用单机)
  coefficients    JSON            {large, standard, other} 费用系数
  created_at      DateTime
  updated_at      DateTime
  关联: -> QuotationParticipant, Module, OtherFee, LaborHour, 
        PackingEntry, TravelPersonDays, TravelPersonTrip,
        VersionSnapshot, ChangeRequest
""")

_reg("quotation_participants", "报价单参与人员", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  user_id         Integer         FK->users.id
  participant_type String(20)     project(项目)/agency(机构)/electrical(电气)
  created_at      DateTime
""")

_reg("modules", "报价单的模块", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  name            String(100)     模块名称
  name_en         String(150)     英文名称
  code            String(50)      编码
  description     Text            描述
  created_at      DateTime
  关联: -> ModuleParticipant, ModuleMaterial, OtherFee, ChangeRequest
""")

_reg("module_participants", "模块参与人员", """
  id              Integer         PK
  module_id       Integer         FK->modules.id
  user_id         Integer         FK->users.id
  created_at      DateTime
""")

_reg("materials", "物料库（基础数据）", """
  id              Integer         PK
  name            String(100)     物料名称
  spec            String(100)     规格
  brand           String(50)      品牌
  unit            String(20)      单位
  unit_price      Numeric(10,2)   单价
  category        String(20)      分类: 大件/核心部件/其他件, 默认核心部件
  param1          String(100)     关键参数01
  param2          String(100)     关键参数02
  param3          String(100)     关键参数03
  status          String(20)      active/inactive, 默认active
  created_at      DateTime
  tip: 物料在报价单中的实际用量在 module_materials 表（多对多关联）
""")

_reg("module_materials", "模块物料关联（多对多）", """
  id              Integer         PK
  module_id       Integer         FK->modules.id 模块ID
  material_id     Integer         FK->materials.id 物料ID
  is_other        Boolean         true=其他类物料, 默认false
  quantity        Integer         数量, 默认1
  unit_price_override Numeric(10,2) 自定义单价覆盖(material_id=24时用)
  selected_by_id  Integer         FK->users.id 选料人
  created_at      DateTime
  tip: 物料在报价单中的实际用量和自定义单价都在这张表
""")

_reg("labor_hours", "人力工时", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id CASCADE
  name            String(100)     工时名称
  hours           Float           工时数
  unit_price      Float           单价
  total           Float           合计=工时×单价
  created_by      Integer         FK->users.id 创建人
  created_at      DateTime
""")

_reg("other_fees", "其他费用", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  module_id       Integer         FK->modules.id (可空)
  fee_type        String(50)      费用类型
  location        String(20)      厂内/厂外
  amount          Numeric(10,2)   金额
  description     Text            描述
  created_at      DateTime
""")

_reg("packing_entries", "包装条目", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  packing_type_id Integer         FK->packing_types.id
  quantity        Integer         使用数量
  unit_price      Numeric(10,2)   自定义单价(Null则用系统配置)
  remark          String(200)
  created_at      DateTime
  updated_at      DateTime
""")

_reg("travel_person_days", "差旅人天", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  travel_category_id Integer      FK->travel_categories.id
  person_days     Numeric(10,2)   出差人天数
  unit_price      Numeric(10,2)   自定义单价(Null则用系统配置)
  remark          String(200)
  created_at      DateTime
  updated_at      DateTime
  tip: 差旅费用 = person_days × unit_price
""")

_reg("travel_person_trips", "差旅人次", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  travel_category_id Integer      FK->travel_categories.id
  travel_mode_id  Integer         FK->travel_modes.id
  person_count    Integer         人次
  unit_price      Numeric(10,2)   自定义交通单价
  visa_fee        Numeric(10,2)   自定义签证费
  remark          String(200)
  created_at      DateTime
  updated_at      DateTime
  tip: 交通费 = person_count × unit_price; 签证费 = person_count × visa_fee
""")

_reg("version_snapshots", "版本快照", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  version_no      Integer         版本号
  snapshot_data   Text            完整快照 (JSON)
  export_data     Text            脱敏导出 (JSON)
  operation_type  String(20)      create/update/export
  remark          Text            备注
  operator_id     Integer         FK->users.id 操作人
  created_at      DateTime
  word_file       String(500)     Word文件路径
  pdf_file        String(500)     PDF文件路径
""")

_reg("change_requests", "变更申请", """
  id              Integer         PK
  quotation_id    Integer         FK->quotations.id
  module_id       Integer         FK->modules.id
  change_type     String(50)      material_add/update/delete/module_update
  proposed_data   Text            提议变更 (JSON)
  original_data   Text            原始数据 (JSON)
  status          String(20)      pending/approved/rejected
  requested_by    Integer         FK->users.id
  requested_at    DateTime
  reviewed_by     Integer         FK->users.id
  reviewed_at     DateTime
  review_remark   Text
""")

_reg("users", "系统用户", """
  id              BigInteger      PK
  username        String(50)      登录账号(unique)
  password_hash   String(255)     密码哈希
  real_name       String(50)      真实姓名
  role            String(20)      admin/business/purchaser/viewer
  employee_id     BigInteger      FK->employees.id
  dept_id         BigInteger      FK->departments.id
  position_id     BigInteger      FK->positions.id
  is_active       Boolean
  sync_flag       Boolean
  created_at      DateTime
  updated_at      DateTime
""")

_reg("employees", "员工信息（HR系统同步）", """
  id              BigInteger      PK
  user_id         BigInteger      FK->users.id
  employee_no     String(50)      工号(unique)
  cn_name         String(100)     中文姓名
  en_name         String(100)     英文姓名
  nick_name       String(100)     昵称
  gender          SmallInteger    0女/1男
  email           String(100)
  mobile          String(20)
  avatar          String(500)
  dept_id         BigInteger      FK->departments.id
  org_id          BigInteger      FK->organizations.id
  position_id     BigInteger      FK->positions.id
  is_active       Boolean
""")

_reg("departments", "部门", """
  id              BigInteger      PK
  name            String(100)     部门名称
  code            String(50)      编码(unique)
  description     String(500)
  level           SmallInteger    部门层级
  header_id       BigInteger      部门负责人ID
  parent_id       BigInteger      FK->departments.id 上级部门
  parent_path     String(500)
  org_id          BigInteger      组织ID
  dept_type       String(20)
  is_active       Boolean
""")

_reg("organizations", "组织", """
  id              BigInteger      PK
  name            String(100)     组织名称
  code            String(50)      编码(unique)
  org_type        String(20)
  description     String(500)
  is_active       Boolean
""")

_reg("positions", "职位", """
  id              BigInteger      PK
  name            String(100)     职位名称
  code            String(50)      编码(unique)
  description     String(500)
  position_type   String(20)
  position_level  SmallInteger    职位级别
  is_active       Boolean
""")

_reg("fee_types", "费用类型配置", """
  id              Integer         PK
  name            String(50)      名称
  name_en         String(100)     英文名
  location        String(20)      厂内/厂外
  is_active       Boolean
""")

_reg("fee_rates", "费用系数配置", """
  id              Integer         PK
  category        String(50)      物料分类: 大件/核心部件/其他件
  rate            Float           系数, 默认1.0
  description     String(200)
""")

_reg("exchange_rates", "汇率", """
  id              Integer         PK
  currency        String(20)      CNY/USD/EUR
  rate            Float           汇率(相对于基准货币)
  is_base         Boolean         是否为基准货币
  description     String(200)
""")

_reg("packing_types", "包装类型配置", """
  id              Integer         PK
  name            String(50)      纸箱/木箱/托盘
  name_en         String(100)
  unit_price      Numeric(12,2)   单价(元/个)
  description     String(200)
  is_active       Boolean
""")

_reg("travel_categories", "差旅分类配置", """
  id              Integer         PK
  name            String(50)      国内出差/东南亚出差/欧洲出差/美国出差
  code            String(20)      domestic/southeast_asia/europe/usa(unique)
  description     String(200)
  sort_order      Integer
  is_active       Boolean
""")

_reg("travel_day_rates", "差旅人天单价配置", """
  id              Integer         PK
  travel_category_id Integer      FK->travel_categories.id
  unit_price      Numeric(12,2)   元/人天
  currency        String(10)      CNY
  description     String(200)
  is_active       Boolean
""")

_reg("travel_modes", "出行方式配置", """
  id              Integer         PK
  name            String(30)      飞机/高铁/开车
  name_en         String(100)
  code            String(20)      plane/train/car(unique)
  description     String(200)
  is_active       Boolean
""")

_reg("travel_person_trip_fees", "差旅人次单价配置", """
  id              Integer         PK
  travel_category_id Integer      FK->travel_categories.id
  travel_mode_id  Integer         FK->travel_modes.id
  unit_price      Numeric(12,2)   交通单价(元/人次往返)
  visa_fee        Numeric(12,2)   签证费(元/人次)
  currency        String(10)      CNY
  description     String(200)
  is_active       Boolean
""")

_reg("messages", "系统消息/通知", """
  id              BigInteger      PK
  sender_id       BigInteger      FK->users.id (系统消息为NULL)
  recipient_id    BigInteger      FK->users.id
  title           String(200)
  content         Text
  type            String(50)      module_member_added/change_request_submitted/
                                  change_request_approved/change_request_rejected/
                                  version_updated
  related_id      BigInteger      关联ID
  related_type    String(50)      quotation/change_request
  is_read         Boolean
""")

_reg("operation_logs", "操作日志审计", """
  id              BigInteger      PK
  user_id         BigInteger      操作用户ID
  username        String(50)      用户登录名
  action          String(20)      login/logout/create/update/delete/export/submit/
                                  approve/reject
  module          String(20)      auth/quotation/material/fee/exchange_rate/user/role/system
  resource_type   String(30)
  resource_id     String(50)
  detail          String(500)
  ip_address      String(50)
  user_agent      String(200)
  created_at      DateTime
  tip: 看操作历史用这个表。action+module 是查询维度。
""")

_reg("ai_knowledge_base", "AI知识库文档", """
  id              BigInteger      PK
  doc_type        String(30)      spec/faq/experience/rule
  title           String(200)
  content         Text
  keywords        String(500)     逗号分隔
  source          String(100)     admin/auto/system
  created_by      String(50)
  created_at      DateTime
  embedding       Vector(1024)    pgvector向量
  embedding_model String(50)      mini/m3e/mock
  tip: RAG检索用。doc_type筛选类型。content是知识正文。
""")

_reg("participant_type_permissions", "参与类型权限配置", """
  id              Integer         PK
  participant_type String(50)     project/agency/electrical/supplier
  tab_name        String(50)      可访问Tab: modules/participants/coefficients/materials/fees/summary/versions/export
  tab_label       String(100)     中文标签
  type_name       String(100)     分类中文名: 项目/机构/电气/供应商
  sort_order      Integer
  is_disabled     Boolean
  tip: 控制各参与角色能看到报价单中的哪些Tab页
""")

_reg("roles", "角色", """
  id              BigInteger      PK
  name            String(50)      角色名称
  code            String(20)      编码(unique)
  description     String(255)
""")

_reg("permissions", "权限", """
  id              BigInteger      PK
  code            String(50)      权限编码(unique)
  name            String(50)      权限名称
  group           String(50)      权限组
  description     String(255)
""")

# role_permissions 自动生成的多对多关联表


def get_schema_text() -> str:
    """获取完整 schema 文本"""
    lines = ["# 数据库 Schema 参考", ""]
    for name, meta in SCHEMA_MAP.items():
        lines.append(f"## {name}")
        lines.append(f"### {meta['comment']}")
        lines.append("```")
        for line in meta["fields"].strip("\n").split("\n"):
            line = line.rstrip()
            if line:
                lines.append(f"  {line.lstrip()} ")
            else:
                lines.append("")
        lines.append("```")
    lines.append("")
    lines.append("## 核心关系")
    lines.append("""
Quotation (1) ──< (N) QuotationParticipant  报价单-参与人员
Quotation (1) ──< (N) Module                报价单-模块
Module    (1) ──< (N) ModuleParticipant      模块-参与人员
Module    (1) ──< (N) ModuleMaterial ──> Material  模块-物料
Quotation (1) ──< (N) OtherFee              报价单-其他费用
Quotation (1) ──< (N) LaborHour             报价单-工时
Quotation (1) ──< (N) PackingEntry          报价单-包装
Quotation (1) ──< (N) TravelPersonDays      报价单-差旅人天
Quotation (1) ──< (N) TravelPersonTrip      报价单-差旅人次
Quotation (1) ──< (N) VersionSnapshot       报价单-版本快照
Quotation (1) ──< (N) ChangeRequest          报价单-变更申请
""")
    return "\n".join(lines)
