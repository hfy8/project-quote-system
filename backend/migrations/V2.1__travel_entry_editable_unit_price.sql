-- V2.1 W2+: 项目层可编辑单价字段
ALTER TABLE packing_entries ADD COLUMN IF NOT EXISTS unit_price NUMERIC(10,2);
ALTER TABLE travel_person_days ADD COLUMN IF NOT EXISTS unit_price NUMERIC(10,2);
ALTER TABLE travel_person_trips ADD COLUMN IF NOT EXISTS unit_price NUMERIC(10,2);
ALTER TABLE travel_person_trips ADD COLUMN IF NOT EXISTS visa_fee NUMERIC(10,2);