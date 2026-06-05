
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
  review_remark text NULL
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
  updated_at timestamp without time zone NULL
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
  org_id bigint NULL,
  position_id bigint NULL,
  is_active boolean NULL,
  sync_flag boolean NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: exchange_rates
CREATE TABLE exchange_rates (
  id integer DEFAULT nextval('exchange_rates_id_seq'::regclass) NOT NULL,
  currency character varying NOT NULL,
  rate double precision NOT NULL,
  is_base boolean NULL,
  description character varying NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: fee_rates
CREATE TABLE fee_rates (
  id integer DEFAULT nextval('fee_rates_id_seq'::regclass) NOT NULL,
  category character varying NOT NULL,
  rate double precision NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: fee_types
CREATE TABLE fee_types (
  id integer DEFAULT nextval('fee_types_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  location character varying NOT NULL,
  is_active boolean NOT NULL,
  created_at timestamp without time zone NULL,
  name_en character varying NULL
  PRIMARY KEY (id)
);

-- Table: labor_hours
CREATE TABLE labor_hours (
  id integer DEFAULT nextval('labor_hours_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  name character varying NOT NULL,
  hours double precision NULL,
  unit_price double precision NULL,
  total double precision NULL,
  created_by integer NOT NULL,
  created_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: materials
CREATE TABLE materials (
  id integer DEFAULT nextval('materials_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  spec character varying NULL,
  brand character varying NULL,
  unit character varying NULL,
  unit_price numeric NOT NULL,
  category character varying NOT NULL,
  status character varying NOT NULL,
  created_at timestamp without time zone NULL,
  manufacturer character varying NULL,
  part_number character varying NULL,
  lead_time character varying NULL,
  param1 character varying NULL,
  param2 character varying NULL,
  param3 character varying NULL
  PRIMARY KEY (id)
);

-- Table: messages
CREATE TABLE messages (
  id bigint DEFAULT nextval('messages_id_seq'::regclass) NOT NULL,
  sender_id bigint NULL,
  recipient_id bigint NOT NULL,
  title character varying NOT NULL,
  content text NOT NULL,
  type character varying NOT NULL,
  related_id bigint NULL,
  related_type character varying NULL,
  is_read boolean NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: module_materials
CREATE TABLE module_materials (
  id integer DEFAULT nextval('module_materials_id_seq'::regclass) NOT NULL,
  module_id integer NOT NULL,
  material_id integer NULL,
  quantity integer NOT NULL,
  selected_by_id integer NULL,
  created_at timestamp without time zone NULL,
  is_other boolean DEFAULT false NULL,
  unit_price numeric NULL,
  unit_price_override numeric NULL
  PRIMARY KEY (id)
);

-- Table: module_participants
CREATE TABLE module_participants (
  id integer DEFAULT nextval('module_participants_id_seq'::regclass) NOT NULL,
  module_id integer NOT NULL,
  user_id integer NOT NULL,
  created_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: modules
CREATE TABLE modules (
  id integer DEFAULT nextval('modules_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  name character varying NOT NULL,
  code character varying NULL,
  description text NULL,
  created_at timestamp without time zone NULL,
  name_en character varying NULL
  PRIMARY KEY (id)
);

-- Table: operation_logs
CREATE TABLE operation_logs (
  id bigint DEFAULT nextval('operation_logs_id_seq'::regclass) NOT NULL,
  user_id bigint NOT NULL,
  username character varying NOT NULL,
  action character varying NOT NULL,
  module character varying NOT NULL,
  resource_type character varying NULL,
  resource_id character varying NULL,
  detail character varying NULL,
  ip_address character varying NULL,
  user_agent character varying NULL,
  created_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: organizations
CREATE TABLE organizations (
  id bigint DEFAULT nextval('organizations_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NULL,
  org_type character varying NULL,
  description character varying NULL,
  is_active boolean NULL,
  sync_flag boolean NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: other_fees
CREATE TABLE other_fees (
  id integer DEFAULT nextval('other_fees_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  module_id integer NULL,
  fee_type character varying NOT NULL,
  location character varying NOT NULL,
  amount numeric NOT NULL,
  description text NULL,
  created_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: packing_entries
CREATE TABLE packing_entries (
  id integer DEFAULT nextval('packing_entries_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  packing_type_id integer NOT NULL,
  quantity numeric DEFAULT 0 NOT NULL,
  remark text NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  unit_price numeric NULL
  PRIMARY KEY (id)
);

-- Table: packing_types
CREATE TABLE packing_types (
  id integer DEFAULT nextval('packing_types_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  name_en character varying NULL,
  unit_price numeric DEFAULT 0 NOT NULL,
  description text NULL,
  is_active boolean DEFAULT true NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: participant_type_permissions
CREATE TABLE participant_type_permissions (
  id integer DEFAULT nextval('participant_type_permissions_id_seq'::regclass) NOT NULL,
  participant_type character varying NOT NULL,
  tab_name character varying NOT NULL,
  tab_label character varying NOT NULL,
  description character varying NULL,
  sort_order integer NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL,
  is_disabled boolean DEFAULT false NULL,
  type_name character varying NULL
  PRIMARY KEY (id)
);

-- Table: permissions
CREATE TABLE permissions (
  id bigint DEFAULT nextval('permissions_id_seq'::regclass) NOT NULL,
  code character varying NOT NULL,
  name character varying NOT NULL,
  group character varying NULL,
  description character varying NULL
  PRIMARY KEY (id)
);

-- Table: positions
CREATE TABLE positions (
  id bigint DEFAULT nextval('positions_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NULL,
  description character varying NULL,
  position_type character varying NULL,
  position_level smallint NULL,
  is_active boolean NULL,
  sync_flag boolean NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: quotation_participants
CREATE TABLE quotation_participants (
  id integer DEFAULT nextval('quotation_participants_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  user_id integer NOT NULL,
  participant_type character varying DEFAULT 'project'::character varying NULL,
  created_at timestamp without time zone DEFAULT now() NULL
  PRIMARY KEY (id)
);

-- Table: quotations
CREATE TABLE quotations (
  id integer DEFAULT nextval('quotations_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  type character varying NOT NULL,
  scheme_no character varying NULL,
  status character varying NOT NULL,
  business_owner_id integer NULL,
  creator_id integer NOT NULL,
  tax_rate double precision NULL,
  created_at timestamp without time zone NULL,
  updated_at timestamp without time zone NULL,
  current_version integer DEFAULT 1 NULL,
  currency character varying DEFAULT 'CNY'::character varying NULL,
  coefficients json NULL,
  profit_rate double precision DEFAULT 0.0 NULL
  PRIMARY KEY (id)
);

-- Table: role_permissions
CREATE TABLE role_permissions (
  role_id bigint NOT NULL,
  permission_id bigint NOT NULL
  PRIMARY KEY (role_id, permission_id)
);

-- Table: roles
CREATE TABLE roles (
  id bigint DEFAULT nextval('roles_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  code character varying NOT NULL,
  description character varying NULL,
  created_at timestamp without time zone NULL
  PRIMARY KEY (id)
);

-- Table: travel_categories
CREATE TABLE travel_categories (
  id integer DEFAULT nextval('travel_categories_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  name_en character varying NULL,
  code character varying NOT NULL,
  sort_order integer DEFAULT 0 NOT NULL,
  description text NULL,
  is_active boolean DEFAULT true NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: travel_day_rates
CREATE TABLE travel_day_rates (
  id integer DEFAULT nextval('travel_day_rates_id_seq'::regclass) NOT NULL,
  travel_category_id integer NOT NULL,
  unit_price numeric DEFAULT 0 NOT NULL,
  currency character varying DEFAULT 'CNY'::character varying NOT NULL,
  description text NULL,
  is_active boolean DEFAULT true NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: travel_modes
CREATE TABLE travel_modes (
  id integer DEFAULT nextval('travel_modes_id_seq'::regclass) NOT NULL,
  name character varying NOT NULL,
  name_en character varying NULL,
  code character varying NOT NULL,
  description text NULL,
  is_active boolean DEFAULT true NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: travel_person_days
CREATE TABLE travel_person_days (
  id integer DEFAULT nextval('travel_person_days_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  travel_category_id integer NOT NULL,
  person_days numeric DEFAULT 0 NOT NULL,
  remark text NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  unit_price numeric NULL
  PRIMARY KEY (id)
);

-- Table: travel_person_trip_fees
CREATE TABLE travel_person_trip_fees (
  id integer DEFAULT nextval('travel_person_trip_fees_id_seq'::regclass) NOT NULL,
  travel_category_id integer NOT NULL,
  travel_mode_id integer NOT NULL,
  unit_price numeric DEFAULT 0 NOT NULL,
  visa_fee numeric DEFAULT 0 NOT NULL,
  currency character varying DEFAULT 'CNY'::character varying NOT NULL,
  description text NULL,
  is_active boolean DEFAULT true NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: travel_person_trips
CREATE TABLE travel_person_trips (
  id integer DEFAULT nextval('travel_person_trips_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  travel_category_id integer NOT NULL,
  travel_mode_id integer NOT NULL,
  person_count integer DEFAULT 0 NOT NULL,
  remark text NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL,
  unit_price numeric NULL,
  visa_fee numeric NULL
  PRIMARY KEY (id)
);

-- Table: users
CREATE TABLE users (
  id integer DEFAULT nextval('users_id_seq'::regclass) NOT NULL,
  username character varying NOT NULL,
  password_hash character varying NOT NULL,
  real_name character varying NOT NULL,
  role character varying NOT NULL,
  created_at timestamp without time zone NULL,
  employee_id bigint NULL,
  dept_id bigint NULL,
  position_id bigint NULL,
  sync_flag boolean DEFAULT true NULL,
  is_active boolean DEFAULT true NULL,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NULL
  PRIMARY KEY (id)
);

-- Table: version_snapshots
CREATE TABLE version_snapshots (
  id integer DEFAULT nextval('version_snapshots_id_seq'::regclass) NOT NULL,
  quotation_id integer NOT NULL,
  version_no integer NOT NULL,
  snapshot_data text NOT NULL,
  operation_type character varying NOT NULL,
  remark text NULL,
  operator_id integer NOT NULL,
  created_at timestamp without time zone NULL,
  word_file character varying NULL,
  pdf_file character varying NULL,
  export_data text NULL
  PRIMARY KEY (id)
);
