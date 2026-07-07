-- Table: change_requests
CREATE TABLE change_requests (
  id integer DEFAULT nextval('change_requests_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  module_id integer NOT NULL,
  change_type character varying NOT NULL,
  proposed_data text NOT NULL,
  original_data text NULL,
  status character varying NOT NULL,
  requested_by integer NOT NULL,
  requested_at timestamp without time zone NULL,
  reviewed_by integer NULL,
  reviewed_at timestamp without time zone NULL,
  review_remark text NULL,
  PRIMARY KEY (id)
);

-- Table: departments
CREATE TABLE departments (
  id bigint DEFAULT nextval('departments_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  description character varying NULL,
  level smallint NULL,
  header_id bigint NULL,
  parent_id bigint NULL,
  parent_path character varying NULL,
  org_id bigint NULL,
  dept_type character varying NULL,
  is_active boolean NULL,
  sync_flag boolean NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL,
  PRIMARY KEY (id)
);

-- Table: employees
CREATE TABLE employees (
  id bigint DEFAULT nextval('employees_id_seq'::regclass) NOT NULL,
  user_id bigint NULL,
  employee_no character varying NULL,
  cn_name character varying NOT NULL,
  en_name character varying NULL,
  nick_name character varying NULL,
  gender smallint NULL,
  email character varying NULL,
  mobile character varying NULL,
  avatar character varying NULL,
  dept_id bigint NULL,
  position_id bigint NULL,
  is_active boolean DEFAULT true NOT NULL,
  join_date date NULL,
  leave_date date NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: exchange_rates
CREATE TABLE exchange_rates (
  id integer DEFAULT nextval('exchange_rates_id_seq'::regclass) NOT NULL,
  currency character varying NOT NULL,
  rate numeric(10, 6) NOT NULL,
  updated_at timestamp without time zone NULL,
  updated_by integer NULL,
  PRIMARY KEY (id)
);

-- Table: fee_rates
CREATE TABLE fee_rates (
  id integer DEFAULT nextval('fee_rates_id_seq'::regclass) NOT NULL,
  category character varying NOT NULL,
  rate numeric(10, 4) NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: fee_types
CREATE TABLE fee_types (
  id integer DEFAULT nextval('fee_types_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  category character varying NOT NULL,
  default_unit character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: labor_hours
CREATE TABLE labor_hours (
  id integer DEFAULT nextval('labor_hours_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  module_id integer NULL,
  work_type character varying NOT NULL,
  hours numeric(10, 2) NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: materials
CREATE TABLE materials (
  id integer DEFAULT nextval('materials_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  model_spec character varying NULL,
  unit character varying NULL,
  brand character varying NULL,
  param1 character varying NULL,
  param2 character varying NULL,
  param3 character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: messages
CREATE TABLE messages (
  id integer DEFAULT nextval('messages_id_seq'::regclass) NOT NULL,
  sender_id integer NOT NULL,
  conversation_id character varying NOT NULL,
  content text NOT NULL,
  message_type character varying DEFAULT 'text' NOT NULL,
  is_read boolean DEFAULT false NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: module_materials
CREATE TABLE module_materials (
  id integer DEFAULT nextval('module_materials_id_seq'::regclass) NOT NULL,
  module_id integer NOT NULL,
  material_id integer NOT NULL,
  quantity numeric(10, 4) NOT NULL,
  -- unit_price 字段 B4 已 DROP (2026-07-07): 137 行全 None + ORM 不同步 + 无业务引用
  -- 业务计算走 material.unit_price + module_materials.unit_price_override (后者仅特例 is_other)
  unit_price_override numeric(12, 2) NULL,
  is_other boolean NULL DEFAULT false,
  selected_by_id integer NULL,
  notes character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: module_participants
CREATE TABLE module_participants (
  id integer DEFAULT nextval('module_participants_id_seq'::regclass) NOT NULL,
  module_id integer NOT NULL,
  user_id integer NOT NULL,
  participant_type character varying NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: modules
CREATE TABLE modules (
  id integer DEFAULT nextval('modules_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  name character varying NOT NULL,
  module_type character varying NULL,
  process_section character varying NULL,
  sort_order integer DEFAULT 0 NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: operation_logs
CREATE TABLE operation_logs (
  id integer DEFAULT nextval('operation_logs_id_seq'::regclass) NOT NULL,
  action character varying NOT NULL,
  module character varying NOT NULL,
  user_id integer NULL,
  username character varying NULL,
  resource_type character varying NULL,
  resource_id character varying NULL,
  detail text NULL,
  ip_address character varying NULL,
  user_agent text NULL,
  created_at timestamp without time zone DEFAULT now() NOT NULL,
  PRIMARY KEY (id)
);

-- Table: organizations
CREATE TABLE organizations (
  id bigint DEFAULT nextval('organizations_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  org_type character varying NULL,
  parent_id bigint NULL,
  parent_path character varying NULL,
  level smallint NULL,
  description character varying NULL,
  is_active boolean DEFAULT true NOT NULL,
  sync_flag boolean DEFAULT false NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: other_fees
CREATE TABLE other_fees (
  id integer DEFAULT nextval('other_fees_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  fee_type character varying NOT NULL,
  description character varying NULL,
  amount numeric(12, 2) NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: packing_entries
CREATE TABLE packing_entries (
  id integer DEFAULT nextval('packing_entries_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  packing_type_id integer NOT NULL,
  quantity integer DEFAULT 1 NOT NULL,
  unit_price numeric(12, 2) DEFAULT 0 NOT NULL,
  notes character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: packing_types
CREATE TABLE packing_types (
  id integer DEFAULT nextval('packing_types_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  unit character varying NULL,
  default_price numeric(12, 2) DEFAULT 0 NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: participant_type_permissions
CREATE TABLE participant_type_permissions (
  id integer DEFAULT nextval('participant_type_permissions_id_seq'::regclass) NOT NULL,
  participant_type character varying NOT NULL,
  tab_name character varying NOT NULL,
  can_view boolean DEFAULT false NOT NULL,
  can_edit boolean DEFAULT false NOT NULL,
  PRIMARY KEY (id)
);

-- Table: permissions
CREATE TABLE permissions (
  id integer DEFAULT nextval('permissions_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: positions
CREATE TABLE positions (
  id bigint DEFAULT nextval('positions_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  level smallint NULL,
  dept_id bigint NULL,
  description character varying NULL,
  is_active boolean DEFAULT true NOT NULL,
  sync_flag boolean DEFAULT false NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: quotation_participants
CREATE TABLE quotation_participants (
  id integer DEFAULT nextval('quotation_participants_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  user_id integer NOT NULL,
  participant_type character varying NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: quotations
CREATE TABLE quotations (
  id integer DEFAULT nextval('quotations_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  type character varying NOT NULL,
  scheme_no character varying NULL,
  status character varying NOT NULL DEFAULT 'draft',
  business_owner_id integer NULL,
  creator_id integer NOT NULL,
  tax_rate double precision DEFAULT 0.13,
  profit_rate double precision DEFAULT 0.0,
  currency character varying DEFAULT 'CNY',
  current_version integer DEFAULT 1,
  parent_id integer REFERENCES quotations(id),
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  coefficients json DEFAULT '{}',
  PRIMARY KEY (id)
);

-- Table: role_permissions
CREATE TABLE role_permissions (
  id integer DEFAULT nextval('role_permissions_id_seq'::regclass) NOT NULL,
  role_id integer NOT NULL,
  permission_id integer NOT NULL,
  PRIMARY KEY (id)
);

-- Table: roles
CREATE TABLE roles (
  id integer DEFAULT nextval('roles_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_categories
CREATE TABLE travel_categories (
  id integer DEFAULT nextval('travel_categories_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_day_rates
CREATE TABLE travel_day_rates (
  id integer DEFAULT nextval('travel_day_rates_id_seq'::regclass) NOT NULL,
  category character varying NOT NULL,
  unit_price numeric(12, 2) NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_modes
CREATE TABLE travel_modes (
  id integer DEFAULT nextval('travel_modes_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  unit character varying NULL,
  default_price numeric(12, 2) DEFAULT 0 NOT NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_person_days
CREATE TABLE travel_person_days (
  id integer DEFAULT nextval('travel_person_days_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  category_id integer NOT NULL,
  person_count integer DEFAULT 1 NOT NULL,
  days numeric(10, 2) DEFAULT 1 NOT NULL,
  unit_price numeric(12, 2) DEFAULT 0 NOT NULL,
  notes character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_person_trip_fees
CREATE TABLE travel_person_trip_fees (
  id integer DEFAULT nextval('travel_person_trip_fees_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  category_id integer NOT NULL,
  trip_count integer DEFAULT 1 NOT NULL,
  unit_price numeric(12, 2) DEFAULT 0 NOT NULL,
  notes character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: travel_person_trips
CREATE TABLE travel_person_trips (
  id integer DEFAULT nextval('travel_person_trips_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  category_id integer NOT NULL,
  person_count integer DEFAULT 1 NOT NULL,
  trips integer DEFAULT 1 NOT NULL,
  unit_price numeric(12, 2) DEFAULT 0 NOT NULL,
  notes character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: users
CREATE TABLE users (
  id integer DEFAULT nextval('users_id_seq'::regclass) NOT NULL,
  username character varying NOT NULL,
  password_hash character varying NOT NULL,
  real_name character varying NULL,
  email character varying NULL,
  mobile character varying NULL,
  role character varying NOT NULL,
  is_active boolean DEFAULT true NOT NULL,
  last_login timestamp without time zone NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  updated_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);

-- Table: version_snapshots
CREATE TABLE version_snapshots (
  id integer DEFAULT nextval('version_snapshots_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  version_no integer NOT NULL,
  operation_type character varying NOT NULL,
  remark text NULL,
  snapshot_data jsonb NOT NULL,
  created_by integer NULL,
  created_at timestamp without time zone DEFAULT now() NULL,
  PRIMARY KEY (id)
);