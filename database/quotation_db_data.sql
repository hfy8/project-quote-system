--
-- PostgreSQL database dump
--

\restrict tb7q5TikvxwMTaFQ3CGnnYT0tSl8CcWpbKZK9wbzPUdUaD36khHz1glX8jWZY30

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg12+1)
-- Dumped by pg_dump version 16.14 (Debian 16.14-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: -
--

SET SESSION AUTHORIZATION DEFAULT;

ALTER TABLE public.departments DISABLE TRIGGER ALL;

INSERT INTO public.departments VALUES (721, '法务部Ⅰ', '742', NULL, 1, 9446, NULL, '721-', 27, '1', true, true, '2026-07-13 06:43:58.942351', '2026-07-13 06:43:58.942355');
INSERT INTO public.departments VALUES (882, '综合管理部Ⅰ', '905', NULL, 1, 9438, NULL, '882-', 27, '1', true, true, '2026-07-13 06:43:58.94408', '2026-07-13 06:43:58.944083');
INSERT INTO public.departments VALUES (1023, '综合管理部Ⅱ', '1044', NULL, 1, 9438, NULL, '1023-', 24, '1', true, true, '2026-07-13 06:43:58.945333', '2026-07-13 06:43:58.945336');
INSERT INTO public.departments VALUES (1035, '交付管理部NⅠ', '1053', NULL, 1, 9447, NULL, '1035-', 27, '3', true, true, '2026-07-13 06:43:58.946534', '2026-07-13 06:43:58.946538');
INSERT INTO public.departments VALUES (1036, '交付管理部NⅡ', '1054', NULL, 1, 9447, NULL, '1036-', 24, '3', true, true, '2026-07-13 06:43:58.947683', '2026-07-13 06:43:58.947686');
INSERT INTO public.departments VALUES (1037, '交付管理部NⅢ', '1055', NULL, 1, 9447, NULL, '1037-', 28, '3', true, true, '2026-07-13 06:43:58.948851', '2026-07-13 06:43:58.948854');
INSERT INTO public.departments VALUES (1038, '销售部NⅠ', '1056', NULL, 1, 9110, NULL, '1038-', 27, '3', true, true, '2026-07-13 06:43:58.950011', '2026-07-13 06:43:58.950014');
INSERT INTO public.departments VALUES (1039, '销售部NⅢ', '1057', NULL, 1, 9110, NULL, '1039-', 28, '3', true, true, '2026-07-13 06:43:58.951124', '2026-07-13 06:43:58.951148');
INSERT INTO public.departments VALUES (1040, '生产部NⅠ', '1058', NULL, 1, 8921, NULL, '1040-', 27, '2', true, true, '2026-07-13 06:43:58.952308', '2026-07-13 06:43:58.952311');
INSERT INTO public.departments VALUES (1041, '制造部NⅡ', '1059', NULL, 1, 9446, NULL, '1041-', 24, '2', true, true, '2026-07-13 06:43:58.953434', '2026-07-13 06:43:58.953437');
INSERT INTO public.departments VALUES (1042, '生产部NⅢ', '1060', NULL, 1, 8921, NULL, '1042-', 28, '2', true, true, '2026-07-13 06:43:58.954546', '2026-07-13 06:43:58.95455');
INSERT INTO public.departments VALUES (1044, '电控软件部CⅡ', '1062', NULL, 1, 378, NULL, '1044-', 24, '5', true, true, '2026-07-13 06:43:58.955696', '2026-07-13 06:43:58.955698');
INSERT INTO public.departments VALUES (1045, '电控软件部CⅢ', '1063', NULL, 1, 378, NULL, '1045-', 28, '5', true, true, '2026-07-13 06:43:58.956826', '2026-07-13 06:43:58.956829');
INSERT INTO public.departments VALUES (1046, '机构部CⅡ', '1064', NULL, 1, 9509, NULL, '1046-', 24, '5', true, true, '2026-07-13 06:43:58.957949', '2026-07-13 06:43:58.957953');
INSERT INTO public.departments VALUES (1047, '交付管理部CⅡ', '1065', NULL, 1, 781, NULL, '1047-', 24, '3', true, true, '2026-07-13 06:43:58.959206', '2026-07-13 06:43:58.95921');
INSERT INTO public.departments VALUES (1048, '项目部CⅡ', '1066', NULL, 1, 9440, NULL, '1048-', 24, '3', true, true, '2026-07-13 06:43:58.960505', '2026-07-13 06:43:58.960508');
INSERT INTO public.departments VALUES (1049, '销售部CⅠ', '1067', NULL, 1, 9438, NULL, '1049-', 27, '3', true, true, '2026-07-13 06:43:58.961654', '2026-07-13 06:43:58.961658');
INSERT INTO public.departments VALUES (1050, '销售部CⅡ', '1068', NULL, 1, 9438, NULL, '1050-', 24, '3', true, true, '2026-07-13 06:43:58.962791', '2026-07-13 06:43:58.962795');
INSERT INTO public.departments VALUES (1051, '销售部CⅢ', '1069', NULL, 1, 9438, NULL, '1051-', 28, '3', true, true, '2026-07-13 06:43:58.963993', '2026-07-13 06:43:58.963997');
INSERT INTO public.departments VALUES (1052, '供应链管理部Ⅰ', '1070', NULL, 1, 9438, NULL, '1052-', 27, '2', true, true, '2026-07-13 06:43:58.96515', '2026-07-13 06:43:58.965153');
INSERT INTO public.departments VALUES (1053, '供应链管理部Ⅱ', '1071', NULL, 1, 9438, NULL, '1053-', 24, '2', true, true, '2026-07-13 06:43:58.966286', '2026-07-13 06:43:58.966289');
INSERT INTO public.departments VALUES (1064, '机加部NⅠ', '1082', NULL, 1, 9050, NULL, '1064-', 27, '2', true, true, '2026-07-13 06:43:58.967457', '2026-07-13 06:43:58.967459');
INSERT INTO public.departments VALUES (1065, '机加部NⅢ', '1083', NULL, 1, 9050, NULL, '1065-', 28, '2', true, true, '2026-07-13 06:43:58.968619', '2026-07-13 06:43:58.968623');
INSERT INTO public.departments VALUES (1066, '品质部NⅢ', '1084', NULL, 1, 9488, NULL, '1066-', 28, '2', true, true, '2026-07-13 06:43:58.969724', '2026-07-13 06:43:58.969728');
INSERT INTO public.departments VALUES (1067, '技术部NⅠ', '1085', NULL, 1, 9047, NULL, '1067-', 27, '5', true, true, '2026-07-13 06:43:58.970867', '2026-07-13 06:43:58.97087');
INSERT INTO public.departments VALUES (1068, '研发部NⅡ', '1086', NULL, 1, 9047, NULL, '1068-', 24, '5', true, true, '2026-07-13 06:43:58.972007', '2026-07-13 06:43:58.97201');
INSERT INTO public.departments VALUES (1069, '技术部NⅢ', '1087', NULL, 1, 9047, NULL, '1069-', 28, '5', true, true, '2026-07-13 06:43:58.973107', '2026-07-13 06:43:58.973111');
INSERT INTO public.departments VALUES (1070, '装配部NⅢ', '1088', NULL, 1, 9048, NULL, '1070-', 28, '2', true, true, '2026-07-13 06:43:58.97423', '2026-07-13 06:43:58.974233');
INSERT INTO public.departments VALUES (1123, '综合管理部Ⅲ', '1142', NULL, 1, 9438, NULL, '1123-', 28, '1', true, true, '2026-07-13 06:43:58.975457', '2026-07-13 06:43:58.975461');
INSERT INTO public.departments VALUES (1125, '财务部NⅠ', '1145', NULL, 1, 9389, NULL, '1125-', 27, '1', true, true, '2026-07-13 06:43:58.976633', '2026-07-13 06:43:58.976636');
INSERT INTO public.departments VALUES (1126, '财务部CⅠ', '1144', NULL, 1, 9441, NULL, '1126-', 27, '1', true, true, '2026-07-13 06:43:58.9778', '2026-07-13 06:43:58.977804');
INSERT INTO public.departments VALUES (1127, '财务部CⅡ', '1143', NULL, 1, 9441, NULL, '1127-', 24, '1', true, true, '2026-07-13 06:43:58.978953', '2026-07-13 06:43:58.978956');
INSERT INTO public.departments VALUES (1132, '交付管理部NⅣ', '1150', NULL, 1, 9447, NULL, '1132-', 26, '3', true, true, '2026-07-13 06:43:58.980123', '2026-07-13 06:43:58.980146');
INSERT INTO public.departments VALUES (1133, '制造部NⅣ', '1151', NULL, 1, 9446, NULL, '1133-', 26, '2', true, true, '2026-07-13 06:43:58.981252', '2026-07-13 06:43:58.981256');
INSERT INTO public.departments VALUES (1135, '生产部NⅣ', '1153', NULL, 1, 8921, NULL, '1135-', 26, '2', true, true, '2026-07-13 06:43:58.982339', '2026-07-13 06:43:58.982342');
INSERT INTO public.departments VALUES (1143, '机构部CⅢ', '1161', NULL, 1, 9509, NULL, '1143-', 28, '5', true, true, '2026-07-13 06:43:58.98346', '2026-07-13 06:43:58.983463');
INSERT INTO public.departments VALUES (1145, '总经办NⅠ', '1163', NULL, 1, 9446, NULL, '1145-', 27, '1', true, true, '2026-07-13 06:43:58.984577', '2026-07-13 06:43:58.98458');
INSERT INTO public.departments VALUES (1151, '销售部NⅡ', '1169', NULL, 1, 9110, NULL, '1151-', 24, '3', true, true, '2026-07-13 06:43:58.985666', '2026-07-13 06:43:58.985669');
INSERT INTO public.departments VALUES (1155, '技术部NⅣ', '1173', NULL, 1, 9047, NULL, '1155-', 26, '5', true, true, '2026-07-13 06:43:58.986738', '2026-07-13 06:43:58.986741');
INSERT INTO public.departments VALUES (1156, '品质部NⅠ', '1174', NULL, 1, 9488, NULL, '1156-', 27, '2', true, true, '2026-07-13 06:43:58.987834', '2026-07-13 06:43:58.987837');
INSERT INTO public.departments VALUES (722, '法务Ⅰ', '743', NULL, 2, 9446, 721, '721-722-', 27, '1', true, true, '2026-07-13 06:43:58.988962', '2026-07-13 06:43:58.988965');
INSERT INTO public.departments VALUES (928, '人事部Ⅰ', '1000', NULL, 2, 9446, 882, '882-928-', 27, '1', true, true, '2026-07-13 06:43:58.990265', '2026-07-13 06:43:58.990268');
INSERT INTO public.departments VALUES (1025, '安环部Ⅰ', '1046', NULL, 2, 9358, 882, '882-1025-', 27, '1', true, true, '2026-07-13 06:43:58.991434', '2026-07-13 06:43:58.991437');
INSERT INTO public.departments VALUES (1026, '行政部Ⅰ', '1047', NULL, 2, 9358, 882, '882-1026-', 27, '1', true, true, '2026-07-13 06:43:58.992601', '2026-07-13 06:43:58.992605');
INSERT INTO public.departments VALUES (1024, 'IT部Ⅱ', '1045', NULL, 2, 9358, 1023, '1023-1024-', 24, '1', true, true, '2026-07-13 06:43:58.993722', '2026-07-13 06:43:58.993725');
INSERT INTO public.departments VALUES (1055, '售后组NⅠ', '1073', NULL, 2, 9447, 1035, '1035-1055-', 27, '3', true, true, '2026-07-13 06:43:58.994892', '2026-07-13 06:43:58.994895');
INSERT INTO public.departments VALUES (1058, '项目组NⅠ', '1076', NULL, 2, 9447, 1035, '1035-1058-', 27, '3', true, true, '2026-07-13 06:43:58.996092', '2026-07-13 06:43:58.996095');
INSERT INTO public.departments VALUES (1154, '交付管理NⅠ', '1172', NULL, 2, 9447, 1035, '1035-1154-', 27, '3', true, true, '2026-07-13 06:43:58.997254', '2026-07-13 06:43:58.997257');
INSERT INTO public.departments VALUES (1159, '维保组NⅠ', '1177', NULL, 2, 9447, 1035, '1035-1159-', 27, '3', true, true, '2026-07-13 06:43:58.998409', '2026-07-13 06:43:58.998413');
INSERT INTO public.departments VALUES (1054, '交付管理NⅡ', '1072', NULL, 2, 9447, 1036, '1036-1054-', 24, '3', true, true, '2026-07-13 06:43:58.999541', '2026-07-13 06:43:58.999544');
INSERT INTO public.departments VALUES (1056, '售后部NⅡ', '1074', NULL, 2, 9447, 1036, '1036-1056-', 24, '3', true, true, '2026-07-13 06:43:59.00068', '2026-07-13 06:43:59.000684');
INSERT INTO public.departments VALUES (1059, '项目组NⅡ', '1077', NULL, 2, 9447, 1036, '1036-1059-', 24, '3', true, true, '2026-07-13 06:43:59.001793', '2026-07-13 06:43:59.001796');
INSERT INTO public.departments VALUES (1057, '售后组NⅢ', '1075', NULL, 2, 9447, 1037, '1037-1057-', 28, '3', true, true, '2026-07-13 06:43:59.0029', '2026-07-13 06:43:59.002904');
INSERT INTO public.departments VALUES (1060, '项目组NⅢ', '1078', NULL, 2, 9447, 1037, '1037-1060-', 28, '3', true, true, '2026-07-13 06:43:59.004057', '2026-07-13 06:43:59.00406');
INSERT INTO public.departments VALUES (1061, '销售一部NⅠ', '1079', NULL, 2, 9446, 1038, '1038-1061-', 27, '3', true, true, '2026-07-13 06:43:59.005183', '2026-07-13 06:43:59.005186');
INSERT INTO public.departments VALUES (1169, '销售二部NⅠ', '1187', NULL, 2, 9446, 1038, '1038-1169-', 27, '1', true, true, '2026-07-13 06:43:59.006273', '2026-07-13 06:43:59.006276');
INSERT INTO public.departments VALUES (1062, '销售一部NⅢ', '1080', NULL, 2, 9446, 1039, '1039-1062-', 28, '3', true, true, '2026-07-13 06:43:59.007393', '2026-07-13 06:43:59.007396');
INSERT INTO public.departments VALUES (1147, '前工序组NⅠ', '1165', NULL, 2, 9051, 1040, '1040-1147-', 27, '2', true, true, '2026-07-13 06:43:59.008503', '2026-07-13 06:43:59.008506');
INSERT INTO public.departments VALUES (1161, '总务组NⅠ', '1179', NULL, 2, 9446, 1040, '1040-1161-', 27, '2', true, true, '2026-07-13 06:43:59.009604', '2026-07-13 06:43:59.009607');
INSERT INTO public.departments VALUES (1166, '装配组NⅠ', '1184', NULL, 2, 9048, 1040, '1040-1166-', 27, '2', true, true, '2026-07-13 06:43:59.010667', '2026-07-13 06:43:59.01067');
INSERT INTO public.departments VALUES (1063, '总务组NⅢ', '1081', NULL, 2, 8921, 1042, '1042-1063-', 28, '2', true, true, '2026-07-13 06:43:59.011787', '2026-07-13 06:43:59.01179');
INSERT INTO public.departments VALUES (1096, '前工序组NⅢ', '1114', NULL, 2, 9051, 1042, '1042-1096-', 28, '2', true, true, '2026-07-13 06:43:59.012898', '2026-07-13 06:43:59.012901');
INSERT INTO public.departments VALUES (1149, '装配组NⅢ', '1167', NULL, 2, 9048, 1042, '1042-1149-', 28, '2', true, true, '2026-07-13 06:43:59.013977', '2026-07-13 06:43:59.01398');
INSERT INTO public.departments VALUES (1164, '机加组NⅢ', '1182', NULL, 2, 9050, 1042, '1042-1164-', 28, '2', true, true, '2026-07-13 06:43:59.015088', '2026-07-13 06:43:59.015091');
INSERT INTO public.departments VALUES (1072, '电控部CⅡ', '1090', NULL, 2, 378, 1044, '1044-1072-', 24, '5', true, true, '2026-07-13 06:43:59.016235', '2026-07-13 06:43:59.016239');
INSERT INTO public.departments VALUES (1075, '软件部CⅡ', '1093', NULL, 2, 378, 1044, '1044-1075-', 24, '5', true, true, '2026-07-13 06:43:59.017342', '2026-07-13 06:43:59.017345');
INSERT INTO public.departments VALUES (1170, '技术部CⅡ', '1188', NULL, 2, 9438, 1044, '1044-1170-', 24, '5', true, true, '2026-07-13 06:43:59.018448', '2026-07-13 06:43:59.018452');
INSERT INTO public.departments VALUES (1073, '电控部CⅢ', '1091', NULL, 2, 378, 1045, '1045-1073-', 28, '5', true, true, '2026-07-13 06:43:59.019735', '2026-07-13 06:43:59.019738');
INSERT INTO public.departments VALUES (1076, '机构部CⅡ', '1094', NULL, 2, 9509, 1046, '1046-1076-', 24, '5', true, true, '2026-07-13 06:43:59.020872', '2026-07-13 06:43:59.020875');
INSERT INTO public.departments VALUES (1077, '交付管理CⅡ', '1095', NULL, 2, 781, 1047, '1047-1077-', 24, '2', true, true, '2026-07-13 06:43:59.021982', '2026-07-13 06:43:59.021986');
INSERT INTO public.departments VALUES (1078, '品质部CⅡ', '1096', NULL, 2, 781, 1047, '1047-1078-', 24, '2', true, true, '2026-07-13 06:43:59.023076', '2026-07-13 06:43:59.023079');
INSERT INTO public.departments VALUES (1079, '生产部CⅡ', '1097', NULL, 2, 781, 1047, '1047-1079-', 24, '2', true, true, '2026-07-13 06:43:59.024244', '2026-07-13 06:43:59.024247');
INSERT INTO public.departments VALUES (1080, '售后部CⅡ', '1098', NULL, 2, 195, 1047, '1047-1080-', 24, '2', true, true, '2026-07-13 06:43:59.025366', '2026-07-13 06:43:59.02537');
INSERT INTO public.departments VALUES (1081, '项目部CⅡ', '1099', NULL, 2, 9440, 1048, '1048-1081-', 24, '3', true, true, '2026-07-13 06:43:59.026461', '2026-07-13 06:43:59.026464');
INSERT INTO public.departments VALUES (1083, '业务部CⅠ', '1101', NULL, 2, 9438, 1049, '1049-1083-', 27, '3', true, true, '2026-07-13 06:43:59.027547', '2026-07-13 06:43:59.02755');
INSERT INTO public.departments VALUES (1082, '方案部CⅡ', '1100', NULL, 2, 9438, 1050, '1050-1082-', 24, '3', true, true, '2026-07-13 06:43:59.028651', '2026-07-13 06:43:59.028654');
INSERT INTO public.departments VALUES (1084, '业务部CⅡ', '1102', NULL, 2, 9438, 1050, '1050-1084-', 24, '3', true, true, '2026-07-13 06:43:59.029754', '2026-07-13 06:43:59.029758');
INSERT INTO public.departments VALUES (1085, '业务部CⅢ', '1103', NULL, 2, 9438, 1051, '1051-1085-', 28, '3', true, true, '2026-07-13 06:43:59.030846', '2026-07-13 06:43:59.030849');
INSERT INTO public.departments VALUES (1086, '采购部Ⅰ', '1104', NULL, 2, 9446, 1052, '1052-1086-', 27, '2', true, true, '2026-07-13 06:43:59.031959', '2026-07-13 06:43:59.031962');
INSERT INTO public.departments VALUES (1088, '资材部Ⅰ', '1106', NULL, 2, 9338, 1052, '1052-1088-', 27, '2', true, true, '2026-07-13 06:43:59.033082', '2026-07-13 06:43:59.033085');
INSERT INTO public.departments VALUES (1087, '仓储部Ⅱ', '1105', NULL, 2, 9338, 1053, '1053-1087-', 24, '2', true, true, '2026-07-13 06:43:59.034206', '2026-07-13 06:43:59.03421');
INSERT INTO public.departments VALUES (1089, '资材部Ⅱ', '1107', NULL, 2, 9338, 1053, '1053-1089-', 24, '2', true, true, '2026-07-13 06:43:59.035305', '2026-07-13 06:43:59.035308');
INSERT INTO public.departments VALUES (1148, '机加NⅢ', '1166', NULL, 2, 9050, 1065, '1065-1148-', 28, '2', true, true, '2026-07-13 06:43:59.036428', '2026-07-13 06:43:59.036431');
INSERT INTO public.departments VALUES (1097, '质量检验NⅢ', '1115', NULL, 2, 9446, 1066, '1066-1097-', 28, '2', true, true, '2026-07-13 06:43:59.037522', '2026-07-13 06:43:59.037525');
INSERT INTO public.departments VALUES (1150, '品质部NⅢ', '1168', NULL, 2, 9488, 1066, '1066-1150-', 28, '2', true, true, '2026-07-13 06:43:59.038729', '2026-07-13 06:43:59.038732');
INSERT INTO public.departments VALUES (1100, '电控组NⅠ', '1118', NULL, 2, 9047, 1067, '1067-1100-', 27, '5', true, true, '2026-07-13 06:43:59.03993', '2026-07-13 06:43:59.039933');
INSERT INTO public.departments VALUES (1103, '机构2组NⅠ', '1121', NULL, 2, 9047, 1067, '1067-1103-', 27, '5', true, true, '2026-07-13 06:43:59.041154', '2026-07-13 06:43:59.041158');
INSERT INTO public.departments VALUES (1160, '机构3组NⅠ', '1178', NULL, 2, 9047, 1067, '1067-1160-', 27, '5', true, true, '2026-07-13 06:43:59.042335', '2026-07-13 06:43:59.042338');
INSERT INTO public.departments VALUES (1101, '电控部NⅡ', '1119', NULL, 2, 9047, 1068, '1068-1101-', 24, '5', true, true, '2026-07-13 06:43:59.043488', '2026-07-13 06:43:59.043492');
INSERT INTO public.departments VALUES (1106, '软件部NⅡ', '1124', NULL, 2, 9047, 1068, '1068-1106-', 24, '5', true, true, '2026-07-13 06:43:59.044601', '2026-07-13 06:43:59.044605');
INSERT INTO public.departments VALUES (1102, '电控组NⅢ', '1120', NULL, 2, 9047, 1069, '1069-1102-', 28, '5', true, true, '2026-07-13 06:43:59.045754', '2026-07-13 06:43:59.045757');
INSERT INTO public.departments VALUES (1104, '机构1组NⅢ', '1122', NULL, 2, 9047, 1069, '1069-1104-', 28, '5', true, true, '2026-07-13 06:43:59.046893', '2026-07-13 06:43:59.046896');
INSERT INTO public.departments VALUES (1105, '机构2组NⅢ', '1123', NULL, 2, 9047, 1069, '1069-1105-', 28, '5', true, true, '2026-07-13 06:43:59.048081', '2026-07-13 06:43:59.048085');
INSERT INTO public.departments VALUES (1107, '软件部NⅢ', '1125', NULL, 2, 9047, 1069, '1069-1107-', 28, '5', true, true, '2026-07-13 06:43:59.049264', '2026-07-13 06:43:59.049267');
INSERT INTO public.departments VALUES (1124, '行政部Ⅲ', '1141', NULL, 2, 9358, 1123, '1123-1124-', 28, '1', true, true, '2026-07-13 06:43:59.050437', '2026-07-13 06:43:59.05044');
INSERT INTO public.departments VALUES (1128, '财务NⅠ', '1146', NULL, 2, 9389, 1125, '1125-1128-', 27, '1', true, true, '2026-07-13 06:43:59.051567', '2026-07-13 06:43:59.051571');
INSERT INTO public.departments VALUES (1129, '财务CⅠ', '1147', NULL, 2, 9441, 1126, '1126-1129-', 27, '1', true, true, '2026-07-13 06:43:59.052671', '2026-07-13 06:43:59.052674');
INSERT INTO public.departments VALUES (1130, '财务CⅡ', '1148', NULL, 2, 9441, 1127, '1127-1130-', 24, '1', true, true, '2026-07-13 06:43:59.053812', '2026-07-13 06:43:59.053815');
INSERT INTO public.departments VALUES (1134, '项目组NⅣ', '1152', NULL, 2, 9447, 1132, '1132-1134-', 26, '3', true, true, '2026-07-13 06:43:59.054929', '2026-07-13 06:43:59.054931');
INSERT INTO public.departments VALUES (1165, '装配组NⅣ', '1183', NULL, 2, 9048, 1135, '1135-1165-', 26, '2', true, true, '2026-07-13 06:43:59.056067', '2026-07-13 06:43:59.05607');
INSERT INTO public.departments VALUES (1144, '机构部CⅢ', '1162', NULL, 2, 9509, 1143, '1143-1144-', 28, '5', true, true, '2026-07-13 06:43:59.057255', '2026-07-13 06:43:59.057257');
INSERT INTO public.departments VALUES (1146, '总经办NⅠ', '1164', NULL, 2, 9446, 1145, '1145-1146-', 27, '1', true, true, '2026-07-13 06:43:59.058422', '2026-07-13 06:43:59.058426');
INSERT INTO public.departments VALUES (1152, '销售NⅡ', '1170', NULL, 2, 9110, 1151, '1151-1152-', 24, '3', true, true, '2026-07-13 06:43:59.059585', '2026-07-13 06:43:59.059588');
INSERT INTO public.departments VALUES (1157, '电控组NⅣ', '1175', NULL, 2, 9047, 1155, '1155-1157-', 26, '5', true, true, '2026-07-13 06:43:59.060706', '2026-07-13 06:43:59.060709');
INSERT INTO public.departments VALUES (1158, '品质部NⅠ', '1176', NULL, 2, 9488, 1156, '1156-1158-', 27, '2', true, true, '2026-07-13 06:43:59.061852', '2026-07-13 06:43:59.061855');
INSERT INTO public.departments VALUES (1131, '人事Ⅰ', '1149', NULL, 3, 9358, 928, '882-928-1131-', 27, '1', true, true, '2026-07-13 06:43:59.063027', '2026-07-13 06:43:59.063031');
INSERT INTO public.departments VALUES (1091, '制浆/涂布项目NⅠ', '1109', NULL, 3, 9447, 1058, '1035-1058-1091-', 27, '3', true, true, '2026-07-13 06:43:59.064187', '2026-07-13 06:43:59.06419');
INSERT INTO public.departments VALUES (1153, '自动化项目NⅠ', '1171', NULL, 3, 9447, 1058, '1035-1058-1153-', 27, '3', true, true, '2026-07-13 06:43:59.065334', '2026-07-13 06:43:59.065338');
INSERT INTO public.departments VALUES (1092, '制浆/涂布项目NⅡ', '1110', NULL, 3, 9447, 1059, '1036-1059-1092-', 24, '3', true, true, '2026-07-13 06:43:59.066469', '2026-07-13 06:43:59.066472');
INSERT INTO public.departments VALUES (1093, '自动化项目NⅡ', '1111', NULL, 3, 9447, 1059, '1036-1059-1093-', 24, '3', true, true, '2026-07-13 06:43:59.067611', '2026-07-13 06:43:59.067614');
INSERT INTO public.departments VALUES (1090, '分切项目NⅢ', '1108', NULL, 3, 9447, 1060, '1037-1060-1090-', 28, '3', true, true, '2026-07-13 06:43:59.068734', '2026-07-13 06:43:59.068737');
INSERT INTO public.departments VALUES (1142, '销售NⅠ', '1160', NULL, 3, 9110, 1061, '1038-1061-1142-', 27, '3', true, true, '2026-07-13 06:43:59.069894', '2026-07-13 06:43:59.069898');
INSERT INTO public.departments VALUES (1116, '电控1组CⅡ', '1134', NULL, 3, 9479, 1072, '1044-1072-1116-', 24, '5', true, true, '2026-07-13 06:43:59.071071', '2026-07-13 06:43:59.071075');
INSERT INTO public.departments VALUES (1119, '电控2组CⅡ', '1137', NULL, 3, 637, 1072, '1044-1072-1119-', 24, '5', true, true, '2026-07-13 06:43:59.072261', '2026-07-13 06:43:59.072264');
INSERT INTO public.departments VALUES (1117, '电控1组CⅢ', '1135', NULL, 3, 9479, 1073, '1045-1073-1117-', 28, '5', true, true, '2026-07-13 06:43:59.073417', '2026-07-13 06:43:59.07342');
INSERT INTO public.departments VALUES (1120, '软件1组CⅡ', '1138', NULL, 3, 2183, 1075, '1044-1075-1120-', 24, '5', true, true, '2026-07-13 06:43:59.07457', '2026-07-13 06:43:59.074573');
INSERT INTO public.departments VALUES (1122, '软件2组CⅡ', '1140', NULL, 3, 6223, 1075, '1044-1075-1122-', 24, '5', true, true, '2026-07-13 06:43:59.075742', '2026-07-13 06:43:59.075745');
INSERT INTO public.departments VALUES (1108, '质量检验CⅡ', '1126', NULL, 3, 781, 1078, '1047-1078-1108-', 24, '2', true, true, '2026-07-13 06:43:59.07688', '2026-07-13 06:43:59.076883');
INSERT INTO public.departments VALUES (1109, '质量体系CⅡ', '1127', NULL, 3, 781, 1078, '1047-1078-1109-', 24, '2', true, true, '2026-07-13 06:43:59.078061', '2026-07-13 06:43:59.078064');
INSERT INTO public.departments VALUES (1138, '生产机构装配CⅡ', '1156', NULL, 3, 195, 1079, '1047-1079-1138-', 24, '2', true, true, '2026-07-13 06:43:59.079213', '2026-07-13 06:43:59.079216');
INSERT INTO public.departments VALUES (1139, '生产电气装配CⅡ', '1157', NULL, 3, 195, 1079, '1047-1079-1139-', 24, '2', true, true, '2026-07-13 06:43:59.080368', '2026-07-13 06:43:59.080371');
INSERT INTO public.departments VALUES (1140, '售后机构装配CⅡ', '1158', NULL, 3, 195, 1080, '1047-1080-1140-', 24, '2', true, true, '2026-07-13 06:43:59.081475', '2026-07-13 06:43:59.081478');
INSERT INTO public.departments VALUES (1141, '售后电气装配CⅡ', '1159', NULL, 3, 195, 1080, '1047-1080-1141-', 24, '2', true, true, '2026-07-13 06:43:59.082629', '2026-07-13 06:43:59.082632');
INSERT INTO public.departments VALUES (1113, '采购开发Ⅰ', '1128', NULL, 3, 9338, 1086, '1052-1086-1113-', 27, '2', true, true, '2026-07-13 06:43:59.083846', '2026-07-13 06:43:59.083849');
INSERT INTO public.departments VALUES (1114, '采购执行Ⅰ', '1129', NULL, 3, 9338, 1086, '1052-1086-1114-', 27, '2', true, true, '2026-07-13 06:43:59.085114', '2026-07-13 06:43:59.085118');
INSERT INTO public.departments VALUES (1115, '仓储Ⅱ', '1130', NULL, 3, 9353, 1087, '1053-1087-1115-', 24, '2', true, true, '2026-07-13 06:43:59.086389', '2026-07-13 06:43:59.086392');
INSERT INTO public.departments VALUES (1111, '物流Ⅰ', '1132', NULL, 3, 3489, 1088, '1052-1088-1111-', 27, '2', true, true, '2026-07-13 06:43:59.087673', '2026-07-13 06:43:59.087677');
INSERT INTO public.departments VALUES (1110, '计划Ⅱ', '1131', NULL, 3, 3489, 1089, '1053-1089-1110-', 24, '2', true, true, '2026-07-13 06:43:59.088918', '2026-07-13 06:43:59.088922');
INSERT INTO public.departments VALUES (1112, '物料Ⅱ', '1133', NULL, 3, 3489, 1089, '1053-1089-1112-', 24, '2', true, true, '2026-07-13 06:43:59.090233', '2026-07-13 06:43:59.090236');
INSERT INTO public.departments VALUES (1162, '制缸NⅢ', '1180', NULL, 3, 9051, 1096, '1042-1096-1162-', 28, '2', true, true, '2026-07-13 06:43:59.091569', '2026-07-13 06:43:59.091572');
INSERT INTO public.departments VALUES (1136, '分切项目NⅣ', '1154', NULL, 3, 9447, 1134, '1132-1134-1136-', 26, '3', true, true, '2026-07-13 06:43:59.09284', '2026-07-13 06:43:59.092843');
INSERT INTO public.departments VALUES (1163, '制缸NⅠ', '1181', NULL, 3, 9051, 1147, '1040-1147-1163-', 27, '2', true, true, '2026-07-13 06:43:59.09404', '2026-07-13 06:43:59.094044');
INSERT INTO public.departments VALUES (1098, '萃取设备NⅢ', '1116', NULL, 3, 9048, 1149, '1042-1149-1098-', 28, '2', true, true, '2026-07-13 06:43:59.095216', '2026-07-13 06:43:59.095219');
INSERT INTO public.departments VALUES (1099, '分切设备NⅢ', '1117', NULL, 3, 9048, 1149, '1042-1149-1099-', 28, '2', true, true, '2026-07-13 06:43:59.096386', '2026-07-13 06:43:59.09639');
INSERT INTO public.departments VALUES (1094, '车床NⅢ', '1112', NULL, 3, 9050, 1164, '1042-1164-1094-', 28, '2', true, true, '2026-07-13 06:43:59.097512', '2026-07-13 06:43:59.097515');
INSERT INTO public.departments VALUES (1095, '铣床NⅢ', '1113', NULL, 3, 9050, 1164, '1042-1164-1095-', 28, '2', true, true, '2026-07-13 06:43:59.098634', '2026-07-13 06:43:59.098637');
INSERT INTO public.departments VALUES (1171, '打磨组NⅢ', '1189', NULL, 3, 9050, 1164, '1042-1164-1171-', 28, '2', true, true, '2026-07-13 06:43:59.09978', '2026-07-13 06:43:59.099783');
INSERT INTO public.departments VALUES (1172, '钳工NⅢ', '1190', NULL, 3, 9050, 1164, '1042-1164-1172-', 28, '2', true, true, '2026-07-13 06:43:59.100946', '2026-07-13 06:43:59.10095');
INSERT INTO public.departments VALUES (1137, '分切设备NⅣ', '1155', NULL, 3, 9048, 1165, '1135-1165-1137-', 26, '2', true, true, '2026-07-13 06:43:59.102106', '2026-07-13 06:43:59.102109');
INSERT INTO public.departments VALUES (1167, '萃取设备NⅠ', '1185', NULL, 3, 9048, 1166, '1040-1166-1167-', 27, '2', true, true, '2026-07-13 06:43:59.10331', '2026-07-13 06:43:59.103312');


ALTER TABLE public.departments ENABLE TRIGGER ALL;

--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.positions DISABLE TRIGGER ALL;

INSERT INTO public.positions VALUES (82, '3D动漫设计', '114', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.125207', '2026-07-13 06:43:59.125212');
INSERT INTO public.positions VALUES (83, '5S专员', '115', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.126997', '2026-07-13 06:43:59.127001');
INSERT INTO public.positions VALUES (84, 'IT', '116', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.128454', '2026-07-13 06:43:59.128459');
INSERT INTO public.positions VALUES (85, '采购', '117', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.129806', '2026-07-13 06:43:59.129811');
INSERT INTO public.positions VALUES (86, '仓管', '118', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.131209', '2026-07-13 06:43:59.131213');
INSERT INTO public.positions VALUES (87, '常熟宿管', '119', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.132347', '2026-07-13 06:43:59.132351');
INSERT INTO public.positions VALUES (88, '常务副总', '120', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.133397', '2026-07-13 06:43:59.133401');
INSERT INTO public.positions VALUES (89, '厂务', '121', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.134441', '2026-07-13 06:43:59.134444');
INSERT INTO public.positions VALUES (90, '成本会计', '122', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.135462', '2026-07-13 06:43:59.135465');
INSERT INTO public.positions VALUES (91, '出纳', '123', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.13651', '2026-07-13 06:43:59.136512');
INSERT INTO public.positions VALUES (92, '大组长', '124', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.137549', '2026-07-13 06:43:59.137553');
INSERT INTO public.positions VALUES (93, '代理大组长', '125', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.138562', '2026-07-13 06:43:59.138565');
INSERT INTO public.positions VALUES (94, '电工', '126', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.139561', '2026-07-13 06:43:59.139565');
INSERT INTO public.positions VALUES (95, '电气工程师', '127', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.140634', '2026-07-13 06:43:59.140637');
INSERT INTO public.positions VALUES (96, '电气检验', '128', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.141689', '2026-07-13 06:43:59.141692');
INSERT INTO public.positions VALUES (97, '电气设计', '129', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.142709', '2026-07-13 06:43:59.142712');
INSERT INTO public.positions VALUES (98, '电气装配', '130', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.143709', '2026-07-13 06:43:59.143712');
INSERT INTO public.positions VALUES (99, '副经理', '131', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.144701', '2026-07-13 06:43:59.144704');
INSERT INTO public.positions VALUES (100, '副主管', '132', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.145713', '2026-07-13 06:43:59.145716');
INSERT INTO public.positions VALUES (101, '副总经理', '133', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.146721', '2026-07-13 06:43:59.146725');
INSERT INTO public.positions VALUES (102, '高级工艺经理', '134', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.147722', '2026-07-13 06:43:59.147725');
INSERT INTO public.positions VALUES (103, '高级经理', '135', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.148728', '2026-07-13 06:43:59.148732');
INSERT INTO public.positions VALUES (104, '售后工程师', '136', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.149764', '2026-07-13 06:43:59.149767');
INSERT INTO public.positions VALUES (105, '生产工艺工程师', '137', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.150779', '2026-07-13 06:43:59.150782');
INSERT INTO public.positions VALUES (106, '质量工程师', '138', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.151827', '2026-07-13 06:43:59.15183');
INSERT INTO public.positions VALUES (107, '气密性售后工程师', '139', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.152848', '2026-07-13 06:43:59.152852');
INSERT INTO public.positions VALUES (108, '采购工程师', '140', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.153852', '2026-07-13 06:43:59.153856');
INSERT INTO public.positions VALUES (109, '工艺副主管', '141', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.154855', '2026-07-13 06:43:59.154858');
INSERT INTO public.positions VALUES (110, '关务', '142', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.155893', '2026-07-13 06:43:59.155897');
INSERT INTO public.positions VALUES (111, '行政专员', '143', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.156958', '2026-07-13 06:43:59.156962');
INSERT INTO public.positions VALUES (112, '合并报表会计', '144', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.158', '2026-07-13 06:43:59.158003');
INSERT INTO public.positions VALUES (113, '绘图', '145', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.159008', '2026-07-13 06:43:59.159012');
INSERT INTO public.positions VALUES (114, '机器人应用', '146', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.160007', '2026-07-13 06:43:59.16001');
INSERT INTO public.positions VALUES (115, '机器视觉副经理', '147', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.161043', '2026-07-13 06:43:59.161046');
INSERT INTO public.positions VALUES (116, '机械检验', '148', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.162065', '2026-07-13 06:43:59.162069');
INSERT INTO public.positions VALUES (117, '机械经理', '149', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.163065', '2026-07-13 06:43:59.163069');
INSERT INTO public.positions VALUES (118, '机械设计', '150', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.164087', '2026-07-13 06:43:59.164091');
INSERT INTO public.positions VALUES (119, '机械装配', '151', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.16512', '2026-07-13 06:43:59.165123');
INSERT INTO public.positions VALUES (120, '技术经理', '152', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.166146', '2026-07-13 06:43:59.166149');
INSERT INTO public.positions VALUES (121, '进料检验', '153', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.167158', '2026-07-13 06:43:59.167161');
INSERT INTO public.positions VALUES (122, '经理', '154', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.168168', '2026-07-13 06:43:59.168171');
INSERT INTO public.positions VALUES (123, '量测', '155', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.169179', '2026-07-13 06:43:59.169182');
INSERT INTO public.positions VALUES (124, '品检', '156', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.170214', '2026-07-13 06:43:59.170217');
INSERT INTO public.positions VALUES (125, '前台', '157', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.171225', '2026-07-13 06:43:59.171229');
INSERT INTO public.positions VALUES (126, '人力成本会计', '158', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.172232', '2026-07-13 06:43:59.172236');
INSERT INTO public.positions VALUES (127, '软件副主管', '159', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.17326', '2026-07-13 06:43:59.173264');
INSERT INTO public.positions VALUES (128, '软件工程师', '160', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.174255', '2026-07-13 06:43:59.174259');
INSERT INTO public.positions VALUES (129, '商务管理', '161', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.175267', '2026-07-13 06:43:59.17527');
INSERT INTO public.positions VALUES (130, '商务专员', '162', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.176319', '2026-07-13 06:43:59.176321');
INSERT INTO public.positions VALUES (131, '生产计划', '163', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.177323', '2026-07-13 06:43:59.177326');
INSERT INTO public.positions VALUES (132, '市场经理', '164', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.178356', '2026-07-13 06:43:59.178359');
INSERT INTO public.positions VALUES (133, '市场开发经理', '165', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.179387', '2026-07-13 06:43:59.179391');
INSERT INTO public.positions VALUES (134, '市场专员', '166', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.180408', '2026-07-13 06:43:59.180411');
INSERT INTO public.positions VALUES (135, '售后工程师', '167', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.18141', '2026-07-13 06:43:59.181414');
INSERT INTO public.positions VALUES (136, '司机', '168', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.182452', '2026-07-13 06:43:59.182455');
INSERT INTO public.positions VALUES (137, '调试工程师', '169', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.183473', '2026-07-13 06:43:59.183476');
INSERT INTO public.positions VALUES (138, '现金出纳', '170', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.184484', '2026-07-13 06:43:59.184487');
INSERT INTO public.positions VALUES (139, '项目工程师', '171', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.185545', '2026-07-13 06:43:59.185548');
INSERT INTO public.positions VALUES (140, '销售工程师', '172', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.186545', '2026-07-13 06:43:59.186549');
INSERT INTO public.positions VALUES (141, '小组长', '173', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.187532', '2026-07-13 06:43:59.187535');
INSERT INTO public.positions VALUES (142, '薪酬专员', '174', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.188502', '2026-07-13 06:43:59.188506');
INSERT INTO public.positions VALUES (143, '业务工程师', '175', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.189509', '2026-07-13 06:43:59.189512');
INSERT INTO public.positions VALUES (144, '制程检验', '176', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.190508', '2026-07-13 06:43:59.190511');
INSERT INTO public.positions VALUES (145, '治具设计', '177', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.191495', '2026-07-13 06:43:59.191498');
INSERT INTO public.positions VALUES (146, '治具设计工程师', '178', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.192468', '2026-07-13 06:43:59.192471');
INSERT INTO public.positions VALUES (147, '主办会计', '179', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.19343', '2026-07-13 06:43:59.193433');
INSERT INTO public.positions VALUES (148, '主管', '180', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.194378', '2026-07-13 06:43:59.194382');
INSERT INTO public.positions VALUES (149, '专机助理', '181', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.195389', '2026-07-13 06:43:59.195392');
INSERT INTO public.positions VALUES (150, '售后助理', '182', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.196416', '2026-07-13 06:43:59.196421');
INSERT INTO public.positions VALUES (151, '计划助理', '183', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.197398', '2026-07-13 06:43:59.197402');
INSERT INTO public.positions VALUES (152, '项目助理', '184', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.19837', '2026-07-13 06:43:59.198374');
INSERT INTO public.positions VALUES (153, '总经理特别助理', '185', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.199374', '2026-07-13 06:43:59.199378');
INSERT INTO public.positions VALUES (154, '助理电控设计', '186', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.200387', '2026-07-13 06:43:59.20039');
INSERT INTO public.positions VALUES (155, '助理电气设计', '187', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.20138', '2026-07-13 06:43:59.201383');
INSERT INTO public.positions VALUES (156, '助理工程师', '188', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.202341', '2026-07-13 06:43:59.202345');
INSERT INTO public.positions VALUES (157, '助理机械设计', '189', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.203313', '2026-07-13 06:43:59.203317');
INSERT INTO public.positions VALUES (158, '助理项目工程师', '190', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.204325', '2026-07-13 06:43:59.204329');
INSERT INTO public.positions VALUES (159, '专机调试', '191', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.205306', '2026-07-13 06:43:59.205309');
INSERT INTO public.positions VALUES (160, '资源开发高级工程师', '192', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.206272', '2026-07-13 06:43:59.206275');
INSERT INTO public.positions VALUES (161, '资源开发工程师', '193', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.207234', '2026-07-13 06:43:59.207238');
INSERT INTO public.positions VALUES (162, '自动化', '194', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.208239', '2026-07-13 06:43:59.208242');
INSERT INTO public.positions VALUES (163, '总经理', '195', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.209225', '2026-07-13 06:43:59.209228');
INSERT INTO public.positions VALUES (164, '质量非标组长', '196', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.210216', '2026-07-13 06:43:59.210219');
INSERT INTO public.positions VALUES (165, '仓库组长', '197', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.211179', '2026-07-13 06:43:59.211182');
INSERT INTO public.positions VALUES (166, 'CNC电控设计', '198', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.212175', '2026-07-13 06:43:59.212178');
INSERT INTO public.positions VALUES (167, 'CNC工艺工程师', '199', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.213181', '2026-07-13 06:43:59.213184');
INSERT INTO public.positions VALUES (168, 'CNC机构设计', '200', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.214193', '2026-07-13 06:43:59.214197');
INSERT INTO public.positions VALUES (169, 'CNC机械设计', '201', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.215173', '2026-07-13 06:43:59.215176');
INSERT INTO public.positions VALUES (170, 'CNC调试开发', '202', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.216173', '2026-07-13 06:43:59.216176');
INSERT INTO public.positions VALUES (171, 'IOS开发工程师', '203', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.217139', '2026-07-13 06:43:59.217143');
INSERT INTO public.positions VALUES (172, 'Java开发工程师', '204', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.218147', '2026-07-13 06:43:59.21815');
INSERT INTO public.positions VALUES (173, 'TPM', '205', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.219161', '2026-07-13 06:43:59.219164');
INSERT INTO public.positions VALUES (174, '采购', '206', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.220154', '2026-07-13 06:43:59.220158');
INSERT INTO public.positions VALUES (175, '仓管', '207', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.22116', '2026-07-13 06:43:59.221164');
INSERT INTO public.positions VALUES (176, '仓管员', '208', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.222144', '2026-07-13 06:43:59.222147');
INSERT INTO public.positions VALUES (177, '大组长', '209', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.223098', '2026-07-13 06:43:59.223101');
INSERT INTO public.positions VALUES (178, '代理大组长', '210', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.224077', '2026-07-13 06:43:59.22408');
INSERT INTO public.positions VALUES (179, '档案管理', '211', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.225176', '2026-07-13 06:43:59.225179');
INSERT INTO public.positions VALUES (180, '电气工程师', '212', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.226202', '2026-07-13 06:43:59.226205');
INSERT INTO public.positions VALUES (181, '电气助理工程师', '213', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.227231', '2026-07-13 06:43:59.227234');
INSERT INTO public.positions VALUES (182, '电气装配', '214', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.228259', '2026-07-13 06:43:59.228263');
INSERT INTO public.positions VALUES (183, '电子工程师', '215', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.229238', '2026-07-13 06:43:59.229241');
INSERT INTO public.positions VALUES (184, '副经理', '216', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.23019', '2026-07-13 06:43:59.230194');
INSERT INTO public.positions VALUES (185, '副主管', '217', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.231187', '2026-07-13 06:43:59.23119');
INSERT INTO public.positions VALUES (186, '高级经理', '218', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.232196', '2026-07-13 06:43:59.232199');
INSERT INTO public.positions VALUES (187, '高级助理', '219', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.233169', '2026-07-13 06:43:59.233173');
INSERT INTO public.positions VALUES (188, '售后工程师', '220', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.234119', '2026-07-13 06:43:59.234122');
INSERT INTO public.positions VALUES (189, '非标生产工程师', '221', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.235091', '2026-07-13 06:43:59.235094');
INSERT INTO public.positions VALUES (190, '工艺工程师', '222', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.236124', '2026-07-13 06:43:59.236142');
INSERT INTO public.positions VALUES (191, '工业工程师', '223', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.237125', '2026-07-13 06:43:59.237142');
INSERT INTO public.positions VALUES (192, '工艺工程师', '224', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.238095', '2026-07-13 06:43:59.238098');
INSERT INTO public.positions VALUES (193, '售后机器人服务工程师', '225', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.239047', '2026-07-13 06:43:59.23905');
INSERT INTO public.positions VALUES (194, '顾问', '226', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.240014', '2026-07-13 06:43:59.240018');
INSERT INTO public.positions VALUES (195, '刮研技工', '227', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.241027', '2026-07-13 06:43:59.24103');
INSERT INTO public.positions VALUES (196, '机器人应用', '228', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.242016', '2026-07-13 06:43:59.242019');
INSERT INTO public.positions VALUES (197, '机械副经理', '229', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.243002', '2026-07-13 06:43:59.243005');
INSERT INTO public.positions VALUES (198, '机械副主管', '230', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.244044', '2026-07-13 06:43:59.244047');
INSERT INTO public.positions VALUES (199, '机械工程师', '231', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.245046', '2026-07-13 06:43:59.245049');
INSERT INTO public.positions VALUES (200, '机械设计', '232', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.246038', '2026-07-13 06:43:59.246041');
INSERT INTO public.positions VALUES (201, '机械装配', '233', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.247019', '2026-07-13 06:43:59.247022');
INSERT INTO public.positions VALUES (202, '机械组长', '234', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.248053', '2026-07-13 06:43:59.248056');
INSERT INTO public.positions VALUES (203, '技术支持副经理', '235', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.249051', '2026-07-13 06:43:59.249054');
INSERT INTO public.positions VALUES (204, '绩效专员', '236', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.250008', '2026-07-13 06:43:59.250012');
INSERT INTO public.positions VALUES (205, '检验', '237', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.250969', '2026-07-13 06:43:59.250972');
INSERT INTO public.positions VALUES (206, '检验员', '238', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.251936', '2026-07-13 06:43:59.251939');
INSERT INTO public.positions VALUES (207, '经理', '239', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.25295', '2026-07-13 06:43:59.252954');
INSERT INTO public.positions VALUES (208, '量测', '240', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.253941', '2026-07-13 06:43:59.253944');
INSERT INTO public.positions VALUES (209, '软件测试工程师', '241', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.254906', '2026-07-13 06:43:59.25491');
INSERT INTO public.positions VALUES (210, '软件工程师', '242', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.255873', '2026-07-13 06:43:59.255876');
INSERT INTO public.positions VALUES (211, '软件经理', '243', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.25684', '2026-07-13 06:43:59.256844');
INSERT INTO public.positions VALUES (212, '商务专员', '244', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.257844', '2026-07-13 06:43:59.257848');
INSERT INTO public.positions VALUES (213, '生产计划', '245', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.258817', '2026-07-13 06:43:59.258821');
INSERT INTO public.positions VALUES (214, '生产主管', '246', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.259798', '2026-07-13 06:43:59.259801');
INSERT INTO public.positions VALUES (215, '实施工程师', '247', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.260767', '2026-07-13 06:43:59.260771');
INSERT INTO public.positions VALUES (216, '人事实习生', '248', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.261772', '2026-07-13 06:43:59.261775');
INSERT INTO public.positions VALUES (217, '采购实习生', '249', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.262752', '2026-07-13 06:43:59.262755');
INSERT INTO public.positions VALUES (218, '市场专员', '250', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.26373', '2026-07-13 06:43:59.263733');
INSERT INTO public.positions VALUES (219, '售后工程师', '251', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.264711', '2026-07-13 06:43:59.264714');
INSERT INTO public.positions VALUES (220, '售后工程师', '252', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.265725', '2026-07-13 06:43:59.265728');
INSERT INTO public.positions VALUES (221, '体系工程师', '253', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.26671', '2026-07-13 06:43:59.266713');
INSERT INTO public.positions VALUES (222, '文控', '254', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.267693', '2026-07-13 06:43:59.267696');
INSERT INTO public.positions VALUES (223, '项目副经理', '255', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.26865', '2026-07-13 06:43:59.268653');
INSERT INTO public.positions VALUES (224, '项目工程师', '256', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.26967', '2026-07-13 06:43:59.269673');
INSERT INTO public.positions VALUES (225, '销售副经理', '257', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.270665', '2026-07-13 06:43:59.270668');
INSERT INTO public.positions VALUES (226, '小组长', '258', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.271634', '2026-07-13 06:43:59.271637');
INSERT INTO public.positions VALUES (227, '业务经理', '259', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.272608', '2026-07-13 06:43:59.272612');
INSERT INTO public.positions VALUES (228, '业务专员', '260', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.273632', '2026-07-13 06:43:59.273635');
INSERT INTO public.positions VALUES (229, '招聘专员', '261', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.274637', '2026-07-13 06:43:59.274641');
INSERT INTO public.positions VALUES (230, '主管', '262', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.275647', '2026-07-13 06:43:59.27565');
INSERT INTO public.positions VALUES (231, '人事助理', '263', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.276637', '2026-07-13 06:43:59.276641');
INSERT INTO public.positions VALUES (232, '计划助理', '264', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.277688', '2026-07-13 06:43:59.277692');
INSERT INTO public.positions VALUES (233, '采购助理', '265', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.278675', '2026-07-13 06:43:59.278678');
INSERT INTO public.positions VALUES (234, '行政助理', '266', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.279638', '2026-07-13 06:43:59.279641');
INSERT INTO public.positions VALUES (235, '售后助理', '267', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.280626', '2026-07-13 06:43:59.280629');
INSERT INTO public.positions VALUES (236, '助理电子工程师', '268', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.281643', '2026-07-13 06:43:59.281647');
INSERT INTO public.positions VALUES (237, '助理工程师', '269', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.282721', '2026-07-13 06:43:59.282724');
INSERT INTO public.positions VALUES (238, '助理机械工程师', '270', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.283884', '2026-07-13 06:43:59.283888');
INSERT INTO public.positions VALUES (239, '助理机械设计', '271', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.285344', '2026-07-13 06:43:59.285347');
INSERT INTO public.positions VALUES (240, '助理软件工程师', '272', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.286774', '2026-07-13 06:43:59.286778');
INSERT INTO public.positions VALUES (241, '专机调试', '273', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.28824', '2026-07-13 06:43:59.288244');
INSERT INTO public.positions VALUES (242, '装配', '274', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.289656', '2026-07-13 06:43:59.28966');
INSERT INTO public.positions VALUES (243, '资深采购工程师', '275', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.29105', '2026-07-13 06:43:59.291053');
INSERT INTO public.positions VALUES (244, '资深机械工程师', '276', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.29252', '2026-07-13 06:43:59.292523');
INSERT INTO public.positions VALUES (245, '资深机械设计', '277', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.293979', '2026-07-13 06:43:59.293983');
INSERT INTO public.positions VALUES (246, '自动化', '278', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.295423', '2026-07-13 06:43:59.295426');
INSERT INTO public.positions VALUES (247, '总经理', '279', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.296839', '2026-07-13 06:43:59.296843');
INSERT INTO public.positions VALUES (248, '组长', '280', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.29828', '2026-07-13 06:43:59.298283');
INSERT INTO public.positions VALUES (249, '实习生', '281', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.299737', '2026-07-13 06:43:59.29974');
INSERT INTO public.positions VALUES (250, '物料员', '282', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.30117', '2026-07-13 06:43:59.301174');
INSERT INTO public.positions VALUES (251, '机器人应用工程师', '283', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.302597', '2026-07-13 06:43:59.3026');
INSERT INTO public.positions VALUES (252, '人事经理', '300', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.304048', '2026-07-13 06:43:59.304051');
INSERT INTO public.positions VALUES (253, '建模师', '301', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.305462', '2026-07-13 06:43:59.305465');
INSERT INTO public.positions VALUES (254, '工程师', '302', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.306857', '2026-07-13 06:43:59.306861');
INSERT INTO public.positions VALUES (255, '电气设计工程师', '303', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.308266', '2026-07-13 06:43:59.30827');
INSERT INTO public.positions VALUES (256, '总经办助理', '304', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.309686', '2026-07-13 06:43:59.309688');
INSERT INTO public.positions VALUES (257, '总经办助理', '313', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.311083', '2026-07-13 06:43:59.311087');
INSERT INTO public.positions VALUES (258, '总经办助理', '314', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.312498', '2026-07-13 06:43:59.312501');
INSERT INTO public.positions VALUES (259, '专员', '315', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.313908', '2026-07-13 06:43:59.313912');
INSERT INTO public.positions VALUES (260, '会计', '316', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.315433', '2026-07-13 06:43:59.315436');
INSERT INTO public.positions VALUES (261, '助理工程师', '317', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.316863', '2026-07-13 06:43:59.316866');
INSERT INTO public.positions VALUES (262, '质检', '318', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.318278', '2026-07-13 06:43:59.318281');
INSERT INTO public.positions VALUES (263, '技术员', '319', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.319692', '2026-07-13 06:43:59.319695');
INSERT INTO public.positions VALUES (264, '助理', '320', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.321163', '2026-07-13 06:43:59.321166');
INSERT INTO public.positions VALUES (265, '计划员', '321', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.322547', '2026-07-13 06:43:59.322551');
INSERT INTO public.positions VALUES (266, '品检', '322', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.32394', '2026-07-13 06:43:59.323943');
INSERT INTO public.positions VALUES (267, '特别助理', '323', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.32535', '2026-07-13 06:43:59.325353');
INSERT INTO public.positions VALUES (268, '总监', '324', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.326743', '2026-07-13 06:43:59.326746');
INSERT INTO public.positions VALUES (269, '高级工程师', '325', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.328152', '2026-07-13 06:43:59.328155');
INSERT INTO public.positions VALUES (270, '常务副总经理', '330', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.329553', '2026-07-13 06:43:59.329556');
INSERT INTO public.positions VALUES (271, '区域主管', '399', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.330958', '2026-07-13 06:43:59.330962');
INSERT INTO public.positions VALUES (272, '副总监', '400', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.332384', '2026-07-13 06:43:59.332387');
INSERT INTO public.positions VALUES (273, '总经理助理', '401', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.333771', '2026-07-13 06:43:59.333775');
INSERT INTO public.positions VALUES (274, '顾问', '402', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.335191', '2026-07-13 06:43:59.335194');
INSERT INTO public.positions VALUES (275, '总经理特助', '403', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.336564', '2026-07-13 06:43:59.336567');
INSERT INTO public.positions VALUES (276, '专家', '404', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.338031', '2026-07-13 06:43:59.338034');
INSERT INTO public.positions VALUES (277, '部长', '405', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.339451', '2026-07-13 06:43:59.339454');
INSERT INTO public.positions VALUES (278, '焊工', '406', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.340861', '2026-07-13 06:43:59.340864');
INSERT INTO public.positions VALUES (279, 'CNC操作工', '407', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.342316', '2026-07-13 06:43:59.342319');
INSERT INTO public.positions VALUES (280, '铣床工', '408', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.343763', '2026-07-13 06:43:59.343766');
INSERT INTO public.positions VALUES (281, 'CNC工程师', '409', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.344986', '2026-07-13 06:43:59.344989');
INSERT INTO public.positions VALUES (282, '产品助理', '410', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.346591', '2026-07-13 06:43:59.346594');
INSERT INTO public.positions VALUES (283, '储罐项目及制浆系统负责人', '411', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.34799', '2026-07-13 06:43:59.347993');
INSERT INTO public.positions VALUES (284, '储罐项目及制浆系统负责人', '412', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.3494', '2026-07-13 06:43:59.349403');
INSERT INTO public.positions VALUES (285, '磨床工', '413', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.350803', '2026-07-13 06:43:59.350806');
INSERT INTO public.positions VALUES (286, '数控车工', '414', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.352252', '2026-07-13 06:43:59.352255');
INSERT INTO public.positions VALUES (287, '机加钳工', '415', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.353632', '2026-07-13 06:43:59.353635');
INSERT INTO public.positions VALUES (288, '跟单', '416', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.35503', '2026-07-13 06:43:59.355033');
INSERT INTO public.positions VALUES (289, '激光下料工', '417', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.356483', '2026-07-13 06:43:59.356486');
INSERT INTO public.positions VALUES (290, '抛光工', '418', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.35788', '2026-07-13 06:43:59.357884');
INSERT INTO public.positions VALUES (291, '线切割技师', '419', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.359367', '2026-07-13 06:43:59.35937');
INSERT INTO public.positions VALUES (292, '冷作工', '420', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.360773', '2026-07-13 06:43:59.360777');
INSERT INTO public.positions VALUES (293, '管道安装工', '421', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.362168', '2026-07-13 06:43:59.362172');
INSERT INTO public.positions VALUES (294, '业务经理', '422', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.363612', '2026-07-13 06:43:59.363615');
INSERT INTO public.positions VALUES (295, '业务副经理', '423', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.365002', '2026-07-13 06:43:59.365005');
INSERT INTO public.positions VALUES (296, '项目管理兼翻译', '424', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.366438', '2026-07-13 06:43:59.366441');
INSERT INTO public.positions VALUES (297, '工厂长', '425', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.36784', '2026-07-13 06:43:59.367844');
INSERT INTO public.positions VALUES (298, '副部长', '426', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.369326', '2026-07-13 06:43:59.369329');
INSERT INTO public.positions VALUES (299, '科长', '427', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.370745', '2026-07-13 06:43:59.370748');
INSERT INTO public.positions VALUES (300, '副科长', '428', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.372181', '2026-07-13 06:43:59.372185');
INSERT INTO public.positions VALUES (301, '系长', '429', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.373567', '2026-07-13 06:43:59.373571');
INSERT INTO public.positions VALUES (302, '主任', '430', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.374943', '2026-07-13 06:43:59.374946');
INSERT INTO public.positions VALUES (303, '采购担当', '431', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.37639', '2026-07-13 06:43:59.376393');
INSERT INTO public.positions VALUES (304, '仓库担当', '432', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.377816', '2026-07-13 06:43:59.37782');
INSERT INTO public.positions VALUES (305, '机械担当', '433', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.379257', '2026-07-13 06:43:59.37926');
INSERT INTO public.positions VALUES (306, '制缸担当', '434', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.380698', '2026-07-13 06:43:59.380701');
INSERT INTO public.positions VALUES (307, '组装担当', '435', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.38207', '2026-07-13 06:43:59.382074');
INSERT INTO public.positions VALUES (308, '部长', '436', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.383479', '2026-07-13 06:43:59.383482');
INSERT INTO public.positions VALUES (309, '总经理助理兼人力资源总监', '437', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.384888', '2026-07-13 06:43:59.384892');
INSERT INTO public.positions VALUES (310, '副总经理兼CMO', '438', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.386373', '2026-07-13 06:43:59.386377');
INSERT INTO public.positions VALUES (311, '副总监', '439', NULL, '3', NULL, true, true, '2026-07-13 06:43:59.387804', '2026-07-13 06:43:59.387808');
INSERT INTO public.positions VALUES (312, '系长兼总经理助理', '440', NULL, '1', NULL, true, true, '2026-07-13 06:43:59.389236', '2026-07-13 06:43:59.389239');
INSERT INTO public.positions VALUES (313, '动力技术员', '441', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.390595', '2026-07-13 06:43:59.390598');
INSERT INTO public.positions VALUES (314, '打磨工', '442', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.39202', '2026-07-13 06:43:59.392022');
INSERT INTO public.positions VALUES (315, '装配工', '443', NULL, '2', NULL, true, true, '2026-07-13 06:43:59.393467', '2026-07-13 06:43:59.39347');


ALTER TABLE public.positions ENABLE TRIGGER ALL;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.users DISABLE TRIGGER ALL;

INSERT INTO public.users VALUES (1, 'admin', 'scrypt:32768:8:1$zKiIJLgNhncGm4zm$9c6da75f420506f1e642df5ecc4fc650511d7ebef1bc1f87220e9459a8899618514bd2b4a1ef3fdde26fa36f1d2d032371e37343a08f2b0cd5922bba3cc5fe0b', '系统管理员', 'admin', NULL, NULL, NULL, true, true, '2026-07-13 06:32:20.867177', '2026-07-13 06:32:20.867184');
INSERT INTO public.users VALUES (2, 'RS100', 'scrypt:32768:8:1$PAfMU00f9TowsGy8$ef84c7e4cacf69d76733a99cd219c4c72bd5dede5ac58f240b21e45acfcc838d4eb943f35c04df5bd6ecc66b07fe5d2bc74c69a47325c2538658c8337d224ce7', '李洋', 'business', 195, 1141, 99, true, true, '2026-07-13 06:43:59.928557', '2026-07-13 06:43:59.928562');
INSERT INTO public.users VALUES (3, 'RS065', 'scrypt:32768:8:1$bHYsvCmj5AUibBZ5$fcebaeb5b8228453d8ba88cea806ad889de717eeb68416d3bbd293c98331921dde53db6aad1774ea2be0af6a9493d579a5cdfd94c545b566b00d5461024b8572', '胡国进', 'business', 264, 1141, 100, true, true, '2026-07-13 06:44:00.02197', '2026-07-13 06:44:00.021974');
INSERT INTO public.users VALUES (4, 'RS217', 'scrypt:32768:8:1$Bu9eb5JUPQ7pFP5O$16c854655b71ec2787ff24d7e8e8ae5de274b3599e07bd9aca39f4e420d8d8704d4486517734497492d26630e1b1a4ec116a365debe2189112af51f87ac9707a', '李吉民', 'business', 378, 1072, 103, true, true, '2026-07-13 06:44:00.119296', '2026-07-13 06:44:00.1193');
INSERT INTO public.users VALUES (5, 'RS741', 'scrypt:32768:8:1$0WQ4bm01LoPDJJxv$b566e8c4802bafdc172d8cd21dfc643ec80edb46b2dde624250012496a1290ac01b875fc3e62efeff6ca078ba1da584e5ed1149208a46171de0ea5845ad7d48f', '魏焕友', 'business', 425, 1120, 254, true, true, '2026-07-13 06:44:00.213872', '2026-07-13 06:44:00.213876');
INSERT INTO public.users VALUES (6, 'RS598', 'scrypt:32768:8:1$Dpfp9tiJthKmmKZO$bcc1c8f0f4d226710de7c888360e5dc5aa492896b24d91781f6f2c26cdc298a259a38e74c4882f3ba646b9e2f03720b382c381c3c06b02350e9cc5dbf9cb900a', '李鹏', 'business', 427, 1120, 100, true, true, '2026-07-13 06:44:00.309285', '2026-07-13 06:44:00.30929');
INSERT INTO public.users VALUES (7, 'RS768', 'scrypt:32768:8:1$PJPnTlUQM0shXHfM$4b5283075f7ef1ecf8835916db35cb0e2b0e6ead2faf375c2152f13b7d4e3653e30818694ae1af6025189d24809f37cb41aaf0dc3844675e023b1a400f6cae1b', '吴军军', 'business', 519, 1081, 100, true, true, '2026-07-13 06:44:00.403442', '2026-07-13 06:44:00.403446');
INSERT INTO public.users VALUES (8, 'RS505', 'scrypt:32768:8:1$YLQlDNhcrNC7ZJbJ$a56980bb0ea83a37fff386e42d0bae48057503465eb248bb94755953cd105a47cbca026b57972cf76b4a6258ea109b8dcf27acb934583fea3d49275a6fef3d1c', '谢国建', 'business', 563, 1119, 254, true, true, '2026-07-13 06:44:00.499771', '2026-07-13 06:44:00.499777');
INSERT INTO public.users VALUES (9, 'RS936', 'scrypt:32768:8:1$bGNt6DKEQ4rEuFvC$e13dcbf0cbbd38b518e8963e8a4c625ef91ce8cb25837ae9a2ddf47620fec4c08134302baecb73836aefaf98a7bebfcb60470cc92f21cdbf8ee02d11368ca219', '王学松', 'business', 598, 1116, 254, true, true, '2026-07-13 06:44:00.593919', '2026-07-13 06:44:00.593925');
INSERT INTO public.users VALUES (10, 'RS1350', 'scrypt:32768:8:1$fjzmYTyneC2J2mLs$0fb29c9b76ceabf5e29cec069008445d96bea1f9339e9b4594f71a2796e07b0174653dc5dfb44cb78bd9d8ad6ba1bf8520c299832df8ef74ac4fbcaa6a78e362', '苏建庭', 'business', 624, 1119, 254, true, true, '2026-07-13 06:44:00.688455', '2026-07-13 06:44:00.68846');
INSERT INTO public.users VALUES (11, 'RS827', 'scrypt:32768:8:1$oxvTokJSLEAv1dTz$f502f2ddae4fe3eabec8845c9e32c050c0d32c953d744a099fd84057c4e1079d2a80076368ea3884d7168b29f06de503c4002a5786c5d118e78fb873d86db9ba', '胡锴莉', 'business', 637, 1119, 100, true, true, '2026-07-13 06:44:00.78259', '2026-07-13 06:44:00.782596');
INSERT INTO public.users VALUES (12, 'RS1649', 'scrypt:32768:8:1$wq9WIDPnqo180qNx$81be1043002013bea58cc4e0adccc201a2a64b926f826c6b93fc9b3ef3d5c6bed0cf5e9cf372896c120e6d0c9363ea87454a2312141fb8d305c0bb508a09b47b', '柳正荣', 'business', 666, 1076, 254, true, true, '2026-07-13 06:44:00.878468', '2026-07-13 06:44:00.878472');
INSERT INTO public.users VALUES (13, 'RS1799', 'scrypt:32768:8:1$TdVYMDZ0Ue0DlAPL$866161c51c16860d8beca3cc5b6831afaf3be64b2212f81040ad378bfe6732565ff635ae4183ad6676fdb7885252489372be2770becfbd108c844e868ad6a88a', '王玉明', 'business', 731, 1081, 148, true, true, '2026-07-13 06:44:00.974627', '2026-07-13 06:44:00.974632');
INSERT INTO public.users VALUES (14, 'RS1897', 'scrypt:32768:8:1$3wPezUgtKOjKZQpN$0bd35b04b0667d33ce96e2d7fa2d1459cac13d7d883270291fe5ce9a593ceceb9b951415c1629b3da1ce1a02182e54a8bcd73edeeac05d7b6a07a2f496a3fd37', '王大磊', 'business', 781, 1077, 99, true, true, '2026-07-13 06:44:01.064847', '2026-07-13 06:44:01.064851');
INSERT INTO public.users VALUES (15, 'RS3602', 'scrypt:32768:8:1$ElXFhOphQJIaIvd8$f235094805d02f51371adfe123224226293738b5451604bfdb96a2233b0f605954ecdde8c47fd2fc55e532d004733163d9b77e0f89e1e55d1766cf95e2c3699f', '闵国军', 'business', 1262, 1116, 254, true, true, '2026-07-13 06:44:01.160213', '2026-07-13 06:44:01.160217');
INSERT INTO public.users VALUES (16, 'RS3646', 'scrypt:32768:8:1$8GPm76ruGbkWEVl8$a51862c83147f7db4e389595696e68d0daa6a6aee8a6cf9713b5c45d8dfb799a384a1696251f9794eebb2c2f047ccb886e14a9df9a951f3a64796d8de44b2747', '卢云峰', 'business', 1301, 1116, 254, true, true, '2026-07-13 06:44:01.253297', '2026-07-13 06:44:01.253301');
INSERT INTO public.users VALUES (17, 'RS4560', 'scrypt:32768:8:1$CmiVAfWTePMhfoec$36d91cef14a2ec62859683222a6b69964e56810c0e83b6c98aab974b86b5a0d88c52d51e088d61b70f0a8b8af30a884f9915c2e88b9f6f4525efea2ad8ff9591', '刘加庆', 'business', 2183, 1120, 148, true, true, '2026-07-13 06:44:01.348889', '2026-07-13 06:44:01.348894');
INSERT INTO public.users VALUES (18, 'RS5477', 'scrypt:32768:8:1$B1z8a6sFJXom0vTe$a46e93a78fd325be722c9617f3ed0b06abf5985e9d7be13f8c142e3eb5a1bd5524e25911887e714705b82e6af5da1d48bc6fca3a90e63e89851eeec75503b5ee', '王腾飞', 'business', 3102, 1120, 254, true, true, '2026-07-13 06:44:01.442556', '2026-07-13 06:44:01.442561');
INSERT INTO public.users VALUES (19, 'RS5500', 'scrypt:32768:8:1$Y6eijmGi4tHIxK7W$2510688ac239f9fd424fdd5f36b4f0692544e9007110d1459e10d5939bd7aaf440d209fc730619924b1d952f18deb520476fa892fbf44f25105dacbc376e44b3', '严雅萍', 'business', 3110, 1072, 264, true, true, '2026-07-13 06:44:01.536749', '2026-07-13 06:44:01.536754');
INSERT INTO public.users VALUES (20, 'RS5518', 'scrypt:32768:8:1$Gcx5rjIQed7WGRBA$aa372d72e58d34861feceae04201d473ef09886c09fff7c54216890698c490b766f790b56e51c39067cd9eacff2c48291f749468d63fa71d8787f58eeb7271c1', '谢献民', 'business', 3129, 1076, 99, true, true, '2026-07-13 06:44:01.627073', '2026-07-13 06:44:01.627078');
INSERT INTO public.users VALUES (21, 'RS5786', 'scrypt:32768:8:1$CazzCLSHdae6dbx3$5521ab1fa9594346cad03f669c13c0e0e2cf80f957ff5609bbd3b53c2a401ab90fe1265447c13f25e6aa1d98100c8d9600f44200bf3c890c8aa5606bb5cce212', '王理想', 'business', 3393, 1141, 141, true, true, '2026-07-13 06:44:01.720359', '2026-07-13 06:44:01.720365');
INSERT INTO public.users VALUES (22, 'RS5880', 'scrypt:32768:8:1$3vdonCOSaC1Php0Q$71d4c9f7915e45da4043798491a83bed8ba9e3ccbcd838b659e98f0bb20e51a20614851767be21fd0136406d51b8b7094a1afce9c11b54be1de7140b88e5138b', '吴燕娟', 'business', 3489, 1110, 100, true, true, '2026-07-13 06:44:01.81409', '2026-07-13 06:44:01.814095');
INSERT INTO public.users VALUES (23, 'RS5944', 'scrypt:32768:8:1$U5x5f2p0izdBkmv0$33f408629a7da6fb588128e2bdf04a08f605ceb04b487eeea8b4d2251c1326745e4e3ce650371d6e90a929e00352d9ca2e2d480414b563af87a3e598ee3f1e36', '杜海峰', 'business', 3553, 1081, 254, true, true, '2026-07-13 06:44:01.909325', '2026-07-13 06:44:01.90933');
INSERT INTO public.users VALUES (24, 'RS6258', 'scrypt:32768:8:1$A2IB1M8hvp4fKabg$8b603d6ef91127d9e9038ce157ec5b808e840e0de2cdf3b75accd2178842ad457b8222c28facd8356fcf0b3ec779d03597a4e3639b9e5d624e4ff0da6dc227d3', '胡世杰', 'business', 4047, 1141, 92, true, true, '2026-07-13 06:44:02.001213', '2026-07-13 06:44:02.001217');
INSERT INTO public.users VALUES (25, 'RS7063', 'scrypt:32768:8:1$VsvSy0uyZ7VAEYZF$4c03d816aa79f7901527fd5d8634d3c47e64a6422ee38a92f486939dfe008e8b4d1656ace8fcff6331433d2b3d5292cc46c162a397364fba74e1871a428b2061', '陶硕', 'business', 4681, 1109, 254, true, true, '2026-07-13 06:44:02.094868', '2026-07-13 06:44:02.094875');
INSERT INTO public.users VALUES (26, 'RS7198', 'scrypt:32768:8:1$b5O5XWpCZFUxI0h0$76136ebcfd0ad79a4600fae3c79dc4858579beb6c7efa7221dc9274f69acd333702d4fc2a951c52c6cf9ea012165df18ecc4bffdefc3bc8c13bde5ec0ff929e7', '吴磊', 'business', 4788, 1141, 254, true, true, '2026-07-13 06:44:02.188848', '2026-07-13 06:44:02.188854');
INSERT INTO public.users VALUES (27, 'RS7219', 'scrypt:32768:8:1$NBx5N4QTGop8g3km$6cfae7b6a4732e04e68f97567bfce85552b5feba300adf822ac2d8ef16c09d71b87c98b44467f9683ab4b08b06cd722b9cf30208bd9578221c2176819219d18e', '宣亏堂', 'business', 4809, 1140, 254, true, true, '2026-07-13 06:44:02.28354', '2026-07-13 06:44:02.283545');
INSERT INTO public.users VALUES (28, 'RS7344', 'scrypt:32768:8:1$tVaIoQ05P0xSn6F8$b90b175c4d1c421cf966c2f77784c49462d86664b6c0bf93091069851e2a17ac9c6acf2e81b89b70cc6529584364124b04a44cae7e8f3de847af906c597b2f51', '储怀和', 'business', 4872, 1141, 141, true, true, '2026-07-13 06:44:02.37581', '2026-07-13 06:44:02.375815');
INSERT INTO public.users VALUES (29, 'RS7281', 'scrypt:32768:8:1$BR3CV5QILrk9Lwwf$27400ff9891d03746ec9b70bea0b39904a9873c3af55cd76cfa8c06ccbe9ad58b008b482838e95ba29e1d84d12780bad732336f7337de72550768ca24064e356', '王亚军', 'business', 4893, 1139, 263, true, true, '2026-07-13 06:44:02.466732', '2026-07-13 06:44:02.466737');
INSERT INTO public.users VALUES (30, 'RS7289', 'scrypt:32768:8:1$kxljHpLFQ5LT6rfy$6413839375ff6760a0e959e744191eb3c68b5dcdc3dd52536783128a4e9f4ef076af4d211b133b8611046469bc1aaf97f6d6e8e7c91f23f290a2ee2ad4e680f0', '赵鹏程', 'business', 4901, 1140, 254, true, true, '2026-07-13 06:44:02.562402', '2026-07-13 06:44:02.562406');
INSERT INTO public.users VALUES (31, 'RS7290', 'scrypt:32768:8:1$BMZsCxLL7KmL5LHo$74325a91c8e9d4ada8cbe40a05110457b07566fdd4d000f835f8f770d1a49f05f4344f0b5a1be811ce337e8342ced751b45004ef3a7c535dea902dbf351fe329', '王宁雷', 'business', 4902, 1140, 254, true, true, '2026-07-13 06:44:02.655735', '2026-07-13 06:44:02.65574');
INSERT INTO public.users VALUES (32, 'RS7596', 'scrypt:32768:8:1$72W8ap8HNQ8HEe0X$efcf53e675934201bcbb2eb2523b905a30e022d17ac48332c93830dfca9c826a4cdae7e6382e8d758f95bea164f9d2e84914fc40af393a79169206c755c6a679', '尹申云', 'business', 5261, 1119, 254, true, true, '2026-07-13 06:44:02.750727', '2026-07-13 06:44:02.750731');
INSERT INTO public.users VALUES (33, 'RS7603', 'scrypt:32768:8:1$UQ7Lk0ijDMKFRA6e$2da8e65ccc39fa080ca55cf0bf650c361bbd40e523361924e6c7c2fb842a61066e602f068d850699dbeee592e5a78e4188c180bc6cc2f47ba6b313a7f6299d2d', '孙雪锋', 'business', 5319, 1024, 148, true, true, '2026-07-13 06:44:02.844066', '2026-07-13 06:44:02.844071');
INSERT INTO public.users VALUES (34, 'RS7954', 'scrypt:32768:8:1$SKv0wUDi8KXtTRJk$0e020a07c2a5185378b2c2f198bd6af5d85b1773d74394ee7174c9d38505f77d4931b77a55ae3b6f9459edbd709bf43c655dbe7621102630ecf34b88a3dcf264', '张国生', 'business', 6223, 1122, 148, true, true, '2026-07-13 06:44:02.938245', '2026-07-13 06:44:02.93825');
INSERT INTO public.users VALUES (35, 'RS8046', 'scrypt:32768:8:1$cAFDI97dsnrHzmD5$de6df97f5f0c6397b11fb4cfae5797ceed78a833a2d77bb594cda362ac37f6662cb456bbaa3ff9697a1944fe35fa9e8937b5e1f3a71e191cdf94680e4091cc59', '倪青', 'business', 6758, 1120, 254, true, true, '2026-07-13 06:44:03.030884', '2026-07-13 06:44:03.030889');
INSERT INTO public.users VALUES (36, 'RS8066', 'scrypt:32768:8:1$8XxO1KzzqKEFvSj1$87b265a01db8b813dd229f69bc1591e1456bbb6b0700d4cca9a541529bff539240c7cbb8567fd1d1a6daa712d2fc5af3a6f29618dcec852beae9e08010933fe8', '王哲', 'business', 6797, 1120, 254, true, true, '2026-07-13 06:44:03.128227', '2026-07-13 06:44:03.128232');
INSERT INTO public.users VALUES (37, 'RS8079', 'scrypt:32768:8:1$UnO4ccfDKQP94Fu0$c42bbedadf97e597755367393f7037b60dbb2b16397af5f3ef6209f7829588eae997a8a286b7e6ff6cc6782457a6bb4a8f6a015c0ff791debb51a4f0b7bb5f44', '刘洪', 'business', 6812, 1076, 254, true, true, '2026-07-13 06:44:03.226826', '2026-07-13 06:44:03.226831');
INSERT INTO public.users VALUES (38, 'RS8139', 'scrypt:32768:8:1$myVRmHtTCFdVWlV3$10e14b2558ef4f684d66ecab90149ff26a59aa4d1719701c6f27da8ce2550fa071efa41a799de26a737e48d754da1237b5ad77d267cf9afe46ad4d12688af62a', '李超', 'business', 6970, 1084, 294, true, true, '2026-07-13 06:44:03.324498', '2026-07-13 06:44:03.324505');
INSERT INTO public.users VALUES (39, 'RS8169', 'scrypt:32768:8:1$JVtPrAL5nsrNw5mD$a4b7e175aea354da1443e3523bc8c83722e5fd4d56835c6d3e2fdb68ec58f14a1e82e129cd8f20117240a47b2b10623f1dad2641e34adf908e306bf98fb457b8', '赵萌', 'business', 6990, 1081, 254, true, true, '2026-07-13 06:44:03.420382', '2026-07-13 06:44:03.420387');
INSERT INTO public.users VALUES (40, 'RS8168', 'scrypt:32768:8:1$0j350nU6avresMz8$6da5cc4c2b28db83d86055d98c51243395c60679498a1f87a7b45a6d62b315bba8c2f28256b74a7ec54e635d63bb88d44a94b4ed2b9eb937f91f8394c32b17d6', '罗松', 'business', 6992, 1140, 254, true, true, '2026-07-13 06:44:03.517944', '2026-07-13 06:44:03.51795');
INSERT INTO public.users VALUES (41, 'RS8248', 'scrypt:32768:8:1$dVMOhfXXHLnabVLb$01a7d69f602ec08a9ef25edbd13f2d2baf5e2731596ba2c18793ac608fc572ab2bda86668ff3ead9cea7f29a1d9266ed65b4645dd2697d04c6f4958c260b746b', '王杰', 'business', 7355, 1108, 254, true, true, '2026-07-13 06:44:03.615067', '2026-07-13 06:44:03.615074');
INSERT INTO public.users VALUES (42, 'RS8251', 'scrypt:32768:8:1$ecLU0UfVokIH00a8$a72720b218a3b88de0dce4ba2007c8ab9573686536e5b70ce2743d3ac8890bf4b03255515c5e9bf93d8fd3ec9bad761c902726197c2af0d7c3ffa5cc94d0972d', '曾伟', 'business', 7357, 1122, 254, true, true, '2026-07-13 06:44:03.714625', '2026-07-13 06:44:03.714631');
INSERT INTO public.users VALUES (43, 'RS8284', 'scrypt:32768:8:1$ccEdWFTlK1BWLYGw$9ecd5246daffcc7f597b6673b8933e794668cc0f3c27fa69dfe6e6dc65f3765c3b2a614c3df1df204d24b061e72a7805515794debf9ece46e44842138e196936', '孔伟杰', 'business', 7415, 1076, 254, true, true, '2026-07-13 06:44:03.81286', '2026-07-13 06:44:03.812866');
INSERT INTO public.users VALUES (44, 'RS8437', 'scrypt:32768:8:1$LUXVGO0l96KTQDoF$a892fb8d1f74c1827cbda98e0f7716586d40482d90ec76153f1408f75e868db10095770b076bc995068c8dd708b46323649db1e8dfc9798b7d567f4b24e4952f', '杨延财', 'business', 7526, 1076, 254, true, true, '2026-07-13 06:44:03.91203', '2026-07-13 06:44:03.912035');
INSERT INTO public.users VALUES (45, 'RS8455', 'scrypt:32768:8:1$CJscHQ0SmXczdGgp$150ece4ea62112655f6db1fe92593113988317ae1c16a3984c0506b37573e43808158205a92c6c650a9868a456399801b33baa1ff519ad346ac058bc93e4b9c8', '王震', 'business', 7645, 1076, 254, true, true, '2026-07-13 06:44:04.009149', '2026-07-13 06:44:04.009154');
INSERT INTO public.users VALUES (46, 'RS8457', 'scrypt:32768:8:1$N0rBM8W6fsiMk1e7$a225839bee7282b88a4a07fcb61ee1829d0a18929f2b4c944c6d9b514cd3948e93970860ad6561ba4b21b20f8f8a8975c4ebebdf4fbbdd247820e96aa4b5777b', '种张鹏', 'business', 7658, 1138, 248, true, true, '2026-07-13 06:44:04.1063', '2026-07-13 06:44:04.106306');
INSERT INTO public.users VALUES (47, 'RS8461', 'scrypt:32768:8:1$aLflIi2sCq6tJsvn$5abec20f57db614992a27c1fa2c68a1f451f9f1bada8fe44ad3f5a710707c209f17f060d253be4b753a97cde4ccc041178dcf114de7c8ac45fbccc32440c7925', '李小博', 'business', 7662, 1116, 254, true, true, '2026-07-13 06:44:04.204573', '2026-07-13 06:44:04.204578');
INSERT INTO public.users VALUES (48, 'RS8467', 'scrypt:32768:8:1$jBAguXchyaWsmceF$ba1cfc314a96e57866bd39d5d980a3df6b3b6e104c897d314ea6e72983f71b778baaebf17f5041c6e7542220458016f74a3b9ef33bca82c969b738bf7f501be3', '周信霖', 'business', 7668, 1076, 254, true, true, '2026-07-13 06:44:04.303098', '2026-07-13 06:44:04.303103');
INSERT INTO public.users VALUES (49, 'RS8495', 'scrypt:32768:8:1$aBIPGfA1GQUSAI11$2e803cf4f0d508d38ef5e7b13801c0c7c47cc1bde660f7e358418b6f40997cca4beb98b8b306acffcb2150b7a206815f5e15e8b61a10a474f46b1917289c762f', '马晓雯', 'business', 7736, 1130, 260, true, true, '2026-07-13 06:44:04.400804', '2026-07-13 06:44:04.40081');
INSERT INTO public.users VALUES (50, 'RS8511', 'scrypt:32768:8:1$j78plZGoK1QTMzUg$bc174a83f2d5072233cc1aff904b41063f42a44e9b0f1d8413ea2a6fc9be7c12e50744d2da25d0afdf65ac33f3519c57b27de62ec9b8257c2c09b8e410aa6dc9', '王辉', 'business', 7756, 1122, 254, true, true, '2026-07-13 06:44:04.498912', '2026-07-13 06:44:04.498918');
INSERT INTO public.users VALUES (51, 'RS8568', 'scrypt:32768:8:1$SeSiEupcFzisGx9z$f849a73a448f2f60a0f652cf089d9084991c6a23e5eaf2c041751fe8c1b07b4c50455f966f8987562093f0d230c6b21ac69c0d354fb72687c65a2cffdd1c8d8c', '卞杰', 'business', 8099, 1120, 254, true, true, '2026-07-13 06:44:04.594173', '2026-07-13 06:44:04.594178');
INSERT INTO public.users VALUES (52, 'RS8605', 'scrypt:32768:8:1$Mi2qFBZ7HoCjtCx7$83b001ec80ae3e56caa2898118100ddc24e3aa43addab422b1660c5b2545e58522435171b1c4b4fb4866b0d620bb6ebd1a215f51dc7d1e0ce53722ff632bd2ee', '蒋雄', 'business', 8148, 1120, 254, true, true, '2026-07-13 06:44:04.690715', '2026-07-13 06:44:04.69072');
INSERT INTO public.users VALUES (53, 'RS8639', 'scrypt:32768:8:1$eDlivkt2LPxK2NmS$530ea9665a8eec1dbde05ae4c1b69d9e2669291c9f076ba270ff34a863fb8d7bfcc874f9408fe82bb75407d454042fe2ceb29f201ed8d2b9738514a423c140af', '李林旭', 'business', 8215, 1120, 254, true, true, '2026-07-13 06:44:04.787094', '2026-07-13 06:44:04.787099');
INSERT INTO public.users VALUES (54, 'RS8679', 'scrypt:32768:8:1$iuBGsCUHGbqvKLZ7$1e2a740bcf883f81b45316305fc44513e3979cf09242461c9180cbc7c83de6bbd61f66391c04d7405db19ed92ecbe0bc5fe74c371749660a4c5df38b5ffb4259', '马振峰', 'business', 8287, 1116, 254, true, true, '2026-07-13 06:44:04.883236', '2026-07-13 06:44:04.883242');
INSERT INTO public.users VALUES (55, 'RS8759', 'scrypt:32768:8:1$EeejliXTe3TYnmtu$79498fc62d72c1b2cfeab96fee15592657ce4cbfdcfe2a5ff8c1903a3e8e441db0596f3997aea7913a3d126cb288ee2478e8755992af28e2d5e3d5642e37b785', '吴东林', 'business', 8391, 1116, 254, true, true, '2026-07-13 06:44:04.982256', '2026-07-13 06:44:04.982262');
INSERT INTO public.users VALUES (56, 'RS8791', 'scrypt:32768:8:1$Wb4IopCEZQV8VcJJ$c7ade4e1a411fc11af1ceb22d7e68a305a5b59bcee831f7c1424c45a451bf9f98bd6429ff3fe6f2f4069b669ad6cbbd73ef5abf5d39ff47eff5fa785a665b66a', '栗晓国', 'business', 8446, 1139, 263, true, true, '2026-07-13 06:44:05.080721', '2026-07-13 06:44:05.080726');
INSERT INTO public.users VALUES (57, 'JS90038', 'scrypt:32768:8:1$OqLQm1f1uOI4Ub1B$19cba3c35e700a31300bb7b1e6efe391ee6cdc5dd1bcb59e67d03e1a521ac3d05ec5aa00e955182229e5b99df8922609c1476cf72bf3e46918a9ecb0fd35814a', '徐志', 'business', 8471, 1058, 254, true, true, '2026-07-13 06:44:05.179515', '2026-07-13 06:44:05.17952');
INSERT INTO public.users VALUES (58, 'JS90049', 'scrypt:32768:8:1$Rz9qOIynreVEZQYr$9a1e7d8e3c02d4ffa5963e95d3e41c4b5c18acbf73bfcdea6dd28b2c85e19a257c062b76d9b2c7153c24bd31cf218977961ffeac515b4939afa06aca6ca20fc9', '杨胜', 'business', 8482, 1100, 254, true, true, '2026-07-13 06:44:05.27786', '2026-07-13 06:44:05.277865');
INSERT INTO public.users VALUES (59, 'JS90060', 'scrypt:32768:8:1$pIaRtnosWAwJwGCG$ba19e4d8c053b2ecf4e74e60cf365fb9f5378866e153c92dfdfc0fa958b41a03542339f41cab802f71cb9524d59756101c3d0c412cdc0c44048496b963b6800b', '贺国志', 'business', 8493, 1055, 254, true, true, '2026-07-13 06:44:05.37944', '2026-07-13 06:44:05.379445');
INSERT INTO public.users VALUES (60, 'JS90062', 'scrypt:32768:8:1$Sei6UaSvV3SW5Zmi$089b9c695cacc49ab5f4592783d1d6936bfe79a1e8437f55057f364d0afc69990aa5623f24450b209685809fe8b12e569d40b558082bd90e5402425cb67a343f', '刘海学', 'business', 8495, 1100, 254, true, true, '2026-07-13 06:44:05.47745', '2026-07-13 06:44:05.477456');
INSERT INTO public.users VALUES (61, 'JS90063', 'scrypt:32768:8:1$l11xlZrNNsBqJhlR$0849a18b4503c04af8775c1a42bc4a3d4ee12da94c308333538f6abe722c3b2d0f155829e6f452dd2ced2517293adf24587ad5c201472fb2fa8b93f845313b85', '吕宁', 'business', 8496, 1103, 254, true, true, '2026-07-13 06:44:05.574339', '2026-07-13 06:44:05.574344');
INSERT INTO public.users VALUES (62, 'JS90065', 'scrypt:32768:8:1$lCGc9NrdsVcDxLwB$73ac3f1fa5b0f9428d0172cca809f6122646f2ae5488e6a695634e1c763a85669543a91d162356a7ba696b1a73e904cab8078e6d46bdb857ac7f40ad039391ea', '王飞', 'business', 8498, 1103, 254, true, true, '2026-07-13 06:44:05.670094', '2026-07-13 06:44:05.6701');
INSERT INTO public.users VALUES (63, 'RS8797', 'scrypt:32768:8:1$XeGldC7q9MC1rAT9$dfae2d275b6743a416d329bd168376645570c7f7545d2fd0b913a24aab11be658c624507791d75483005fbdd46877518d3cf9cdc1aedb53f366e86b1d80f89fd', '梁纪东', 'business', 8503, 1140, 254, true, true, '2026-07-13 06:44:05.765994', '2026-07-13 06:44:05.765999');
INSERT INTO public.users VALUES (64, 'RS8798', 'scrypt:32768:8:1$uYQVisCJFZeLWoiR$8747e8208fef48296dde5fdba9b99c9115892823b5e4fc850dcb37ce858e29bde89331c316acec6e001f69a9bcd6da7ec02bb023abe5e2f8d545547c7ea7d5df', '王忠印', 'business', 8508, 1120, 254, true, true, '2026-07-13 06:44:05.859357', '2026-07-13 06:44:05.859362');
INSERT INTO public.users VALUES (65, 'JS90071', 'scrypt:32768:8:1$OH2LtfaaEtbrLYZe$c4c072ca5e84802ba4f78c8f8f3a2f92c777d086ebe3d7d7f8081dd60b856c585ff5963650059d3a59ba5c10aaa35fe22270e89bc85ee9cf159f73c5a18cd106', '李荣壮', 'business', 8522, 1100, 254, true, true, '2026-07-13 06:44:05.954662', '2026-07-13 06:44:05.954667');
INSERT INTO public.users VALUES (66, 'RS8816', 'scrypt:32768:8:1$GEOtIZoVmHj6aCZH$c0d23bc14ab66adc649d1d5fe95fb3070c27fd28cd75bf01d00dd0243094baa7f5f71d468fba3128432b6cd4df02549dfe117af360ecebc5483c743d094c0679', '余强智', 'business', 8535, 1139, 263, true, true, '2026-07-13 06:44:06.045573', '2026-07-13 06:44:06.045578');
INSERT INTO public.users VALUES (67, 'JS90080', 'scrypt:32768:8:1$lHOWvDyE5vNlXYt0$3b8b225735508af26dd8be524765f5f39251299efff54d03a3be5fbfa4e519adf66717ede721960f1023e5f2d65cd50b778a0a840cf559070e31ade9ad10781d', '寇耘诚', 'business', 8549, 1147, 248, true, true, '2026-07-13 06:44:06.141892', '2026-07-13 06:44:06.141898');
INSERT INTO public.users VALUES (68, 'JS90081', 'scrypt:32768:8:1$JlTFqcvwxyvrGnIq$eed211f0a43dc86898b3d8d2ff0afc9bf4bf59219aed338b8e64ad9e7d25b34834eafd8f6e5308cc6cfac3b553773c08d7ab2ed2f7fc0f2fce10016218590287', '常贵凯', 'business', 8550, 1167, 263, true, true, '2026-07-13 06:44:06.236616', '2026-07-13 06:44:06.236621');
INSERT INTO public.users VALUES (69, 'JS90082', 'scrypt:32768:8:1$MP82fBzEZRhx8St6$334a6aa91f94fecc5fc1dc8dbe76795dc7cd65b15ecdae2b6ab1a34cb6f2e328ee977e35df68bec6325069b4abd1580fb2e83ff4376ee1fedb9f89ed88bfc2c2', '李南', 'business', 8551, 1058, 254, true, true, '2026-07-13 06:44:06.330841', '2026-07-13 06:44:06.330846');
INSERT INTO public.users VALUES (70, 'JS90090', 'scrypt:32768:8:1$cCNN8lgsSV0mEZh9$b13666dd44308e55b68857bc820d2b5613040cb9b9db4a4f8b1d43309848081874e2ba7ebd1ba0acf6e97a82f6d9cbd10577997b88afb3eaebe9ee96c5e59a80', '刘帅', 'business', 8576, 1058, 254, true, true, '2026-07-13 06:44:06.421219', '2026-07-13 06:44:06.421223');
INSERT INTO public.users VALUES (71, 'RS8834', 'scrypt:32768:8:1$OeMKLr3fc8C3ySGk$e6db598dff73316808dd59b4f220053abb3d3cb362ca0c3e070ed9163af0e3ca4321b1ba99d476dcfbdada5f4958d3831f332b73920681d4d2872b419a52717f', '苏润戈', 'business', 8618, 1138, 263, true, true, '2026-07-13 06:44:06.515189', '2026-07-13 06:44:06.515194');
INSERT INTO public.users VALUES (72, 'RS8835', 'scrypt:32768:8:1$SXZ57J790dMuvrSy$0bd13d840e12e8218f8044a9b910872434d4c515139a59790aef81fcabc73a9c7082835d89271e485dd9c9138585c9db1668362213e13599abacb1c6171bcdc3', '鄢园红', 'business', 8619, 1138, 263, true, true, '2026-07-13 06:44:06.610358', '2026-07-13 06:44:06.610363');
INSERT INTO public.users VALUES (73, 'RS8837', 'scrypt:32768:8:1$ZoYnL4xY3tp7mptz$3c8837b7684d99ec33e6cb8323a8cf407d47f114dff36e6392b43f58df73baa1195e1088ef0e98dde7768c23c68008986cbf1a23f75137a4013e28408329f668', '夏永立', 'business', 8621, 1076, 254, true, true, '2026-07-13 06:44:06.704641', '2026-07-13 06:44:06.704646');
INSERT INTO public.users VALUES (74, 'JS90094', 'scrypt:32768:8:1$RI2u4DJ3rnh2lZiZ$9d97714322068ec7d7ea1bdcd45abe7610ada7e6285f0c2548a9bbe69cd3930b6b7037e10f9cfbe38a5f3bdaa6de93ac14281f65baec1bd86a84eb1cc2bfa295', '刘江涛', 'business', 8625, 1100, 254, true, true, '2026-07-13 06:44:06.797297', '2026-07-13 06:44:06.797301');
INSERT INTO public.users VALUES (75, 'JS90096', 'scrypt:32768:8:1$J1uCzKmLwttsUz4b$826786692f584ae9aa80a5e44999b56a6a0bfc8f122db2bee983cea99a9d6e0e44e33e209319ddac787d02a6bd2a7380f57e2e0306c473c768ce4f9957b7d905', '张财', 'business', 8637, 1160, 254, true, true, '2026-07-13 06:44:06.892212', '2026-07-13 06:44:06.892217');
INSERT INTO public.users VALUES (76, 'JS90098', 'scrypt:32768:8:1$J8lMcPYc7BCNtvs2$d075f18656f316e48482fe190184801014a0bce665faffb9264ddd32534805e1508733c7f61830994b5e1974aef5692890052e4ca6c4beba02578ac0557b39ad', '崔伟伟', 'business', 8640, 1100, 254, true, true, '2026-07-13 06:44:06.984864', '2026-07-13 06:44:06.98487');
INSERT INTO public.users VALUES (77, 'RS8855', 'scrypt:32768:8:1$ylOaVduXNphsiUE9$e4b28dde9b8ea0075abf013d0f6cf8320d88ed4ccafe727d7292547779ff076af8f0f46fe6c691bc955a1e582d2869661cce5658a66504e9741812463a09a0bf', '项圆龙', 'business', 8658, 1122, 254, true, true, '2026-07-13 06:44:07.075844', '2026-07-13 06:44:07.075849');
INSERT INTO public.users VALUES (78, 'RS8865', 'scrypt:32768:8:1$IP0HVKua9g8lmolG$cd521e3f4c8e52e459cd3718b14d33b499f0d767552b502e890aa951e9696ac95cc2ea067fb59de35716cc89a2b0963dd12a2454aff08539d4e9c732c01701f2', '吴昊男', 'business', 8711, 1115, 86, true, true, '2026-07-13 06:44:07.170178', '2026-07-13 06:44:07.170184');
INSERT INTO public.users VALUES (79, 'RS8866', 'scrypt:32768:8:1$bsSKCMhl0gL29l6K$135422ae524144d858832cc27ea24f266be0aa9db6315ccf1a9f1279bbc0fa581b30b353565d8867978c96f60d11f10bde35b09247c583770a3554725b44c85c', '谭勇', 'business', 8712, 1115, 86, true, true, '2026-07-13 06:44:07.262969', '2026-07-13 06:44:07.262974');
INSERT INTO public.users VALUES (80, 'RS8873', 'scrypt:32768:8:1$Z9FZHuArmDf1C846$1b015c0defd1b52561210682d614bc4c18296aa51c5c08df6422e6fba72b5c6ae47ffda493fb87ab41bffdd5505e8f4f5e5daa032f3c2b255654b2988e5b74f8', '孙世梅', 'business', 8772, 1115, 86, true, true, '2026-07-13 06:44:07.356817', '2026-07-13 06:44:07.356822');
INSERT INTO public.users VALUES (81, 'RS8870', 'scrypt:32768:8:1$eR91lvjm0tXE0qhA$f5a962d14dea1bfcb38e6d08bae3c2c45ebf98a9bfe631daa639041700f141774eec288649434e84b3d19b0afbf280c365e88c4533f2b0e33e4d0be932805704', '马振杨', 'business', 8777, 1122, 254, true, true, '2026-07-13 06:44:07.447802', '2026-07-13 06:44:07.447807');
INSERT INTO public.users VALUES (82, 'RS8875', 'scrypt:32768:8:1$fauoU6t7uf5S2kZQ$fb3beed9b3dc058b3b9754a387d7f4054dff026e569ff56a26ad8f98764e4ae4fa101e9c6f6f7e2a166cbb39f8b5c5664a44fbeaa0430e719720c86b36ea630e', '史永龙', 'business', 8780, 1138, 263, true, true, '2026-07-13 06:44:07.540158', '2026-07-13 06:44:07.540163');
INSERT INTO public.users VALUES (83, 'RS8900', 'scrypt:32768:8:1$KcvmUyZmDqcctjjP$a056bebea4ba72babc21e6e428edaac2b5ec24683345bc474e17cd6779a9ef4ef13da90e9f8282a141945d7e2061ddc8db6f8b0e2ba5f0458f9fd9286dff74c8', '杜旭升', 'business', 8830, 1076, 254, true, true, '2026-07-13 06:44:07.631567', '2026-07-13 06:44:07.631571');
INSERT INTO public.users VALUES (84, 'RS8915', 'scrypt:32768:8:1$JeIBrPmQ9FYNXbRt$c85a0e48116954f1a5e7ac3c07ab3ce479a6fe2983b83fc787c21e3e03564ace44bfc2ebfa1727c073d2fdb0e2586c5da629be6e6aaf16882453c1395234de43', '杨姬召', 'business', 8856, 1115, 86, true, true, '2026-07-13 06:44:07.724179', '2026-07-13 06:44:07.724184');
INSERT INTO public.users VALUES (85, 'JS90154', 'scrypt:32768:8:1$PuskgvqdPdplVg2U$a379d0c36f72a68c022496cda5807de3a62b147026bd0a37239ed256af86c0ed5436f795171ae05911d5f3c57f426070e03474c412b2be96b06801b0ae6dc8b0', '张育通', 'business', 8897, 1103, 254, true, true, '2026-07-13 06:44:07.816176', '2026-07-13 06:44:07.816181');
INSERT INTO public.users VALUES (86, 'JS90165', 'scrypt:32768:8:1$nYpSPafqZ2owngMd$dce94095ab696ee7688fc10aed2e55e7d0a85a8452eb1ad431b56b129aa33dfcdef892f792f0e65949b794767b93eb7ce2eb86e943815230f381785d7e4259ca', '张合功', 'business', 8917, 1055, 254, true, true, '2026-07-13 06:44:07.911685', '2026-07-13 06:44:07.91169');
INSERT INTO public.users VALUES (87, 'JS90172', 'scrypt:32768:8:1$c7MfpS2mbLkp1lOf$e21bd707e7904e509d21197fdc28d1b5f88680106f451a4a90eed3bcc52db71e85056e9f5387a550c67488e7b98d895c889432acc831721bacc30517d69402d3', '王东', 'business', 8921, 1161, 122, true, true, '2026-07-13 06:44:08.004814', '2026-07-13 06:44:08.004818');
INSERT INTO public.users VALUES (88, 'JS90176', 'scrypt:32768:8:1$jzFTTS4SD25XsQTl$9a7d401f4f277557dd8b6137f7ed9c24a31abd1e3a8eb6362f6e43d24f11769de562c1874a45807bd595c1b1348288440a90c6e2b3c67718a2d4a55a5dfcc43a', '王辰', 'business', 8930, 1142, 264, true, true, '2026-07-13 06:44:08.097498', '2026-07-13 06:44:08.097503');
INSERT INTO public.users VALUES (89, 'RS8956', 'scrypt:32768:8:1$fvNUGCeHgqgYuw8c$476a53977196694d8f926ee359f66f16be64407138e4540252919b8430ab784a517bfc16e60efac63dc0b682beedeb2d97cd865bbf197afbf6aa5bd41870b457', '沈波', 'business', 8957, 1110, 265, true, true, '2026-07-13 06:44:08.189463', '2026-07-13 06:44:08.189469');
INSERT INTO public.users VALUES (90, 'JS90186', 'scrypt:32768:8:1$lY8rC8RNHimxD62P$a7e04a48828ed3685ed54387e4ccdc1b3006188e5d9c954953eccb565f2fc92b53e207f41410de8cc51715a7c3690dd0082080a2eec5d6549978feaa3b923ee0', '庞闻', 'business', 8962, 1114, 85, true, true, '2026-07-13 06:44:08.279564', '2026-07-13 06:44:08.27957');
INSERT INTO public.users VALUES (91, 'RS8962', 'scrypt:32768:8:1$nVFmSj0ehxE97Fdr$f1769ff13d4bb8b780fa120533c0f2ff82a9a27c5fc8461a4c61dffcedf382dc7149ff99d299d034bc7c23d00064af8d24511c256f77e1575333addfdecbdb5b', '杜海亮', 'business', 8968, 1115, 86, true, true, '2026-07-13 06:44:08.37198', '2026-07-13 06:44:08.371984');
INSERT INTO public.users VALUES (92, 'RS8964', 'scrypt:32768:8:1$7b9L4bTieZdpizgC$57f490c4320e48fa33e0267cf6aac864f8499327dc9d8b020c886242c2df3c4675d5b73f27d1160e2986794bacf98d211515f7996605935fb3f6985b667dda59', '张林', 'business', 8970, 1076, 254, true, true, '2026-07-13 06:44:08.46286', '2026-07-13 06:44:08.462865');
INSERT INTO public.users VALUES (93, 'RS8971', 'scrypt:32768:8:1$URQeG2CKke86be8D$ae147ec1e358b7b4a742ba65e1348e0721fb737848d474814f5662cb6b8881e1b31a785f91a89e4fe831f6f39805567ead99ffaac783f91a712bb8564c8d08f0', '严镇', 'business', 8978, 1076, 254, true, true, '2026-07-13 06:44:08.560123', '2026-07-13 06:44:08.560141');
INSERT INTO public.users VALUES (94, 'JX60003', 'scrypt:32768:8:1$xFnXDgnsmPtq0qDM$8d52db84e746e445758a2c9b2248419ccc45613454d5a1782ff38dc280c7c963e27707ba3bc8a7b59993af966bc8b9b42fc2cbf95a55dc6ec6e1c1e9091b41d6', '王嘉仪', 'business', 9047, 1104, 299, true, true, '2026-07-13 06:44:08.65917', '2026-07-13 06:44:08.659177');
INSERT INTO public.users VALUES (95, 'JX60004', 'scrypt:32768:8:1$YhJqZamkxYnApO33$d79dfa315a807b9fc875653e83bee1cd18e863169878acad34a4f990e7c6e4d263b90963d29689118699467a26c293d3d497e7662c296156d549bbd0eb5a593f', '王强', 'business', 9048, 1149, 299, true, true, '2026-07-13 06:44:08.756406', '2026-07-13 06:44:08.756412');
INSERT INTO public.users VALUES (96, 'JX60008', 'scrypt:32768:8:1$TlDy71XsGo4Xp15w$452c00072a5a619b041e6857b71309e3e0575b785800d725f0863f6e2cc215e7265bf538087d13326069e35847163ab54a5e96d230bea8f76b524523f7e59a4a', '郭洪华', 'business', 9050, 1164, 277, true, true, '2026-07-13 06:44:08.85204', '2026-07-13 06:44:08.852045');
INSERT INTO public.users VALUES (97, 'JX60009', 'scrypt:32768:8:1$FqsBc2UiXC2xaQ5M$e20a6a05662276fadefff89e8cc7f69809b114661d3a1b7377f790216c2dce3719ab1f09c593401d169d4422f86b2e9bcb05c01432838492655380bab78ab254', '侯元峰', 'business', 9051, 1096, 277, true, true, '2026-07-13 06:44:08.950143', '2026-07-13 06:44:08.950148');
INSERT INTO public.users VALUES (98, 'JX60012', 'scrypt:32768:8:1$6Uv2IGiZuzbQQdr0$6810044ec6d51ee432ee5d5545af8b6d85649a08214cdb913aecd334d5ce24f1f51bb3d43ec245f5b63d01af9cc18c3e09d3c6f18ebbe24c94bf8ebae0bf5971', '孙裕佳', 'business', 9053, 1096, 301, true, true, '2026-07-13 06:44:09.047004', '2026-07-13 06:44:09.04701');
INSERT INTO public.users VALUES (99, 'JX60021', 'scrypt:32768:8:1$7ZzrInzzpZBQgtpN$a8fc6f9c0caf8a7360c47f1ce75cf91d47664296d49cd361ede5bac2340b7b47c98553f346b3ac28633656a18f82cc7b2a62df88a90e015bd7beca1dd485dbee', '张亚忠', 'business', 9057, 1098, 300, true, true, '2026-07-13 06:44:09.146118', '2026-07-13 06:44:09.146124');
INSERT INTO public.users VALUES (100, 'JX60025', 'scrypt:32768:8:1$nKwiJqaK5zYsQtw6$31d39feb77f0ec57a05d31df6e8cf4a9c68a9abfceafb85f0d34401ecbb1eac2198c780e1e7c7761c2271a049620f9c09e997c2d425caa71421430c7517d7d6b', '张夏青', 'business', 9058, 1104, 301, true, true, '2026-07-13 06:44:09.243924', '2026-07-13 06:44:09.243929');
INSERT INTO public.users VALUES (101, 'JX60026', 'scrypt:32768:8:1$HiZHlSvLh2yssUGG$ed8ac9fec076a0bfe5a1862a547fc5188a61b9aadb32bdce6cbd2dbb33352981eada5d60fcdc48932cb0bfba9cf09565ab90073841484a51def617f9d5090143', '钱雪峰', 'business', 9059, 1094, 300, true, true, '2026-07-13 06:44:09.343256', '2026-07-13 06:44:09.343262');
INSERT INTO public.users VALUES (102, 'JX60027', 'scrypt:32768:8:1$gCglfO0boZnO3XiP$732aa5aeeb5af1e47719b034e8c5f0b24baba0d9503e840a42cd1fbdaa517c1f258e8b93dfba2e1bbecd87c8be1f3595d6816bb9eba2b632c04cc02135455c4a', '邵冬生', 'business', 9060, 1171, 301, true, true, '2026-07-13 06:44:09.440263', '2026-07-13 06:44:09.440268');
INSERT INTO public.users VALUES (103, 'JX60031', 'scrypt:32768:8:1$ZMej9osEUYOgDaTa$993879fcdcc471da8006041c0eea00eb89b409559e2b248bdd4bcaccdd18eb0263d1be52b64802c212e72522ea4db5e8e34271136a841ca91b079c7e22965567', '梁志颖', 'business', 9061, 1096, 302, true, true, '2026-07-13 06:44:09.539452', '2026-07-13 06:44:09.539458');
INSERT INTO public.users VALUES (104, 'JX60037', 'scrypt:32768:8:1$g8DH5GVA358UyGqX$0501e1f5806d9a8fc7598e6ef28f4d7a3e90713245b3fa5f51522caff3b4eb966aa3cb23956e223eef0653862efadec26a4a1bf9bbc5be7c17ba314052674cfd', '唐兴东', 'business', 9064, 1096, 301, true, true, '2026-07-13 06:44:09.637427', '2026-07-13 06:44:09.637433');
INSERT INTO public.users VALUES (105, 'JX60038', 'scrypt:32768:8:1$wly7HEIIcWxaAOeP$168d588eaab8779ae06a13ecb887bc6d83586fbf1ae091cc5fdadbd50ba150213526906640203b9c078e2d3c1ade1f6e1da9efca76c04441039620b7aab93033', '朱利军', 'business', 9065, 1171, 302, true, true, '2026-07-13 06:44:09.734339', '2026-07-13 06:44:09.734345');
INSERT INTO public.users VALUES (106, 'JX60048', 'scrypt:32768:8:1$PI4rWqFToofdi8Go$dd9f0693da58470575ee23de9fc3bf746f78bd2f9c8f312dbcebe4befacafe8e82506027ff3234331316c5c08815039402f8553e924f63aa4b6a8fda6043db63', '张小荣', 'business', 9066, 1094, 300, true, true, '2026-07-13 06:44:09.825962', '2026-07-13 06:44:09.825967');
INSERT INTO public.users VALUES (107, 'JX60049', 'scrypt:32768:8:1$gezYOvjQAm36brEl$a3a87708b2a9043045521b1c013706745e514b59bbc8535e6b4b7c8f8fa900f7921e6bba0050548f8c5bca95c9974b4f5f9eb1af88b9541b61924fd337a55eae', '徐佳明', 'business', 9067, 1098, 302, true, true, '2026-07-13 06:44:09.919056', '2026-07-13 06:44:09.919061');
INSERT INTO public.users VALUES (108, 'JX60054', 'scrypt:32768:8:1$e2czkzXEXOvILLpH$b09258562ffac109602e0e2702abd5e0f7f60edf0dcbf45fe2e1cac2c50970afc4c274765917f175c3942eb0eedebe405bdb8edb8f12127b1d3e0d96c43ad5ba', '李丹', 'business', 9068, 1098, 302, true, true, '2026-07-13 06:44:10.011375', '2026-07-13 06:44:10.01138');
INSERT INTO public.users VALUES (109, 'JX60055', 'scrypt:32768:8:1$VpsDxRrO7ktbyOrf$4f7ddd08dd1c19aac25fa443aea955b1ecea6c0f9d3d8df03140e04ba405fbec5be65eb5775b0cef7119d31edb50d74e24949f2136530b0edc657a1c0e64bbdb', '叶映秋', 'business', 9069, 1124, 312, true, true, '2026-07-13 06:44:10.103806', '2026-07-13 06:44:10.103811');
INSERT INTO public.users VALUES (110, 'JX60057', 'scrypt:32768:8:1$231jqXTHRYBLTB6X$b75ca397b951d3136b2d02f6689d5f157d51c49a1906576d8760071ca5600c6132a0180d2e9ce2e24b9c306244633a5707c4091c39d49c62690c4efe3cc40f82', '陈梦星', 'business', 9071, 1095, 302, true, true, '2026-07-13 06:44:10.194004', '2026-07-13 06:44:10.194008');
INSERT INTO public.users VALUES (111, 'JX60058', 'scrypt:32768:8:1$dVFEhxwuhLrDthiy$089ba40a6d3b355f377cadcf0fe4fe43834e56436f48042ca72b9409c75a754ba376a09d7e0bb7a594b894f393fe5b6d90598e0eec576eb176c5f7c92b24db52', '季灿冬', 'business', 9072, 1104, 254, true, true, '2026-07-13 06:44:10.284286', '2026-07-13 06:44:10.284291');
INSERT INTO public.users VALUES (112, 'JX60059', 'scrypt:32768:8:1$M9y5FgHxfeTovlsn$47761e752f8463cd0aa36584d77d263d955924ca4a4d262d5a82a36689841fa301d2e039053d8083c15096935619532279940cdbb39a63186e90a92488e54cf9', '曹萌德', 'business', 9073, 1104, 254, true, true, '2026-07-13 06:44:10.374997', '2026-07-13 06:44:10.375002');
INSERT INTO public.users VALUES (113, 'JX60060', 'scrypt:32768:8:1$oRuemkYHiKsZHL7P$67433d7050f10bfe2277ebabd66ea16e0e160a053a25319d8ea134f7236633fc19a81f20a0631fc33d34d9295cdd0eab944a9cb8e9e01a423a35a587d8821fea', '章红', 'business', 9074, 1063, 259, true, true, '2026-07-13 06:44:10.464627', '2026-07-13 06:44:10.464632');
INSERT INTO public.users VALUES (114, 'JX60061', 'scrypt:32768:8:1$aHNpejyetIRsH0Pa$3b74eaa4a80010a2f132e81be45810351ad4347802316140d4a149385a4b4af89e8fa55f7d154d3515bba7efc61b030130f178c9e545f79cc475a8a5f236a0d2', '张红连', 'business', 9075, 1096, 250, true, true, '2026-07-13 06:44:10.556462', '2026-07-13 06:44:10.556467');
INSERT INTO public.users VALUES (115, 'JX60062', 'scrypt:32768:8:1$W3rQ95FN6rn7GKyG$d6be5ebe5d4f1a5e80bb4c1ce93ded19bfab62aeff9e7624908b3c33dca1157c67174a7f615c2b0d4107a26e8ac5ee59a10e9ec78e1163652a841182698ad7b5', '宋景贤', 'business', 9076, 1104, 254, true, true, '2026-07-13 06:44:10.646177', '2026-07-13 06:44:10.646181');
INSERT INTO public.users VALUES (116, 'JX60063', 'scrypt:32768:8:1$IjhqDSCDoQHaFIIL$741310c0a74da886a28b79faa478936c990f1b68ad6742612cbc09fda2fe4b39412dc294d1988504b8bf4ecfc2eddc9d584ee99c2c6e23eaff704e2f9ff3a198', '王善勇', 'business', 9077, 1096, 306, true, true, '2026-07-13 06:44:10.738334', '2026-07-13 06:44:10.738339');
INSERT INTO public.users VALUES (117, 'JX60064', 'scrypt:32768:8:1$4FgJzW4d7VwiYzpa$0a0a7c0ca9482761b0a687b537e5e9681cb36d868ad7e2321f1e096b441c551b5ad02919cf1ffe50835468dd6f0a716986d5ccdc60d78a993f78897f2cfddf7c', '孙成可', 'business', 9078, 1096, 306, true, true, '2026-07-13 06:44:10.828305', '2026-07-13 06:44:10.828309');
INSERT INTO public.users VALUES (118, 'JX60065', 'scrypt:32768:8:1$ANQulj2LwoIccGPG$ccb1ff1651e05d2b2d511e89873c8b9afbf986b9eb8d61913cf66e09c58c4e52dd177f4a9cd724c1206fd2e7f038eefb07a09e283eb47432c9e443f4824e4de1', '雷升', 'business', 9079, 1096, 306, true, true, '2026-07-13 06:44:10.922697', '2026-07-13 06:44:10.922702');
INSERT INTO public.users VALUES (119, 'JX60066', 'scrypt:32768:8:1$5Oe16qeUioA8ThYS$ff66ee0a5eebaf54eb28f78e1dd40852469834104bb2a3a9fa357c9e2bfba0fac94358a2bad514f5cf980d0aa861edd0eb5f4e9b512343c806b216877fcdee12', '刘占琦', 'business', 9080, 1095, 305, true, true, '2026-07-13 06:44:11.013575', '2026-07-13 06:44:11.01358');
INSERT INTO public.users VALUES (120, 'JX60068', 'scrypt:32768:8:1$n9kVDkd1UVBHCwhM$39c1449390eb65fe29a96fb3bcf3ee6883d5e5b40ce1dcc4fc772b71a89eaaf3b902eec3bf329457b702661e65e45bc601fde50caee0e6f806a7ddeb9f347210', '王兵', 'business', 9082, 1095, 305, true, true, '2026-07-13 06:44:11.105237', '2026-07-13 06:44:11.105242');
INSERT INTO public.users VALUES (121, 'JX60071', 'scrypt:32768:8:1$gmYKqIMsDucGrxLi$0076522836c2a580e31d54602a5eedfd98af40ea803759facd2977236e16ae9312839b43137032bbc9306cc24aebd0f839916ea42396847e398e351d848d787b', '邵磊', 'business', 9084, 1098, 307, true, true, '2026-07-13 06:44:11.195326', '2026-07-13 06:44:11.195332');
INSERT INTO public.users VALUES (122, 'JX60075', 'scrypt:32768:8:1$QOdaJQJwS7oR5kED$b066373fa52b3812f47d8aee24b3ec4b4ccff8dcfa30ef755fcba01132c9e6178a2199f7b1d4cbf2542fb85826824eb435e6b85c741d8418f6683b543ac13b86', '王根强', 'business', 9086, 1098, 307, true, true, '2026-07-13 06:44:11.286211', '2026-07-13 06:44:11.286216');
INSERT INTO public.users VALUES (123, 'JX60077', 'scrypt:32768:8:1$0puXWmal8AJAsFLi$06670c9c3e63004c1f06e04088106c33751b6949fb77061225c1c6587015beef323ef2ce40cbb8670a7463365788fc171412109fdb85cfb127e39ba1146114f1', '杨深', 'business', 9088, 1094, 305, true, true, '2026-07-13 06:44:11.376829', '2026-07-13 06:44:11.376834');
INSERT INTO public.users VALUES (124, 'JX60078', 'scrypt:32768:8:1$v9fC517VkOi5q3sS$906651f1060b30ea9b067941e25e2de09f641bf6fd62f15ff384b07b1e8156f49fa4052d7119fa4719929612038e0bb14da5a8464a2008eb01657cc0e6abde2b', '姚舟', 'business', 9089, 1150, 124, true, true, '2026-07-13 06:44:11.466758', '2026-07-13 06:44:11.466762');
INSERT INTO public.users VALUES (125, 'JX60080', 'scrypt:32768:8:1$K8sY1XHnCX9hsDjw$4d36480d8c03cc8ebb633f3e706ff3d4ba19631ae96ea80a226efc12f58711ec1c30b1506954bc32fff449e72ff959f96ca2dffe7d68d3c41799a90fed0ebfbe', '杨志鹏', 'business', 9091, 1095, 305, true, true, '2026-07-13 06:44:11.55889', '2026-07-13 06:44:11.558894');
INSERT INTO public.users VALUES (126, 'JX60081', 'scrypt:32768:8:1$saJpWGVxd0Q3nStA$541bbd4ab2ec1d0f7b3fd002057498c40239b86caecde27274bdb6a3b494c018763e584ecec30e54131985fdc899613f76722ba0794934243a7b566bd77d0fa2', '王一晖', 'business', 9092, 1094, 305, true, true, '2026-07-13 06:44:11.648842', '2026-07-13 06:44:11.648847');
INSERT INTO public.users VALUES (127, 'JX60082', 'scrypt:32768:8:1$yUI2ZcQBOSHNY7jk$47aa18553093c3c8d5ad6583bcd86f271c82aa398a098c173fd71ca1063d4ec25146c59a6ed73edff8ddeb2786034a979d2cda1f952d326229e4bca227acc523', '蔡铭', 'business', 9093, 1094, 305, true, true, '2026-07-13 06:44:11.740945', '2026-07-13 06:44:11.74095');
INSERT INTO public.users VALUES (128, 'JX60083', 'scrypt:32768:8:1$7Nl8SHi117DUpN43$8e73aef46bc6d7dbcb1ae0a218d209c3bfbcbd551972170c9ef1761b4f16c21467108f393c5daa01f34811eadd0d9b0efc9e4b26ae251d0424eb866e05ef25f8', '施伟杰', 'business', 9094, 1098, 307, true, true, '2026-07-13 06:44:11.830659', '2026-07-13 06:44:11.830664');
INSERT INTO public.users VALUES (129, 'JX60087', 'scrypt:32768:8:1$m5aQCDvIXURLZXdt$d26bcc93b14eb932c0184a7812965f5f608df67539fb79f61c7f0d79435382a86759eabd49ae18fdd45acfc6b1f83e2c05c7eb47203b1ff0155942d943564e2f', '陈超', 'business', 9098, 1104, 254, true, true, '2026-07-13 06:44:11.923563', '2026-07-13 06:44:11.923568');
INSERT INTO public.users VALUES (130, 'JX60089', 'scrypt:32768:8:1$XhCdV5G70s88ZIIR$0d97a89918ea45abca8bfe115ed25cdbf2075e06b8d015466a6b2adb7555b9603394edb5a2d83dc7aaee75bda973711904f9cb9a6957e5c29e9d1b7caed54934', '刘林洋', 'business', 9099, 1096, 306, true, true, '2026-07-13 06:44:12.016275', '2026-07-13 06:44:12.016279');
INSERT INTO public.users VALUES (131, 'JX60090', 'scrypt:32768:8:1$084csyLZMh4uBbve$941076cec4debe20eb93fbe6d944427a07b26f408a92e452bc0216c2c0e2b10b24965d9cc3c430de28ebc1374e342ac93123e6065d22cffa4f8ba7160e1c0d28', '沈浩', 'business', 9100, 1098, 307, true, true, '2026-07-13 06:44:12.109745', '2026-07-13 06:44:12.109751');
INSERT INTO public.users VALUES (132, 'JX60091', 'scrypt:32768:8:1$txkRvEArZ98SBelK$3dcb79077750e9fcfe9f81bb6e5c491e93059e4af0b6c48f8b9da20c1e0ce974d36920a505604716f4600d8983de58d0cf3179ddb98688500460eb0262f8d4c8', '何彦平', 'business', 9101, 1096, 289, true, true, '2026-07-13 06:44:12.200738', '2026-07-13 06:44:12.200743');
INSERT INTO public.users VALUES (133, 'JX60093', 'scrypt:32768:8:1$fRq1YWMS5WNxgVpB$ddc6db4c73edf189122436757c800ca55a3957ff521980ec28f01b9a944f988ee80d33391ee8ab92d7a6f560cf58e7f087d684247ea9c14c2b437f87a51a02a4', '惠康', 'business', 9103, 1094, 305, true, true, '2026-07-13 06:44:12.295802', '2026-07-13 06:44:12.295807');
INSERT INTO public.users VALUES (134, 'JX60095', 'scrypt:32768:8:1$XHHsg2b5wWw4nVeQ$d7c1fea2c2113943c173febfcf88a6d68bc44dc86aeb47a3e8aeadc50a1e49705ace5b1743a28b0f565c4f7e6f2ca910548f6091e5868129055827ca6f59fdd2', '刘涛', 'business', 9105, 1095, 305, true, true, '2026-07-13 06:44:12.386518', '2026-07-13 06:44:12.386523');
INSERT INTO public.users VALUES (135, 'JX60097', 'scrypt:32768:8:1$qkVg2XBtNJBw3TQc$48bf3fb25c00bea3f5e62f7f1fae37570317711eab4e6f75619fe51a54ea72a86cc64231b00e1ed888cc91f301179f1baa7271b06cfd375bd20156324ac44470', '孙磊', 'business', 9107, 1095, 305, true, true, '2026-07-13 06:44:12.477398', '2026-07-13 06:44:12.477403');
INSERT INTO public.users VALUES (136, 'JX60101', 'scrypt:32768:8:1$Tr45H9AvAbkIFNsv$f784b299f0c5e84865238b4970178e6dc1eb8e0737e68dd0a77df983d4f9f36baf4a87ee18953ad9df640599d0b685518ec50be8e9652ccd42f2a242f390ee4f', '李涛', 'business', 9109, 1102, 301, true, true, '2026-07-13 06:44:12.569732', '2026-07-13 06:44:12.569737');
INSERT INTO public.users VALUES (137, 'JX60102', 'scrypt:32768:8:1$ggeKLGNPvbxpKLha$bdb8fb8642bf16dad6ac44597564e1d3798af9d2261a510865ed3ac1e9189bf51b6d75cf183b34b3600aa1939997292a40027b53df6d01163f309e1e7a050ea9', '许智荣', 'business', 9110, 1062, 277, true, true, '2026-07-13 06:44:12.660472', '2026-07-13 06:44:12.660477');
INSERT INTO public.users VALUES (138, 'JX60115', 'scrypt:32768:8:1$BB1Gc1NEl8qSD6Qs$ef95774f3279aaa21fcd5d288f9bbfc983a99fd57e2ff1738e101968a7892c73ce3f78818bcedce78b282b02028a03dbab606929cca53ca09c3efae63f1147f0', '宁振浩', 'business', 9122, 1104, 299, true, true, '2026-07-13 06:44:12.752354', '2026-07-13 06:44:12.752359');
INSERT INTO public.users VALUES (139, 'JX60116', 'scrypt:32768:8:1$y1qduZMgrlSEO6ry$958edb64961e89b2a3796d83a2f8a33a4d3a90fba429137a66399ddccf00e4b47e8598d224910ab91af0c0f3b1b9c14a6d35b8cdad8734c7fea38c013d4ee373', '殷程波', 'business', 9123, 1104, 301, true, true, '2026-07-13 06:44:12.842062', '2026-07-13 06:44:12.842067');
INSERT INTO public.users VALUES (140, 'JX60118', 'scrypt:32768:8:1$TiiUzahGH7fandUt$53468c57c9211a97842cbd60222515664b2c6646e5725176faee4d0190134c1624770870dde27fed5c7c24da90646c1acf521ebe56210dfd3a9310a718d4c4fa', '谢伟', 'business', 9125, 1102, 299, true, true, '2026-07-13 06:44:12.935728', '2026-07-13 06:44:12.935733');
INSERT INTO public.users VALUES (141, 'JX60124', 'scrypt:32768:8:1$U13Lc1NCcpQJbO75$68b11bce3e3c96392d38a7fa4f358be19ca37a467a0a9d242ea807440f5e62b86724cc9c63da4b9e0d784625b4a906fe920dba8759031b2d95333c6c24f6f2fa', '罗仁全', 'business', 9131, 1057, 307, true, true, '2026-07-13 06:44:13.027385', '2026-07-13 06:44:13.02739');
INSERT INTO public.users VALUES (142, 'JX60130', 'scrypt:32768:8:1$FZQyPPYZwS7zojbO$8e862f87623dd2c22eee80290514aad9bd97bab23079cd4634e49a7d48f52d6a8b2770f3a42d801e8467b1fca9e3fd28bc9a0c4f427c66a175e7c498176c50fb', '王井泉', 'business', 9137, 1099, 299, true, true, '2026-07-13 06:44:13.119728', '2026-07-13 06:44:13.119733');
INSERT INTO public.users VALUES (143, 'JX60137', 'scrypt:32768:8:1$7YuXCVlsqurzwBpC$7e2045ffb66e1f861356701af82fbe58b8953a027df1decc1f22d1610440e0387051a5bf9f130f7eb78a864c846e454b88583c819b54199069a8bfc209b1d31e', '殷亮', 'business', 9144, 1057, 307, true, true, '2026-07-13 06:44:13.214214', '2026-07-13 06:44:13.21422');
INSERT INTO public.users VALUES (144, 'JX60139', 'scrypt:32768:8:1$WY2lHht3UHgDWZjs$7c7a2f489c8e62613c721c2ab604fa0afc16ff333fbd41d2c4fe27c4be3333276b0d345e708a281c8af72f67116d68d123e813517d24c5a36da6214b4fa01d5c', '李仙海', 'business', 9146, 1057, 307, true, true, '2026-07-13 06:44:13.306547', '2026-07-13 06:44:13.306552');
INSERT INTO public.users VALUES (145, 'JX60140', 'scrypt:32768:8:1$Kp9o3JK5qQ7Iy7H6$c68fd1a6768c4aca9f8b08e3a2376c956ec4fb7cf0b0244e3b64a8c8c68853daf544fcf1dd1ad516d2ecd8bee3d96b7e3dde70ea9229f5711b069683f1518198', '陈宇超', 'business', 9149, 1099, 307, true, true, '2026-07-13 06:44:13.396084', '2026-07-13 06:44:13.396088');
INSERT INTO public.users VALUES (146, 'JS90196', 'scrypt:32768:8:1$ssHQvHCGli6gbb2E$37fd120b25aa61fbae085ec32e44724fd34f297e0cede388ca5a3b93117feef2bc4dae4fde4cc1009e45908df3ee3eefa52d06b3ff99e498fedb9655b5e3ef05', '何俊祥', 'business', 9210, 1100, 254, true, true, '2026-07-13 06:44:13.486831', '2026-07-13 06:44:13.486838');
INSERT INTO public.users VALUES (147, 'JS90202', 'scrypt:32768:8:1$EwGKg5bVF6mr0QBS$275ac461eaba2c9f47a83c32f87e8bafb4afa0ed0dcea1e6430bae93e0e361907a146c4c2cdbf214fc00ed51c1005aa98ff6cf09ff18ada3825061a470587e6c', '谢蒙恩', 'business', 9325, 1131, 259, true, true, '2026-07-13 06:44:13.576852', '2026-07-13 06:44:13.576858');
INSERT INTO public.users VALUES (148, 'JS90203', 'scrypt:32768:8:1$ovBUHI4oNcjJcisw$7f57a96701d562e855234be760989cbbb3f9d21cab1102efb1fb4f4644bf4270bd81c6d8f62f63e955d9ff739474c28eb188eb8070c3c88779ca2c100277d602', '谢贝宁', 'business', 9326, 1131, 259, true, true, '2026-07-13 06:44:13.666601', '2026-07-13 06:44:13.666606');
INSERT INTO public.users VALUES (149, 'JS90208', 'scrypt:32768:8:1$mZLly238VRvjiBnw$f2a3ea17160a1d7a8701861eefb5f09476a83ab7f85149347eb94caa2124489df9ff49475a29aa995a026b264b9fb39aa903fe7689adf0c644298a03f7c18f2b', '孔祥飞', 'business', 9331, 1025, 148, true, true, '2026-07-13 06:44:13.759408', '2026-07-13 06:44:13.759413');
INSERT INTO public.users VALUES (150, 'JS90209', 'scrypt:32768:8:1$z5tX6ojOLY5StsIi$bc29cbdf1dde200ecd4b187e64473384060496ab601831d9020ea6ebb62629a6a82d709190f4918a565a485aaf36c102dceb35b74c18172a9188037417e81b42', '贾兰兰', 'business', 9332, 1026, 259, true, true, '2026-07-13 06:44:13.854303', '2026-07-13 06:44:13.854308');
INSERT INTO public.users VALUES (151, 'JS90210', 'scrypt:32768:8:1$1EdqglP7xcon2Lrw$d50266564e8d1e45ed9b492db1769315ea49f18af4ca73ef5ffcefaa1114ae09fe62ee9a7585c091c2844e009ea7fe708d931ad3eccfd803bad0a04768d641ba', '崔占云', 'business', 9333, 1025, 94, true, true, '2026-07-13 06:44:13.951468', '2026-07-13 06:44:13.951473');
INSERT INTO public.users VALUES (152, 'JS90211', 'scrypt:32768:8:1$vC4GOn4Rjx3UKqd5$5363a4ff571f4f74351e53bd15d8baa14d2422a599705c0e510ab759f013a3574fb472aff738f24a56006f0bc21998c6ccfb1f41fbc502d5c60ded9f799ce3bb', '张培', 'business', 9334, 1128, 148, true, true, '2026-07-13 06:44:14.04687', '2026-07-13 06:44:14.046875');
INSERT INTO public.users VALUES (153, 'JS90212', 'scrypt:32768:8:1$BiPmWx5y4m4s3Owr$ac3934d4088081a97ef6f55fb9da8f6ae3ecfc4e9dd8eb6d65a00c348d9c8a3e28a5409edfa187355c57d57ffaff5c3beb4a0584fbcf89457d8973789b059691', '周洁', 'business', 9335, 1128, 100, true, true, '2026-07-13 06:44:14.144209', '2026-07-13 06:44:14.144214');
INSERT INTO public.users VALUES (154, 'JS90215', 'scrypt:32768:8:1$yqqcVqrkDsnwuHPK$1f0d08f18e9ee72f888116bfcf8103bfe88a4928bd8048063a7162198c29b6e742d3ebeb83a2f229e34eb9fa31fe837cfc07ca73de77673433004636607e75b0', '刘晓燕', 'business', 9337, 1128, 308, true, true, '2026-07-13 06:44:14.239187', '2026-07-13 06:44:14.239192');
INSERT INTO public.users VALUES (155, 'JS90216', 'scrypt:32768:8:1$DsFbd2EI93DwxqaY$29425fc39dc29f72f27d916123324212e1c10e1d95b35aaddba3dbe631bbde872b517a228fc4f3953ab3612a8edf2046ab50e7d0dbca708516ba067dab9bdc66', '林政宏', 'business', 9338, 1086, 268, true, true, '2026-07-13 06:44:14.33562', '2026-07-13 06:44:14.335625');
INSERT INTO public.users VALUES (156, 'JS90217', 'scrypt:32768:8:1$h4kiHYvlIwMQwhwj$3d1025668118104c62a1ff8d27035fbf0993494a632822d5b948783cb548d12610fc71f21d906cc647db612f5c2eff4ef31ae5a16b2ac4780345da1ba549339b', '袁艳', 'business', 9339, 1128, 301, true, true, '2026-07-13 06:44:14.43063', '2026-07-13 06:44:14.430635');
INSERT INTO public.users VALUES (157, 'JS90218', 'scrypt:32768:8:1$t8H3WdhcRYs5VYNY$e50ede9dc710eadf5b18f403878ecc22c9cb82435f5b18151a885cb819c7eef629942154b26ff5b6ada89d0b02f2a9fdf629ce1ef591e2fdb65b4af29b7aaff2', '石勇', 'business', 9340, 1113, 85, true, true, '2026-07-13 06:44:14.529341', '2026-07-13 06:44:14.529346');
INSERT INTO public.users VALUES (158, 'JS90219', 'scrypt:32768:8:1$KTTZj3oCxZ71qbGR$c516f7d9f4ef43d5753a80891743e31a16a631c788040c5ec55120e6478f185eb559c0f8214c70533cd10974187ec2fd0f36f727e6169a4fdf4a5854860ab9e4', '刘炳娇', 'business', 9341, 1113, 85, true, true, '2026-07-13 06:44:14.626959', '2026-07-13 06:44:14.626964');
INSERT INTO public.users VALUES (159, 'JS90220', 'scrypt:32768:8:1$UGzaditl6AUGmLNJ$d4850b9820aa7fd60416eab1189d6169c1db8a7830e9e572e88c6317ab6ab40df70f7ff56146625c252de13c7bc8cb9510e1236e5519a59e59a69947bb2eedab', '任燕秋', 'business', 9342, 1113, 148, true, true, '2026-07-13 06:44:14.723444', '2026-07-13 06:44:14.723449');
INSERT INTO public.users VALUES (160, 'JS90223', 'scrypt:32768:8:1$ZmfU7AH6aSQuz1Ol$32ca95fab6d58ee30f0c69b33f83677fd8a28c68e2d7068119a14876e5235b588946e2e1891b443f33222dea4294dfd7be80b4fa1c29cdaaa071e1e243fe17ef', '查锌', 'business', 9345, 1114, 85, true, true, '2026-07-13 06:44:14.818436', '2026-07-13 06:44:14.818441');
INSERT INTO public.users VALUES (161, 'JS90227', 'scrypt:32768:8:1$2rcnzUQh6mECsiGI$b45590d9ba23eb38b690107ae11c305882cbba29326ebd1fadc0d893092aaa7d6c3239618d4aeef5d9bf43e2a7126a4dae7af93e5480732f28affeefb5b36733', '濮钰荣', 'business', 9349, 1083, 259, true, true, '2026-07-13 06:44:14.915694', '2026-07-13 06:44:14.9157');
INSERT INTO public.users VALUES (162, 'JS90228', 'scrypt:32768:8:1$B6uH5O1EbZnLdmt7$fdd142ee19d66cec546512e892f2c80501e247b2f956617af17315980e7b53cff284c3109e87ff3e709fa721ef57b46781233e72d120807e6f7913e9ba937d2f', '侯奉君', 'business', 9350, 1111, 259, true, true, '2026-07-13 06:44:15.012838', '2026-07-13 06:44:15.012843');
INSERT INTO public.users VALUES (163, 'RS8990', 'scrypt:32768:8:1$vhnkIIFXW4Rb1Pyh$f0acbdf7214c4d6570feb9d185d7da3acc846d33384cd3193c08f7499d1d9b1f2cbfca91c864fa60dd95061a97ce5457e23e14b2ccbe323acabba1c1fc1a7f2e', '王兴华', 'business', 9353, 1115, 148, true, true, '2026-07-13 06:44:15.10975', '2026-07-13 06:44:15.109755');
INSERT INTO public.users VALUES (164, 'JS90200', 'scrypt:32768:8:1$aOcGDA5y7a0IRRBT$079c143b3fd432cdee4e480d2509c75f1b6e9cd039b14294acd68633ca81bc232c7b4e568795f60fb39e7de9725533907cf233f0f8cfbae88bd1798f288c46f7', '曾美华', 'business', 9358, 928, 311, true, true, '2026-07-13 06:44:15.204901', '2026-07-13 06:44:15.204907');
INSERT INTO public.users VALUES (165, 'JS90201', 'scrypt:32768:8:1$Fcr3xY6sHR4I6fD1$90178cd32130c997c8cf5eb8f83dd1d44becb32606f02728de32c31c176e7058d489db10889b72d73da0eb48d34ef4212c2cc36ff5ab19c0760ba20b4e0deab7', '石小蒙', 'business', 9359, 1131, 259, true, true, '2026-07-13 06:44:15.300612', '2026-07-13 06:44:15.300617');
INSERT INTO public.users VALUES (166, 'JX60147', 'scrypt:32768:8:1$KsrYHR00y3m1qW8z$471880a9aff32d17ac56103f771049bf7afa2411244ddd74a563e4a5a34b30f62467c548dcc005f9f3a6eae043c2c48fb1d6dcf1126c3668d1272ad3e7fe5385', '陈昊', 'business', 9364, 1105, 254, true, true, '2026-07-13 06:44:15.394099', '2026-07-13 06:44:15.394103');
INSERT INTO public.users VALUES (167, 'JX60148', 'scrypt:32768:8:1$sP6T9Jn6IAOmnqZo$b6a8cac6ced2358457884f1f53f460389d280f2d388c9916b8a1b18e1cdca37a2044830e2623a78917c74d89a1f14dd19cc4870979717c19e2960fd1ed29d095', '倪焕杰', 'business', 9365, 1105, 254, true, true, '2026-07-13 06:44:15.487966', '2026-07-13 06:44:15.48797');
INSERT INTO public.users VALUES (168, 'JX60150', 'scrypt:32768:8:1$TmxLU5QmA7JgKE4o$5657df0adc8a888e9a6eeed6e64a51dcacac29f0e02d328397d26f56c26e54aaba97f85e22fbce91cc459928301d9bfb01a95b483572af60638639798ca4735c', '杨骁', 'business', 9367, 1105, 269, true, true, '2026-07-13 06:44:15.57857', '2026-07-13 06:44:15.578575');
INSERT INTO public.users VALUES (169, 'RS8995', 'scrypt:32768:8:1$HTcpVLDag9YG81sT$fe36875978192b176eaec910944bbab4087a02e8f7eec636c6cd84b9ba04b3dbe5e4df9185d05541412272f2841430c0c89a10251e290e3397bdb08426d78290', '盘美玲', 'business', 9379, 1112, 156, true, true, '2026-07-13 06:44:15.670791', '2026-07-13 06:44:15.670797');
INSERT INTO public.users VALUES (170, 'JS90232', 'scrypt:32768:8:1$25OI2N8C0PDsk1Wb$4a55ea539c16b7a69ae569602367966bb3db80710e90815c036baca0b7dc6e95eda1e62e2667d9a098c34899dd79414387eaf90f927184d53f5ac01fe4a056e5', '刘龙', 'business', 9383, 1103, 254, true, true, '2026-07-13 06:44:15.764587', '2026-07-13 06:44:15.764591');
INSERT INTO public.users VALUES (171, 'JS90236', 'scrypt:32768:8:1$sTQcZDPlUsqLFWBY$7d8a8e4ea2b07f15d0a8782151672e4894709cbe55c652a0bc3ca449aac8ebc5cdf387780aed74ebbb1196d0edec4dfcecde25fd8448d00df72502942ac8ed04', '刘吉强', 'business', 9389, 1128, 277, true, true, '2026-07-13 06:44:15.855737', '2026-07-13 06:44:15.855741');
INSERT INTO public.users VALUES (172, 'JS90238', 'scrypt:32768:8:1$Xob5i76eK6GagaE8$6af412c51683a25afa1fe5dbdaa91fa60290da1154060121f253277717f3c3e23fa3f4b559e46889f5bd918325d38be1c607294200d4fb9c0d15c05c8db8105c', '吴焕', 'business', 9435, 722, 122, true, true, '2026-07-13 06:44:15.948511', '2026-07-13 06:44:15.948516');
INSERT INTO public.users VALUES (173, 'JS90239', 'scrypt:32768:8:1$WbPpaTtwivH0OXqI$2d8c7191b0921c761c8703baacbf98836d0aeeaccb2ab6f6097b6a138c97704ac0efaef4cd39ce667883679934cd3e70b4fcab16c39ab2e870414a9ce96488dd', '蒋勇', 'business', 9438, 1083, 310, true, true, '2026-07-13 06:44:16.039101', '2026-07-13 06:44:16.039107');
INSERT INTO public.users VALUES (174, 'RS9000', 'scrypt:32768:8:1$KANMit3tyCqiNNWY$92c71bf99e4a0b1f76b548d56492bbd3c62a3745cb17f07a2d9fbe9e6dc288aa18186dcf96b73567f2317e6fdfe03c7d57ee14622b4bbc61f58d381d32baf788', '袁保存', 'business', 9439, 1076, 254, true, true, '2026-07-13 06:44:16.13437', '2026-07-13 06:44:16.134375');
INSERT INTO public.users VALUES (175, 'RS9001', 'scrypt:32768:8:1$Rn2mSi5deP8DATPp$1582d4e57bb1b7396bcd3d3a79db5fafb6cfa93dce6159c92514c75e78d697e485b726ad7198b4e9aac5a80adb5854be64d72e2e4a0ca5a2938221d3045a1983', '胡任行', 'business', 9440, 1081, 122, true, true, '2026-07-13 06:44:16.224933', '2026-07-13 06:44:16.224938');
INSERT INTO public.users VALUES (176, 'RS9002', 'scrypt:32768:8:1$NKzf6j44ykLYsk4p$53cc7f0883b4eaa25348c13d045882ad4995df148d0b42bb2c283a811ba0d8c5eadc2eed2dcebff0b55934236ac87ab0fde2e16227734e4852b2c419088ad546', '高峰', 'business', 9441, 1130, 148, true, true, '2026-07-13 06:44:16.317877', '2026-07-13 06:44:16.317882');
INSERT INTO public.users VALUES (177, 'JN80001', 'scrypt:32768:8:1$ZOGpPxzD1M6FfBck$60df55f27a1a4c74eff80942fce5ac73fc766a665dc5e77dcd6b9fd81eaee64184df76b8ed1fed0a77ab0b055d799ee0f95afb03273636ef1bfe02174a09c8ec', '张雨生', 'business', 9442, 1134, 277, true, true, '2026-07-13 06:44:16.407704', '2026-07-13 06:44:16.407709');
INSERT INTO public.users VALUES (178, 'JN80002', 'scrypt:32768:8:1$R1wGkrTDjVuCeyyS$a045f1bf6f3c232df117955096ef00e24cdb662dc2036f14f9c816c761dd3e342546bd5a46e406c76181cb5f55d964a608203f3adcb0cda1d4861e89d06467e7', '崔海天', 'business', 9443, 1137, 300, true, true, '2026-07-13 06:44:16.499567', '2026-07-13 06:44:16.499572');
INSERT INTO public.users VALUES (179, 'RS9003', 'scrypt:32768:8:1$d7ByPAfWdW7cg0fw$6d70cd21c8fa40d43b67318bbfa63a9b71f11420ac1bcf9adf4024e71f119e97aceafc98d5b2bfe5dc3c3c0596536eab1c217f7dfe98385f8b640dc7df709350', '顾开国', 'business', 9444, 1108, 124, true, true, '2026-07-13 06:44:16.589335', '2026-07-13 06:44:16.58934');
INSERT INTO public.users VALUES (180, 'JS90240', 'scrypt:32768:8:1$1ZOYalOJJD5QwN2s$4f22cff755c47b782e0d14f709302f7c796d8555e7c2273de1823a968c8c8c440cb516983215236190389d244ee2f546e1d6fcbd81322702b2278def12d3f4fa', '赵永轩', 'business', 9446, 1146, 163, true, true, '2026-07-13 06:44:16.679285', '2026-07-13 06:44:16.67929');
INSERT INTO public.users VALUES (181, 'JS90241', 'scrypt:32768:8:1$lZj8s04aNj7uU1ZP$de714fd0a706112106c8df122553d2c1542e029b170912f714c7d23ac4edbf526a31c838c3f00db60840b76c672b51b0c3eb1a86d23916faf794204afae26762', '桂亮', 'business', 9447, 1154, 268, true, true, '2026-07-13 06:44:16.772024', '2026-07-13 06:44:16.772029');
INSERT INTO public.users VALUES (182, 'JS90242', 'scrypt:32768:8:1$L9rBEHJGqctLp142$bb162ae243b49348aab3297b57cac770ba91fdb6ec8d8fe84a8a9b44ad0b91a78c8f582dcdefa041f140da4932a7797ac63aa5966f26e9f514019995cd113998', '瞿鑫', 'business', 9448, 1160, 103, true, true, '2026-07-13 06:44:16.861978', '2026-07-13 06:44:16.861982');
INSERT INTO public.users VALUES (183, 'JS90243', 'scrypt:32768:8:1$hwcmlFz4ET9Ar2lm$2cfee28321ba6c42520146b55adf2e0f5000e93123087e6af54a5a1168f792d37266621b67c0a7c21edf2cb4e08e3dc15c7fcf8969f929fc761eda9e6520a089', '祝大龙', 'business', 9449, 1055, 99, true, true, '2026-07-13 06:44:16.955287', '2026-07-13 06:44:16.955292');
INSERT INTO public.users VALUES (184, 'JS90244', 'scrypt:32768:8:1$vo2T40SZih77fOBA$7356e2055359e1419c7cb9bc61151227cbd0737433ed4cd8edfa0c55fd2b4b33ca25366522b7c1cbf00e1c0a273b99c49a9ceb1d33cb9423770f045dfa060095', '殷佳斌', 'business', 9450, 1055, 99, true, true, '2026-07-13 06:44:17.046916', '2026-07-13 06:44:17.046922');
INSERT INTO public.users VALUES (185, 'JS90245', 'scrypt:32768:8:1$lj8dqGBgYrHqj01Y$c4f5629282170e4c65858a7e610cd798856491b1a291e22d87b1020b33ab2aef82f1ce12087ffb57c8899213fc4d76d7c2adda7b629a6ccc77fb44e1ff8ac8a2', '武钱勇', 'business', 9451, 1142, 148, true, true, '2026-07-13 06:44:17.141096', '2026-07-13 06:44:17.141101');
INSERT INTO public.users VALUES (186, 'JS90246', 'scrypt:32768:8:1$4LVoJT11qgXRd7QP$f2555987486a57966abf7e0532d9fb3581397e4269368a350cba16da1198edc6592501b4f7f4f3d3b5d82e70d9bcbc30eded8f7d502b25c5239f2ed9c500dd92', '吕楠', 'business', 9452, 1100, 148, true, true, '2026-07-13 06:44:17.233264', '2026-07-13 06:44:17.233269');
INSERT INTO public.users VALUES (187, 'JS90247', 'scrypt:32768:8:1$Cdzfg6N0HHWkWle0$ee4ed9c37a3832efa50889faa5948f1db70deef5c347f0a9a03a1a7cd7cc4f5374cf39c5e8876d31fbad1386b858906373e04f505cd0ce3e025762da4d7421fe', '杨杰', 'business', 9453, 1100, 148, true, true, '2026-07-13 06:44:17.36252', '2026-07-13 06:44:17.362525');
INSERT INTO public.users VALUES (188, 'JS90249', 'scrypt:32768:8:1$mt6kgV05jMCO4DJo$bebc8e1fe36a8d5e915c49cf01f58fb0ec985f5442df5e364a07a6aaf65ba558e52997a62430af778d1cffd26ab4ce3097a042d26128b141e024686d87a890b1', '肖佳伟', 'business', 9455, 1160, 100, true, true, '2026-07-13 06:44:17.452775', '2026-07-13 06:44:17.45278');
INSERT INTO public.users VALUES (189, 'JS90250', 'scrypt:32768:8:1$Lf8Js5zc9clQHcnf$ce1d12719506b01dd357ae732c6bd3c9cd33ca67768a65d05babc8c9123a752ce010a4c7eaeb0ac06046ba0ce226543f08b2d2e891d45bfa4dacb49e278ebb8b', '李超', 'business', 9456, 1055, 100, true, true, '2026-07-13 06:44:17.545602', '2026-07-13 06:44:17.545607');
INSERT INTO public.users VALUES (190, 'JS90251', 'scrypt:32768:8:1$gatHzvbZcpIcBpw2$0ebf48d4b07e16d02e9990a29d328bd9f7195613dbf27e4cf947cadd57f79b242a264bfc830c90755972e1aa914165afd34b7cfb9a55e2ec6c93c9597231d52b', '吕春鹏', 'business', 9457, 1055, 271, true, true, '2026-07-13 06:44:17.635602', '2026-07-13 06:44:17.635607');
INSERT INTO public.users VALUES (191, 'JS90252', 'scrypt:32768:8:1$lLcx59RxfY9oX19c$ee256d69f3d3fd87f65e0d2a035cbfd0ef726fe078a7702c5b6e4b119bfb32bd474ce131a7a2b73195f0d99b1924c5e3e950f8527e523438710fd664b94b0046', '樊连玉', 'business', 9458, 1058, 254, true, true, '2026-07-13 06:44:17.727517', '2026-07-13 06:44:17.727522');
INSERT INTO public.users VALUES (192, 'JS90253', 'scrypt:32768:8:1$3cA8eVCpBugfadfZ$1eff336b0e15d43594264cf7bdb59616b2e903e1b801dd3ef11965564173f418359979df25a0ad049e104a4a3f060af15a1e367ec511aaa6039c2bfd09263e46', '马忠鑫', 'business', 9459, 1100, 254, true, true, '2026-07-13 06:44:17.818665', '2026-07-13 06:44:17.81867');
INSERT INTO public.users VALUES (193, 'JS90254', 'scrypt:32768:8:1$1Yd7AbfDFPiNPmKJ$fcfe61681351f9a143b9102ddb09e079addf2c6a29ad077f9f4b96c1acf4ae5483ffec41723cef1ec41a0bd0881642a9d15862058b5633dd1c24bb24da945470', '张武帅', 'business', 9460, 1100, 254, true, true, '2026-07-13 06:44:17.911805', '2026-07-13 06:44:17.91181');
INSERT INTO public.users VALUES (194, 'JS90255', 'scrypt:32768:8:1$zechCEQY5Az0xOs9$c3484d305f387469de15da85cb704c6de76cc3f8c23fbf78f3290727cc22c3a4c1b04365110179e83377f5396ca5126161e1d93cb77024e6462f1df1c79fb1d4', '石胜全', 'business', 9461, 1100, 254, true, true, '2026-07-13 06:44:18.005433', '2026-07-13 06:44:18.005438');
INSERT INTO public.users VALUES (195, 'JS90256', 'scrypt:32768:8:1$KCsYjN6yuyh2z2Q3$23cb2bac3e8aba1fbe56e6021e297d7a1c2d533410c46c02bf37b624a1b22546dac653d45d68cdf286fdf151577a4d61c145fa27e1f4db934f470618bd5e4350', '苗文学', 'business', 9462, 1160, 254, true, true, '2026-07-13 06:44:18.10007', '2026-07-13 06:44:18.100075');
INSERT INTO public.users VALUES (196, 'JS90257', 'scrypt:32768:8:1$CaB6kihfvKt78U1m$eb2846c0395e51813cb5b8518fab6bff4ef577e44827b622264c8875e26df718bf2049926f5fccf41cdcd4d8ff7130861481513ae422765bb951594f435cf29b', '胡天富', 'business', 9463, 1160, 254, true, true, '2026-07-13 06:44:18.190656', '2026-07-13 06:44:18.190662');
INSERT INTO public.users VALUES (197, 'JS90258', 'scrypt:32768:8:1$4eeXwaEIqnEPBwHR$5f38534553b37b7cc5af616c525e9b27fb0f6ae2a0c821ff8fded57dabb267f3275ab1ffb07720f4b896fbd312e8e345abb2c8e3ab0674030d91b4f99da951be', '蔡鹏飞', 'business', 9464, 1160, 254, true, true, '2026-07-13 06:44:18.280645', '2026-07-13 06:44:18.28065');
INSERT INTO public.users VALUES (198, 'JS90259', 'scrypt:32768:8:1$qCw4rVJoFHWap528$2f9dbd69ed115e70a36a7b7074c35d4e6be010b4397ef5f11d5765a9fe54fec250d4d1428986f66e739528550e3bb22faeac6ddb11515b6b2754285ca6b2ce1e', '孔令强', 'business', 9465, 1100, 254, true, true, '2026-07-13 06:44:18.372334', '2026-07-13 06:44:18.372338');
INSERT INTO public.users VALUES (199, 'JS90260', 'scrypt:32768:8:1$gBXRR5zuq2vlQP6J$04a03e8423b55bbd51954bf2bf2de3cbc0f308b6aec1033bf992c803e014bf47453f29f704df7ccc7d20c4f5d9e3fd4d02cde232ab662c158430d6dd2ce4e466', '谢海松', 'business', 9466, 1055, 254, true, true, '2026-07-13 06:44:18.462144', '2026-07-13 06:44:18.462149');
INSERT INTO public.users VALUES (200, 'JS90261', 'scrypt:32768:8:1$3BuVFlsgnLYVIqQ1$8c08dcf3c0cba72107cd77f0eae61168867ae7d4f7a292254cc527753401700dac284d35d61d872f5fa17db8fb0c05fd60e82930a299b5630a8a1d23e399ec34', '马尧', 'business', 9467, 1055, 254, true, true, '2026-07-13 06:44:18.554508', '2026-07-13 06:44:18.554513');
INSERT INTO public.users VALUES (201, 'JS90262', 'scrypt:32768:8:1$2zmAYcoMVfRcxbJU$430505ec1a6185f633051f7906aec04c6b8815142b1f4325cf0eab285a2984dd342042250f86aeb9e96b93e0d7e2776a10556f7c0d8a6e3de266e5b9dd431590', '张文亮', 'business', 9468, 1055, 254, true, true, '2026-07-13 06:44:18.647057', '2026-07-13 06:44:18.647062');
INSERT INTO public.users VALUES (202, 'JS90263', 'scrypt:32768:8:1$AkLwhlPFwYheESFD$afcfb504adf283e305f4aca8ce1b62f8fde789d886c13a960ebb73a629cd8c55bdc6e51ae3b2af70409cea5018a76bb18456847c2b775275c9e9366a4595014e', '吴扣存', 'business', 9469, 1055, 254, true, true, '2026-07-13 06:44:18.740725', '2026-07-13 06:44:18.74073');
INSERT INTO public.users VALUES (203, 'JS90264', 'scrypt:32768:8:1$l7W8cvdCxDW3sGzO$3128654af20f12ebaa4363abe8c18e342e6a6f28b108a24e8f322c8cf649268bbcf2ba54eb5cecd268c7615b70497ce2541e149e7aa19a68d34632335d8e7225', '易志', 'business', 9470, 1055, 254, true, true, '2026-07-13 06:44:18.830454', '2026-07-13 06:44:18.830459');
INSERT INTO public.users VALUES (204, 'JS90265', 'scrypt:32768:8:1$jzQEHeVeWG03Zhbh$2af04d563406ef203c58df355418b2695792e89994d840ffed6e2b67e8d74b334f11bcc6f32faf7d4a4d79ec573703f33a15dcf0696fb35a6d4e2c6ba4620a34', '周江山', 'business', 9471, 1055, 254, true, true, '2026-07-13 06:44:18.923225', '2026-07-13 06:44:18.923231');
INSERT INTO public.users VALUES (205, 'JS90266', 'scrypt:32768:8:1$xHWACyI0W4nxgu9a$c20da09801cfd0b42e74538fc3898898e0e49a9eeada3551afbfd078b51bb1095939e967c2e61460eb0a89223719a1c4b52416fbe684eab5611869933e3da05d', '苏林宇', 'business', 9472, 1160, 254, true, true, '2026-07-13 06:44:19.013659', '2026-07-13 06:44:19.013664');
INSERT INTO public.users VALUES (206, 'JS90267', 'scrypt:32768:8:1$QW9sTyRM3FUSDBLj$8582a4cb2a85d30438ecaa32c66ce2cfd6cfc1b0ba8ae199c8317908f062b73466a673988686df3c019b2812575f8084f6e4da744177e5e61fde54b9a49e4718', '徐涛', 'business', 9473, 1058, 254, true, true, '2026-07-13 06:44:19.106425', '2026-07-13 06:44:19.10643');
INSERT INTO public.users VALUES (207, 'JS90268', 'scrypt:32768:8:1$ETWAH9abV54r2oWn$31bf8e02c1c165b346aeef178db1c9eb132e4bdb82dd41c50ce8dcf6e00bfa0aecc140a2e44d25a29abc2223a823043811c1db71a8b1f5779e6e385e45f1177a', '彭串', 'business', 9474, 1055, 254, true, true, '2026-07-13 06:44:19.1967', '2026-07-13 06:44:19.196706');
INSERT INTO public.users VALUES (208, 'JS90269', 'scrypt:32768:8:1$BuOVlycyUuBaYqBP$6b4265989606e2f90ff2d78bb197c5a31e6245cd260cfd8f6ec82b4d173f39a1bfb63ab4624349f7ccef6aab9547b5d47c3b003a80960f9ab7f408e829ffdcd7', '严青', 'business', 9475, 1160, 254, true, true, '2026-07-13 06:44:19.287957', '2026-07-13 06:44:19.287963');
INSERT INTO public.users VALUES (209, 'JS90270', 'scrypt:32768:8:1$mFnuoKVNBaRhWszq$e57c50304096439527898850cda87d57ad84b563d943ced09111e05b197ba1e1d7091d049fb8490ef314da6fa0cc0383516ad34e5bb3e8aec6b727949e310645', '汪洋', 'business', 9476, 1055, 141, true, true, '2026-07-13 06:44:19.380654', '2026-07-13 06:44:19.380659');
INSERT INTO public.users VALUES (210, 'JS90271', 'scrypt:32768:8:1$Jji8FSWHyB8jrGZb$dab0c036db338f4e67e90942b94d1027e0caf36da1c620c0cdd09248113b222ef4251c3205ef9a903504e6636c390860af358c8ec216a0f927ee2a7cab7984f2', '刘耀东', 'business', 9477, 1055, 141, true, true, '2026-07-13 06:44:19.475951', '2026-07-13 06:44:19.475955');
INSERT INTO public.users VALUES (211, 'JS90272', 'scrypt:32768:8:1$dtl9xDJZv1IIapq6$8ffacbb18de0c6d7286b6c1d6d45101b1c67882416bad47b0d5a74034a9bdf1e82cd82de85130721c16cdf741be175ba63b07d05294c42188423f6a309d0b152', '谢宇', 'business', 9478, 1154, 264, true, true, '2026-07-13 06:44:19.580933', '2026-07-13 06:44:19.58094');
INSERT INTO public.users VALUES (212, 'RS9004', 'scrypt:32768:8:1$fw5wX3E6FkC6dcVy$d7b4de599ce15f3d6ffcd7bdca81d85167af65b8133f2bda8f52c8bf929f1c3396ff01fd842f78936bf63b0352e54201af474c9896c48077f0e7b8c719321a05', '王振', 'business', 9479, 1170, 298, true, true, '2026-07-13 06:44:19.681682', '2026-07-13 06:44:19.681688');
INSERT INTO public.users VALUES (213, 'RS9005', 'scrypt:32768:8:1$9kBYGjAaNWT0MQMg$9b91dd869b6c2f8bdf4701ba8da69072447e7081bcff8e1eeba5482a568e1bce3dd38e7adb802da25795fe0957ba9353f08e47d4552cbd74f5995ae190073f71', '姬英男', 'business', 9480, 1119, 254, true, true, '2026-07-13 06:44:19.778893', '2026-07-13 06:44:19.778897');
INSERT INTO public.users VALUES (214, 'RS9006', 'scrypt:32768:8:1$jv0bonfcUPvM8Tn1$90b1633a007c2ee22e72ad58136269cdd2acc647ee0fb8c0dd98022dae54089107a96dcff298503d9be5cd912c2819cd5e7a06591df5cdfc7ba7248dd39b7f39', '袁亚军', 'business', 9481, 1122, 254, true, true, '2026-07-13 06:44:19.875578', '2026-07-13 06:44:19.875583');
INSERT INTO public.users VALUES (215, 'RS9007', 'scrypt:32768:8:1$pYeApMtCIHmvQJSC$e475e1014275c2eda13b40eb9f1eefad869168099ef11790c1e7838659674956f66e0a5b18e6f0ee18a9f11de2ab74431496cff5d9833db5a351637e523d1ad2', '陈梦', 'business', 9482, 1076, 301, true, true, '2026-07-13 06:44:19.973957', '2026-07-13 06:44:19.973962');
INSERT INTO public.users VALUES (216, 'RS9008', 'scrypt:32768:8:1$GlIFit5EUiFeaRKk$453b717d269eac72033794a6de298885956ddf1a3b0c35cc38ecfa4f676d43d733fdfd9b8556fa8543e3c4c2ae35a9dc9d0da2aa8b586c9851cf09b3faa72234', '计亚宁', 'business', 9483, 1130, 260, true, true, '2026-07-13 06:44:20.071486', '2026-07-13 06:44:20.071491');
INSERT INTO public.users VALUES (217, 'RS9009', 'scrypt:32768:8:1$sjETnakT7zTz0pH3$a60cb8dc569e496282cce25b4ac0c062dac74748c6fbecc6e87598c283dfd9dee6e5f1b936c14b08978abbc780cb9151c8413eb0fb70911443bb6414ace94b03', '范钊', 'business', 9484, 1084, 259, true, true, '2026-07-13 06:44:20.17025', '2026-07-13 06:44:20.170256');
INSERT INTO public.users VALUES (218, 'RS9010', 'scrypt:32768:8:1$rR3sZpIZNjP78wk3$d15390a9c0e96b031fbc9f4186228c411d4d435130e6f930d0c7a782fcf5604225651e8975eecface43262d9f56594baf882e002d8bf756b269b1ff9f98af88d', '朱玲', 'business', 9485, 1084, 264, true, true, '2026-07-13 06:44:20.26629', '2026-07-13 06:44:20.266296');
INSERT INTO public.users VALUES (219, 'JS90273', 'scrypt:32768:8:1$mNwaCPlK8u08BLH4$e0055ccf00adae68fe92ec27b0ad359d50520a17899b2091d76c5be915cb6af553be18a6076f1801369b7a7c942a5d7fff294ee5832712f41aa7bf5c988d37da', '贺雷博', 'business', 9486, 1058, 100, true, true, '2026-07-13 06:44:20.364187', '2026-07-13 06:44:20.364192');
INSERT INTO public.users VALUES (220, 'JN80003', 'scrypt:32768:8:1$Y9u0CMaYE9EEo8YX$852016dd0f9b4b2142190c93beff5ae017505c20c2208b251863bae5a135fd078e5d2454863c90f96ee82cca475e1a6944421b0592396e5e3facb3ec2204a73d', '顾鉴', 'business', 9487, 1157, 301, true, true, '2026-07-13 06:44:20.459659', '2026-07-13 06:44:20.459665');
INSERT INTO public.users VALUES (221, 'JS90274', 'scrypt:32768:8:1$iFTk3MOm1sZ7ju2J$93c1d46e518d08da8176e26b4e3d3d306a0da056043f274c9dc5742fd5370d203e47da1971543d45b54be2e3a30e53d4d7e97fd43e17ee96faca343d9301c7e3', '张成伟', 'business', 9488, 1158, 148, true, true, '2026-07-13 06:44:20.558782', '2026-07-13 06:44:20.558788');
INSERT INTO public.users VALUES (222, 'JS902321', 'scrypt:32768:8:1$zwrq12a800cdCkKR$2c14cc2b7dc6e99f921a0deb13c58e9422fbe639f456415641658eb94225c5598ed65fc4d68ad34949031fa032a914eeb4d228d2cfd92148d1c6df015d2b2e8e', '刘成建', 'business', 9495, 1055, 254, true, true, '2026-07-13 06:44:20.656068', '2026-07-13 06:44:20.656074');
INSERT INTO public.users VALUES (223, 'JS90275', 'scrypt:32768:8:1$BWKB1oHhQg2Umf75$6b63bb731f0d9b22a680deced5ab80ae970d17b79a27ec3ee184f4b2cf9a8c8c13ceebe6dc3b61b5e51953a42fe35562b7ed116b48fbf89df022cc88f228f1a1', '石丽萍', 'business', 9503, 1131, 259, true, true, '2026-07-13 06:44:20.754498', '2026-07-13 06:44:20.754503');
INSERT INTO public.users VALUES (224, 'JS90276', 'scrypt:32768:8:1$792UbnzP8hhPGwWG$37ef67e552ecfa04566fe78cbd2431449eee0bc1d64b939d86637e2090b20802836611bd02e48c26183d0c83cf86742d6f3a36d061a0a0c5d647d112304ff3c4', '吴艺阳', 'business', 9504, 1055, 263, true, true, '2026-07-13 06:44:20.85104', '2026-07-13 06:44:20.851045');
INSERT INTO public.users VALUES (225, 'JS90277', 'scrypt:32768:8:1$9k9f1Wufb6R9DSDH$219c298f387664bde9ad0b62bde9059e795e20693bb21bb8f281d8c358b55d8db8065c523fcfe5050b2bd19d85212cd3b472b331d03613c966412624382c9d5f', '刘华培', 'business', 9505, 1158, 124, true, true, '2026-07-13 06:44:20.946816', '2026-07-13 06:44:20.94682');
INSERT INTO public.users VALUES (226, 'JS90278', 'scrypt:32768:8:1$fKQFszjDOSr5sXEX$3a9a8b8137fff2ec7c66f4c2d48085d954b4b24e4317a88c93c563675943dccdb792297eddd9dfd115ea1a3cfc728a28623737f52631df2965e9d2658d091f14', '马文涛', 'business', 9506, 1159, 263, true, true, '2026-07-13 06:44:21.039308', '2026-07-13 06:44:21.039313');
INSERT INTO public.users VALUES (227, 'JX60156', 'scrypt:32768:8:1$OKnSiVLgSMdz9N3a$095b1fe4f2326ac3efe6bc8faa50a318b325ca17dc2f840128f8cb81bec9fbe4e182f01d47d04d953ea11b88cc26b6495d7facedf4b9d5a326d783b8b117d1d9', '张铭哲', 'business', 9507, 1095, 305, true, true, '2026-07-13 06:44:21.13462', '2026-07-13 06:44:21.134624');
INSERT INTO public.users VALUES (228, 'RS9011', 'scrypt:32768:8:1$bhChUqehfnRRA5OK$3d16616f1476e44738a466185e6fbf2301a191513674ac381d3756a9dc65a49c416ae658c0301e8df30b00c00bb189f002d4f4b2b44497a482e20bcde14543ad', '郭耀', 'business', 9509, 1082, 122, true, true, '2026-07-13 06:44:21.227596', '2026-07-13 06:44:21.227601');
INSERT INTO public.users VALUES (229, 'JS90279', 'scrypt:32768:8:1$BvR5Wnlf38wPGKzG$80492cff876fe8006c64931e0e8ca24a88c9bbd2e4701e343128f3ca6903629115bc5f3d19ea25e97e24e33dada959e5071e276a00b662e7123b6be79e02daea', '沈伟强', 'business', 9510, 1058, 254, true, true, '2026-07-13 06:44:21.321376', '2026-07-13 06:44:21.321381');
INSERT INTO public.users VALUES (230, 'JX60159', 'scrypt:32768:8:1$8jtv0YKwazFcZqJe$7b297e0636fed9fab6d1b4f0f2b89cc16d695212471ccb298eea543a3d34956fa2a2c2e1c48dda0cd93545f3563ede16c9416880cf6f4ab9bb3231b2d1906fbd', '吕傲飞', 'business', 9512, 1098, 307, true, true, '2026-07-13 06:44:21.416859', '2026-07-13 06:44:21.416864');
INSERT INTO public.users VALUES (231, 'JX60161', 'scrypt:32768:8:1$ABtoBg5oKwRefHNt$ed49a6a8cc947578d1a573bd51291e1a3c5e25c077d4fd25d766b99629037ba69487025c0b4f6581a8a274b0949d52b2697758d2ff899fab47503d19c96bd073', '魏良海', 'business', 9516, 1095, 305, true, true, '2026-07-13 06:44:21.513606', '2026-07-13 06:44:21.513611');
INSERT INTO public.users VALUES (232, 'JX60162', 'scrypt:32768:8:1$Giz9HQBmTJWvEXja$eb8d8c5191e00393c847c57ddbbe4a21cd12bbb6de01968c9043c83bdd6c3c7d77594fb2115620bb33f980f169364f6506002c185f7c5adcffb8cf523f2e5731', '卫国锋', 'business', 9519, 1172, 263, true, true, '2026-07-13 06:44:21.609235', '2026-07-13 06:44:21.60924');
INSERT INTO public.users VALUES (233, 'JX60163', 'scrypt:32768:8:1$jIkTTlpymZ3hAbQU$14a0dc16e24b80e556f54602358f7e20b8da41146f7652caee66dc4c346d11c0a88364c45b0df0657aebd8d1c9588f489fd944dc5a75f808a9b078ab304a5119', '孙安心', 'business', 9520, 1095, 305, true, true, '2026-07-13 06:44:21.7034', '2026-07-13 06:44:21.703405');
INSERT INTO public.users VALUES (234, 'JX60164', 'scrypt:32768:8:1$HTVyudJ7p3aohWRK$71b4c4dd1b83d0f522059b4c9f8422dbd428e5c14ab45fd2feb30085a28c6d4053a8185dd0d339883dcb9264b789bac82967e747f705ff3a508114493a69aecc', '廉帅达', 'business', 9521, 1098, 305, true, true, '2026-07-13 06:44:21.795293', '2026-07-13 06:44:21.795297');
INSERT INTO public.users VALUES (235, 'JX60167', 'scrypt:32768:8:1$rfVEltG79Bocz7Q6$769affa6cb6b523822c3b2049abffeb0f7fd6debe8dc662887c6e5e6cb1be42ce686085f0eef1b79f1a052764f393f72f4fa433257641e97ff728dd562e4c981', '李鹏', 'business', 9528, 1095, 305, true, true, '2026-07-13 06:44:21.887243', '2026-07-13 06:44:21.887247');
INSERT INTO public.users VALUES (236, 'JX60168', 'scrypt:32768:8:1$wWZBdkRe5qVs3nCc$e434f79225cf5ef7c2b482fe10e44ec8990596ec51be8713e3b56e855d9b8cd347eeff584c685edb38c643376a4700870c77a11f425418cfb3b1228b7ff8f115', '陈洋', 'business', 9529, 1098, 307, true, true, '2026-07-13 06:44:21.978749', '2026-07-13 06:44:21.978754');
INSERT INTO public.users VALUES (237, 'JS902333', 'scrypt:32768:8:1$LLZFZALOOzobKNF2$2b11b27f897082751a0540e4cc6e50d0c41200495df1a5e4809f35c0275cc457016e9869bb048ad5ce4b1255a5cabfa2a870ae841491703d128aa57043898be0', '丁宇星', 'business', 9530, 1055, 254, true, true, '2026-07-13 06:44:22.070029', '2026-07-13 06:44:22.070035');
INSERT INTO public.users VALUES (238, 'JS902334', 'scrypt:32768:8:1$Q1ubdBYlLSfPdG2w$3048126ee6a17d5b7c43e19752ef1eef609a76cab9d56f1f7b654a75456fe7ef436756b56766a27afd0f2e52d146a568d1b166d33a63005f9a7f0f10a6a09b64', '何路阳', 'business', 9531, 1055, 254, true, true, '2026-07-13 06:44:22.163887', '2026-07-13 06:44:22.163892');
INSERT INTO public.users VALUES (239, 'JS90283', 'scrypt:32768:8:1$HhacTu8wdziSDv5Y$e974c9c2486643590ba9417bc9cdecb31ad20a588d3db3ebb685d4460d5599b8c4cab46dd44192449e637c156db2d0b4787a9bc5016b66cb27c75d5dc26b2233', '高晓丹', 'business', 9532, 1114, 85, true, true, '2026-07-13 06:44:22.254901', '2026-07-13 06:44:22.254906');
INSERT INTO public.users VALUES (240, 'JS902335', 'scrypt:32768:8:1$VEwVcNVfGHKn3TNo$24084a07632886494a3045642b2752abf0340703beb72b89d458fde66667f82d79109895c14c39a78badf735b5009da691693c4f8123c662528ad7921808388b', '杨凯', 'business', 9533, 1159, 313, true, true, '2026-07-13 06:44:22.350627', '2026-07-13 06:44:22.350632');
INSERT INTO public.users VALUES (241, 'JX60169', 'scrypt:32768:8:1$L1Z7zcaMiLXDgF0F$c9565ba94e69f56ddf6a678424b56a4fcee3708aacb47a6ed76413b37464468ddce8e272c575ced074fea3e96ad015e0dc339a954f262cf5abacca14a202d22d', '周海', 'business', 9534, 1095, 305, true, true, '2026-07-13 06:44:22.442417', '2026-07-13 06:44:22.442423');
INSERT INTO public.users VALUES (242, 'JS902336', 'scrypt:32768:8:1$eSARrRjbGmxRTduD$7c7cfb2f03c0bc23342ee0023d247773785762c3234930cebc56ba867254788e383199838868b84677790811ba8a88ea42e20eee84f616ab267f2fe0c8d5bb35', '周祥', 'business', 9535, 1159, 313, true, true, '2026-07-13 06:44:22.536409', '2026-07-13 06:44:22.536414');
INSERT INTO public.users VALUES (243, 'JX60170', 'scrypt:32768:8:1$qLYjMh92jaIYNzpX$d3b9c661f95d6ea1e14362affc64a226021b6e561cec733ffd162e9d12df79b02eaa641478bc51038cac52f84d53ae8c4162a82a8d7f39ba98c88003c47b205c', '宗燚超', 'business', 9536, 1098, 307, true, true, '2026-07-13 06:44:22.629578', '2026-07-13 06:44:22.629583');
INSERT INTO public.users VALUES (244, 'JX60171', 'scrypt:32768:8:1$3FHMmImFfgBoHGwQ$7f1755e7189272100533011337dba42299e8e10eba6c920008e8bbb5ea2b2747e7dff5eccedaf4a397a10a1ffb579e7fb0accabc56861a0bdc7cb9f478b01d60', '杜猛旭', 'business', 9537, 1095, 305, true, true, '2026-07-13 06:44:22.722589', '2026-07-13 06:44:22.722593');
INSERT INTO public.users VALUES (245, 'JX60172', 'scrypt:32768:8:1$YNF9fXkakmpGFnZT$5417aed961db8181c35d4b6aadb1788fbc4fa4bd5cc2907dcf36450b7012aad2760c2f7129bf06c20c2fd75a7779c2e2bee51c14a7e42651149a3ac1406e9110', '王强', 'business', 9538, 1095, 305, true, true, '2026-07-13 06:44:22.813896', '2026-07-13 06:44:22.813902');
INSERT INTO public.users VALUES (246, 'JS90284', 'scrypt:32768:8:1$jo3VjbpMUKvO9z0A$910f8d4a457b9f11939c9a5f7cfb610dffabb9c8b44c093b6f2ce5bac2cfa47d736cd44711466bec85bacf8647558370c5948c69af640f950ad8568c92f0f63f', '朱丽娜', 'business', 9539, 1113, 85, true, true, '2026-07-13 06:44:22.9076', '2026-07-13 06:44:22.907604');
INSERT INTO public.users VALUES (247, 'JX600301', 'scrypt:32768:8:1$n7Ds9tdZmLGyS8K6$3571594c73f1e1bcd93e998a07665ba1d9cae8c09a55b6fd232286d749afd0eb9e4da86250ffba8b5c4e0cca3298fccb645c306b9501528bdd9a97d0f0cff27b', '胡玉全', 'business', 9540, 1149, 315, true, true, '2026-07-13 06:44:22.999845', '2026-07-13 06:44:22.99985');
INSERT INTO public.users VALUES (248, 'JX600304', 'scrypt:32768:8:1$XPZNBAZimFfKlfLV$921b1f9ba4b3baeb4532b80ee7864d678bbfe92679a15aa6f7449b30cc9fa191c844aac0e37499cbd1d0ee2036011de34e3a5bce800245c10fff626547d495ad', '李富营', 'business', 9541, 1149, 315, true, true, '2026-07-13 06:44:23.092511', '2026-07-13 06:44:23.092517');
INSERT INTO public.users VALUES (249, 'JX600306', 'scrypt:32768:8:1$aFaXqdkwfnEbsAOp$8e13bfc82095553aff3b155bef78b3bd23c4fdc7c4f4613b1b8f8664fc98731d2dc6c5edc2bc590048b799f7528af02c41cf5151155b3b9930b542e31f62b30f', '仲磊', 'business', 9542, 1149, 315, true, true, '2026-07-13 06:44:23.184514', '2026-07-13 06:44:23.184519');
INSERT INTO public.users VALUES (250, 'JX600307', 'scrypt:32768:8:1$aiZ1V1rh2yWqxcci$875a1848b3f10946119ea36f227bbdb8f96746c69934149b79b4ad724cd094a74f20e79057e85e6b18236530137b8626e3ec723e3d9fe2c1ba4312cd195b5b85', '谭文举', 'business', 9543, 1149, 315, true, true, '2026-07-13 06:44:23.27664', '2026-07-13 06:44:23.276645');
INSERT INTO public.users VALUES (251, 'JX600308', 'scrypt:32768:8:1$zgPtDqGElFic1eKK$f652b0c750cd672d14dd90a18b7e0c631d1b1c83b7cad574af01b7244ca7bdb1f259a0dd5aaec6d346bcefd7100847ede20806de3ef5de8ad708fe569f5b040e', '胡强', 'business', 9544, 1149, 315, true, true, '2026-07-13 06:44:23.370221', '2026-07-13 06:44:23.370227');
INSERT INTO public.users VALUES (252, 'JX600313', 'scrypt:32768:8:1$8mfXZtyzumyKmUyO$f1ef7f9bbaee1dee936057ea2f48ff02e4e82d4a3233b0ed2212d60a2e7e45a8b411361bbe4147854062fe22dc5ac7cc1e5a58ed0f215a9cf654e316a0ef72f0', '娄菩菩', 'business', 9545, 1149, 315, true, true, '2026-07-13 06:44:23.463003', '2026-07-13 06:44:23.463007');
INSERT INTO public.users VALUES (253, 'JX600328', 'scrypt:32768:8:1$nMbIxudNTrZoVZQ2$a40d85f6aed73bfe1c65f412e1c5c8bcf3e763815c9146c7a35193bb766c6ea8fef2337513f1f59901356ff84c8b0e40244de447a0edc1b47adce1de0a597294', '朱昊宇', 'business', 9546, 1096, 278, true, true, '2026-07-13 06:44:23.557027', '2026-07-13 06:44:23.557031');
INSERT INTO public.users VALUES (254, 'JX600330', 'scrypt:32768:8:1$7udE9g9E1K2Oe36d$3e327f911b63b6e5ecb7e1a2899b190e46dc17d25e3464b58214d5b9e5061bb81c44a5db48d413df7f84e9b2617057e62b60c70a69ba5140e458a9b112d33691', '王伟杰', 'business', 9547, 1096, 278, true, true, '2026-07-13 06:44:23.649252', '2026-07-13 06:44:23.649257');
INSERT INTO public.users VALUES (255, 'JX600332', 'scrypt:32768:8:1$buaPyFqgUzKHQC2Q$e986eff2fcf6a231c3c446f46915592bdd65930d405f6ab11448283713a50e62b9b108361bcb41186341335ae369b66651d5a5a340f1ad6d042a55d37a8c1ea3', '邓加勋', 'business', 9549, 1171, 314, true, true, '2026-07-13 06:44:23.742186', '2026-07-13 06:44:23.742192');
INSERT INTO public.users VALUES (256, 'JX600333', 'scrypt:32768:8:1$HaeQW9MkUpZ7vF1n$308035fb970033580bc0bcdab3ea73063e09222c3f08184874687f7fd88facf377e7ef0b712d6ae2712b79d895ae7d7584992b3d668492b6192fa16edf95e335', '徐召远', 'business', 9550, 1096, 278, true, true, '2026-07-13 06:44:23.832591', '2026-07-13 06:44:23.832596');
INSERT INTO public.users VALUES (257, 'JX600335', 'scrypt:32768:8:1$dK2Ew9J4FhjMjR16$5cf6e493172a36eba4f14f2636a8f5c767ad4c812c90df70ca50cbcb264e735e0012cd8509d60f66fe5616b0227fcad8ed4f59084ac45636f18616f609d29b3d', '邓帅友', 'business', 9552, 1096, 278, true, true, '2026-07-13 06:44:23.925828', '2026-07-13 06:44:23.925832');
INSERT INTO public.users VALUES (258, 'JX600336', 'scrypt:32768:8:1$lgZ4XJa4f8v0rZJu$086693096ddec751016c958a70352222e3ea6b25b80c44b75b3ee527ec96df1566082fa7204bcd3e6f7b5aeb4e9a66f68d437d8c00b02fe924cc2f1ec44d5348', '金多标', 'business', 9553, 1095, 280, true, true, '2026-07-13 06:44:24.016854', '2026-07-13 06:44:24.016858');
INSERT INTO public.users VALUES (259, 'JX600337', 'scrypt:32768:8:1$dFBCAqg8cpoyxWzZ$44b67f7fc47e95be463b99686b192b2621c3b98567239dde9dc8ecd9f76150a76be9e2a1c821ed000f59deb92470032983b49c05c5a0592e9dfd9f96992d9191', '吴鹏', 'business', 9554, 1095, 280, true, true, '2026-07-13 06:44:24.109593', '2026-07-13 06:44:24.109598');
INSERT INTO public.users VALUES (260, 'JX600338', 'scrypt:32768:8:1$RBOD7D6bO2nLj4D4$6b612008df8bab828f77ed7fbf832071187657ba6bab9421f85e515afe55baa50ac21a728e015681ebfff4f86370a1764561c40bcb69e76a3da2a7e4e03acf27', '李鹏博', 'business', 9555, 1095, 280, true, true, '2026-07-13 06:44:24.2001', '2026-07-13 06:44:24.200106');
INSERT INTO public.users VALUES (261, 'JX600339', 'scrypt:32768:8:1$9zdNh7tkRqDA8hVR$81509ed19820fc86608e32d8838f5a3056faafbefe28607de76eee055746be0232f6e32a76069a027d16c21fba88447e7b13d882657358a256f2e85c68c72483', '孙明辉', 'business', 9556, 1095, 280, true, true, '2026-07-13 06:44:24.29299', '2026-07-13 06:44:24.292995');
INSERT INTO public.users VALUES (262, 'JX600340', 'scrypt:32768:8:1$TUPWMq9BIhucKW1N$e4db38e3bfabfcf127bfcb61bf422ff0aae496f005c191cdf96f6c942521001c6b2a1d92a153b4bfd3ca3fb461d95b9e909558029c9ecd94257ae5b36c90ec1a', '张浩', 'business', 9557, 1095, 280, true, true, '2026-07-13 06:44:24.387842', '2026-07-13 06:44:24.387848');
INSERT INTO public.users VALUES (263, 'JX600341', 'scrypt:32768:8:1$B1gZdcdpBaSjcShV$a70d523e4546d3a82aaa953874e735079e0bec3478a15dc7f65c809aea85e78f0b597c7a063959e111793b349e765e256f8c7258228220c394b48f5b839c4dc7', '刘明厅', 'business', 9558, 1095, 280, true, true, '2026-07-13 06:44:24.484587', '2026-07-13 06:44:24.484592');
INSERT INTO public.users VALUES (264, 'JX600342', 'scrypt:32768:8:1$RdMKoNYAbCuC5gcH$8d6e2145d2472c5f38fd253bd6fb7af3672b63a66807bec3acbe14baa34d4a047f0a9a92f1a8244b8e83061b96f36782dc4286662eaa0acf941a13332c52ba63', '陈想', 'business', 9559, 1095, 280, true, true, '2026-07-13 06:44:24.581631', '2026-07-13 06:44:24.581636');
INSERT INTO public.users VALUES (265, 'JX600343', 'scrypt:32768:8:1$bewyFB78b1rquAZX$ddbc87e9b74ccebe91ff2ab38980a0813449dfad58d019c3836334d633d8c38c5143691ae39731bc3ed20b3ddfd81ba588e62e15dcf20e55be5d049970b8ae1a', '荆慕轩', 'business', 9560, 1095, 280, true, true, '2026-07-13 06:44:24.679108', '2026-07-13 06:44:24.679115');
INSERT INTO public.users VALUES (266, 'JX600344', 'scrypt:32768:8:1$GOlxbu1t0h0mBO7Z$5021f60d5c9f76d4c8dd1023a78f1f78cf19b8be3b1d532c5faa367b57765869b4c35f7e7e2f47edd9490d48518ce16517bf3b33768739cb0eefc94821a329c9', '梁北', 'business', 9561, 1095, 280, true, true, '2026-07-13 06:44:24.778691', '2026-07-13 06:44:24.778697');
INSERT INTO public.users VALUES (267, 'JX600345', 'scrypt:32768:8:1$YJZ7wVEPcwzDyoAF$60ab53b789f599f669323530acce443e0a46b5037b6c5f438e2cddb8184342d3b01a4caeb7e14b2cc891c88ccf4073b1e5e8819f55976b79fd986890356d41d2', '生志阳', 'business', 9562, 1149, 315, true, true, '2026-07-13 06:44:24.876716', '2026-07-13 06:44:24.876721');
INSERT INTO public.users VALUES (268, 'JX600347', 'scrypt:32768:8:1$wMSXZIV5aMnxPOVs$281b50a3c4314ca7ce6ca038f780e2a19b369c56fddd37e13a20deaf56906367cab84eec54382032e6ba69caf17feef91fcf665824b5cf19b7eae45c8c3200f6', '陈谢鹏', 'business', 9564, 1095, 280, true, true, '2026-07-13 06:44:24.977828', '2026-07-13 06:44:24.977834');
INSERT INTO public.users VALUES (269, 'JX600348', 'scrypt:32768:8:1$wyKKFDSkFAyvGNGm$d4f6dab24bb4cd7b06621ff3d6a1b97b3902d271707a985f29d0b1925c9af37e24f0cd2d36f0df0fdb21700eac01f251de9fa8d9ecc7a6dae0fed404e9c1a2d5', '侯记森', 'business', 9565, 1149, 315, true, true, '2026-07-13 06:44:25.079207', '2026-07-13 06:44:25.079213');
INSERT INTO public.users VALUES (270, 'JX600349', 'scrypt:32768:8:1$D08ry6tXR2oE1vDI$274959df5312e2a1c619c4570f29a3050827ebbf55079ca31b143a1c21042abfd9c98d3a243029fa022b1113577ac0aa11134f930edf3797eb89a109069b157c', '张晋泽', 'business', 9566, 1095, 280, true, true, '2026-07-13 06:44:25.179689', '2026-07-13 06:44:25.179694');
INSERT INTO public.users VALUES (271, 'JX600350', 'scrypt:32768:8:1$36ikPhKeRo7ncCk2$cc5f43d415ddf9af6f0ae59309e3bcfc92198953cab625f2371434bbd6fbb0ec7ff8fd9fa1567f9109a71bcd027461c9f28f9fd546303e2cbb1d354476b2aa9b', '薛永兴', 'business', 9567, 1149, 315, true, true, '2026-07-13 06:44:25.278423', '2026-07-13 06:44:25.278429');
INSERT INTO public.users VALUES (272, 'JX600351', 'scrypt:32768:8:1$AhndgSxed6WMMKFV$876d90882a99301ca32739b8acc87bb0abdb58fae6c1ce85050354a034470b433e98037289f59463366645bbb872b49b0f9bfadf73518a100e0cdc327571eefb', '郭德宝', 'business', 9568, 1095, 280, true, true, '2026-07-13 06:44:25.379971', '2026-07-13 06:44:25.379977');
INSERT INTO public.users VALUES (273, 'JX600354', 'scrypt:32768:8:1$0xhd4wWVcZY3qFBw$1f0eef7bf15ea8356e64010e88a92ec7213940136dc683d899a29aad6f1cb692c1e86fbf23b0c0148d6e9ef9a9684c09705af88aad2a50fd3659a2280c27d8fa', '李永亮', 'business', 9571, 1149, 315, true, true, '2026-07-13 06:44:25.480855', '2026-07-13 06:44:25.480861');
INSERT INTO public.users VALUES (274, 'JX600355', 'scrypt:32768:8:1$vHL6WHAaw1uwPeip$922823c5ae01db5c33f1a2e37ebeea839a37eee28d43fe3a669d3c8390c05e20d647a1bad9d569ab496c0404f4e42c6ea797956675b744d546a696004a716d22', '李鹏', 'business', 9572, 1149, 315, true, true, '2026-07-13 06:44:25.580252', '2026-07-13 06:44:25.580257');
INSERT INTO public.users VALUES (275, 'JX600356', 'scrypt:32768:8:1$rhW9vvZpWsYvChtk$2667d2817b03074b2c5f8e4e39d0a54dc9f8a543f6890fa363c452d1187e2452acf22ffe3b3fa449d8741a04a171f18d6262846fc5dce0816ccea14fa6120ef0', '张帅', 'business', 9573, 1149, 315, true, true, '2026-07-13 06:44:25.680012', '2026-07-13 06:44:25.680018');
INSERT INTO public.users VALUES (276, 'JX600357', 'scrypt:32768:8:1$voIRupe7qCqW0x73$b18014bac7cfd6abdec7d24f3e1b56a523ca2a524af1a3483a80affa6881777247c47b120baee9d2d5fc3cb7e88537f16d8594f9f146dce9511a7253a01ba94e', '王硕', 'business', 9574, 1149, 315, true, true, '2026-07-13 06:44:25.778114', '2026-07-13 06:44:25.778119');
INSERT INTO public.users VALUES (277, 'JX600358', 'scrypt:32768:8:1$23vWjKPYYGvxaqzy$1533921d25debde9c2df1ced319047526ba63ab3c68a74d67d4cb14b9076937901cf17911ab0194836f8128ac3c03915a5f634ba5d0cf2ccc2e18459d8e068e2', '冯宁', 'business', 9575, 1149, 315, true, true, '2026-07-13 06:44:25.874252', '2026-07-13 06:44:25.874257');
INSERT INTO public.users VALUES (278, 'JX600359', 'scrypt:32768:8:1$aNH3i7itnZ2tAmKY$bcb75f459e51e724122a5174184692d310f3f7a81dce863d2b68402fb724f97be72e7b5cfe552a926ec3fd7e333dee60fd7fe6e9a0c21739321d18a0a0c3d6bf', '杨存', 'business', 9576, 1149, 315, true, true, '2026-07-13 06:44:25.973659', '2026-07-13 06:44:25.973664');
INSERT INTO public.users VALUES (279, 'JX600360', 'scrypt:32768:8:1$R1N5G8k9QEsJmA06$f8da02d9295c6b40d34ffe7cfcb670da20a12022909ece29dbd3a904956c544cdabfe7c3fc476bfb3dbef9d2483385028a0c6c5bd2d4d1799842abe8f203ac7c', '周想文', 'business', 9577, 1149, 315, true, true, '2026-07-13 06:44:26.071342', '2026-07-13 06:44:26.071347');
INSERT INTO public.users VALUES (280, 'JX600361', 'scrypt:32768:8:1$NuY6MrQTIAgg1OWg$30f67572358c6d7499f379afb7c6fea2ca9175269cd6599a1d20b37ea37ac7e62189a14d92237434ea7ec2a2af29e9911866be47742dd81be2ba543eda0c33e3', '李克聪', 'business', 9578, 1149, 315, true, true, '2026-07-13 06:44:26.168604', '2026-07-13 06:44:26.16861');
INSERT INTO public.users VALUES (281, 'JX600362', 'scrypt:32768:8:1$eK4Giw5VQEN254Oj$d3e422a6cadd9b221b7f065a891f61776c7da936a1dd180c314a7b7699b84f3363afa2dd8e85f58fff835b48360bc24644c2b5f962ccd0a5afdf966f87c6fed4', '徐玉峰', 'business', 9579, 1149, 315, true, true, '2026-07-13 06:44:26.267201', '2026-07-13 06:44:26.267207');
INSERT INTO public.users VALUES (282, 'JX600363', 'scrypt:32768:8:1$iGS8lVSiT0dkM2Cx$2a1f30d4c96297ccd90d18b85c5ae652c2a803fd61403e4211dda787150cf339ac1799e1ff1a2ec72b8d47ba41d7c80dcb83d3dde6ebe08d6a526e789a5e0d2a', '徐开放', 'business', 9580, 1149, 315, true, true, '2026-07-13 06:44:26.365441', '2026-07-13 06:44:26.365446');
INSERT INTO public.users VALUES (283, 'JX600364', 'scrypt:32768:8:1$n0sSSJ6d5u1HsFQZ$7e8ed4e4201d520ca980db68b70391fe97771ed13968161c26d4100c26d91ab5c70183cea003e18fd66cfdc592fc9809dde5fd130da957785573c688686c2a30', '王远中', 'business', 9581, 1149, 315, true, true, '2026-07-13 06:44:26.457762', '2026-07-13 06:44:26.457766');
INSERT INTO public.users VALUES (284, 'JX600365', 'scrypt:32768:8:1$Re1fHe3IOJ44LTuT$526830bc161b34b5f7ae659808f607c6fcc50658e10d034ec1be2b9f227be5e3b99abbaa44f580055dc4038310cb9a6fa5853e6904feca5f64eec3b0e7fb7aeb', '肖宇', 'business', 9582, 1149, 315, true, true, '2026-07-13 06:44:26.550207', '2026-07-13 06:44:26.550211');
INSERT INTO public.users VALUES (285, 'JX600366', 'scrypt:32768:8:1$Meto57s86WrtyHDX$c6dda3a03dd0ea4e8ea16454b7448977456826ab2566e441f61acb799093f560cfaac95e54af9c54114d45aa0dda7bd226d946311b13f3f0ae8d8a3d2b9f6f2c', '田鑫洋', 'business', 9583, 1095, 280, true, true, '2026-07-13 06:44:26.640549', '2026-07-13 06:44:26.640554');


ALTER TABLE public.users ENABLE TRIGGER ALL;

--
-- Data for Name: ai_conversations; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.ai_conversations DISABLE TRIGGER ALL;

INSERT INTO public.ai_conversations VALUES ('cf7ca637-e89a-402c-9c3a-4a67670529a6', 1, '新对话', '2026-07-13 07:24:47.857509', NULL);


ALTER TABLE public.ai_conversations ENABLE TRIGGER ALL;

--
-- Data for Name: ai_knowledge_base; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.ai_knowledge_base DISABLE TRIGGER ALL;



ALTER TABLE public.ai_knowledge_base ENABLE TRIGGER ALL;

--
-- Data for Name: ai_messages; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.ai_messages DISABLE TRIGGER ALL;



ALTER TABLE public.ai_messages ENABLE TRIGGER ALL;

--
-- Data for Name: quotations; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.quotations DISABLE TRIGGER ALL;

INSERT INTO public.quotations VALUES (1, '自动折盒机', 'single', 'CS26005', 'draft', 38, 1, 0.13, 0.1, 'CNY', 1, NULL, '2026-07-13 07:40:34.053933', '2026-07-13 07:40:34.053939', '{"large": 1, "standard": 1, "other": 1}');


ALTER TABLE public.quotations ENABLE TRIGGER ALL;

--
-- Data for Name: archive_approvals; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.archive_approvals DISABLE TRIGGER ALL;



ALTER TABLE public.archive_approvals ENABLE TRIGGER ALL;

--
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.modules DISABLE TRIGGER ALL;

INSERT INTO public.modules VALUES (1, 1, '机构01', '01', NULL, '', '2026-07-13 07:44:11.838511', 'mechanical');
INSERT INTO public.modules VALUES (2, 1, '机构02', '02', NULL, '', '2026-07-13 07:44:28.567322', 'mechanical');
INSERT INTO public.modules VALUES (3, 1, '电气01', 'ds01', NULL, '', '2026-07-13 07:44:40.06725', 'electrical');
INSERT INTO public.modules VALUES (4, 1, '其他', 'other', NULL, '', '2026-07-13 07:44:52.59118', 'other');


ALTER TABLE public.modules ENABLE TRIGGER ALL;

--
-- Data for Name: change_requests; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.change_requests DISABLE TRIGGER ALL;



ALTER TABLE public.change_requests ENABLE TRIGGER ALL;

--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.organizations DISABLE TRIGGER ALL;

INSERT INTO public.organizations VALUES (24, '苏州富强科技有限公司', 'FQKJ-0001', NULL, NULL, true, true, '2026-07-13 06:43:58.912195', '2026-07-13 06:43:58.9122');
INSERT INTO public.organizations VALUES (25, '苏州富强加能精机有限公司', 'FQJN-0002', NULL, NULL, true, true, '2026-07-13 06:43:58.91389', '2026-07-13 06:43:58.913894');
INSERT INTO public.organizations VALUES (26, '苏州富强加能精机有限公司', 'FQJN-0003', NULL, NULL, true, true, '2026-07-13 06:43:58.915056', '2026-07-13 06:43:58.91506');
INSERT INTO public.organizations VALUES (27, '苏州捷胜科技有限公司', 'JSKJ-0004', NULL, NULL, true, true, '2026-07-13 06:43:58.916107', '2026-07-13 06:43:58.91611');
INSERT INTO public.organizations VALUES (28, '常熟市巨兴机械有限公司', 'JXKJ-0005', NULL, NULL, true, true, '2026-07-13 06:43:58.917124', '2026-07-13 06:43:58.917146');


ALTER TABLE public.organizations ENABLE TRIGGER ALL;

--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.employees DISABLE TRIGGER ALL;

INSERT INTO public.employees VALUES (195, NULL, 'RS100', '李洋', 'jeffery.li', '李洋', 1, 'jeffery.li@rs-machining.com', '13776079254', NULL, 1141, 24, 99, true, true, '2026-07-13 06:43:59.416763', '2026-07-13 06:43:59.416766');
INSERT INTO public.employees VALUES (264, NULL, 'RS065', '胡国进', 'bruce.Hu', '胡国进', 1, 'bruce.hu@rs-machining.com', '15995436620', NULL, 1141, 24, 100, true, true, '2026-07-13 06:43:59.419941', '2026-07-13 06:43:59.419944');
INSERT INTO public.employees VALUES (378, NULL, 'RS217', '李吉民', 'sirius.li', '李吉民', 1, 'sirius.li@rs-machining.com', '15995421573', NULL, 1072, 24, 103, true, true, '2026-07-13 06:43:59.422108', '2026-07-13 06:43:59.422111');
INSERT INTO public.employees VALUES (425, NULL, 'RS741', '魏焕友', 'huanyou.wei', '魏焕友', 1, 'huanyou.wei@rs-machining.com', '18645052007', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.424061', '2026-07-13 06:43:59.424064');
INSERT INTO public.employees VALUES (427, NULL, 'RS598', '李鹏', 'peng.li', '李鹏', 1, 'peng.li@rs-machining.com', '13616279619', NULL, 1120, 24, 100, true, true, '2026-07-13 06:43:59.425987', '2026-07-13 06:43:59.425991');
INSERT INTO public.employees VALUES (519, NULL, 'RS768', '吴军军', 'simon.wu', '吴军军', 1, 'simon.wu@rs-machining.com', '15050448863', NULL, 1081, 24, 100, true, true, '2026-07-13 06:43:59.427964', '2026-07-13 06:43:59.427967');
INSERT INTO public.employees VALUES (563, NULL, 'RS505', '谢国建', 'guojian.xie', '谢国建', 1, 'guojian.xie@rs.local', '15995705023', NULL, 1119, 24, 254, true, true, '2026-07-13 06:43:59.429986', '2026-07-13 06:43:59.42999');
INSERT INTO public.employees VALUES (598, NULL, 'RS936', '王学松', 'xuesong.wang', '王学松', 1, 'xuesong.wang@rs-machining.com', '18119502357', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.43189', '2026-07-13 06:43:59.431894');
INSERT INTO public.employees VALUES (624, NULL, 'RS1350', '苏建庭', 'jianting.su', '苏建庭', 1, 'jt.su@rs-machining.com', '18549816206', NULL, 1119, 24, 254, true, true, '2026-07-13 06:43:59.43381', '2026-07-13 06:43:59.433814');
INSERT INTO public.employees VALUES (637, NULL, 'RS827', '胡锴莉', 'kaili.hu', '胡锴莉', 1, 'katana.hu@rs-machining.com', '13187379171', NULL, 1119, 24, 100, true, true, '2026-07-13 06:43:59.435606', '2026-07-13 06:43:59.43561');
INSERT INTO public.employees VALUES (666, NULL, 'RS1649', '柳正荣', 'zhengrong.liu', '柳正荣', 1, 'zhengrong.liu@rs-machining.com', '18205055812', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.437336', '2026-07-13 06:43:59.43734');
INSERT INTO public.employees VALUES (731, NULL, 'RS1799', '王玉明', 'yuming.wang', '王玉明', 1, 'yuming.wang@rs-machining.com', '13686857761', NULL, 1081, 24, 148, true, true, '2026-07-13 06:43:59.439054', '2026-07-13 06:43:59.439057');
INSERT INTO public.employees VALUES (781, NULL, 'RS1897', '王大磊', 'alex.wang', '王大磊', 1, 'alex.wang@rs-machining.com', '13771671419', NULL, 1077, 24, 99, true, true, '2026-07-13 06:43:59.440803', '2026-07-13 06:43:59.440806');
INSERT INTO public.employees VALUES (1262, NULL, 'RS3602', '闵国军', 'guojun.min', '闵国军', 1, 'guojun.min@rs-machining.com', '18068442205', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.442561', '2026-07-13 06:43:59.442564');
INSERT INTO public.employees VALUES (1301, NULL, 'RS3646', '卢云峰', NULL, '卢云峰', 1, NULL, '18334770179', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.444279', '2026-07-13 06:43:59.444283');
INSERT INTO public.employees VALUES (2183, NULL, 'RS4560', '刘加庆', 'liujiaqing', '刘加庆', 1, 'Andy.Liu2@rs-machining.com', '17625342998', NULL, 1120, 24, 148, true, true, '2026-07-13 06:43:59.445986', '2026-07-13 06:43:59.445989');
INSERT INTO public.employees VALUES (3102, NULL, 'RS5477', '王腾飞', 'wangtengfei', '王腾飞', 1, NULL, '18334771492', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.447766', '2026-07-13 06:43:59.447769');
INSERT INTO public.employees VALUES (3110, NULL, 'RS5500', '严雅萍', 'yanyaping', '严雅萍', NULL, NULL, '15995790242', NULL, 1072, 24, 264, true, true, '2026-07-13 06:43:59.44955', '2026-07-13 06:43:59.449553');
INSERT INTO public.employees VALUES (3129, NULL, 'RS5518', '谢献民', 'xiexianmin', '谢献民', 1, 'xianmin.xie@rs-machining.com', '13207235109', NULL, 1076, 24, 99, true, true, '2026-07-13 06:43:59.451527', '2026-07-13 06:43:59.451532');
INSERT INTO public.employees VALUES (3393, NULL, 'RS5786', '王理想', 'wanglixiang', '王理想', 1, NULL, '18812612958', NULL, 1141, 24, 141, true, true, '2026-07-13 06:43:59.453527', '2026-07-13 06:43:59.453532');
INSERT INTO public.employees VALUES (3489, NULL, 'RS5880', '吴燕娟', 'wuyanjuan', '吴燕娟', NULL, 'Yanjuan.wu@rs-machining.com', '13776116323', NULL, 1110, 24, 100, true, true, '2026-07-13 06:43:59.455561', '2026-07-13 06:43:59.455565');
INSERT INTO public.employees VALUES (3553, NULL, 'RS5944', '杜海峰', 'duhaifeng', '杜海峰', 1, NULL, '15162490140', NULL, 1081, 24, 254, true, true, '2026-07-13 06:43:59.457539', '2026-07-13 06:43:59.457542');
INSERT INTO public.employees VALUES (4047, NULL, 'RS6258', '胡世杰', 'hushijie', '胡世杰', 1, 'shijie.hu@rs-machining.com', '18039596952', NULL, 1141, 24, 92, true, true, '2026-07-13 06:43:59.461066', '2026-07-13 06:43:59.461077');
INSERT INTO public.employees VALUES (4681, NULL, 'RS7063', '陶硕', 'taoshuo', '陶硕', 1, NULL, '18860460750', NULL, 1109, 24, 254, true, true, '2026-07-13 06:43:59.46332', '2026-07-13 06:43:59.463323');
INSERT INTO public.employees VALUES (4788, NULL, 'RS7198', '吴磊', 'wulei', '吴磊', 1, 'lei.wu@rs-machining.com', '13929415797', NULL, 1141, 24, 254, true, true, '2026-07-13 06:43:59.465122', '2026-07-13 06:43:59.465147');
INSERT INTO public.employees VALUES (4809, NULL, 'RS7219', '宣亏堂', 'xuankuitang', '宣亏堂', 1, NULL, '15738616052', NULL, 1140, 24, 254, true, true, '2026-07-13 06:43:59.466895', '2026-07-13 06:43:59.466898');
INSERT INTO public.employees VALUES (4872, NULL, 'RS7344', '储怀和', 'chuhuaihe', '储怀和', 1, NULL, '13399546016', NULL, 1141, 24, 141, true, true, '2026-07-13 06:43:59.46866', '2026-07-13 06:43:59.468663');
INSERT INTO public.employees VALUES (4893, NULL, 'RS7281', '王亚军', 'wangyajun', '王亚军', 1, NULL, '18092961068', NULL, 1139, 24, 263, true, true, '2026-07-13 06:43:59.470394', '2026-07-13 06:43:59.470397');
INSERT INTO public.employees VALUES (4901, NULL, 'RS7289', '赵鹏程', 'zhaopengcheng', '赵鹏程', 1, NULL, '18336777121', NULL, 1140, 24, 254, true, true, '2026-07-13 06:43:59.47209', '2026-07-13 06:43:59.472093');
INSERT INTO public.employees VALUES (4902, NULL, 'RS7290', '王宁雷', 'wangninglei', '王宁雷', 1, NULL, '17638170285', NULL, 1140, 24, 254, true, true, '2026-07-13 06:43:59.473561', '2026-07-13 06:43:59.473565');
INSERT INTO public.employees VALUES (5261, NULL, 'RS7596', '尹申云', 'yinshenyun', '尹申云', 1, NULL, '13866615023', NULL, 1119, 24, 254, true, true, '2026-07-13 06:43:59.474702', '2026-07-13 06:43:59.474705');
INSERT INTO public.employees VALUES (5319, NULL, 'RS7603', '孙雪锋', 'sunxuefeng', '孙雪锋', 1, 'xf.sun@rs-machining.com', '18751233986', NULL, 1024, 24, 148, true, true, '2026-07-13 06:43:59.475896', '2026-07-13 06:43:59.475899');
INSERT INTO public.employees VALUES (6223, NULL, 'RS7954', '张国生', 'zhangguosheng', '张国生', 1, 'guosheng.zhang@rs-machining.com', '15366292837', NULL, 1122, 24, 148, true, true, '2026-07-13 06:43:59.477078', '2026-07-13 06:43:59.477082');
INSERT INTO public.employees VALUES (6758, NULL, 'RS8046', '倪青', 'niqing', '倪青', 1, NULL, '17826263833', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.478254', '2026-07-13 06:43:59.478258');
INSERT INTO public.employees VALUES (6797, NULL, 'RS8066', '王哲', 'wangzhe', '王哲', 1, NULL, '18838202531', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.479366', '2026-07-13 06:43:59.47937');
INSERT INTO public.employees VALUES (6812, NULL, 'RS8079', '刘洪', 'liuhong', '刘洪', 1, NULL, '13862072433', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.480533', '2026-07-13 06:43:59.480535');
INSERT INTO public.employees VALUES (6970, NULL, 'RS8139', '李超', 'lichao', '李超', 1, 'pamas@rs-machining.com', '13392861856', NULL, 1084, 24, 294, true, true, '2026-07-13 06:43:59.481654', '2026-07-13 06:43:59.481657');
INSERT INTO public.employees VALUES (6990, NULL, 'RS8169', '赵萌', 'zhaomeng', '赵萌', NULL, NULL, '13270999360', NULL, 1081, 24, 254, true, true, '2026-07-13 06:43:59.482801', '2026-07-13 06:43:59.482804');
INSERT INTO public.employees VALUES (6992, NULL, 'RS8168', '罗松', 'luosong', '罗松', 1, NULL, '18054077080', NULL, 1140, 24, 254, true, true, '2026-07-13 06:43:59.484218', '2026-07-13 06:43:59.484221');
INSERT INTO public.employees VALUES (7355, NULL, 'RS8248', '王杰', 'wangjie', '王杰', 1, NULL, '13771791351', NULL, 1108, 24, 254, true, true, '2026-07-13 06:43:59.485798', '2026-07-13 06:43:59.485802');
INSERT INTO public.employees VALUES (7357, NULL, 'RS8251', '曾伟', 'zengwei', '曾伟', 1, NULL, '13222184238', NULL, 1122, 24, 254, true, true, '2026-07-13 06:43:59.487407', '2026-07-13 06:43:59.487413');
INSERT INTO public.employees VALUES (7415, NULL, 'RS8284', '孔伟杰', 'kongweijie', '孔伟杰', 1, NULL, '18550399430', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.488985', '2026-07-13 06:43:59.488989');
INSERT INTO public.employees VALUES (7526, NULL, 'RS8437', '杨延财', 'yangyancai', '杨延财', 1, NULL, '18907496985', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.490602', '2026-07-13 06:43:59.490606');
INSERT INTO public.employees VALUES (7645, NULL, 'RS8455', '王震', 'wangzhen', '王震', 1, NULL, '15862480226', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.492192', '2026-07-13 06:43:59.492195');
INSERT INTO public.employees VALUES (7658, NULL, 'RS8457', '种张鹏', 'zhongzhangpeng', '种张鹏', 1, NULL, '13401466078', NULL, 1138, 24, 248, true, true, '2026-07-13 06:43:59.493876', '2026-07-13 06:43:59.493879');
INSERT INTO public.employees VALUES (7662, NULL, 'RS8461', '李小博', 'lixiaobo', '李小博', 1, NULL, '13255761612', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.495627', '2026-07-13 06:43:59.495631');
INSERT INTO public.employees VALUES (7668, NULL, 'RS8467', '周信霖', 'zhouxinlin', '周信霖', 1, NULL, '13140953110', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.497363', '2026-07-13 06:43:59.497367');
INSERT INTO public.employees VALUES (7736, NULL, 'RS8495', '马晓雯', 'maxiaowen', '马晓雯', NULL, NULL, '13151405137', NULL, 1130, 24, 260, true, true, '2026-07-13 06:43:59.498988', '2026-07-13 06:43:59.498992');
INSERT INTO public.employees VALUES (7756, NULL, 'RS8511', '王辉', 'wanghui', '王辉', 1, NULL, '15206187786', NULL, 1122, 24, 254, true, true, '2026-07-13 06:43:59.500673', '2026-07-13 06:43:59.500677');
INSERT INTO public.employees VALUES (8099, NULL, 'RS8568', '卞杰', 'bianjie', '卞杰', 1, NULL, '18862250373', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.502335', '2026-07-13 06:43:59.502339');
INSERT INTO public.employees VALUES (8148, NULL, 'RS8605', '蒋雄', 'jiangxiong', '蒋雄', 1, NULL, '18015519995', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.504036', '2026-07-13 06:43:59.50404');
INSERT INTO public.employees VALUES (8215, NULL, 'RS8639', '李林旭', 'lilinxu', '李林旭', 1, NULL, '15703478692', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.505741', '2026-07-13 06:43:59.505745');
INSERT INTO public.employees VALUES (8287, NULL, 'RS8679', '马振峰', 'mazhenfeng', '马振峰', 1, NULL, '17698598550', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.507466', '2026-07-13 06:43:59.507468');
INSERT INTO public.employees VALUES (8391, NULL, 'RS8759', '吴东林', 'wudonglin', '吴东林', 1, NULL, '15162692456', NULL, 1116, 24, 254, true, true, '2026-07-13 06:43:59.509543', '2026-07-13 06:43:59.509546');
INSERT INTO public.employees VALUES (8446, NULL, 'RS8791', '栗晓国', 'lixiaoguo', '栗晓国', 1, NULL, '18317704917', NULL, 1139, 24, 263, true, true, '2026-07-13 06:43:59.511235', '2026-07-13 06:43:59.511239');
INSERT INTO public.employees VALUES (8471, NULL, 'JS90038', '徐志', 'xuzhi', '徐志', 1, NULL, '13598858810', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.512906', '2026-07-13 06:43:59.51291');
INSERT INTO public.employees VALUES (8482, NULL, 'JS90049', '杨胜', 'yangsheng', '杨胜', 1, NULL, '15861432518', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.514647', '2026-07-13 06:43:59.51465');
INSERT INTO public.employees VALUES (8493, NULL, 'JS90060', '贺国志', 'heguozhi', '贺国志', 1, NULL, '15660671021', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.516394', '2026-07-13 06:43:59.516397');
INSERT INTO public.employees VALUES (8495, NULL, 'JS90062', '刘海学', 'liuhaixue', '刘海学', 1, NULL, '13861875305', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.518048', '2026-07-13 06:43:59.518052');
INSERT INTO public.employees VALUES (8496, NULL, 'JS90063', '吕宁', 'lvning', '吕宁', 1, NULL, '13819199057', NULL, 1103, 27, 254, true, true, '2026-07-13 06:43:59.519246', '2026-07-13 06:43:59.51925');
INSERT INTO public.employees VALUES (8498, NULL, 'JS90065', '王飞', 'wangfei', '王飞', 1, NULL, '13771955274', NULL, 1103, 27, 254, true, true, '2026-07-13 06:43:59.520375', '2026-07-13 06:43:59.520378');
INSERT INTO public.employees VALUES (8503, NULL, 'RS8797', '梁纪东', 'liangjidong', '梁纪东', 1, NULL, '15906130097', NULL, 1140, 24, 254, true, true, '2026-07-13 06:43:59.521554', '2026-07-13 06:43:59.521557');
INSERT INTO public.employees VALUES (8508, NULL, 'RS8798', '王忠印', 'wangzhongyin', '王忠印', 1, NULL, '15670123915', NULL, 1120, 24, 254, true, true, '2026-07-13 06:43:59.522699', '2026-07-13 06:43:59.522702');
INSERT INTO public.employees VALUES (8522, NULL, 'JS90071', '李荣壮', 'lirongzhuang', '李荣壮', 1, NULL, '15995738559', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.523861', '2026-07-13 06:43:59.523865');
INSERT INTO public.employees VALUES (8535, NULL, 'RS8816', '余强智', 'yuqiangzhi', '余强智', 1, NULL, '15591512709', NULL, 1139, 24, 263, true, true, '2026-07-13 06:43:59.524991', '2026-07-13 06:43:59.524995');
INSERT INTO public.employees VALUES (8549, NULL, 'JS90080', '寇耘诚', 'kouyuncheng', '寇耘诚', 1, NULL, '13661655396', NULL, 1147, 27, 248, true, true, '2026-07-13 06:43:59.526151', '2026-07-13 06:43:59.526154');
INSERT INTO public.employees VALUES (8550, NULL, 'JS90081', '常贵凯', 'changguikai', '常贵凯', 1, NULL, '15716261785', NULL, 1167, 27, 263, true, true, '2026-07-13 06:43:59.527323', '2026-07-13 06:43:59.527327');
INSERT INTO public.employees VALUES (8551, NULL, 'JS90082', '李南', 'linan', '李南', 1, NULL, '13961935626', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.528477', '2026-07-13 06:43:59.528481');
INSERT INTO public.employees VALUES (8576, NULL, 'JS90090', '刘帅', 'liushuai', '刘帅', 1, NULL, '15555536617', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.529595', '2026-07-13 06:43:59.529598');
INSERT INTO public.employees VALUES (8618, NULL, 'RS8834', '苏润戈', 'surunge', '苏润戈', 1, NULL, '15135900829', NULL, 1138, 24, 263, true, true, '2026-07-13 06:43:59.530705', '2026-07-13 06:43:59.530707');
INSERT INTO public.employees VALUES (8619, NULL, 'RS8835', '鄢园红', 'yanyuanhong', '鄢园红', 1, NULL, '15262450785', NULL, 1138, 24, 263, true, true, '2026-07-13 06:43:59.531884', '2026-07-13 06:43:59.531887');
INSERT INTO public.employees VALUES (8621, NULL, 'RS8837', '夏永立', 'xiayongli', '夏永立', 1, NULL, '15539081020', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.533013', '2026-07-13 06:43:59.533017');
INSERT INTO public.employees VALUES (8625, NULL, 'JS90094', '刘江涛', 'liujiangtao', '刘江涛', 1, NULL, '17609387234', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.534212', '2026-07-13 06:43:59.534215');
INSERT INTO public.employees VALUES (8637, NULL, 'JS90096', '张财', 'zhangcai', '张财', 1, NULL, '19557178392', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.535337', '2026-07-13 06:43:59.53534');
INSERT INTO public.employees VALUES (8640, NULL, 'JS90098', '崔伟伟', 'cuiweiwei', '崔伟伟', 1, NULL, '13921466387', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.536507', '2026-07-13 06:43:59.53651');
INSERT INTO public.employees VALUES (8658, NULL, 'RS8855', '项圆龙', 'xiangyuanlong', '项圆龙', 1, NULL, '17625950714', NULL, 1122, 24, 254, true, true, '2026-07-13 06:43:59.537665', '2026-07-13 06:43:59.537668');
INSERT INTO public.employees VALUES (8711, NULL, 'RS8865', '吴昊男', 'wuhaonan', '吴昊男', 1, NULL, '18435130259', NULL, 1115, 24, 86, true, true, '2026-07-13 06:43:59.538784', '2026-07-13 06:43:59.538787');
INSERT INTO public.employees VALUES (8712, NULL, 'RS8866', '谭勇', 'tanyong', '谭勇', 1, NULL, '18021806153', NULL, 1115, 24, 86, true, true, '2026-07-13 06:43:59.539913', '2026-07-13 06:43:59.539917');
INSERT INTO public.employees VALUES (8772, NULL, 'RS8873', '孙世梅', 'sunshimei', '孙世梅', NULL, NULL, '18721528530', NULL, 1115, 24, 86, true, true, '2026-07-13 06:43:59.541084', '2026-07-13 06:43:59.541087');
INSERT INTO public.employees VALUES (8777, NULL, 'RS8870', '马振杨', 'mazhenyang', '马振杨', 1, NULL, '15003875661', NULL, 1122, 24, 254, true, true, '2026-07-13 06:43:59.542257', '2026-07-13 06:43:59.54226');
INSERT INTO public.employees VALUES (8780, NULL, 'RS8875', '史永龙', 'shiyonglong', '史永龙', 1, NULL, '13915416115', NULL, 1138, 24, 263, true, true, '2026-07-13 06:43:59.54338', '2026-07-13 06:43:59.543383');
INSERT INTO public.employees VALUES (8830, NULL, 'RS8900', '杜旭升', 'duxusheng', '杜旭升', 1, NULL, '18329953113', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.544543', '2026-07-13 06:43:59.544547');
INSERT INTO public.employees VALUES (8856, NULL, 'RS8915', '杨姬召', 'yangjizhao', '杨姬召', 1, NULL, '15136976859', NULL, 1115, 24, 86, true, true, '2026-07-13 06:43:59.545696', '2026-07-13 06:43:59.5457');
INSERT INTO public.employees VALUES (8897, NULL, 'JS90154', '张育通', 'zhangyutong', '张育通', 1, NULL, '17602607521', NULL, 1103, 27, 254, true, true, '2026-07-13 06:43:59.546829', '2026-07-13 06:43:59.546832');
INSERT INTO public.employees VALUES (8917, NULL, 'JS90165', '张合功', 'zhanghegong', '张合功', 1, NULL, '18838990282', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.547959', '2026-07-13 06:43:59.547962');
INSERT INTO public.employees VALUES (8921, NULL, 'JS90172', '王东', 'wangdong', '王东', 1, NULL, '18918026228', NULL, 1161, 27, 122, true, true, '2026-07-13 06:43:59.549121', '2026-07-13 06:43:59.549124');
INSERT INTO public.employees VALUES (8930, NULL, 'JS90176', '王辰', 'wangchen', '王辰', NULL, NULL, '19963494826', NULL, 1142, 27, 264, true, true, '2026-07-13 06:43:59.550298', '2026-07-13 06:43:59.550302');
INSERT INTO public.employees VALUES (8957, NULL, 'RS8956', '沈波', 'shenbo', '沈波', 1, NULL, '18694920783', NULL, 1110, 24, 265, true, true, '2026-07-13 06:43:59.551401', '2026-07-13 06:43:59.551407');
INSERT INTO public.employees VALUES (8962, NULL, 'JS90186', '庞闻', 'pangwen', '庞闻', NULL, NULL, '13771839379', NULL, 1114, 27, 85, true, true, '2026-07-13 06:43:59.552555', '2026-07-13 06:43:59.552558');
INSERT INTO public.employees VALUES (8968, NULL, 'RS8962', '杜海亮', 'duhailiang', '杜海亮', 1, NULL, '17715520703', NULL, 1115, 24, 86, true, true, '2026-07-13 06:43:59.553752', '2026-07-13 06:43:59.553755');
INSERT INTO public.employees VALUES (8970, NULL, 'RS8964', '张林', 'zhanglin', '张林', 1, NULL, '13472490173', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.55488', '2026-07-13 06:43:59.554883');
INSERT INTO public.employees VALUES (8978, NULL, 'RS8971', '严镇', 'yanzhen', '严镇', 1, NULL, '15051853203', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.55604', '2026-07-13 06:43:59.556043');
INSERT INTO public.employees VALUES (9047, NULL, 'JX60003', '王嘉仪', 'wangjiayi', '王嘉仪', 1, 'wangjiayi@rs-machining.com', '13773026995', NULL, 1104, 28, 299, true, true, '2026-07-13 06:43:59.557168', '2026-07-13 06:43:59.557172');
INSERT INTO public.employees VALUES (9048, NULL, 'JX60004', '王强', 'wangqiang', '王强', 1, 'wangqiang@rs-machining.com', '13913646563', NULL, 1149, 28, 299, true, true, '2026-07-13 06:43:59.558309', '2026-07-13 06:43:59.558312');
INSERT INTO public.employees VALUES (9050, NULL, 'JX60008', '郭洪华', 'guohonghua', '郭洪华', 1, 'guohonghua@rs-machining.com', '13573465686', NULL, 1164, 28, 277, true, true, '2026-07-13 06:43:59.55947', '2026-07-13 06:43:59.559473');
INSERT INTO public.employees VALUES (9051, NULL, 'JX60009', '侯元峰', 'houyuanfeng', '侯元峰', 1, 'houyuanfeng@rs-machining.com', '15850838688', NULL, 1096, 28, 277, true, true, '2026-07-13 06:43:59.560614', '2026-07-13 06:43:59.560618');
INSERT INTO public.employees VALUES (9053, NULL, 'JX60012', '孙裕佳', 'sunyujia', '孙裕佳', 1, 'sunyujia@rs-machining.com', '18013683396', NULL, 1096, 28, 301, true, true, '2026-07-13 06:43:59.561732', '2026-07-13 06:43:59.561736');
INSERT INTO public.employees VALUES (9057, NULL, 'JX60021', '张亚忠', 'zhangyazhong', '张亚忠', 1, NULL, '18068013926', NULL, 1098, 28, 300, true, true, '2026-07-13 06:43:59.562862', '2026-07-13 06:43:59.562865');
INSERT INTO public.employees VALUES (9058, NULL, 'JX60025', '张夏青', 'zhangxiaqing', '张夏青', NULL, NULL, '17715567859', NULL, 1104, 28, 301, true, true, '2026-07-13 06:43:59.56403', '2026-07-13 06:43:59.564033');
INSERT INTO public.employees VALUES (9059, NULL, 'JX60026', '钱雪峰', 'qianxuefeng', '钱雪峰', 1, NULL, '18051538663', NULL, 1094, 28, 300, true, true, '2026-07-13 06:43:59.565191', '2026-07-13 06:43:59.565196');
INSERT INTO public.employees VALUES (9060, NULL, 'JX60027', '邵冬生', 'shaodongsheng', '邵冬生', 1, NULL, '15995912074', NULL, 1171, 28, 301, true, true, '2026-07-13 06:43:59.566306', '2026-07-13 06:43:59.566309');
INSERT INTO public.employees VALUES (9061, NULL, 'JX60031', '梁志颖', 'liangzhiying', '梁志颖', 1, 'liangzhiying@rs-machining.com', '18015468532', NULL, 1096, 28, 302, true, true, '2026-07-13 06:43:59.56747', '2026-07-13 06:43:59.567473');
INSERT INTO public.employees VALUES (9064, NULL, 'JX60037', '唐兴东', 'tangxingdong', '唐兴东', 1, NULL, '13773067455', NULL, 1096, 28, 301, true, true, '2026-07-13 06:43:59.568626', '2026-07-13 06:43:59.568629');
INSERT INTO public.employees VALUES (9065, NULL, 'JX60038', '朱利军', 'zhulijun', '朱利军', 1, NULL, '13814949813', NULL, 1171, 28, 302, true, true, '2026-07-13 06:43:59.56974', '2026-07-13 06:43:59.569743');
INSERT INTO public.employees VALUES (9066, NULL, 'JX60048', '张小荣', 'zhangxiaorong', '张小荣', 1, NULL, '13773049691', NULL, 1094, 28, 300, true, true, '2026-07-13 06:43:59.570864', '2026-07-13 06:43:59.570868');
INSERT INTO public.employees VALUES (9067, NULL, 'JX60049', '徐佳明', 'xujiaming', '徐佳明', 1, NULL, '17701577559', NULL, 1098, 28, 302, true, true, '2026-07-13 06:43:59.572046', '2026-07-13 06:43:59.572048');
INSERT INTO public.employees VALUES (9068, NULL, 'JX60054', '李丹', 'lidan', '李丹', 1, NULL, '13862256362', NULL, 1098, 28, 302, true, true, '2026-07-13 06:43:59.57321', '2026-07-13 06:43:59.573213');
INSERT INTO public.employees VALUES (9069, NULL, 'JX60055', '叶映秋', 'yeyingqiu', '叶映秋', NULL, 'yeyingqiu@rs-machining.com', '18962381705', NULL, 1124, 28, 312, true, true, '2026-07-13 06:43:59.57436', '2026-07-13 06:43:59.574364');
INSERT INTO public.employees VALUES (9071, NULL, 'JX60057', '陈梦星', 'chenmengxing', '陈梦星', 1, NULL, '18913670336', NULL, 1095, 28, 302, true, true, '2026-07-13 06:43:59.575527', '2026-07-13 06:43:59.57553');
INSERT INTO public.employees VALUES (9072, NULL, 'JX60058', '季灿冬', 'jicandong', '季灿冬', 1, 'jicandong@rs-machining.com', '18662419689', NULL, 1104, 28, 254, true, true, '2026-07-13 06:43:59.57664', '2026-07-13 06:43:59.576644');
INSERT INTO public.employees VALUES (9073, NULL, 'JX60059', '曹萌德', 'caomengde', '曹萌德', 1, 'caomengde@rs-machining.com', '18015608806', NULL, 1104, 28, 254, true, true, '2026-07-13 06:43:59.577772', '2026-07-13 06:43:59.577775');
INSERT INTO public.employees VALUES (9074, NULL, 'JX60060', '章红', 'zhanghong', '章红', NULL, 'zhanghong@rs-machining.com', '13776232011', NULL, 1063, 28, 259, true, true, '2026-07-13 06:43:59.578936', '2026-07-13 06:43:59.57894');
INSERT INTO public.employees VALUES (9075, NULL, 'JX60061', '张红连', 'zhanghonglian', '张红连', 1, NULL, '13862347996', NULL, 1096, 28, 250, true, true, '2026-07-13 06:43:59.580084', '2026-07-13 06:43:59.580087');
INSERT INTO public.employees VALUES (9076, NULL, 'JX60062', '宋景贤', 'songjingxian', '宋景贤', NULL, 'songjingxian@rs-machining.com', '15850803470', NULL, 1104, 28, 254, true, true, '2026-07-13 06:43:59.581292', '2026-07-13 06:43:59.581295');
INSERT INTO public.employees VALUES (9077, NULL, 'JX60063', '王善勇', 'wangshanyong', '王善勇', 1, NULL, '13953448556', NULL, 1096, 28, 306, true, true, '2026-07-13 06:43:59.582474', '2026-07-13 06:43:59.582477');
INSERT INTO public.employees VALUES (9078, NULL, 'JX60064', '孙成可', 'sunchengke', '孙成可', 1, NULL, '18913637650', NULL, 1096, 28, 306, true, true, '2026-07-13 06:43:59.583877', '2026-07-13 06:43:59.58388');
INSERT INTO public.employees VALUES (9079, NULL, 'JX60065', '雷升', 'leisheng', '雷升', 1, NULL, '13771803164', NULL, 1096, 28, 306, true, true, '2026-07-13 06:43:59.585388', '2026-07-13 06:43:59.585391');
INSERT INTO public.employees VALUES (9080, NULL, 'JX60066', '刘占琦', 'liuzhanqi', '刘占琦', 1, NULL, '18293498707', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.586916', '2026-07-13 06:43:59.586919');
INSERT INTO public.employees VALUES (9082, NULL, 'JX60068', '王兵', 'wangbing', '王兵', 1, NULL, '15195632460', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.588452', '2026-07-13 06:43:59.588455');
INSERT INTO public.employees VALUES (9084, NULL, 'JX60071', '邵磊', 'shaolei', '邵磊', 1, NULL, '18136405112', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.589905', '2026-07-13 06:43:59.589908');
INSERT INTO public.employees VALUES (9086, NULL, 'JX60075', '王根强', 'wanggenqiang', '王根强', 1, NULL, '17327555554', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.591451', '2026-07-13 06:43:59.591453');
INSERT INTO public.employees VALUES (9088, NULL, 'JX60077', '杨深', 'yangshen', '杨深', 1, NULL, '18914936816', NULL, 1094, 28, 305, true, true, '2026-07-13 06:43:59.593037', '2026-07-13 06:43:59.593041');
INSERT INTO public.employees VALUES (9089, NULL, 'JX60078', '姚舟', 'yaozhou', '姚舟', 1, 'yaozhou@rs-machining.com', '18015664820', NULL, 1150, 28, 124, true, true, '2026-07-13 06:43:59.594606', '2026-07-13 06:43:59.59461');
INSERT INTO public.employees VALUES (9091, NULL, 'JX60080', '杨志鹏', 'yangzhipeng', '杨志鹏', 1, NULL, '15100767502', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.596254', '2026-07-13 06:43:59.596257');
INSERT INTO public.employees VALUES (9092, NULL, 'JX60081', '王一晖', 'wangyihui', '王一晖', 1, NULL, '18013695662', NULL, 1094, 28, 305, true, true, '2026-07-13 06:43:59.59789', '2026-07-13 06:43:59.597894');
INSERT INTO public.employees VALUES (9093, NULL, 'JX60082', '蔡铭', 'caiming', '蔡铭', 1, NULL, '17715511025', NULL, 1094, 28, 305, true, true, '2026-07-13 06:43:59.599512', '2026-07-13 06:43:59.599515');
INSERT INTO public.employees VALUES (9094, NULL, 'JX60083', '施伟杰', 'shiweijie', '施伟杰', 1, NULL, '13814970770', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.601103', '2026-07-13 06:43:59.601106');
INSERT INTO public.employees VALUES (9098, NULL, 'JX60087', '陈超', 'chenchao', '陈超', 1, 'chenchao@rs-machining.com', '15370154320', NULL, 1104, 28, 254, true, true, '2026-07-13 06:43:59.602767', '2026-07-13 06:43:59.60277');
INSERT INTO public.employees VALUES (9099, NULL, 'JX60089', '刘林洋', 'liulinyang', '刘林洋', 1, NULL, '17609890149', NULL, 1096, 28, 306, true, true, '2026-07-13 06:43:59.604485', '2026-07-13 06:43:59.604488');
INSERT INTO public.employees VALUES (9100, NULL, 'JX60090', '沈浩', 'shenhao', '沈浩', 1, NULL, '15850819587', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.606163', '2026-07-13 06:43:59.606165');
INSERT INTO public.employees VALUES (9101, NULL, 'JX60091', '何彦平', 'heyanping', '何彦平', 1, NULL, '15599078187', NULL, 1096, 28, 289, true, true, '2026-07-13 06:43:59.607871', '2026-07-13 06:43:59.607874');
INSERT INTO public.employees VALUES (9103, NULL, 'JX60093', '惠康', 'huikang', '惠康', 1, NULL, '18156247098', NULL, 1094, 28, 305, true, true, '2026-07-13 06:43:59.609599', '2026-07-13 06:43:59.609602');
INSERT INTO public.employees VALUES (9105, NULL, 'JX60095', '刘涛', 'liutao', '刘涛', 1, NULL, '13365579816', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.611259', '2026-07-13 06:43:59.611263');
INSERT INTO public.employees VALUES (9107, NULL, 'JX60097', '孙磊', 'sunlei', '孙磊', 1, NULL, '17708741702', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.612936', '2026-07-13 06:43:59.612939');
INSERT INTO public.employees VALUES (9109, NULL, 'JX60101', '李涛', 'litao', '李涛', 1, NULL, '15035656102', NULL, 1102, 28, 301, true, true, '2026-07-13 06:43:59.614636', '2026-07-13 06:43:59.614639');
INSERT INTO public.employees VALUES (9110, NULL, 'JX60102', '许智荣', 'xuzhirong', '许智荣', 1, NULL, '18796808949', NULL, 1062, 28, 277, true, true, '2026-07-13 06:43:59.616364', '2026-07-13 06:43:59.616367');
INSERT INTO public.employees VALUES (9122, NULL, 'JX60115', '宁振浩', 'ningzhenhao', '宁振浩', 1, NULL, '13732601149', NULL, 1104, 28, 299, true, true, '2026-07-13 06:43:59.618006', '2026-07-13 06:43:59.618009');
INSERT INTO public.employees VALUES (9123, NULL, 'JX60116', '殷程波', 'yinchengbo', '殷程波', 1, NULL, '13235167076', NULL, 1104, 28, 301, true, true, '2026-07-13 06:43:59.619695', '2026-07-13 06:43:59.619698');
INSERT INTO public.employees VALUES (9125, NULL, 'JX60118', '谢伟', 'xiewei', '谢伟', 1, NULL, '18914079109', NULL, 1102, 28, 299, true, true, '2026-07-13 06:43:59.621416', '2026-07-13 06:43:59.621419');
INSERT INTO public.employees VALUES (9131, NULL, 'JX60124', '罗仁全', 'luorenquan', '罗仁全', 1, NULL, '17366111030', NULL, 1057, 28, 307, true, true, '2026-07-13 06:43:59.623057', '2026-07-13 06:43:59.62306');
INSERT INTO public.employees VALUES (9137, NULL, 'JX60130', '王井泉', 'wangjingquan', '王井泉', 1, NULL, '18796590196', NULL, 1099, 28, 299, true, true, '2026-07-13 06:43:59.624781', '2026-07-13 06:43:59.624785');
INSERT INTO public.employees VALUES (9144, NULL, 'JX60137', '殷亮', 'yinliang', '殷亮', 1, NULL, '15629643231', NULL, 1057, 28, 307, true, true, '2026-07-13 06:43:59.626487', '2026-07-13 06:43:59.626491');
INSERT INTO public.employees VALUES (9146, NULL, 'JX60139', '李仙海', 'lixianhai', '李仙海', 1, NULL, '19525863749', NULL, 1057, 28, 307, true, true, '2026-07-13 06:43:59.628165', '2026-07-13 06:43:59.628169');
INSERT INTO public.employees VALUES (9149, NULL, 'JX60140', '陈宇超', 'chenyuchao', '陈宇超', 1, NULL, '13812960773', NULL, 1099, 28, 307, true, true, '2026-07-13 06:43:59.629836', '2026-07-13 06:43:59.629839');
INSERT INTO public.employees VALUES (9210, NULL, 'JS90196', '何俊祥', 'hejunxiang', '何俊祥', 1, NULL, '17712634662', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.63159', '2026-07-13 06:43:59.631593');
INSERT INTO public.employees VALUES (9325, NULL, 'JS90202', '谢蒙恩', 'xiemengen', '谢蒙恩', NULL, NULL, '18506231960', NULL, 1131, 27, 259, true, true, '2026-07-13 06:43:59.633273', '2026-07-13 06:43:59.633276');
INSERT INTO public.employees VALUES (9326, NULL, 'JS90203', '谢贝宁', 'xiebeining', '谢贝宁', NULL, NULL, '18155260255', NULL, 1131, 27, 259, true, true, '2026-07-13 06:43:59.634933', '2026-07-13 06:43:59.634937');
INSERT INTO public.employees VALUES (9331, NULL, 'JS90208', '孔祥飞', 'kongxiangfei', '孔祥飞', 1, 'xfei.kong@rs-machining.com', '13862169804', NULL, 1025, 27, 148, true, true, '2026-07-13 06:43:59.63664', '2026-07-13 06:43:59.636643');
INSERT INTO public.employees VALUES (9332, NULL, 'JS90209', '贾兰兰', 'jialanlan', '贾兰兰', NULL, NULL, '15194470094', NULL, 1026, 27, 259, true, true, '2026-07-13 06:43:59.638371', '2026-07-13 06:43:59.638374');
INSERT INTO public.employees VALUES (9333, NULL, 'JS90210', '崔占云', 'cuizhanyun', '崔占云', 1, NULL, '15501661354', NULL, 1025, 27, 94, true, true, '2026-07-13 06:43:59.640032', '2026-07-13 06:43:59.640036');
INSERT INTO public.employees VALUES (9334, NULL, 'JS90211', '张培', 'zhangpei', '张培', NULL, NULL, '13732626846', NULL, 1128, 27, 148, true, true, '2026-07-13 06:43:59.641684', '2026-07-13 06:43:59.641688');
INSERT INTO public.employees VALUES (9335, NULL, 'JS90212', '周洁', 'zhoujie', '周洁', NULL, NULL, '13914941370', NULL, 1128, 27, 100, true, true, '2026-07-13 06:43:59.643443', '2026-07-13 06:43:59.643445');
INSERT INTO public.employees VALUES (9337, NULL, 'JS90215', '刘晓燕', 'liuxiaoyan', '刘晓燕', NULL, 'liuxiaoyan@rs-machining.com', '13862308019', NULL, 1128, 27, 308, true, true, '2026-07-13 06:43:59.645102', '2026-07-13 06:43:59.645105');
INSERT INTO public.employees VALUES (9338, NULL, 'JS90216', '林政宏', 'linzhenghong', '林政宏', 1, 'Hunter.Lin@rs-machining.com', '13915588594', NULL, 1086, 27, 268, true, true, '2026-07-13 06:43:59.646812', '2026-07-13 06:43:59.646816');
INSERT INTO public.employees VALUES (9339, NULL, 'JS90217', '袁艳', 'yuanyan', '袁艳', NULL, 'yuanyan@rs-machining.com', '13915662934', NULL, 1128, 27, 301, true, true, '2026-07-13 06:43:59.648541', '2026-07-13 06:43:59.648543');
INSERT INTO public.employees VALUES (9340, NULL, 'JS90218', '石勇', 'shiyong', '石勇', 1, 'yong.shi@rs-machining.com', '13862015540', NULL, 1113, 27, 85, true, true, '2026-07-13 06:43:59.650236', '2026-07-13 06:43:59.650239');
INSERT INTO public.employees VALUES (9341, NULL, 'JS90219', '刘炳娇', 'liubingjiao', '刘炳娇', 1, NULL, '18994439047', NULL, 1113, 27, 85, true, true, '2026-07-13 06:43:59.65196', '2026-07-13 06:43:59.651963');
INSERT INTO public.employees VALUES (9342, NULL, 'JS90220', '任燕秋', 'renyanqiu', '任燕秋', NULL, 'mary.ren@rs-machining.com', '18662422181', NULL, 1113, 27, 148, true, true, '2026-07-13 06:43:59.653679', '2026-07-13 06:43:59.653682');
INSERT INTO public.employees VALUES (9345, NULL, 'JS90223', '查锌', 'zhaxin', '查锌', NULL, 'zhaxin@rs-machining.com', '13260802651', NULL, 1114, 27, 85, true, true, '2026-07-13 06:43:59.655363', '2026-07-13 06:43:59.655366');
INSERT INTO public.employees VALUES (9349, NULL, 'JS90227', '濮钰荣', 'puyurong', '濮钰荣', NULL, NULL, '18261918822', NULL, 1083, 27, 259, true, true, '2026-07-13 06:43:59.656993', '2026-07-13 06:43:59.656997');
INSERT INTO public.employees VALUES (9350, NULL, 'JS90228', '侯奉君', 'houfengjun', '侯奉君', NULL, NULL, '15162306241', NULL, 1111, 27, 259, true, true, '2026-07-13 06:43:59.658794', '2026-07-13 06:43:59.658797');
INSERT INTO public.employees VALUES (9353, NULL, 'RS8990', '王兴华', 'wangxinghua', '王兴华', 1, NULL, '13776085679', NULL, 1115, 24, 148, true, true, '2026-07-13 06:43:59.660531', '2026-07-13 06:43:59.660535');
INSERT INTO public.employees VALUES (9358, NULL, 'JS90200', '曾美华', 'zengmeihua', '曾美华', NULL, 'Michelle.Zeng@rs-machining.com', '13511608573', NULL, 928, 27, 311, true, true, '2026-07-13 06:43:59.662197', '2026-07-13 06:43:59.6622');
INSERT INTO public.employees VALUES (9359, NULL, 'JS90201', '石小蒙', 'shixiaomeng', '石小蒙', NULL, NULL, '13127836018', NULL, 1131, 27, 259, true, true, '2026-07-13 06:43:59.663922', '2026-07-13 06:43:59.663924');
INSERT INTO public.employees VALUES (9364, NULL, 'JX60147', '陈昊', 'chenhao', '陈昊', 1, NULL, '18851436135', NULL, 1105, 28, 254, true, true, '2026-07-13 06:43:59.665619', '2026-07-13 06:43:59.665622');
INSERT INTO public.employees VALUES (9365, NULL, 'JX60148', '倪焕杰', 'nihuanjie', '倪焕杰', 1, NULL, '18115769846', NULL, 1105, 28, 254, true, true, '2026-07-13 06:43:59.667306', '2026-07-13 06:43:59.667309');
INSERT INTO public.employees VALUES (9367, NULL, 'JX60150', '杨骁', 'yangxiao', '杨骁', 1, NULL, '15852843680', NULL, 1105, 28, 269, true, true, '2026-07-13 06:43:59.669007', '2026-07-13 06:43:59.66901');
INSERT INTO public.employees VALUES (9379, NULL, 'RS8995', '盘美玲', 'panmeiling', '盘美玲', NULL, NULL, '18760705816', NULL, 1112, 24, 156, true, true, '2026-07-13 06:43:59.670751', '2026-07-13 06:43:59.670755');
INSERT INTO public.employees VALUES (9383, NULL, 'JS90232', '刘龙', 'liulong', '刘龙', 1, NULL, '18767125385', NULL, 1103, 27, 254, true, true, '2026-07-13 06:43:59.672454', '2026-07-13 06:43:59.672457');
INSERT INTO public.employees VALUES (9389, NULL, 'JS90236', '刘吉强', 'liujiqiang', '刘吉强', 1, NULL, '18550831740', NULL, 1128, 27, 277, true, true, '2026-07-13 06:43:59.674106', '2026-07-13 06:43:59.674109');
INSERT INTO public.employees VALUES (9435, NULL, 'JS90238', '吴焕', 'wuhuan', '吴焕', 1, NULL, '17351873143', NULL, 722, 27, 122, true, true, '2026-07-13 06:43:59.675855', '2026-07-13 06:43:59.675858');
INSERT INTO public.employees VALUES (9438, NULL, 'JS90239', '蒋勇', 'jiangyong', '蒋勇', 1, NULL, '13817831806', NULL, 1083, 27, 310, true, true, '2026-07-13 06:43:59.677548', '2026-07-13 06:43:59.677552');
INSERT INTO public.employees VALUES (9439, NULL, 'RS9000', '袁保存', 'yuanbaocun', '袁保存', 1, NULL, '13862553256', NULL, 1076, 24, 254, true, true, '2026-07-13 06:43:59.67921', '2026-07-13 06:43:59.679213');
INSERT INTO public.employees VALUES (9440, NULL, 'RS9001', '胡任行', 'hurenxing', '胡任行', 1, NULL, '13584845716', NULL, 1081, 24, 122, true, true, '2026-07-13 06:43:59.680913', '2026-07-13 06:43:59.680916');
INSERT INTO public.employees VALUES (9441, NULL, 'RS9002', '高峰', 'gaofeng', '高峰', NULL, NULL, '13771968330', NULL, 1130, 24, 148, true, true, '2026-07-13 06:43:59.682623', '2026-07-13 06:43:59.682626');
INSERT INTO public.employees VALUES (9442, NULL, 'JN80001', '张雨生', 'zhangyusheng', '张雨生', 1, NULL, '15995893658', NULL, 1134, 26, 277, true, true, '2026-07-13 06:43:59.68447', '2026-07-13 06:43:59.684473');
INSERT INTO public.employees VALUES (9443, NULL, 'JN80002', '崔海天', 'cuihaitian', '崔海天', 1, NULL, '15995401659', NULL, 1137, 26, 300, true, true, '2026-07-13 06:43:59.686263', '2026-07-13 06:43:59.686266');
INSERT INTO public.employees VALUES (9444, NULL, 'RS9003', '顾开国', 'gukaiguo', '顾开国', 1, NULL, '17605108371', NULL, 1108, 24, 124, true, true, '2026-07-13 06:43:59.688054', '2026-07-13 06:43:59.688057');
INSERT INTO public.employees VALUES (9446, NULL, 'JS90240', '赵永轩', 'zhaoyongxuan', '赵永轩', 1, NULL, '15053208506', NULL, 1146, 27, 163, true, true, '2026-07-13 06:43:59.689839', '2026-07-13 06:43:59.689842');
INSERT INTO public.employees VALUES (9447, NULL, 'JS90241', '桂亮', 'guiliang', '桂亮', 1, NULL, '18796876780', NULL, 1154, 27, 268, true, true, '2026-07-13 06:43:59.691638', '2026-07-13 06:43:59.691642');
INSERT INTO public.employees VALUES (9448, NULL, 'JS90242', '瞿鑫', 'juxin', '瞿鑫', 1, NULL, '18550009928', NULL, 1160, 27, 103, true, true, '2026-07-13 06:43:59.693432', '2026-07-13 06:43:59.693435');
INSERT INTO public.employees VALUES (9449, NULL, 'JS90243', '祝大龙', 'zhudalong', '祝大龙', 1, NULL, '18862347932', NULL, 1055, 27, 99, true, true, '2026-07-13 06:43:59.6951', '2026-07-13 06:43:59.695103');
INSERT INTO public.employees VALUES (9450, NULL, 'JS90244', '殷佳斌', 'yinjiabin', '殷佳斌', 1, NULL, '15062361266', NULL, 1055, 27, 99, true, true, '2026-07-13 06:43:59.696771', '2026-07-13 06:43:59.696775');
INSERT INTO public.employees VALUES (9451, NULL, 'JS90245', '武钱勇', 'wuqianyong', '武钱勇', 1, NULL, '18662524129', NULL, 1142, 27, 148, true, true, '2026-07-13 06:43:59.698453', '2026-07-13 06:43:59.698456');
INSERT INTO public.employees VALUES (9452, NULL, 'JS90246', '吕楠', 'lvnan', '吕楠', 1, NULL, '13405140509', NULL, 1100, 27, 148, true, true, '2026-07-13 06:43:59.700163', '2026-07-13 06:43:59.700166');
INSERT INTO public.employees VALUES (9453, NULL, 'JS90247', '杨杰', 'yangjie', '杨杰', 1, NULL, '15862366126', NULL, 1100, 27, 148, true, true, '2026-07-13 06:43:59.701846', '2026-07-13 06:43:59.701849');
INSERT INTO public.employees VALUES (9455, NULL, 'JS90249', '肖佳伟', 'xiaojiawei', '肖佳伟', 1, NULL, '15895688735', NULL, 1160, 27, 100, true, true, '2026-07-13 06:43:59.703531', '2026-07-13 06:43:59.703534');
INSERT INTO public.employees VALUES (9456, NULL, 'JS90250', '李超', 'lichao', '李超', 1, NULL, '13661832512', NULL, 1055, 27, 100, true, true, '2026-07-13 06:43:59.705203', '2026-07-13 06:43:59.705207');
INSERT INTO public.employees VALUES (9457, NULL, 'JS90251', '吕春鹏', 'lvchunpeng', '吕春鹏', 1, NULL, '15935620252', NULL, 1055, 27, 271, true, true, '2026-07-13 06:43:59.706894', '2026-07-13 06:43:59.706898');
INSERT INTO public.employees VALUES (9458, NULL, 'JS90252', '樊连玉', 'fanlianyu', '樊连玉', 1, NULL, '18860903101', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.708592', '2026-07-13 06:43:59.708595');
INSERT INTO public.employees VALUES (9459, NULL, 'JS90253', '马忠鑫', 'mazhongxin', '马忠鑫', 1, NULL, '18896551530', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.71027', '2026-07-13 06:43:59.710273');
INSERT INTO public.employees VALUES (9460, NULL, 'JS90254', '张武帅', 'zhangwushuai', '张武帅', 1, NULL, '13383460771', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.711947', '2026-07-13 06:43:59.71195');
INSERT INTO public.employees VALUES (9461, NULL, 'JS90255', '石胜全', 'shishengquan', '石胜全', 1, NULL, '18550912858', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.713626', '2026-07-13 06:43:59.71363');
INSERT INTO public.employees VALUES (9462, NULL, 'JS90256', '苗文学', 'miaowenxue', '苗文学', 1, NULL, '15850356342', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.715312', '2026-07-13 06:43:59.715314');
INSERT INTO public.employees VALUES (9463, NULL, 'JS90257', '胡天富', 'hutianfu', '胡天富', 1, NULL, '13039952631', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.717', '2026-07-13 06:43:59.717004');
INSERT INTO public.employees VALUES (9464, NULL, 'JS90258', '蔡鹏飞', 'caipengfei', '蔡鹏飞', 1, NULL, '15754324050', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.718456', '2026-07-13 06:43:59.718459');
INSERT INTO public.employees VALUES (9465, NULL, 'JS90259', '孔令强', 'konglingqiang', '孔令强', 1, NULL, '17625809780', NULL, 1100, 27, 254, true, true, '2026-07-13 06:43:59.719564', '2026-07-13 06:43:59.719567');
INSERT INTO public.employees VALUES (9466, NULL, 'JS90260', '谢海松', 'xiehaisong', '谢海松', 1, NULL, '13245064863', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.72072', '2026-07-13 06:43:59.720722');
INSERT INTO public.employees VALUES (9467, NULL, 'JS90261', '马尧', 'mayao', '马尧', 1, NULL, '13814213975', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.721844', '2026-07-13 06:43:59.721848');
INSERT INTO public.employees VALUES (9468, NULL, 'JS90262', '张文亮', 'zhangwenliang', '张文亮', 1, NULL, '18362621434', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.72278', '2026-07-13 06:43:59.722783');
INSERT INTO public.employees VALUES (9469, NULL, 'JS90263', '吴扣存', 'wukoucun', '吴扣存', 1, NULL, '15962539923', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.724099', '2026-07-13 06:43:59.724101');
INSERT INTO public.employees VALUES (9470, NULL, 'JS90264', '易志', 'yizhi', '易志', 1, NULL, '15003763767', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.725294', '2026-07-13 06:43:59.725297');
INSERT INTO public.employees VALUES (9471, NULL, 'JS90265', '周江山', 'zhoujiangshan', '周江山', 1, NULL, '17787268168', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.726422', '2026-07-13 06:43:59.726425');
INSERT INTO public.employees VALUES (9472, NULL, 'JS90266', '苏林宇', 'sulinyu', '苏林宇', 1, NULL, '15051238983', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.727572', '2026-07-13 06:43:59.727574');
INSERT INTO public.employees VALUES (9473, NULL, 'JS90267', '徐涛', 'xutao', '徐涛', 1, NULL, '15195692244', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.728726', '2026-07-13 06:43:59.728728');
INSERT INTO public.employees VALUES (9474, NULL, 'JS90268', '彭串', 'pengchuan', '彭串', 1, NULL, '15995419835', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.729876', '2026-07-13 06:43:59.729879');
INSERT INTO public.employees VALUES (9475, NULL, 'JS90269', '严青', 'yanqing', '严青', 1, NULL, '18626051314', NULL, 1160, 27, 254, true, true, '2026-07-13 06:43:59.730992', '2026-07-13 06:43:59.730995');
INSERT INTO public.employees VALUES (9476, NULL, 'JS90270', '汪洋', 'wangyang', '汪洋', 1, NULL, '15298893233', NULL, 1055, 27, 141, true, true, '2026-07-13 06:43:59.732175', '2026-07-13 06:43:59.732178');
INSERT INTO public.employees VALUES (9477, NULL, 'JS90271', '刘耀东', 'liuyaodong', '刘耀东', 1, NULL, '13453018274', NULL, 1055, 27, 141, true, true, '2026-07-13 06:43:59.733346', '2026-07-13 06:43:59.733349');
INSERT INTO public.employees VALUES (9478, NULL, 'JS90272', '谢宇', 'xieyu', '谢宇', NULL, NULL, '17807250492', NULL, 1154, 27, 264, true, true, '2026-07-13 06:43:59.734466', '2026-07-13 06:43:59.734469');
INSERT INTO public.employees VALUES (9479, NULL, 'RS9004', '王振', 'wangzhen', '王振', 1, NULL, '13515145743', NULL, 1170, 24, 298, true, true, '2026-07-13 06:43:59.735616', '2026-07-13 06:43:59.735618');
INSERT INTO public.employees VALUES (9480, NULL, 'RS9005', '姬英男', 'jiyingnan', '姬英男', 1, NULL, '17602184525', NULL, 1119, 24, 254, true, true, '2026-07-13 06:43:59.73677', '2026-07-13 06:43:59.736773');
INSERT INTO public.employees VALUES (9481, NULL, 'RS9006', '袁亚军', 'yuanyajun', '袁亚军', 1, NULL, '13641767605', NULL, 1122, 24, 254, true, true, '2026-07-13 06:43:59.737891', '2026-07-13 06:43:59.737894');
INSERT INTO public.employees VALUES (9482, NULL, 'RS9007', '陈梦', 'chenmeng', '陈梦', 1, NULL, '16651178582', NULL, 1076, 24, 301, true, true, '2026-07-13 06:43:59.738991', '2026-07-13 06:43:59.738994');
INSERT INTO public.employees VALUES (9483, NULL, 'RS9008', '计亚宁', 'jiyaning', '计亚宁', NULL, NULL, '13125083779', NULL, 1130, 24, 260, true, true, '2026-07-13 06:43:59.740179', '2026-07-13 06:43:59.740182');
INSERT INTO public.employees VALUES (9484, NULL, 'RS9009', '范钊', 'fanzhao', '范钊', NULL, NULL, '18051822228', NULL, 1084, 24, 259, true, true, '2026-07-13 06:43:59.741304', '2026-07-13 06:43:59.741307');
INSERT INTO public.employees VALUES (9485, NULL, 'RS9010', '朱玲', 'zhuling', '朱玲', NULL, NULL, '15358922744', NULL, 1084, 24, 264, true, true, '2026-07-13 06:43:59.742434', '2026-07-13 06:43:59.742438');
INSERT INTO public.employees VALUES (9486, NULL, 'JS90273', '贺雷博', 'heleibo', '贺雷博', 1, NULL, '18734874341', NULL, 1058, 27, 100, true, true, '2026-07-13 06:43:59.743551', '2026-07-13 06:43:59.743554');
INSERT INTO public.employees VALUES (9487, NULL, 'JN80003', '顾鉴', 'gujian', '顾鉴', 1, NULL, '15851420123', NULL, 1157, 26, 301, true, true, '2026-07-13 06:43:59.74471', '2026-07-13 06:43:59.744714');
INSERT INTO public.employees VALUES (9488, NULL, 'JS90274', '张成伟', 'zhangchengwei', '张成伟', 1, NULL, '13913196190', NULL, 1158, 27, 148, true, true, '2026-07-13 06:43:59.745847', '2026-07-13 06:43:59.74585');
INSERT INTO public.employees VALUES (9495, NULL, 'JS902321', '刘成建', 'liuchengjian', '刘成建', 1, NULL, '13402841750', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.746954', '2026-07-13 06:43:59.746957');
INSERT INTO public.employees VALUES (9503, NULL, 'JS90275', '石丽萍', 'shiliping', '石丽萍', NULL, NULL, '13915600434', NULL, 1131, 27, 259, true, true, '2026-07-13 06:43:59.748084', '2026-07-13 06:43:59.748086');
INSERT INTO public.employees VALUES (9504, NULL, 'JS90276', '吴艺阳', 'wuyiyang', '吴艺阳', 1, NULL, '18552140499', NULL, 1055, 27, 263, true, true, '2026-07-13 06:43:59.749248', '2026-07-13 06:43:59.749251');
INSERT INTO public.employees VALUES (9505, NULL, 'JS90277', '刘华培', 'liuhuapei', '刘华培', 1, NULL, '19529498993', NULL, 1158, 27, 124, true, true, '2026-07-13 06:43:59.750384', '2026-07-13 06:43:59.750387');
INSERT INTO public.employees VALUES (9506, NULL, 'JS90278', '马文涛', 'mawentao', '马文涛', 1, NULL, '13214547521', NULL, 1159, 27, 263, true, true, '2026-07-13 06:43:59.751521', '2026-07-13 06:43:59.751524');
INSERT INTO public.employees VALUES (9507, NULL, 'JX60156', '张铭哲', 'zhangmingzhe', '张铭哲', 1, NULL, '18702703685', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.752675', '2026-07-13 06:43:59.752679');
INSERT INTO public.employees VALUES (9509, NULL, 'RS9011', '郭耀', 'guoyao', '郭耀', 1, NULL, '18551103408', NULL, 1082, 24, 122, true, true, '2026-07-13 06:43:59.753809', '2026-07-13 06:43:59.753812');
INSERT INTO public.employees VALUES (9510, NULL, 'JS90279', '沈伟强', 'shenweiqiang', '沈伟强', 1, NULL, '18896547829', NULL, 1058, 27, 254, true, true, '2026-07-13 06:43:59.754912', '2026-07-13 06:43:59.754915');
INSERT INTO public.employees VALUES (9512, NULL, 'JX60159', '吕傲飞', 'lvaofei', '吕傲飞', 1, NULL, '18439464239', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.756035', '2026-07-13 06:43:59.756038');
INSERT INTO public.employees VALUES (9516, NULL, 'JX60161', '魏良海', 'weilianghai', '魏良海', 1, NULL, '13182513807', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.757194', '2026-07-13 06:43:59.757198');
INSERT INTO public.employees VALUES (9519, NULL, 'JX60162', '卫国锋', 'weiguofeng', '卫国锋', 1, NULL, '18435765812', NULL, 1172, 28, 263, true, true, '2026-07-13 06:43:59.758338', '2026-07-13 06:43:59.758341');
INSERT INTO public.employees VALUES (9520, NULL, 'JX60163', '孙安心', 'sunanxin', '孙安心', 1, NULL, '19521317049', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.759502', '2026-07-13 06:43:59.759505');
INSERT INTO public.employees VALUES (9521, NULL, 'JX60164', '廉帅达', 'lianshuaida', '廉帅达', 1, NULL, '15735349489', NULL, 1098, 28, 305, true, true, '2026-07-13 06:43:59.760615', '2026-07-13 06:43:59.760618');
INSERT INTO public.employees VALUES (9528, NULL, 'JX60167', '李鹏', 'lipeng', '李鹏', 1, NULL, '18115760134', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.761721', '2026-07-13 06:43:59.761724');
INSERT INTO public.employees VALUES (9529, NULL, 'JX60168', '陈洋', 'chenyang', '陈洋', 1, NULL, '13776228426', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.762795', '2026-07-13 06:43:59.762798');
INSERT INTO public.employees VALUES (9530, NULL, 'JS902333', '丁宇星', 'dingyuxing', '丁宇星', 1, NULL, '18113151982', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.763935', '2026-07-13 06:43:59.763938');
INSERT INTO public.employees VALUES (9531, NULL, 'JS902334', '何路阳', 'heluyang', '何路阳', 1, NULL, '13198193308', NULL, 1055, 27, 254, true, true, '2026-07-13 06:43:59.765069', '2026-07-13 06:43:59.765072');
INSERT INTO public.employees VALUES (9532, NULL, 'JS90283', '高晓丹', 'gaoxiaodan', '高晓丹', NULL, NULL, '13812972251', NULL, 1114, 27, 85, true, true, '2026-07-13 06:43:59.76625', '2026-07-13 06:43:59.766253');
INSERT INTO public.employees VALUES (9533, NULL, 'JS902335', '杨凯', 'yangkai', '杨凯', 1, NULL, '18482606675', NULL, 1159, 27, 313, true, true, '2026-07-13 06:43:59.767386', '2026-07-13 06:43:59.767389');
INSERT INTO public.employees VALUES (9534, NULL, 'JX60169', '周海', 'zhouhai', '周海', 1, NULL, '15995960451', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.768508', '2026-07-13 06:43:59.768512');
INSERT INTO public.employees VALUES (9535, NULL, 'JS902336', '周祥', 'zhouxiang', '周祥', 1, NULL, '13508570213', NULL, 1159, 27, 313, true, true, '2026-07-13 06:43:59.769697', '2026-07-13 06:43:59.7697');
INSERT INTO public.employees VALUES (9536, NULL, 'JX60170', '宗燚超', 'zongyichao', '宗燚超', 1, NULL, '15716130704', NULL, 1098, 28, 307, true, true, '2026-07-13 06:43:59.770829', '2026-07-13 06:43:59.770833');
INSERT INTO public.employees VALUES (9537, NULL, 'JX60171', '杜猛旭', 'dumengxu', '杜猛旭', 1, NULL, '15203774192', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.771961', '2026-07-13 06:43:59.771964');
INSERT INTO public.employees VALUES (9538, NULL, 'JX60172', '王强', 'wangqiang', '王强', 1, NULL, '15895611490', NULL, 1095, 28, 305, true, true, '2026-07-13 06:43:59.773074', '2026-07-13 06:43:59.773077');
INSERT INTO public.employees VALUES (9539, NULL, 'JS90284', '朱丽娜', 'zhulina', '朱丽娜', NULL, NULL, '13773096606', NULL, 1113, 27, 85, true, true, '2026-07-13 06:43:59.774255', '2026-07-13 06:43:59.774259');
INSERT INTO public.employees VALUES (9540, NULL, 'JX600301', '胡玉全', 'huyuquan', '胡玉全', 1, NULL, '15845427148', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.775402', '2026-07-13 06:43:59.775409');
INSERT INTO public.employees VALUES (9541, NULL, 'JX600304', '李富营', 'lifuying', '李富营', 1, NULL, '18761736810', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.776522', '2026-07-13 06:43:59.776525');
INSERT INTO public.employees VALUES (9542, NULL, 'JX600306', '仲磊', 'zhonglei', '仲磊', 1, NULL, '18007563694', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.777714', '2026-07-13 06:43:59.777717');
INSERT INTO public.employees VALUES (9543, NULL, 'JX600307', '谭文举', 'tanwenju', '谭文举', 1, NULL, '15989572391', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.77885', '2026-07-13 06:43:59.778853');
INSERT INTO public.employees VALUES (9544, NULL, 'JX600308', '胡强', 'huqiang', '胡强', 1, NULL, '13333764006', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.779975', '2026-07-13 06:43:59.779978');
INSERT INTO public.employees VALUES (9545, NULL, 'JX600313', '娄菩菩', 'loupupu', '娄菩菩', 1, NULL, '13956845123', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.781081', '2026-07-13 06:43:59.781085');
INSERT INTO public.employees VALUES (9546, NULL, 'JX600328', '朱昊宇', 'zhuhaoyu', '朱昊宇', 1, NULL, '15290163573', NULL, 1096, 28, 278, true, true, '2026-07-13 06:43:59.782233', '2026-07-13 06:43:59.782237');
INSERT INTO public.employees VALUES (9547, NULL, 'JX600330', '王伟杰', 'wangweijie', '王伟杰', 1, NULL, '18651416133', NULL, 1096, 28, 278, true, true, '2026-07-13 06:43:59.783348', '2026-07-13 06:43:59.783351');
INSERT INTO public.employees VALUES (9549, NULL, 'JX600332', '邓加勋', 'dengjiaxun', '邓加勋', 1, NULL, '13147226559', NULL, 1171, 28, 314, true, true, '2026-07-13 06:43:59.784441', '2026-07-13 06:43:59.784444');
INSERT INTO public.employees VALUES (9550, NULL, 'JX600333', '徐召远', 'xuzhaoyuan', '徐召远', 1, NULL, '19963211990', NULL, 1096, 28, 278, true, true, '2026-07-13 06:43:59.785573', '2026-07-13 06:43:59.785576');
INSERT INTO public.employees VALUES (9552, NULL, 'JX600335', '邓帅友', 'dengshuaiyou', '邓帅友', 1, NULL, '13721716605', NULL, 1096, 28, 278, true, true, '2026-07-13 06:43:59.786713', '2026-07-13 06:43:59.786716');
INSERT INTO public.employees VALUES (9553, NULL, 'JX600336', '金多标', 'jinduobiao', '金多标', 1, NULL, '19719638617', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.787834', '2026-07-13 06:43:59.787838');
INSERT INTO public.employees VALUES (9554, NULL, 'JX600337', '吴鹏', 'wupeng', '吴鹏', 1, NULL, '15872041166', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.789003', '2026-07-13 06:43:59.789006');
INSERT INTO public.employees VALUES (9555, NULL, 'JX600338', '李鹏博', 'lipengbo', '李鹏博', 1, NULL, '15221165906', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.790147', '2026-07-13 06:43:59.79015');
INSERT INTO public.employees VALUES (9556, NULL, 'JX600339', '孙明辉', 'sunminghui', '孙明辉', 1, NULL, '15303907630', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.791245', '2026-07-13 06:43:59.791248');
INSERT INTO public.employees VALUES (9557, NULL, 'JX600340', '张浩', 'zhanghao', '张浩', 1, NULL, '15923671874', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.7924', '2026-07-13 06:43:59.792404');
INSERT INTO public.employees VALUES (9558, NULL, 'JX600341', '刘明厅', 'liumingting', '刘明厅', 1, NULL, '18787487344', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.793526', '2026-07-13 06:43:59.793529');
INSERT INTO public.employees VALUES (9559, NULL, 'JX600342', '陈想', 'chenxiang', '陈想', 1, NULL, '18064736895', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.794667', '2026-07-13 06:43:59.79467');
INSERT INTO public.employees VALUES (9560, NULL, 'JX600343', '荆慕轩', 'jingmuxuan', '荆慕轩', 1, NULL, '15793179701', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.795809', '2026-07-13 06:43:59.795812');
INSERT INTO public.employees VALUES (9561, NULL, 'JX600344', '梁北', 'liangbei', '梁北', 1, NULL, '17601293276', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.796966', '2026-07-13 06:43:59.79697');
INSERT INTO public.employees VALUES (9562, NULL, 'JX600345', '生志阳', 'shengzhiyang', '生志阳', 1, NULL, '15939571962', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.798087', '2026-07-13 06:43:59.79809');
INSERT INTO public.employees VALUES (9564, NULL, 'JX600347', '陈谢鹏', 'chenxiepeng', '陈谢鹏', 1, NULL, '17712377994', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.799209', '2026-07-13 06:43:59.799212');
INSERT INTO public.employees VALUES (9565, NULL, 'JX600348', '侯记森', 'houjisen', '侯记森', 1, NULL, '18551366746', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.800374', '2026-07-13 06:43:59.800377');
INSERT INTO public.employees VALUES (9566, NULL, 'JX600349', '张晋泽', 'zhangjinze', '张晋泽', 1, NULL, '13067577938', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.801507', '2026-07-13 06:43:59.801511');
INSERT INTO public.employees VALUES (9567, NULL, 'JX600350', '薛永兴', 'xueyongxing', '薛永兴', 1, NULL, '17712377994', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.802619', '2026-07-13 06:43:59.802622');
INSERT INTO public.employees VALUES (9568, NULL, 'JX600351', '郭德宝', 'guodebao', '郭德宝', 1, NULL, '17503947091', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.803776', '2026-07-13 06:43:59.803779');
INSERT INTO public.employees VALUES (9571, NULL, 'JX600354', '李永亮', 'liyongliang', '李永亮', 1, NULL, '15157951327', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.804948', '2026-07-13 06:43:59.804952');
INSERT INTO public.employees VALUES (9572, NULL, 'JX600355', '李鹏', 'lipeng', '李鹏', 1, NULL, '18509026918', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.80615', '2026-07-13 06:43:59.806154');
INSERT INTO public.employees VALUES (9573, NULL, 'JX600356', '张帅', 'zhangshuai', '张帅', 1, NULL, '13057120150', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.807271', '2026-07-13 06:43:59.807274');
INSERT INTO public.employees VALUES (9574, NULL, 'JX600357', '王硕', 'wangshuo', '王硕', 1, NULL, '18623996208', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.808392', '2026-07-13 06:43:59.808395');
INSERT INTO public.employees VALUES (9575, NULL, 'JX600358', '冯宁', 'fengning', '冯宁', 1, NULL, '17698083195', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.809556', '2026-07-13 06:43:59.809559');
INSERT INTO public.employees VALUES (9576, NULL, 'JX600359', '杨存', 'yangcun', '杨存', 1, NULL, '13343692451', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.810689', '2026-07-13 06:43:59.810692');
INSERT INTO public.employees VALUES (9577, NULL, 'JX600360', '周想文', 'zhouxiangwen', '周想文', 1, NULL, '18919170001', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.811829', '2026-07-13 06:43:59.811832');
INSERT INTO public.employees VALUES (9578, NULL, 'JX600361', '李克聪', 'likecong', '李克聪', 1, NULL, '14787993254', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.812977', '2026-07-13 06:43:59.81298');
INSERT INTO public.employees VALUES (9579, NULL, 'JX600362', '徐玉峰', 'xuyufeng', '徐玉峰', 1, NULL, '16692154920', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.814117', '2026-07-13 06:43:59.81412');
INSERT INTO public.employees VALUES (9580, NULL, 'JX600363', '徐开放', 'xukaifang', '徐开放', 1, NULL, '13384097373', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.815237', '2026-07-13 06:43:59.81524');
INSERT INTO public.employees VALUES (9581, NULL, 'JX600364', '王远中', 'wangyuanzhong', '王远中', 1, NULL, '18036332621', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.816356', '2026-07-13 06:43:59.816359');
INSERT INTO public.employees VALUES (9582, NULL, 'JX600365', '肖宇', 'xiaoyu', '肖宇', 1, NULL, '19155869132', NULL, 1149, 28, 315, true, true, '2026-07-13 06:43:59.817503', '2026-07-13 06:43:59.817506');
INSERT INTO public.employees VALUES (9583, NULL, 'JX600366', '田鑫洋', 'tianxinyang', '田鑫洋', 1, NULL, '18322006139', NULL, 1095, 28, 280, true, true, '2026-07-13 06:43:59.818607', '2026-07-13 06:43:59.818611');


ALTER TABLE public.employees ENABLE TRIGGER ALL;

--
-- Data for Name: exchange_rates; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.exchange_rates DISABLE TRIGGER ALL;

INSERT INTO public.exchange_rates VALUES (1, 'CNY', 1, true, 'CNY汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.310222', '2026-07-13 07:32:19.620009');
INSERT INTO public.exchange_rates VALUES (2, 'USD', 6.779937, false, 'USD汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.311824', '2026-07-13 07:32:19.62574');
INSERT INTO public.exchange_rates VALUES (3, 'EUR', 7.728154, false, 'EUR汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.312868', '2026-07-13 07:32:19.622993');
INSERT INTO public.exchange_rates VALUES (4, 'GBP', 9.069966, false, 'GBP汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.31383', '2026-07-13 07:32:19.623253');
INSERT INTO public.exchange_rates VALUES (5, 'JPY', 0.041842, false, 'JPY汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.31477', '2026-07-13 07:32:19.62465');
INSERT INTO public.exchange_rates VALUES (6, 'HKD', 0.864644, false, 'HKD汇率 (同步自 er-api.com)', '2026-07-13 06:39:52.315632', '2026-07-13 07:32:19.623985');
INSERT INTO public.exchange_rates VALUES (7, 'AED', 1.846142, false, 'AED汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632059', '2026-07-13 07:32:19.632063');
INSERT INTO public.exchange_rates VALUES (8, 'AFN', 0.103951, false, 'AFN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632065', '2026-07-13 07:32:19.632066');
INSERT INTO public.exchange_rates VALUES (9, 'ALL', 0.082585, false, 'ALL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632067', '2026-07-13 07:32:19.632068');
INSERT INTO public.exchange_rates VALUES (10, 'AMD', 0.018461, false, 'AMD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632069', '2026-07-13 07:32:19.63207');
INSERT INTO public.exchange_rates VALUES (11, 'ANG', 3.787692, false, 'ANG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632071', '2026-07-13 07:32:19.632072');
INSERT INTO public.exchange_rates VALUES (12, 'AOA', 0.007095, false, 'AOA汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632073', '2026-07-13 07:32:19.632074');
INSERT INTO public.exchange_rates VALUES (13, 'ARS', 0.004548, false, 'ARS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632075', '2026-07-13 07:32:19.632076');
INSERT INTO public.exchange_rates VALUES (14, 'AUD', 4.702651, false, 'AUD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632078', '2026-07-13 07:32:19.632078');
INSERT INTO public.exchange_rates VALUES (15, 'AWG', 3.787692, false, 'AWG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63208', '2026-07-13 07:32:19.632081');
INSERT INTO public.exchange_rates VALUES (16, 'AZN', 3.989213, false, 'AZN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632082', '2026-07-13 07:32:19.632083');
INSERT INTO public.exchange_rates VALUES (17, 'BAM', 3.951351, false, 'BAM汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632084', '2026-07-13 07:32:19.632085');
INSERT INTO public.exchange_rates VALUES (18, 'BBD', 3.38998, false, 'BBD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632086', '2026-07-13 07:32:19.632087');
INSERT INTO public.exchange_rates VALUES (19, 'BDT', 0.055028, false, 'BDT汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632088', '2026-07-13 07:32:19.632089');
INSERT INTO public.exchange_rates VALUES (20, 'BGN', 3.951351, false, 'BGN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63209', '2026-07-13 07:32:19.632091');
INSERT INTO public.exchange_rates VALUES (21, 'BHD', 18.031664, false, 'BHD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632092', '2026-07-13 07:32:19.632093');
INSERT INTO public.exchange_rates VALUES (22, 'BIF', 0.002268, false, 'BIF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632094', '2026-07-13 07:32:19.632095');
INSERT INTO public.exchange_rates VALUES (23, 'BMD', 6.779983, false, 'BMD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632096', '2026-07-13 07:32:19.632097');
INSERT INTO public.exchange_rates VALUES (24, 'BND', 5.244306, false, 'BND汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632098', '2026-07-13 07:32:19.632099');
INSERT INTO public.exchange_rates VALUES (25, 'BOB', 0.677281, false, 'BOB汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.6321', '2026-07-13 07:32:19.632101');
INSERT INTO public.exchange_rates VALUES (26, 'BRL', 1.328101, false, 'BRL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632102', '2026-07-13 07:32:19.632103');
INSERT INTO public.exchange_rates VALUES (27, 'BSD', 6.779983, false, 'BSD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632104', '2026-07-13 07:32:19.632105');
INSERT INTO public.exchange_rates VALUES (28, 'BTN', 0.071234, false, 'BTN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632106', '2026-07-13 07:32:19.632107');
INSERT INTO public.exchange_rates VALUES (29, 'BWP', 0.466734, false, 'BWP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632108', '2026-07-13 07:32:19.632109');
INSERT INTO public.exchange_rates VALUES (30, 'BYN', 2.369039, false, 'BYN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63211', '2026-07-13 07:32:19.632111');
INSERT INTO public.exchange_rates VALUES (31, 'BZD', 3.38998, false, 'BZD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632112', '2026-07-13 07:32:19.632113');
INSERT INTO public.exchange_rates VALUES (32, 'CAD', 4.785788, false, 'CAD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632114', '2026-07-13 07:32:19.632115');
INSERT INTO public.exchange_rates VALUES (33, 'CDF', 0.002963, false, 'CDF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632116', '2026-07-13 07:32:19.632117');
INSERT INTO public.exchange_rates VALUES (34, 'CHF', 8.371003, false, 'CHF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632118', '2026-07-13 07:32:19.632119');
INSERT INTO public.exchange_rates VALUES (35, 'CLF', 289.435601, false, 'CLF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63212', '2026-07-13 07:32:19.632121');
INSERT INTO public.exchange_rates VALUES (36, 'CLP', 0.007322, false, 'CLP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632122', '2026-07-13 07:32:19.632123');
INSERT INTO public.exchange_rates VALUES (37, 'CNH', 1.000283, false, 'CNH汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632124', '2026-07-13 07:32:19.632135');
INSERT INTO public.exchange_rates VALUES (38, 'COP', 0.002069, false, 'COP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632136', '2026-07-13 07:32:19.632137');
INSERT INTO public.exchange_rates VALUES (39, 'CRC', 0.014907, false, 'CRC汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632138', '2026-07-13 07:32:19.632139');
INSERT INTO public.exchange_rates VALUES (40, 'CUP', 0.282498, false, 'CUP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63214', '2026-07-13 07:32:19.632141');
INSERT INTO public.exchange_rates VALUES (41, 'CVE', 0.070087, false, 'CVE汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632142', '2026-07-13 07:32:19.632143');
INSERT INTO public.exchange_rates VALUES (42, 'CZK', 0.3206, false, 'CZK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632144', '2026-07-13 07:32:19.632145');
INSERT INTO public.exchange_rates VALUES (43, 'DJF', 0.038149, false, 'DJF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632146', '2026-07-13 07:32:19.632147');
INSERT INTO public.exchange_rates VALUES (44, 'DKK', 1.035894, false, 'DKK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632149', '2026-07-13 07:32:19.63215');
INSERT INTO public.exchange_rates VALUES (45, 'DOP', 0.115522, false, 'DOP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632151', '2026-07-13 07:32:19.632152');
INSERT INTO public.exchange_rates VALUES (46, 'DZD', 0.050917, false, 'DZD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632153', '2026-07-13 07:32:19.632154');
INSERT INTO public.exchange_rates VALUES (47, 'EGP', 0.136101, false, 'EGP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632155', '2026-07-13 07:32:19.632156');
INSERT INTO public.exchange_rates VALUES (48, 'ERN', 0.451997, false, 'ERN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632157', '2026-07-13 07:32:19.632158');
INSERT INTO public.exchange_rates VALUES (49, 'ETB', 0.042498, false, 'ETB汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632159', '2026-07-13 07:32:19.63216');
INSERT INTO public.exchange_rates VALUES (50, 'FJD', 3.036588, false, 'FJD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632161', '2026-07-13 07:32:19.632162');
INSERT INTO public.exchange_rates VALUES (51, 'FKP', 9.070048, false, 'FKP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632163', '2026-07-13 07:32:19.632164');
INSERT INTO public.exchange_rates VALUES (52, 'FOK', 1.035895, false, 'FOK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632165', '2026-07-13 07:32:19.632166');
INSERT INTO public.exchange_rates VALUES (53, 'GEL', 2.576377, false, 'GEL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632168', '2026-07-13 07:32:19.632169');
INSERT INTO public.exchange_rates VALUES (54, 'GGP', 9.070048, false, 'GGP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63217', '2026-07-13 07:32:19.632171');
INSERT INTO public.exchange_rates VALUES (55, 'GHS', 0.591439, false, 'GHS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632172', '2026-07-13 07:32:19.632173');
INSERT INTO public.exchange_rates VALUES (56, 'GIP', 9.070048, false, 'GIP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632174', '2026-07-13 07:32:19.632175');
INSERT INTO public.exchange_rates VALUES (57, 'GMD', 0.091272, false, 'GMD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632176', '2026-07-13 07:32:19.632177');
INSERT INTO public.exchange_rates VALUES (58, 'GNF', 0.000771, false, 'GNF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632178', '2026-07-13 07:32:19.632179');
INSERT INTO public.exchange_rates VALUES (59, 'GTQ', 0.889032, false, 'GTQ汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63218', '2026-07-13 07:32:19.632181');
INSERT INTO public.exchange_rates VALUES (60, 'GYD', 0.032406, false, 'GYD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632182', '2026-07-13 07:32:19.632183');
INSERT INTO public.exchange_rates VALUES (61, 'HNL', 0.253438, false, 'HNL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632184', '2026-07-13 07:32:19.632185');
INSERT INTO public.exchange_rates VALUES (62, 'HRK', 1.025703, false, 'HRK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632186', '2026-07-13 07:32:19.632187');
INSERT INTO public.exchange_rates VALUES (63, 'HTG', 0.051842, false, 'HTG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632188', '2026-07-13 07:32:19.632189');
INSERT INTO public.exchange_rates VALUES (64, 'HUF', 0.021761, false, 'HUF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632191', '2026-07-13 07:32:19.632192');
INSERT INTO public.exchange_rates VALUES (65, 'IDR', 0.000375, false, 'IDR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632193', '2026-07-13 07:32:19.632194');
INSERT INTO public.exchange_rates VALUES (66, 'ILS', 2.2531, false, 'ILS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632195', '2026-07-13 07:32:19.632196');
INSERT INTO public.exchange_rates VALUES (67, 'IMP', 9.070048, false, 'IMP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632197', '2026-07-13 07:32:19.632198');
INSERT INTO public.exchange_rates VALUES (68, 'INR', 0.071234, false, 'INR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632199', '2026-07-13 07:32:19.6322');
INSERT INTO public.exchange_rates VALUES (69, 'IQD', 0.005177, false, 'IQD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632201', '2026-07-13 07:32:19.632202');
INSERT INTO public.exchange_rates VALUES (70, 'IRR', 6e-06, false, 'IRR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632203', '2026-07-13 07:32:19.632204');
INSERT INTO public.exchange_rates VALUES (71, 'ISK', 0.054028, false, 'ISK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632205', '2026-07-13 07:32:19.632206');
INSERT INTO public.exchange_rates VALUES (72, 'JEP', 9.070048, false, 'JEP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632207', '2026-07-13 07:32:19.632208');
INSERT INTO public.exchange_rates VALUES (73, 'JMD', 0.042724, false, 'JMD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632209', '2026-07-13 07:32:19.63221');
INSERT INTO public.exchange_rates VALUES (74, 'JOD', 9.562698, false, 'JOD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632212', '2026-07-13 07:32:19.632213');
INSERT INTO public.exchange_rates VALUES (75, 'KES', 0.052493, false, 'KES汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632214', '2026-07-13 07:32:19.632215');
INSERT INTO public.exchange_rates VALUES (76, 'KGS', 0.077505, false, 'KGS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632216', '2026-07-13 07:32:19.632217');
INSERT INTO public.exchange_rates VALUES (77, 'KHR', 0.001684, false, 'KHR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632218', '2026-07-13 07:32:19.632219');
INSERT INTO public.exchange_rates VALUES (78, 'KID', 4.702651, false, 'KID汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63222', '2026-07-13 07:32:19.632221');
INSERT INTO public.exchange_rates VALUES (79, 'KMF', 0.015709, false, 'KMF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632225', '2026-07-13 07:32:19.632226');
INSERT INTO public.exchange_rates VALUES (80, 'KRW', 0.004506, false, 'KRW汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632227', '2026-07-13 07:32:19.632228');
INSERT INTO public.exchange_rates VALUES (81, 'KWD', 22.079442, false, 'KWD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632229', '2026-07-13 07:32:19.63223');
INSERT INTO public.exchange_rates VALUES (82, 'KYD', 8.135968, false, 'KYD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632231', '2026-07-13 07:32:19.632232');
INSERT INTO public.exchange_rates VALUES (83, 'KZT', 0.014377, false, 'KZT汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632233', '2026-07-13 07:32:19.632234');
INSERT INTO public.exchange_rates VALUES (84, 'LAK', 0.000303, false, 'LAK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632236', '2026-07-13 07:32:19.632236');
INSERT INTO public.exchange_rates VALUES (85, 'LBP', 7.6e-05, false, 'LBP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632238', '2026-07-13 07:32:19.632239');
INSERT INTO public.exchange_rates VALUES (86, 'LKR', 0.02015, false, 'LKR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63224', '2026-07-13 07:32:19.632241');
INSERT INTO public.exchange_rates VALUES (87, 'LRD', 0.037407, false, 'LRD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632242', '2026-07-13 07:32:19.632243');
INSERT INTO public.exchange_rates VALUES (88, 'LSL', 0.4167, false, 'LSL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632244', '2026-07-13 07:32:19.632245');
INSERT INTO public.exchange_rates VALUES (89, 'LYD', 1.059942, false, 'LYD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632246', '2026-07-13 07:32:19.632247');
INSERT INTO public.exchange_rates VALUES (90, 'MAD', 0.726153, false, 'MAD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632248', '2026-07-13 07:32:19.632249');
INSERT INTO public.exchange_rates VALUES (91, 'MDL', 0.387298, false, 'MDL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63225', '2026-07-13 07:32:19.632251');
INSERT INTO public.exchange_rates VALUES (92, 'MGA', 0.001587, false, 'MGA汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632252', '2026-07-13 07:32:19.632253');
INSERT INTO public.exchange_rates VALUES (93, 'MKD', 0.125734, false, 'MKD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632254', '2026-07-13 07:32:19.632255');
INSERT INTO public.exchange_rates VALUES (94, 'MMK', 0.003226, false, 'MMK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632256', '2026-07-13 07:32:19.632257');
INSERT INTO public.exchange_rates VALUES (95, 'MNT', 0.001894, false, 'MNT汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632258', '2026-07-13 07:32:19.632259');
INSERT INTO public.exchange_rates VALUES (96, 'MOP', 0.839461, false, 'MOP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63226', '2026-07-13 07:32:19.632261');
INSERT INTO public.exchange_rates VALUES (97, 'MRU', 0.169133, false, 'MRU汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632262', '2026-07-13 07:32:19.632263');
INSERT INTO public.exchange_rates VALUES (98, 'MUR', 0.145038, false, 'MUR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632264', '2026-07-13 07:32:19.632265');
INSERT INTO public.exchange_rates VALUES (99, 'MVR', 0.439176, false, 'MVR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632266', '2026-07-13 07:32:19.632267');
INSERT INTO public.exchange_rates VALUES (100, 'MWK', 0.003896, false, 'MWK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632268', '2026-07-13 07:32:19.632269');
INSERT INTO public.exchange_rates VALUES (101, 'MXN', 0.3877, false, 'MXN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63227', '2026-07-13 07:32:19.632271');
INSERT INTO public.exchange_rates VALUES (102, 'MYR', 1.6688, false, 'MYR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632272', '2026-07-13 07:32:19.632273');
INSERT INTO public.exchange_rates VALUES (103, 'MZN', 0.106629, false, 'MZN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632274', '2026-07-13 07:32:19.632275');
INSERT INTO public.exchange_rates VALUES (104, 'NAD', 0.4167, false, 'NAD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632276', '2026-07-13 07:32:19.632277');
INSERT INTO public.exchange_rates VALUES (105, 'NGN', 0.004928, false, 'NGN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632278', '2026-07-13 07:32:19.632279');
INSERT INTO public.exchange_rates VALUES (106, 'NIO', 0.184343, false, 'NIO汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63228', '2026-07-13 07:32:19.632281');
INSERT INTO public.exchange_rates VALUES (107, 'NOK', 0.696111, false, 'NOK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632282', '2026-07-13 07:32:19.632283');
INSERT INTO public.exchange_rates VALUES (108, 'NPR', 0.044521, false, 'NPR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632284', '2026-07-13 07:32:19.632285');
INSERT INTO public.exchange_rates VALUES (109, 'NZD', 3.896585, false, 'NZD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632286', '2026-07-13 07:32:19.632287');
INSERT INTO public.exchange_rates VALUES (110, 'OMR', 17.633263, false, 'OMR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632288', '2026-07-13 07:32:19.632289');
INSERT INTO public.exchange_rates VALUES (111, 'PAB', 6.779983, false, 'PAB汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63229', '2026-07-13 07:32:19.632291');
INSERT INTO public.exchange_rates VALUES (112, 'PEN', 1.997124, false, 'PEN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632293', '2026-07-13 07:32:19.632294');
INSERT INTO public.exchange_rates VALUES (113, 'PGK', 1.531825, false, 'PGK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632295', '2026-07-13 07:32:19.632296');
INSERT INTO public.exchange_rates VALUES (114, 'PHP', 0.1104, false, 'PHP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632297', '2026-07-13 07:32:19.632298');
INSERT INTO public.exchange_rates VALUES (115, 'PKR', 0.024421, false, 'PKR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632299', '2026-07-13 07:32:19.6323');
INSERT INTO public.exchange_rates VALUES (116, 'PLN', 1.783024, false, 'PLN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632301', '2026-07-13 07:32:19.632302');
INSERT INTO public.exchange_rates VALUES (117, 'PYG', 0.001119, false, 'PYG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632303', '2026-07-13 07:32:19.632304');
INSERT INTO public.exchange_rates VALUES (118, 'QAR', 1.862627, false, 'QAR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632305', '2026-07-13 07:32:19.632306');
INSERT INTO public.exchange_rates VALUES (119, 'RON', 1.480681, false, 'RON汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632307', '2026-07-13 07:32:19.632308');
INSERT INTO public.exchange_rates VALUES (120, 'RSD', 0.06628, false, 'RSD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632309', '2026-07-13 07:32:19.63231');
INSERT INTO public.exchange_rates VALUES (121, 'RUB', 0.0892, false, 'RUB汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632311', '2026-07-13 07:32:19.632313');
INSERT INTO public.exchange_rates VALUES (122, 'RWF', 0.00462, false, 'RWF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632314', '2026-07-13 07:32:19.632315');
INSERT INTO public.exchange_rates VALUES (123, 'SAR', 1.807988, false, 'SAR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632316', '2026-07-13 07:32:19.632317');
INSERT INTO public.exchange_rates VALUES (124, 'SBD', 0.85023, false, 'SBD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632318', '2026-07-13 07:32:19.632319');
INSERT INTO public.exchange_rates VALUES (125, 'SCR', 0.462451, false, 'SCR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63232', '2026-07-13 07:32:19.632321');
INSERT INTO public.exchange_rates VALUES (126, 'SDG', 0.014774, false, 'SDG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632322', '2026-07-13 07:32:19.632323');
INSERT INTO public.exchange_rates VALUES (127, 'SEK', 0.702356, false, 'SEK汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632324', '2026-07-13 07:32:19.632325');
INSERT INTO public.exchange_rates VALUES (128, 'SGD', 5.244251, false, 'SGD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632326', '2026-07-13 07:32:19.632327');
INSERT INTO public.exchange_rates VALUES (129, 'SHP', 9.070048, false, 'SHP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632328', '2026-07-13 07:32:19.632329');
INSERT INTO public.exchange_rates VALUES (130, 'SLE', 0.278687, false, 'SLE汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63233', '2026-07-13 07:32:19.632331');
INSERT INTO public.exchange_rates VALUES (131, 'SLL', 0.000279, false, 'SLL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632332', '2026-07-13 07:32:19.632333');
INSERT INTO public.exchange_rates VALUES (132, 'SOS', 0.011853, false, 'SOS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632334', '2026-07-13 07:32:19.632335');
INSERT INTO public.exchange_rates VALUES (133, 'SRD', 0.179798, false, 'SRD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632336', '2026-07-13 07:32:19.632337');
INSERT INTO public.exchange_rates VALUES (134, 'SSP', 0.001417, false, 'SSP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632338', '2026-07-13 07:32:19.632339');
INSERT INTO public.exchange_rates VALUES (135, 'STN', 0.315435, false, 'STN汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63234', '2026-07-13 07:32:19.632341');
INSERT INTO public.exchange_rates VALUES (136, 'SYP', 0.055754, false, 'SYP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632342', '2026-07-13 07:32:19.632343');
INSERT INTO public.exchange_rates VALUES (137, 'SZL', 0.4167, false, 'SZL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632344', '2026-07-13 07:32:19.632345');
INSERT INTO public.exchange_rates VALUES (138, 'THB', 0.203945, false, 'THB汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632346', '2026-07-13 07:32:19.632347');
INSERT INTO public.exchange_rates VALUES (139, 'TJS', 0.733911, false, 'TJS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632348', '2026-07-13 07:32:19.632349');
INSERT INTO public.exchange_rates VALUES (140, 'TMT', 1.93684, false, 'TMT汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.63235', '2026-07-13 07:32:19.632351');
INSERT INTO public.exchange_rates VALUES (141, 'TND', 2.305651, false, 'TND汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632353', '2026-07-13 07:32:19.632353');
INSERT INTO public.exchange_rates VALUES (142, 'TOP', 2.840845, false, 'TOP汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632355', '2026-07-13 07:32:19.632356');
INSERT INTO public.exchange_rates VALUES (143, 'TRY', 0.1448, false, 'TRY汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632357', '2026-07-13 07:32:19.632358');
INSERT INTO public.exchange_rates VALUES (144, 'TTD', 0.999669, false, 'TTD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632359', '2026-07-13 07:32:19.63236');
INSERT INTO public.exchange_rates VALUES (145, 'TVD', 4.702651, false, 'TVD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632361', '2026-07-13 07:32:19.632362');
INSERT INTO public.exchange_rates VALUES (146, 'TWD', 0.2117, false, 'TWD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632363', '2026-07-13 07:32:19.632364');
INSERT INTO public.exchange_rates VALUES (147, 'TZS', 0.00258, false, 'TZS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632365', '2026-07-13 07:32:19.632366');
INSERT INTO public.exchange_rates VALUES (148, 'UAH', 0.152333, false, 'UAH汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632367', '2026-07-13 07:32:19.632368');
INSERT INTO public.exchange_rates VALUES (149, 'UGX', 0.001853, false, 'UGX汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632369', '2026-07-13 07:32:19.63237');
INSERT INTO public.exchange_rates VALUES (150, 'UYU', 0.168781, false, 'UYU汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632371', '2026-07-13 07:32:19.632372');
INSERT INTO public.exchange_rates VALUES (151, 'UZS', 0.000554, false, 'UZS汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632373', '2026-07-13 07:32:19.632374');
INSERT INTO public.exchange_rates VALUES (152, 'VES', 0.009394, false, 'VES汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632375', '2026-07-13 07:32:19.632376');
INSERT INTO public.exchange_rates VALUES (153, 'VND', 0.000258, false, 'VND汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632377', '2026-07-13 07:32:19.632378');
INSERT INTO public.exchange_rates VALUES (154, 'VUV', 0.056547, false, 'VUV汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632379', '2026-07-13 07:32:19.63238');
INSERT INTO public.exchange_rates VALUES (155, 'WST', 2.486777, false, 'WST汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632381', '2026-07-13 07:32:19.632382');
INSERT INTO public.exchange_rates VALUES (156, 'XAF', 0.011782, false, 'XAF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632383', '2026-07-13 07:32:19.632384');
INSERT INTO public.exchange_rates VALUES (157, 'XCD', 2.511099, false, 'XCD汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632385', '2026-07-13 07:32:19.632386');
INSERT INTO public.exchange_rates VALUES (158, 'XCG', 3.787692, false, 'XCG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632387', '2026-07-13 07:32:19.632388');
INSERT INTO public.exchange_rates VALUES (159, 'XDR', 9.203866, false, 'XDR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632389', '2026-07-13 07:32:19.63239');
INSERT INTO public.exchange_rates VALUES (160, 'XOF', 0.011782, false, 'XOF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632391', '2026-07-13 07:32:19.632392');
INSERT INTO public.exchange_rates VALUES (161, 'XPF', 0.064762, false, 'XPF汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632393', '2026-07-13 07:32:19.632394');
INSERT INTO public.exchange_rates VALUES (162, 'YER', 0.028539, false, 'YER汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632395', '2026-07-13 07:32:19.632396');
INSERT INTO public.exchange_rates VALUES (163, 'ZAR', 0.4167, false, 'ZAR汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632397', '2026-07-13 07:32:19.632398');
INSERT INTO public.exchange_rates VALUES (164, 'ZMW', 0.375644, false, 'ZMW汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632401', '2026-07-13 07:32:19.632402');
INSERT INTO public.exchange_rates VALUES (165, 'ZWG', 0.25378, false, 'ZWG汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632403', '2026-07-13 07:32:19.632404');
INSERT INTO public.exchange_rates VALUES (166, 'ZWL', 0.25378, false, 'ZWL汇率 (同步自 er-api.com)', '2026-07-13 07:32:19.632405', '2026-07-13 07:32:19.632406');


ALTER TABLE public.exchange_rates ENABLE TRIGGER ALL;

--
-- Data for Name: fee_rates; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.fee_rates DISABLE TRIGGER ALL;

INSERT INTO public.fee_rates VALUES (1, 'large', 1.05, '', '2026-07-13 06:34:27.655849', '2026-07-13 06:34:27.655854');
INSERT INTO public.fee_rates VALUES (2, 'standard', 1.2, '', '2026-07-13 06:34:37.617396', '2026-07-13 06:34:37.617403');
INSERT INTO public.fee_rates VALUES (3, 'other', 1.4, '', '2026-07-13 06:34:45.913043', '2026-07-13 06:34:45.913055');


ALTER TABLE public.fee_rates ENABLE TRIGGER ALL;

--
-- Data for Name: fee_types; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.fee_types DISABLE TRIGGER ALL;

INSERT INTO public.fee_types VALUES (1, '认证费', 'ca', 'external', true, '2026-07-13 06:37:59.27047');
INSERT INTO public.fee_types VALUES (2, '项目管理费', 'manage', 'external', true, '2026-07-13 06:38:20.229729');


ALTER TABLE public.fee_types ENABLE TRIGGER ALL;

--
-- Data for Name: labor_hours; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.labor_hours DISABLE TRIGGER ALL;

INSERT INTO public.labor_hours VALUES (1, 1, '机械设计', 80, 200, 16000, 1, '2026-07-13 07:45:18.38729', 'design');
INSERT INTO public.labor_hours VALUES (3, 1, '软件编程厂外调试（C#&Vision&robot）', 80, 200, 16000, 1, '2026-07-13 07:45:33.127302', 'debug');
INSERT INTO public.labor_hours VALUES (2, 1, '生产装配', 160, 200, 32000, 1, '2026-07-13 07:45:27.233918', 'assembly');


ALTER TABLE public.labor_hours ENABLE TRIGGER ALL;

--
-- Data for Name: landing_projects; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.landing_projects DISABLE TRIGGER ALL;

INSERT INTO public.landing_projects VALUES ('L104229-007', '2046754242157809666', '自动包装线改造', '上海鹏达', '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-22 11:24:14", "updateTime": "2026-04-28 13:22:12", "projectId": "2046754242157809666", "schemeNo": "L104229-007", "schemeName": "\u81ea\u52a8\u5305\u88c5\u7ebf\u6539\u9020", "craftType": "\u5176\u4ed6", "customerName": "\u4e0a\u6d77\u9e4f\u8fbe", "projectLocation": "\u4e0a\u6d77", "projectCode": "L104229-007", "projectSpec": "L104229-007", "projectName": "\u9e4f\u8fbe\u81ea\u52a8\u5305\u88c5\u7ebf\u6539\u9020", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-22", "maintainCycle": 300, "actualWorkHours": 1241.0, "schemeWorkHours": 0.0, "projectWorkHours": 1241.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "contractCode": "PO145375", "planWorkHours": 1960.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390685', '2026-07-13 08:10:31.355504');
INSERT INTO public.landing_projects VALUES ('RF104949', '2046754242157809182', 'TJSC-Line2新机型Y7p导入包装线改造（联宝）', NULL, '杜海峰', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809182", "schemeNo": "RF104949", "schemeName": "TJSC-Line2\u65b0\u673a\u578bY7p\u5bfc\u5165\u5305\u88c5\u7ebf\u6539\u9020\uff08\u8054\u5b9d\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "RF104949", "projectSpec": "RF104949", "projectName": "TJSC-Line2\u65b0\u673a\u578bY7p\u5bfc\u5165\u5305\u88c5\u7ebf\u6539\u9020\uff08\u8054\u5b9d\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 42.0, "schemeWorkHours": 0.0, "projectWorkHours": 42.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.3906', '2026-07-13 08:10:31.35537');
INSERT INTO public.landing_projects VALUES ('R105043', '2046754242157809193', 'JOT改机包 MA099415（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:10", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809193", "schemeNo": "R105043", "schemeName": "JOT\u6539\u673a\u5305 MA099415\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105043", "projectSpec": "R105043", "projectName": "JOT\u6539\u673a\u5305 MA099415\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390604', '2026-07-13 08:10:31.355377');
INSERT INTO public.landing_projects VALUES ('R105035', '2046754242157809185', 'JOT改机包 MA097230-64（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:24", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809185", "schemeNo": "R105035", "schemeName": "JOT\u6539\u673a\u5305 MA097230-64\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105035", "projectSpec": "R105035", "projectName": "JOT\u6539\u673a\u5305 MA097230-64\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.39068', '2026-07-13 08:10:31.355496');
INSERT INTO public.landing_projects VALUES ('L104229-006', '2046754242157809178', '三代自动包装线（鹏达）', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809178", "schemeNo": "L104229-006", "schemeName": "\u4e09\u4ee3\u81ea\u52a8\u5305\u88c5\u7ebf\uff08\u9e4f\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u4e0a\u6d77", "projectCode": "L104229-006", "projectSpec": "L104229-006", "projectName": "\u4e09\u4ee3\u81ea\u52a8\u5305\u88c5\u7ebf\uff08\u9e4f\u8fbe\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 24.0, "schemeWorkHours": 0.0, "projectWorkHours": 24.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390608', '2026-07-13 08:10:31.355384');
INSERT INTO public.landing_projects VALUES ('R102443', '2046754242157809230', 'AOI(成都戴尔)', NULL, '吴军军', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809230", "schemeNo": "R102443", "schemeName": "AOI(\u6210\u90fd\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u6210\u90fd", "projectCode": "R102443", "projectSpec": "R102443", "projectName": "AOI(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390518', '2026-07-13 08:10:31.35522');
INSERT INTO public.landing_projects VALUES ('R104678', '2046754242157809217', '导电环自动编号（502所）', NULL, '王玉明', 'MAINTENANCE', false, '{"createTime": "2026-04-28 06:46:06", "updateTime": "2026-04-28 06:46:06", "projectId": "2046754242157809217", "schemeNo": "R104678", "schemeName": "\u5bfc\u7535\u73af\u81ea\u52a8\u7f16\u53f7\uff08502\u6240\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R104678", "projectSpec": "R104678", "projectName": "\u5bfc\u7535\u73af\u81ea\u52a8\u7f16\u53f7\uff08502\u6240\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": false}', '2026-07-13 07:17:43.390579', '2026-07-13 08:10:31.355332');
INSERT INTO public.landing_projects VALUES ('R105038', '2046754242157809188', 'JOT改机包 MA099416（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:16", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809188", "schemeNo": "R105038", "schemeName": "JOT\u6539\u673a\u5305 MA099416\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105038", "projectSpec": "R105038", "projectName": "JOT\u6539\u673a\u5305 MA099416\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390583', '2026-07-13 08:10:31.35534');
INSERT INTO public.landing_projects VALUES ('R104646', '2046754242157809665', '厦门戴尔CPU组装机', '厦门戴尔', '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-22 11:24:14", "updateTime": "2026-04-28 13:22:00", "projectId": "2046754242157809665", "schemeNo": "R104646", "schemeName": "\u53a6\u95e8\u6234\u5c14CPU\u7ec4\u88c5\u673a", "craftType": "\u5176\u4ed6", "customerName": "\u53a6\u95e8\u6234\u5c14", "projectLocation": "\u53a6\u95e8", "projectCode": "L104453", "projectSpec": "L104453", "projectName": "Skyline--\u7ec4\u88c5\u7ebf--C2(\u53a6\u95e8\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-22", "maintainCycle": 300, "actualWorkHours": 4119.5, "schemeWorkHours": 0.0, "projectWorkHours": 4119.5, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "contractCode": "PO709889", "planWorkHours": 3000.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.39071', '2026-07-13 08:10:31.355543');
INSERT INTO public.landing_projects VALUES ('R104471', '2046754242157809223', 'Aladdin CCD TP间隙调整设备（联宝）', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809223", "schemeNo": "R104471", "schemeName": "Aladdin CCD TP\u95f4\u9699\u8c03\u6574\u8bbe\u5907\uff08\u8054\u5b9d\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "R104471", "projectSpec": "R104471", "projectName": "Aladdin CCD TP\u95f4\u9699\u8c03\u6574\u8bbe\u5907\uff08\u8054\u5b9d\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390526', '2026-07-13 08:10:31.355233');
INSERT INTO public.landing_projects VALUES ('R102147', '2046754242157809231', 'Auto Staging Project(成都戴尔)', NULL, '吴军军', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809231", "schemeNo": "R102147", "schemeName": "Auto Staging Project(\u6210\u90fd\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u6210\u90fd", "projectCode": "R102147", "projectSpec": "R102147", "projectName": "Auto Staging Project(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.39053', '2026-07-13 08:10:31.355241');
INSERT INTO public.landing_projects VALUES ('R104675', '2046754242157809220', '自动裂片设备（圣达）', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809220", "schemeNo": "R104675", "schemeName": "\u81ea\u52a8\u88c2\u7247\u8bbe\u5907\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "R104675", "projectSpec": "R104675", "projectName": "\u81ea\u52a8\u88c2\u7247\u8bbe\u5907\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390534', '2026-07-13 08:10:31.355249');
INSERT INTO public.landing_projects VALUES ('RF104784', '2046754242157809225', 'Aladdin CCD TP间隙调整设备（昆山凯普勒)', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809225", "schemeNo": "RF104784", "schemeName": "Aladdin CCD TP\u95f4\u9699\u8c03\u6574\u8bbe\u5907\uff08\u6606\u5c71\u51ef\u666e\u52d2)", "craftType": "\u5176\u4ed6", "projectLocation": "\u8d8a\u5357", "projectCode": "RF104784", "projectSpec": "RF104784", "projectName": "Aladdin CCD TP\u95f4\u9699\u8c03\u6574\u8bbe\u5907\uff08\u6606\u5c71\u51ef\u666e\u52d2)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390538', '2026-07-13 08:10:31.355256');
INSERT INTO public.landing_projects VALUES ('L101945', '2046754242157809227', '厦门戴尔1代&2代组装线--C4(厦门戴尔)', NULL, '王玉明', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809227", "schemeNo": "L101945", "schemeName": "\u53a6\u95e8\u6234\u5c141\u4ee3&2\u4ee3\u7ec4\u88c5\u7ebf--C4(\u53a6\u95e8\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u53a6\u95e8", "projectCode": "L101945", "projectSpec": "L101945", "projectName": "\u53a6\u95e8\u6234\u5c141\u4ee3&2\u4ee3\u7ec4\u88c5\u7ebf--C4(\u53a6\u95e8\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390543', '2026-07-13 08:10:31.355264');
INSERT INTO public.landing_projects VALUES ('R103513', '2046754242157809228', '高压检测(成都戴尔)', NULL, '吴军军', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809228", "schemeNo": "R103513", "schemeName": "\u9ad8\u538b\u68c0\u6d4b(\u6210\u90fd\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u6210\u90fd", "projectCode": "R103513", "projectSpec": "R103513", "projectName": "\u9ad8\u538b\u68c0\u6d4b(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390546', '2026-07-13 08:10:31.355271');
INSERT INTO public.landing_projects VALUES ('RF104750&RF104751', '2046754242157809221', '单面板上下料烧结复制（圣达）', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809221", "schemeNo": "RF104750&RF104751", "schemeName": "\u5355\u9762\u677f\u4e0a\u4e0b\u6599\u70e7\u7ed3\u590d\u5236\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "RF104750&RF104751", "projectSpec": "RF104750&RF104751", "projectName": "\u5355\u9762\u677f\u4e0a\u4e0b\u6599\u70e7\u7ed3\u590d\u5236\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.39055', '2026-07-13 08:10:31.355279');
INSERT INTO public.landing_projects VALUES ('R104449', '2046754242157809226', '厦门戴尔包装线--C4(厦门戴尔)', NULL, '王玉明', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809226", "schemeNo": "R104449", "schemeName": "\u53a6\u95e8\u6234\u5c14\u5305\u88c5\u7ebf--C4(\u53a6\u95e8\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u53a6\u95e8", "projectCode": "R104449", "projectSpec": "R104449", "projectName": "\u53a6\u95e8\u6234\u5c14\u5305\u88c5\u7ebf--C4(\u53a6\u95e8\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 163.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 163.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390555', '2026-07-13 08:10:31.355286');
INSERT INTO public.landing_projects VALUES ('L104542', '2046754242157809218', '呼吸传感器自动化（尚沃）', NULL, '王玉明', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809218", "schemeNo": "L104542", "schemeName": "\u547c\u5438\u4f20\u611f\u5668\u81ea\u52a8\u5316\uff08\u5c1a\u6c83\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u65e0\u9521", "projectCode": "L104542", "projectSpec": "L104542", "projectName": "\u547c\u5438\u4f20\u611f\u5668\u81ea\u52a8\u5316\uff08\u5c1a\u6c83\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390559', '2026-07-13 08:10:31.355294');
INSERT INTO public.landing_projects VALUES ('RF104754', '2046754242157809222', '绝缘耐压复制机（圣达）', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809222", "schemeNo": "RF104754", "schemeName": "\u7edd\u7f18\u8010\u538b\u590d\u5236\u673a\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "RF104754", "projectSpec": "RF104754", "projectName": "\u7edd\u7f18\u8010\u538b\u590d\u5236\u673a\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390563', '2026-07-13 08:10:31.355302');
INSERT INTO public.landing_projects VALUES ('RF104783', '2046754242157809224', 'Hinge cap gap control CCD设备（昆山凯普勒)', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809224", "schemeNo": "RF104783", "schemeName": "Hinge cap gap control CCD\u8bbe\u5907\uff08\u6606\u5c71\u51ef\u666e\u52d2)", "craftType": "\u5176\u4ed6", "projectLocation": "\u8d8a\u5357", "projectCode": "RF104783", "projectSpec": "RF104783", "projectName": "Hinge cap gap control CCD\u8bbe\u5907\uff08\u6606\u5c71\u51ef\u666e\u52d2)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390567', '2026-07-13 08:10:31.355309');
INSERT INTO public.landing_projects VALUES ('R102146-1', '2046754242157809229', 'Auto FAB Project(成都戴尔)', NULL, '吴军军', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809229", "schemeNo": "R102146-1", "schemeName": "Auto FAB Project(\u6210\u90fd\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u6210\u90fd", "projectCode": "R102146-1", "projectSpec": "R102146-1", "projectName": "Auto FAB Project(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390571', '2026-07-13 08:10:31.355317');
INSERT INTO public.landing_projects VALUES ('L102931', '2046754242157809219', '真空包装线（圣达）', NULL, '杜海峰', 'OUT_OF_SERVICE', true, '{"createTime": "2026-04-28 06:46:14", "updateTime": "2026-04-28 06:46:14", "projectId": "2046754242157809219", "schemeNo": "L102931", "schemeName": "\u771f\u7a7a\u5305\u88c5\u7ebf\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "L102931", "projectSpec": "L102931", "projectName": "\u771f\u7a7a\u5305\u88c5\u7ebf\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "OUT_OF_SERVICE", "archiveStatus": true}', '2026-07-13 07:17:43.390575', '2026-07-13 08:10:31.355325');
INSERT INTO public.landing_projects VALUES ('L104229-004/005', '2046754242157809176', '一代/二代自动包装线改造（鹏达）', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809176", "schemeNo": "L104229-004/005", "schemeName": "\u4e00\u4ee3/\u4e8c\u4ee3\u81ea\u52a8\u5305\u88c5\u7ebf\u6539\u9020\uff08\u9e4f\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u4e0a\u6d77", "projectCode": "L104229-004/005", "projectSpec": "L104229-004/005", "projectName": "\u4e00\u4ee3/\u4e8c\u4ee3\u81ea\u52a8\u5305\u88c5\u7ebf\u6539\u9020\uff08\u9e4f\u8fbe\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 36.0, "schemeWorkHours": 0.0, "projectWorkHours": 36.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390587', '2026-07-13 08:10:31.355348');
INSERT INTO public.landing_projects VALUES ('L104491', '2046754242157809174', 'Skyline--面包机包装线--C2(厦门戴尔)', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809174", "schemeNo": "L104491", "schemeName": "Skyline--\u9762\u5305\u673a\u5305\u88c5\u7ebf--C2(\u53a6\u95e8\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u53a6\u95e8", "projectCode": "L104491", "projectSpec": "L104491", "projectName": "Skyline--\u9762\u5305\u673a\u5305\u88c5\u7ebf--C2(\u53a6\u95e8\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390591', '2026-07-13 08:10:31.355355');
INSERT INTO public.landing_projects VALUES ('RF104959', '2046754242157809170', '码垛线--AOI检测(成都戴尔)', NULL, '吴军军', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809170", "schemeNo": "RF104959", "schemeName": "\u7801\u579b\u7ebf--AOI\u68c0\u6d4b(\u6210\u90fd\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u6210\u90fd", "projectCode": "RF104959", "projectSpec": "RF104959", "projectName": "\u7801\u579b\u7ebf--AOI\u68c0\u6d4b(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "contractCode": "PO773881", "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390596', '2026-07-13 08:10:31.355363');
INSERT INTO public.landing_projects VALUES ('R105042', '2046754242157809192', 'JOT改机包 MA097230-63（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:12", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809192", "schemeNo": "R105042", "schemeName": "JOT\u6539\u673a\u5305 MA097230-63\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105042", "projectSpec": "R105042", "projectName": "JOT\u6539\u673a\u5305 MA097230-63\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390612', '2026-07-13 08:10:31.355392');
INSERT INTO public.landing_projects VALUES ('R105041', '2046754242157809191', 'JOT改机包 MA099507（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-06-05 13:30:24", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809191", "schemeNo": "R105041", "schemeName": "JOT\u6539\u673a\u5305 MA099507\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105041", "projectSpec": "R105041", "projectName": "JOT\u6539\u673a\u5305 MA099507\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-06-05", "maintainCycle": 0, "actualWorkHours": 236.0, "schemeWorkHours": 0.0, "projectWorkHours": 236.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390616', '2026-07-13 08:10:31.355399');
INSERT INTO public.landing_projects VALUES ('R104677', '2046754242157809179', '刷丝压力测试（502所）', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809179", "schemeNo": "R104677", "schemeName": "\u5237\u4e1d\u538b\u529b\u6d4b\u8bd5\uff08502\u6240\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R104677", "projectSpec": "R104677", "projectName": "\u5237\u4e1d\u538b\u529b\u6d4b\u8bd5\uff08502\u6240\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 9.0, "schemeWorkHours": 0.0, "projectWorkHours": 9.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.39062', '2026-07-13 08:10:31.355407');
INSERT INTO public.landing_projects VALUES ('R105036', '2046754242157809186', 'JOT改机包 MA099435（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:14", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809186", "schemeNo": "R105036", "schemeName": "JOT\u6539\u673a\u5305 MA099435\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105036", "projectSpec": "R105036", "projectName": "JOT\u6539\u673a\u5305 MA099435\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390625', '2026-07-13 08:10:31.355414');
INSERT INTO public.landing_projects VALUES ('R105044', '2046754242157809194', 'JOT改机包 MA095864（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:18", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809194", "schemeNo": "R105044", "schemeName": "JOT\u6539\u673a\u5305 MA095864\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105044", "projectSpec": "R105044", "projectName": "JOT\u6539\u673a\u5305 MA095864\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390631', '2026-07-13 08:10:31.355422');
INSERT INTO public.landing_projects VALUES ('R105039', '2046754242157809189', 'JOT改机包 MA097496（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:25", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809189", "schemeNo": "R105039", "schemeName": "JOT\u6539\u673a\u5305 MA097496\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105039", "projectSpec": "R105039", "projectName": "JOT\u6539\u673a\u5305 MA097496\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390636', '2026-07-13 08:10:31.35543');
INSERT INTO public.landing_projects VALUES ('RF104724&RF104725', '2046754242157809183', '清洗自动上下料（圣达）', NULL, '杜海峰', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809183", "schemeNo": "RF104724&RF104725", "schemeName": "\u6e05\u6d17\u81ea\u52a8\u4e0a\u4e0b\u6599\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "RF104724&RF104725", "projectSpec": "RF104724&RF104725", "projectName": "\u6e05\u6d17\u81ea\u52a8\u4e0a\u4e0b\u6599\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 230.5, "schemeWorkHours": 0.0, "projectWorkHours": 230.5, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390641', '2026-07-13 08:10:31.355437');
INSERT INTO public.landing_projects VALUES ('R105040', '2046754242157809190', 'JOT改机包 MA099547（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:20", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809190", "schemeNo": "R105040", "schemeName": "JOT\u6539\u673a\u5305 MA099547\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105040", "projectSpec": "R105040", "projectName": "JOT\u6539\u673a\u5305 MA099547\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390646', '2026-07-13 08:10:31.355444');
INSERT INTO public.landing_projects VALUES ('L104492', '2046754242157809173', 'Skyline--常规机包装线--C2(厦门戴尔)', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809173", "schemeNo": "L104492", "schemeName": "Skyline--\u5e38\u89c4\u673a\u5305\u88c5\u7ebf--C2(\u53a6\u95e8\u6234\u5c14)", "craftType": "\u5176\u4ed6", "projectLocation": "\u53a6\u95e8", "projectCode": "L104492", "projectSpec": "L104492", "projectName": "Skyline--\u5e38\u89c4\u673a\u5305\u88c5\u7ebf--C2(\u53a6\u95e8\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.39065', '2026-07-13 08:10:31.355451');
INSERT INTO public.landing_projects VALUES ('R104614', '2046754242157809180', '冷热及脉冲测试机（东创精密）', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809180", "schemeNo": "R104614", "schemeName": "\u51b7\u70ed\u53ca\u8109\u51b2\u6d4b\u8bd5\u673a\uff08\u4e1c\u521b\u7cbe\u5bc6\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u76d0\u57ce", "projectCode": "R104614", "projectSpec": "R104614", "projectName": "\u51b7\u70ed\u53ca\u8109\u51b2\u6d4b\u8bd5\u673a\uff08\u4e1c\u521b\u7cbe\u5bc6\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390655', '2026-07-13 08:10:31.355459');
INSERT INTO public.landing_projects VALUES ('RF104722&RF104723', '2046754242157809184', '双面板烧结自动上下料（圣达）', NULL, '杜海峰', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809184", "schemeNo": "RF104722&RF104723", "schemeName": "\u53cc\u9762\u677f\u70e7\u7ed3\u81ea\u52a8\u4e0a\u4e0b\u6599\uff08\u5723\u8fbe\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5408\u80a5", "projectCode": "RF104722&RF104723", "projectSpec": "RF104722&RF104723", "projectName": "\u53cc\u9762\u677f\u70e7\u7ed3\u81ea\u52a8\u4e0a\u4e0b\u6599\uff08\u5723\u8fbe\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS5944", "projectManagerName": "\u675c\u6d77\u5cf0", "projectManagerPhone": "15162490140", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 2.0, "schemeWorkHours": 0.0, "projectWorkHours": 2.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.39066', '2026-07-13 08:10:31.355466');
INSERT INTO public.landing_projects VALUES ('L104636', '2046754242157809171', '哈飞装配线线边智能辅助工装（联想中天）', '航空工业哈飞', '吴军军', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-29 16:41:39", "operatorNo": "RS768", "operatorName": "\u5434\u519b\u519b", "projectId": "2046754242157809171", "schemeNo": "L104636", "schemeName": "\u54c8\u98de\u88c5\u914d\u7ebf\u7ebf\u8fb9\u667a\u80fd\u8f85\u52a9\u5de5\u88c5\uff08\u8054\u60f3\u4e2d\u5929\uff09", "craftType": "\u5176\u4ed6", "customerName": "\u822a\u7a7a\u5de5\u4e1a\u54c8\u98de", "projectLocation": "\u54c8\u5c14\u6ee8", "projectCode": "L104636", "projectSpec": "L104636", "projectName": "\u54c8\u98de\u88c5\u914d\u7ebf\u7ebf\u8fb9\u667a\u80fd\u8f85\u52a9\u5de5\u88c5\uff08\u8054\u60f3\u4e2d\u5929\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-04-29", "maintainCycle": 0, "actualWorkHours": 17.0, "schemeWorkHours": 0.0, "projectWorkHours": 4.0, "warrantyWorkHours": 11.0, "maintainWorkHours": 2.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390665', '2026-07-13 08:10:31.355474');
INSERT INTO public.landing_projects VALUES ('R105037', '2046754242157809187', 'JOT改机包 MA099432（北京JOT）', NULL, '赵萌', 'MAINTENANCE', true, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-05-25 14:20:21", "operatorNo": "RS8169", "operatorName": "\u8d75\u840c", "projectId": "2046754242157809187", "schemeNo": "R105037", "schemeName": "JOT\u6539\u673a\u5305 MA099432\uff08\u5317\u4eacJOT\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u5317\u4eac", "projectCode": "R105037", "projectSpec": "R105037", "projectName": "JOT\u6539\u673a\u5305 MA099432\uff08\u5317\u4eacJOT\uff09", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectManager": "RS8169", "projectManagerName": "\u8d75\u840c", "projectManagerPhone": "13270999360", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "projectEndTime": "2026-05-25", "maintainCycle": 0, "actualWorkHours": 0.0, "schemeWorkHours": 0.0, "projectWorkHours": 0.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "MAINTENANCE", "archiveStatus": true}', '2026-07-13 07:17:43.390671', '2026-07-13 08:10:31.355481');
INSERT INTO public.landing_projects VALUES ('R104613', '2046754242157809181', '耐压及爆破试验机（东创精密）', NULL, '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-28 06:30:36", "updateTime": "2026-04-28 06:30:36", "projectId": "2046754242157809181", "schemeNo": "R104613", "schemeName": "\u8010\u538b\u53ca\u7206\u7834\u8bd5\u9a8c\u673a\uff08\u4e1c\u521b\u7cbe\u5bc6\uff09", "craftType": "\u5176\u4ed6", "projectLocation": "\u76d0\u57ce", "projectCode": "R104613", "projectSpec": "R104613", "projectName": "\u8010\u538b\u53ca\u7206\u7834\u8bd5\u9a8c\u673a\uff08\u4e1c\u521b\u7cbe\u5bc6\uff09", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-28", "maintainCycle": 0, "actualWorkHours": 8.0, "schemeWorkHours": 0.0, "projectWorkHours": 8.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "planWorkHours": 0.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390676', '2026-07-13 08:10:31.355489');
INSERT INTO public.landing_projects VALUES ('L104229', '2046754242157809668', '自动包装线改造', '上海鹏达', '王玉明', 'IN_PROGRESS', false, '{"createTime": "2026-04-22 11:24:14", "updateTime": "2026-04-22 11:24:15", "projectId": "2046754242157809668", "parentId": "2046754242157809666", "schemeNo": "L104229", "schemeName": "\u81ea\u52a8\u5305\u88c5\u7ebf\u6539\u9020", "craftType": "\u5176\u4ed6", "customerName": "\u4e0a\u6d77\u9e4f\u8fbe", "projectLocation": "\u4e0a\u6d77", "projectCode": "R104230-7", "projectSpec": "R104230-7", "projectName": "\u4e0a\u6599\u8f93\u9001\u7ebf", "businessManager": "RS8139", "businessManagerName": "\u674e\u8d85", "businessManagerPhone": "13392861856", "projectManager": "RS1799", "projectManagerName": "\u738b\u7389\u660e", "projectManagerPhone": "13686857761", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-22", "maintainCycle": 300, "actualWorkHours": 129.0, "schemeWorkHours": 0.0, "projectWorkHours": 129.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "contractCode": "PO145375", "planWorkHours": 3000.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390705', '2026-07-13 08:10:31.355536');
INSERT INTO public.landing_projects VALUES ('CS26002', '2046754242157809664', '成都戴尔码垛', '成都戴尔', '吴军军', 'IN_PROGRESS', false, '{"createTime": "2026-04-22 08:53:32", "updateTime": "2026-04-28 13:41:26", "projectId": "2046754242157809664", "schemeNo": "CS26002", "schemeName": "\u6210\u90fd\u6234\u5c14\u7801\u579b", "craftType": "\u5176\u4ed6", "customerName": "\u6210\u90fd\u6234\u5c14", "projectLocation": "\u6210\u90fd", "projectCode": "RF104958", "projectSpec": "RF104958", "projectName": "\u7801\u579b\u7ebf--\u5206\u9009\u8bbe\u5907(\u6210\u90fd\u6234\u5c14)", "businessManager": "RS1927", "businessManagerName": "\u95f5\u8d85", "businessManagerPhone": "18112626306", "projectOrganization": "RS5518", "projectManager": "RS768", "projectManagerName": "\u5434\u519b\u519b", "projectManagerPhone": "15050448863", "projectProperty": "SALES", "projectTypeId": "2034085315407331328", "projectTypeName": "\u667a\u80fd\u5236\u9020", "projectStartTime": "2026-04-22", "maintainCycle": 290, "actualWorkHours": 1820.0, "schemeWorkHours": 0.0, "projectWorkHours": 1820.0, "warrantyWorkHours": 0.0, "maintainWorkHours": 0.0, "contractCode": "PO773881", "planWorkHours": 3216.0, "projectStatus": "IN_PROGRESS", "archiveStatus": false}', '2026-07-13 07:17:43.390715', '2026-07-13 08:10:31.355551');


ALTER TABLE public.landing_projects ENABLE TRIGGER ALL;

--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.materials DISABLE TRIGGER ALL;

INSERT INTO public.materials VALUES (350, 'RFID', 'IFM AL1100', '', 'pcs', 4333.60, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.81392', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (1, '四轴机械手', 'ESPON LS6-B602S', '', 'pcs', 49050.00, 'large', '额定负载2kg', '臂展600mm', '精度：±0.02mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.065095', '30306342', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (2, '四轴机械手', 'ESPON LS10-B702S-RC90-3M', '', 'pcs', 40500.00, 'large', '额定负载5kg', '臂展700mm', '精度：±0.02mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.071344', 'SX30016890', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (3, '四轴机械手', 'ESPON LS20-BA04S-RC90-3M', '', 'pcs', 50250.00, 'large', '额定负载10kg', '臂展1000mm', '精度：±0.025mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.074076', 'SX30016889', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (4, '四轴机械手', 'MITSUBISHI RH-6FRHR5520-D', '', 'pcs', 48500.00, 'large', '额定负载3kg', '臂展550mm', '精度：±0.012mm，±0.004°（第4关节）', 'active', '2026-07-13 07:30:56.076831', 'SX30027282', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (5, '四轴机械手', 'MITSUBISHI RH-20FRHR8535-D', '', 'pcs', 36600.00, 'large', '额定负载12kg', '臂展850mm', '精度：±0.015mm，±0.005°（第4关节）', 'active', '2026-07-13 07:30:56.079877', 'SX30011609', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (6, '四轴机械手', 'KUKA KR6 R500 Z200-2', '', 'pcs', 33300.00, 'large', '额定负载3kg', '臂展50mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.083271', 'SX30030929', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (7, '四轴机械手', 'KUKA KR12 R750 Z400', '', 'pcs', 55850.00, 'large', '额定负载6kg', '臂展750mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.08529', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (8, '四轴机械手', 'KUKA KR20 R1000 Z450', '', 'pcs', 54250.00, 'large', '额定负载10kg', '臂展1000mm', '精度：±0.03mm，', 'active', '2026-07-13 07:30:56.087213', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (9, '四轴机械手', 'INOVANCE IRS111-6-70Z20TS3', '', 'pcs', 78750.00, 'large', '额定负载5kg', '臂展700mm', '精度：±0.01mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.089862', 'SX30016248', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (10, '四轴机械手', 'INOVANCE IRS111-10-70Z20TS3', '', 'pcs', 40650.00, 'large', '额定负载10kg', '臂展700mm', '精度：±0.01mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.092429', 'SX30020762', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (11, '四轴机械手', 'INOVANCE IR-S20-100Z42S5', '', 'pcs', 36400.00, 'large', '额定负载10kg', '臂展1000mm', '精度：±0.025mm，±0.01°（第4关节）', 'active', '2026-07-13 07:30:56.09378', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (12, '六轴机械手', 'KUKA KR7 R900-3E', '', 'pcs', 65550.00, 'large', '额定负载7kg', '臂展900mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.095493', 'SX30030931', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (492, '其他', '其他', '其他', 'SET', 183.65, 'other', NULL, NULL, NULL, 'active', '2026-07-13 07:31:20.357112', '其他', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (13, '六轴机械手', 'KUKA KR8 R1620', '', 'pcs', 37050.00, 'large', '额定负载8kg', '臂展1620mm', '精度：±0.04mm，', 'active', '2026-07-13 07:30:56.097165', 'SX30003852', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (14, '六轴机械手', 'KUKA KR-10-R1100-2', '', 'pcs', 69950.00, 'large', '额定负载10kg', '臂展1101mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.09882', 'SX30010271', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (15, '六轴机械手', 'KUKA KR16R R1610', '', 'pcs', 77150.00, 'large', '额定负载16kg', '臂展1610mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.100549', 'SX30019856', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (16, '六轴机械手', 'KUKA KR60-3', '', 'pcs', 31700.00, 'large', '额定负载60kg', '臂展2033mm', '精度：±0.06mm，', 'active', '2026-07-13 07:30:56.102245', '30307952', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (17, '六轴机械手', 'KUKA KR500 R2830', '', 'pcs', 31400.00, 'large', '额定负载500kg', '臂展2800mm', '精度：±0.08mm，', 'active', '2026-07-13 07:30:56.103933', 'SX30006965', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (18, '六轴机械手', 'ABB IRB1200-7/0.7', '', 'pcs', 45450.00, 'large', '额定负载7kg', '臂展703mm', '精度：±0.015mm，', 'active', '2026-07-13 07:30:56.105594', 'SX30002099', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (19, '六轴机械手', 'ABB IRB2600ID-15', '', 'pcs', 42950.00, 'large', '额定负载15kg', '臂展1850mm', '精度：±0.026mm，', 'active', '2026-07-13 07:30:56.106783', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (20, '六轴机械手', 'ABB IRB4400-60', '', 'pcs', 59750.00, 'large', '额定负载60kg', '臂展1960mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.108005', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (21, '六轴机械手', 'ABB IRB5720-180/2.6', '', 'pcs', 58300.00, 'large', '额定负载180kg', '臂展2600mm', '精度：±0.06mm，', 'active', '2026-07-13 07:30:56.109259', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (22, '六轴机械手', 'FANUC LR MATE 200ID 7L', '', 'pcs', 56150.00, 'large', '额定负载7kg', '臂展911mm', '精度：±0.01mm，', 'active', '2026-07-13 07:30:56.110955', 'SX30030486', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (23, '六轴机械手', 'FANUC M-10iA 10M', '', 'pcs', 57650.00, 'large', '额定负载10kg', '臂展1422mm', '精度：±0.08mm，', 'active', '2026-07-13 07:30:56.112627', '30320270', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (24, '六轴机械手', 'FANUC M-10iD-16S', '', 'pcs', 47150.00, 'large', '额定负载16kg', '臂展1103mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.114315', 'SX30021213', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (25, '六轴机械手', 'FANUC M-710iC 50', '', 'pcs', 43900.00, 'large', '额定负载50kg', '臂展2050mm', '精度：±0.03mm，', 'active', '2026-07-13 07:30:56.115976', '30320269', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (26, '码垛机械手', 'KUKA KR40 PA', '', 'pcs', 51400.00, 'large', '最大负载40kg', '臂展1530mm', '精度：±0.06mm，', 'active', '2026-07-13 07:30:56.117124', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (27, '码垛机械手', 'KUKA KR240-3400-2', '', 'pcs', 40500.00, 'large', '最大负载240kg', '臂展3400mm', '精度：±0.08mm，', 'active', '2026-07-13 07:30:56.118758', 'SX30032186', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (28, '码垛机械手', 'KUKA KR 180 R3500-2K', '', 'pcs', 32450.00, 'large', '最大负载180kg', '臂展3500mm', '精度：±0.08mm，', 'active', '2026-07-13 07:30:56.120464', 'SX30032229', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (29, '码垛机械手', 'KUKA KR470-2-PA', '', 'pcs', 79900.00, 'large', '最大负载470kg', '臂展3150mm', '精度：±0.08mm，', 'active', '2026-07-13 07:30:56.121618', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (30, '码垛机械手', 'FANUC Robot M-41OiC-185', '', 'pcs', 36700.00, 'large', '额定负载185kg', '臂展3143mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.123582', 'SX30017745', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (31, '码垛机械手', 'FANUC R-2000iC-210F', '', 'pcs', 36350.00, 'large', '额定负载210kg', '臂展2655', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.125802', 'SX30018954', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (32, '码垛机械手', 'FANUC Robot M-41OiC/315', '', 'pcs', 60650.00, 'large', '额定负载315kg', '臂展3143mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.127385', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (33, '码垛机械手', 'FANUC Robot M-41OiC/500', '', 'pcs', 52200.00, 'large', '额定负载500kg', '臂展3143mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.128886', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (34, '码垛机械手', 'YASKAWA PL190', '', 'pcs', 40550.00, 'large', '额定负载190kg', '臂展3159mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.131981', 'SX30029027', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (35, '码垛机械手', 'YASKAWA PL320', '', 'pcs', 45450.00, 'large', '额定负载320kg', '臂展3159mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.133761', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (36, '码垛机械手', 'YASKAWA PL500', '', 'pcs', 60500.00, 'large', '额定负载500kg', '臂展3159mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.135548', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (37, '协作机械手', 'Universal Robots   UR5', '', 'pcs', 43950.00, 'large', '额定负载5kg', '臂展850mm', '精度：±0.03mm，', 'active', '2026-07-13 07:30:56.138146', 'SX30028623', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (38, '协作机械手', 'Universal Robots   UR10e', '', 'pcs', 38400.00, 'large', '额定负载10kg', '臂展1300mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.140785', 'SX30013914', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (39, '协作机械手', 'Universal Robots   UR15', '', 'pcs', 66900.00, 'large', '额定负载15kg', '臂展1300mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.143437', 'SX30031952', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (40, '协作机械手', 'Universal Robots   UR16e', '', 'pcs', 44800.00, 'large', '额定负载16kg', '臂展900mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.146183', 'SX30013767', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (41, '协作机械手', 'Universal Robots   UR20', '', 'pcs', 56450.00, 'large', '额定负载20kg', '臂展1750', '精度：±0.1mm，', 'active', '2026-07-13 07:30:56.148751', 'SX30031990', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (42, '协作机械手', 'ABB CRB15000-5/0.95', '', 'pcs', 61400.00, 'large', '额定负载5kg', '臂展950mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.151291', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (43, '协作机械手', 'ABB CRB15000-12/1.27', '', 'pcs', 52850.00, 'large', '额定负载12kg', '臂展1270mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.152953', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (44, '协作机械手', 'ABB CRB15000-10/1.52', '', 'pcs', 60950.00, 'large', '额定负载10kg', '臂展1520mm', '精度：±0.02mm，', 'active', '2026-07-13 07:30:56.154742', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (45, '协作机械手', 'KUKA LBR iiwa 7 R800', '', 'pcs', 55150.00, 'large', '最大负载7kg', '臂展800mm', '精度：±0.1mm，', 'active', '2026-07-13 07:30:56.157305', 'SX30030930', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (46, '协作机械手', 'KUKA LBR iisy  11 R1300', '', 'pcs', 56650.00, 'large', '最大负载11kg', '臂展1300mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.159028', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (298, 'PLC控制器', 'AB 1769-PA4', '', 'pcs', 3304.60, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.708538', '30203659', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (47, '协作机械手', 'KUKA LBR iico  16 R1000', '', 'pcs', 54500.00, 'large', '最大负载16kg', '臂展1000mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.160902', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (48, '协作机械手', 'FANUC CRX-5iA', '', 'pcs', 55850.00, 'large', '额定负载5kg', '臂展994mm', '精度：±0.04mm，', 'active', '2026-07-13 07:30:56.163093', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (49, '协作机械手', 'FANUC CRX-10iA', '', 'pcs', 55950.00, 'large', '额定负载10kg', '臂展1249mm', '精度：±0.04mm，', 'active', '2026-07-13 07:30:56.164868', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (50, '协作机械手', 'FANUC CRX-25iA', '', 'pcs', 75800.00, 'large', '额定负载25kg', '臂展1889mm', '精度：±0.05mm，', 'active', '2026-07-13 07:30:56.166636', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (51, '螺丝枪', 'DEPRAG 347-310-31U', '', 'pcs', 59850.00, 'large', '扭矩0.3～ 1.4 N·m', '转速1300r/min', '精度：±7.5%，', 'active', '2026-07-13 07:30:56.169166', '30300316', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (52, '螺丝枪', 'DEPRAG 326E27-0042', '', 'pcs', 53100.00, 'large', '扭矩0.7-4.2Nm', '转速10~400r/min', '精度：±7%，', 'active', '2026-07-13 07:30:56.170966', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (53, '螺丝枪', 'WEBER SEM/SEK 03(EC版)', '', 'pcs', 44200.00, 'large', '扭矩0.3-3Nm', '2500 rpm', '精度：±5%，', 'active', '2026-07-13 07:30:56.172897', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (54, '螺丝枪', 'Descutter ERS2-M20', '', 'pcs', 48250.00, 'large', '扭矩0.25-2.5Nm', '3000 rpm', '精度：±2%，', 'active', '2026-07-13 07:30:56.174784', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (55, '螺丝枪', 'BOSCH EC302', '', 'pcs', 30950.00, 'large', '扭矩0.6-5.5Nm', '1000 rpm', '精度：±2%，', 'active', '2026-07-13 07:30:56.176525', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (56, '螺丝枪', '阿特拉斯 ETD ES21‑02‑I06‑PS', '', 'pcs', 56700.00, 'large', '扭矩0.8 ～ 2 N·m', '转速4471r/min', '精度：±7.5%，', 'active', '2026-07-13 07:30:56.178981', '30308834', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (57, '螺丝枪', '阿特拉斯 ETD ES21‑04‑I07‑T25', '', 'pcs', 35300.00, 'large', '扭矩1.6 ～ 4.0 N·m', '转速1909 r/min', '精度：±7.5%，', 'active', '2026-07-13 07:30:56.181567', '30317440', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (58, '螺丝枪', '阿特拉斯 ETV ES61-40-10', '', 'pcs', 58300.00, 'large', '扭矩16 ～ 40 N·m', '转速1153 r/min', '精度：±7.5%，', 'active', '2026-07-13 07:30:56.184068', '30302299', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (306, 'PLC控制器', 'AB 1756-PA75', '', 'pcs', 3358.50, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.729794', '30206051', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (59, '螺丝枪', '阿特拉斯  Scew feeder for M1', '', 'pcs', 75050.00, 'large', '容量200~400PCS', '节拍40~60pcs/min', '卡钉率：0.03~0.05%，', 'active', '2026-07-13 07:30:56.186687', '30302648', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (60, '螺丝枪', '阿特拉斯 PF600', '', 'pcs', 54900.00, 'large', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.189222', '30302300', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (61, '螺丝枪', 'DANIKOR PTC-ASF-0009N-0-H10-015', '', 'pcs', 58300.00, 'large', '扭矩0.2～ 1.4 N·m', '转速3000r/min', '精度：±2.5%，', 'active', '2026-07-13 07:30:56.191798', 'SX30018218', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (62, '螺丝枪', 'DANIKOR PTC-ASF-0014N-0-H10-GS-G3', '', 'pcs', 76500.00, 'large', '扭矩0.2～ 1.4 N·m', '转速3000r/min', '精度：±5%，', 'active', '2026-07-13 07:30:56.194339', 'SX30030779', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (63, '螺丝枪', 'DANIKOR PTC-ASF-0030N-0-H10-030', '', 'pcs', 62300.00, 'large', '扭矩0.5～ 3.0 N·m', '转速95r/min', '精度：±7.5%，', 'active', '2026-07-13 07:30:56.196998', 'SX30018163', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (64, '螺丝枪', 'DANIKOR TMH-SPV-00-P1-H100-L00-B15-D11-X', '', 'pcs', 68150.00, 'large', '通常 0.05～5.0 N·m     （SPV 小扭矩版）', '常用 300～1500 rpm（可编程设定）', '​拧紧精度：±3% FS（闭环伺服控制，含角度步进监控）', 'active', '2026-07-13 07:30:56.199623', 'SX30031138', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (65, '螺丝枪', 'DDK MFT-160M10-S1', '', 'pcs', 74800.00, 'large', '0.24–1.56 N·m', 'Max.转速1250 r/min', '精度：±3%', 'active', '2026-07-13 07:30:56.201376', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (66, '压机', 'KISTLER 2162A010350NT(ES)', '', 'pcs', 32000.00, 'large', '额定吨位:10ｋＮ（１吨）', '压装行程：３５０ｍｍ　　（空埕速度：２５０ｍｍ／ｓ）', '重复定位精度：±0.01 mm', 'active', '2026-07-13 07:30:56.203119', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (67, '压机', 'PROMESS UFM Line5', '', 'pcs', 79400.00, 'large', '额定吨位:10ｋＮ（１吨）', '压装行程：20０ｍｍ　　（压装速度：30０ｍｍ／ｓ）', '重复定位精度：±0.01 mm', 'active', '2026-07-13 07:30:56.204842', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (68, '镭雕机', 'Trumpf  TruMark Station 5010（20W光纤）', '', 'pcs', 71700.00, 'large', '材料：模具等金属件', '光纤激光（波长1062nm）/20W）', '精度：±0.05mm', 'active', '2026-07-13 07:30:56.206661', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (69, '镭雕机', 'Trumpf  TruMark Station3330', '', 'pcs', 79300.00, 'large', '材料：PCB\玻璃\硅片', '紫外激光(UV)（355nm）/3W', '精度：±0.05mm', 'active', '2026-07-13 07:30:56.20849', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (70, '镭雕机', 'KEYENCE MD-U2010(2.5W)', '', 'pcs', 63150.00, 'large', '材料：塑料、硅片、玻璃', '紫外激光(UV)（355nm）/2.5W', NULL, 'active', '2026-07-13 07:30:56.21055', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (71, '镭雕机', 'GRAVOTECH XF510SP', '', 'pcs', 57300.00, 'large', '雕刻速度：≤10字符/s', '波长10.6nm(30W)', '定位精度：±0.01mm', 'active', '2026-07-13 07:30:56.213675', 'SX30018950', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (72, '镭雕机', 'HANSLASER 30W CO2-D30I', '', 'pcs', 68000.00, 'large', '雕刻速度：≤7000mm/s', '波长10.6nm(30W)', '定位精度：±0.01mm', 'active', '2026-07-13 07:30:56.216615', 'SX30029522', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (73, '镭雕机', 'HANSLASER HD-UV05WG', '', 'pcs', 60050.00, 'large', '雕刻速度：≤7000mm/s', '波长355nm(5W)', '定位精度：±0.01mm', 'active', '2026-07-13 07:30:56.219502', 'SX30029521', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (74, '镭雕机', '迅镭激光 QL-FL20G', '', 'pcs', 59250.00, 'large', '雕刻速度：≤7000mm/s', '波长1064nm(20W)', '定位精度± 0.002 ～ ± 0.01 mm', 'active', '2026-07-13 07:30:56.22205', '30312171', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (75, '氦气检测仪', 'INFICON LINXON-LX218', '', 'pcs', 73550.00, 'large', '灵敏度： 1×10⁻¹⁰~5×10⁻¹³ Pa·m³/s', '相应时间：≤0.5~3s', '氦气抽速：≥1.5~3L./s', 'active', '2026-07-13 07:30:56.224634', 'SX200004771', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (76, '氦气检测仪', 'NOY NHJ800D', '', 'pcs', 34400.00, 'large', '灵敏度：3×10⁻¹³ Pa·m³/s', '相应时间：≤0.5s', '氦气抽速2.5 L/s', 'active', '2026-07-13 07:30:56.226431', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (77, '振动盘', 'Deprag  FlexFeed 24', '', 'pcs', 69600.00, 'large', '盘面有效规格：≈195×150 mm', '盘面承重：≤0.5kg', '适应零件尺寸：1~50mm', 'active', '2026-07-13 07:30:56.228184', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (78, '振动盘', 'Danikor MTS-U15', '', 'pcs', 77550.00, 'large', '盘面有效规格：≈120(L)×90(W) mm×15(H) mm', '盘面承重：≤0.5kg', '适应零件尺寸：0.1～15mm', 'active', '2026-07-13 07:30:56.229899', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (79, '振动盘', '天堃：TIANJUN FUF-120', '', 'pcs', 30800.00, 'large', '盘面有效规格：≈120(L)×90(W) mm', '盘面承重：≤0.5kg', '适应零件尺寸：1～30mm', 'active', '2026-07-13 07:30:56.231677', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (80, '振动盘', '脩齐：XQ-FF-120', '', 'pcs', 51350.00, 'large', '盘面有效规格：≈120(L)×90(W) mm', '盘面承重：≤0.5kg', '适应零件尺寸：1～30mm', 'active', '2026-07-13 07:30:56.233457', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (81, '点激光检测', 'KEYENCE LJ-G015', '', 'pcs', 70450.00, 'large', '10±1mm', '0.01u', NULL, 'active', '2026-07-13 07:30:56.236823', '30500161', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (82, '点激光检测', 'KEYENCE LJ-G030', '', 'pcs', 46350.00, 'large', '30±5mm', '0.05u', NULL, 'active', '2026-07-13 07:30:56.239332', '30500162', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (83, '点激光检测', 'KEYENCE LJ-G015K', '', 'pcs', 59600.00, 'large', '15±2.3mm', '0.2u', NULL, 'active', '2026-07-13 07:30:56.241834', '30500604', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (84, '点激光检测', 'KEYENCE LJ-G5001', '', 'pcs', 70050.00, 'large', NULL, NULL, '千兆以太网口：标准 TCP/IP 通讯', 'active', '2026-07-13 07:30:56.244367', '30500163', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (85, '线激光检测', 'KEYENCE LJ-X8080', '', 'pcs', 46450.00, 'large', '73±20.5mm', '0.5u', NULL, 'active', '2026-07-13 07:30:56.246871', 'SX20000856', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (86, '线激光检测', 'KEYENCE LJ-V7020', '', 'pcs', 30600.00, 'large', '20±2.6mm', '0.2u', NULL, 'active', '2026-07-13 07:30:56.249461', '30500168', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (87, '线激光检测', 'KEYENCE LJ-V7060', '', 'pcs', 65350.00, 'large', '80±23mm', '0.4u', NULL, 'active', '2026-07-13 07:30:56.252114', '30500170', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (88, '线激光检测', 'KEYENCE LJ-V7080', '', 'pcs', 63300.00, 'large', '80±23mm', '0.5u', NULL, 'active', '2026-07-13 07:30:56.254695', '30500172', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (89, '线激光检测', 'KEYENCE XG-X2800LJ', '', 'pcs', 37250.00, 'large', NULL, NULL, '千兆以太网口：标准 TCP/IP 通讯', 'active', '2026-07-13 07:30:56.257271', 'SX20006028', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (90, '3D相机', 'Mech-eye-pros-GL-KW', '', 'pcs', 42200.00, 'large', '500~1000', '0.05mm @ 1.0m', NULL, 'active', '2026-07-13 07:30:56.258998', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (91, '彩色相机', 'COGNEX CAM-CIC-10MR-10-GC', '', 'pcs', 46050.00, 'large', '10 MP 10fps，彩色相机', '卷帘', '1/2.3" ,3856×2764 ,1.67 × 1.67 μm', 'active', '2026-07-13 07:30:56.261533', 'SX20000815', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (92, '彩色相机', 'COGNEX CAM-CIC-5MR-14-GC', '', 'pcs', 60700.00, 'large', '5M， 14fps，彩色相机', '卷帘', '1/2.5" 2592×1944  2.2 µm × 2.2 µm', 'active', '2026-07-13 07:30:56.264113', '30501987', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (93, '彩色相机', 'HIKVISION MV-CS200-10GC', '', 'pcs', 49450.00, 'large', '20M,.5.9fps,彩色', '卷帘', '1‘’，5472 × 3648，2.4 µm × 2.4 µm', 'active', '2026-07-13 07:30:56.266691', 'SX20004409', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (94, '彩色相机', 'N HIKVISION MV-CE120-10GC', '', 'pcs', 31600.00, 'large', '12M，9.6fps，彩色', '卷帘', '1/1.7”, 4024×3036,1.85 μm × 1.85 μm', 'active', '2026-07-13 07:30:56.269481', 'SX30006367', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (95, '彩色相机', 'HIKVISION MV-CA050-10GC', '', 'pcs', 30600.00, 'large', '5M，10fps，彩色', '全局', '2/3”， 2448×2048，3.45 µm × 3.45 µm', 'active', '2026-07-13 07:30:56.272024', 'SX20005242', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (96, '彩色相机', 'HIKVISION MV-CH250-90GC', '', 'pcs', 49550.00, 'large', '25M,4.5fps,彩色', '全局', '1.1”,5120 × 5120,2.5 μm × 2.5 μm', 'active', '2026-07-13 07:30:56.27465', 'SX20005245', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (97, '彩色相机', 'BASLER ACA4112-8gc', '', 'pcs', 43000.00, 'large', '12M，8fps,彩色', '全局', '1.1"， 4096 × 3000， 3.45 μm × 3.45 μm', 'active', '2026-07-13 07:30:56.277325', '30502916', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (98, '彩色相机', 'Basler PIA2400-17gc', '', 'pcs', 34200.00, 'large', '5M, 17fps, 彩色', '全局', '2/3"，2454 x 2056，3.45 µm x 3.45 µm', 'active', '2026-07-13 07:30:56.27986', '30503087', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (99, '在线打印机', 'Honeywell PX940A-600DPI', '', 'pcs', 2143.30, 'standard', '分辨率（600 dpi（23.6 dot/mm）', '打印速度：25~150mm/s(1~6 ips)', '打印头定位精度：±0.2mm', 'active', '2026-07-13 07:30:56.282519', 'SX30014277', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (100, '在线打印机', 'ZEBRA ZT610', '', 'pcs', 100.00, 'standard', '分辨率（600 dpi（23.6 dot/mm）', '600dpi：最高 6 ips（152 mm/s）', '打印头定位精度：±0.2mm', 'active', '2026-07-13 07:30:56.284981', 'SX30011204', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (101, '点胶阀', 'NORDSON 7360817XQR41-Without fittings', '', 'pcs', 2736.20, 'standard', '循环频率：＞400次/min', '最小点胶直径=0.15mm', '最大流体压力：7.0Ｂａｒ，', 'active', '2026-07-13 07:30:56.287538', 'SX30002236', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (102, '点胶阀', 'VERMES MDS3200A-0.07-1.0', '', 'pcs', 2422.60, 'standard', '喷射频率：最高 1000 Hz（持续运行）', '喷嘴孔径＝Ø 0.07 mm（70 μm）', '重复精度：±1%～±3%', 'active', '2026-07-13 07:30:56.290164', 'SX30021262', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (103, '点胶阀', 'GK 6000L-P100-D15', '', 'pcs', 198.00, 'standard', '喷射频率：Max 200–250 Hz', 'Ø 0.15 mm', '重复精度：±3%', 'active', '2026-07-13 07:30:56.292746', 'SX30005990', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (104, '点胶阀', 'BMS PJS-100-G10-Z10-L；', '', 'pcs', 663.50, 'standard', '喷射频率：最高 1000 Hz（持续）', '最小胶点直径：０.１５～０.２０ｍｍ', '±1%～±2%（CPK＞1.33 @ 0.5 nL）', 'active', '2026-07-13 07:30:56.296144', 'SX30005909', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (105, '气密检测仪', 'ATEQ F6 CLASS-3P10-ER', '', 'pcs', 2403.00, 'standard', '量程：0~500Pa;', '压差精度：±（1.1%~1.5%RDG+1Pa）', '压差分辨率：0.01~0.1Pa', 'active', '2026-07-13 07:30:56.298748', 'SX20003144', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (106, '气密检测仪', 'LK-D600', '', 'pcs', 1060.40, 'standard', '量程：±500 Pa / ±2 kPa', '±0.05% of ES（满量程），泄漏分辨率 0.1 Pa / 0.001 sccm', '压差分辨率：0.01Pa', 'active', '2026-07-13 07:30:56.300518', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (107, '压力传感器', 'LIGENT LFC-20-20kg-4M+LZ700', '', 'pcs', 4759.90, 'standard', '压力类型：压力', '量程：0~20kg', '综合误差：≤±0.5% F.S.', 'active', '2026-07-13 07:30:56.303045', '30204356', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (108, '压力传感器', 'LIGENT LFC-20-50kg-4M+LZ700', '', 'pcs', 3907.30, 'standard', '压力类型：压力', '量程：0~50kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.305573', '30204064', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (109, '压力传感器', 'LIGENT LFC-20-100kg-4M+LZ700', '', 'pcs', 3309.50, 'standard', '压力类型：压力', '量程：0~100kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.308098', '30203035', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (110, '压力传感器', 'LIGENT LFC-20-200KG', '', 'pcs', 3392.80, 'standard', '压力类型：压力', '量程：0~200kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.310673', '30308855', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (111, '压力传感器', 'LIGENT LFC-20-500kg-4M+LZ700（4-20mA）', '', 'pcs', 3035.10, 'standard', '压力类型：压力', '量程：0~500kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.313285', '30204357', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (112, '压力传感器', 'LIGENT LFC-20-1000kg+LZ700-0-10V', '', 'pcs', 2452.00, 'standard', '压力类型：压力', '量程：0~1000kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.31579', '30205884', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (113, '压力传感器', 'LIGENT LFC-20-2000kg+LZ700-4-20mA', '', 'pcs', 2040.40, 'standard', '压力类型：压力', '量程：0~2000kg', '非线性≤±0.5%FS / 滞后≤±0.5%FS / 重复性≤±0.5%FS', 'active', '2026-07-13 07:30:56.318564', 'SX30014134', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (114, '温控器', 'OMRON E5CC-CX2ASM-804', '', 'pcs', 1594.50, 'standard', 'AC100-240V + 4-20mA主输出', '2点继电器报警', '精度：热电偶 ±(0.3%PV 或 ±1℃ 取大)  ;Pt100 ±(0.2%PV 或 ±0.8℃ 取大）', 'active', '2026-07-13 07:30:56.321512', 'SX20003058', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (115, '温控器', 'HANYOUNGNUX VX4-TC4A-COV', '', 'pcs', 1006.50, 'standard', 'AC100-240V + 4-20mA主输出', '带 1 点辅助继电器报警', '显示精度：热电偶 ±(0.3%PV 或 ±1.5℃ 取大，环境温度 -10～50℃)
Pt100 ±(0.2%PV 或 ±0.8℃ 取大)', 'active', '2026-07-13 07:30:56.324075', 'SX20003577', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (116, '温控器', 'AZBIL C25TC0UA1100', '', 'pcs', 1496.50, 'standard', 'AC100-240V + 4-20mA主输出', '2点 SPST 继电器报警输出', '±0.3%FS±1digit；热电偶负温区 ±0.6%FS±1digit（23±2℃）', 'active', '2026-07-13 07:30:56.327436', 'SX20003559', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (117, '三联件', 'FESTO MS6-LFM-1/2-ARM-DA', '', 'pcs', 1354.40, 'standard', '流量：１７５０～１９00 L/min', '接口G1/2（内螺纹）', '过滤精度：0.01 mm', 'active', '2026-07-13 07:30:56.329111', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (118, '三联件', 'SMC AC30B-03DG-B', '', 'pcs', 1917.90, 'standard', '流量：１２００～１５００ L/min', '接口Ｒｃ３／８“（内螺纹）　　（带压力表）（禁油场合慎用）', '过滤精度：５μm', 'active', '2026-07-13 07:30:56.331703', 'SX30004324', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (119, '三联件', 'AIRTAC B52-GAC30010S', '', 'pcs', 100.00, 'standard', '流量：≤２５００ L/min', '接口Rc 3/8锥螺纹（内螺纹）', '过滤精度：40μm', 'active', '2026-07-13 07:30:56.334303', 'SX30019940', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (120, '阀岛', 'FESTO VTUG-10-MSDR-B1T-44V21-Q8-U-Q6S-16G+M2', '', 'pcs', 2633.30, 'standard', '工作压力：-0.9～10 bar；', '16个电磁阀位', '进气接口：G1/4"（φ8mm）；工作口：（φ6mm）', 'active', '2026-07-13 07:30:56.336768', '30336128', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (121, '阀岛', 'SMC SS5Y3-10SEAN-14B-C6', '', 'pcs', 4887.30, 'standard', '工作压力：0.15～0.9 Mpa', '14个电磁阀位', '接口：	Rc 1/8" 或 Rc 1/4"', 'active', '2026-07-13 07:30:56.339406', '30335394', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (122, '阀岛', 'AIRTAC SV3000-14-E-06', '', 'pcs', 3632.90, 'standard', '工作压力：0.2～0.6 MPa', '14个电磁阀位', '进气接口：	PT 1/4"', 'active', '2026-07-13 07:30:56.34117', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (123, '螺丝供料器', 'DEPRAG SG0211', '', 'pcs', 1736.60, 'standard', '1）螺丝规格：M1.4～M5.0；  2）螺丝总长L≈3～25mm', '螺杆单颗分离 + 压缩空气吹送（Blow Feed）​ 经 φ4～φ6 mm 送钉软管', '供料速度与节拍：60～90pcs/min', 'active', '2026-07-13 07:30:56.342898', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (124, '螺丝供料器', 'DANIKOR FDH-SST-450ML-P1-G1-0CP0(L)', '', 'pcs', 1702.30, 'standard', '1）螺丝规格：M1.0～M4.0；  2）头颈比：L/d 1.5～7.5', '供料方式：滚筒排列→出钉口待取', '供料速度与节拍：Max. 40～50 pcs/min', 'active', '2026-07-13 07:30:56.345469', 'SX30030745', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (125, '标签供料器', 'AREED ARD05-CPF040S180-L-C1-NY01-V1.0-lower level', '', 'pcs', 2961.60, 'standard', '标签长度：4~100mm', '底纸规格：​6~40mm', '出标精度：±0.3mm', 'active', '2026-07-13 07:30:56.347218', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (126, '标签供料器', 'AREED ARD05-CPF040S180-L-C1-NY01-V1.0-upper layer', '', 'pcs', 668.40, 'standard', '标签长度：4~100mm', '底纸规格：​6~40mm', '出标精度：±0.3mm', 'active', '2026-07-13 07:30:56.349207', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (127, '分割器  （DD马达）', 'WEISS TO220C(负载≤32KG)', '', 'pcs', 492.00, 'standard', '输出法兰 Ø220（分割器中心距90mm）', '轴向容许负荷 ≈ 1200 N；径向 ≈ 800 N（依具体安装高度）', '分度数：4等分，270驱动角；，                                           精度：±15″（高端凸轮转台）', 'active', '2026-07-13 07:30:56.351027', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (128, '分割器  （DD马达）', 'YT-R220(内装DS90分割器)', '', 'pcs', 4779.50, 'standard', '输出法兰 Ø220（分割器中心距90mm）', '轴向容许负荷 ≈ 1200 N(距法兰面H≤50mm处)；径向 ≈ 800 N（(距法兰面H≤50mm处)）', '分度数：4等分，270驱动角；，                                           精度：±15″（高端精度版）', 'active', '2026-07-13 07:30:56.352852', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (129, '分割器  （DD马达）', 'CAMDEX RU90DA042702R-S3-VW1 4等分', '', 'pcs', 3211.50, 'standard', '中心距：90mm', '出力轴允许轴向负荷215kNf,                  径向负荷：500kgf;', '分度数：4等分，270驱动角；，                                             精度：±30″（高端凸轮转台）', 'active', '2026-07-13 07:30:56.355664', '30309509', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (130, '倍速线', 'Modular PTS2/L-M700-V16-Bwt480-L3000-OP-F1', '', 'pcs', 4034.70, 'standard', '最大承重：700kg/m, 2.5倍速', '工装板宽度480mm,线体长度3000mm', '速度：8~16M/min,', 'active', '2026-07-13 07:30:56.357605', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (131, '倍速线', 'PARTNERS  H220727-CM02-3m', '', 'pcs', 1192.70, 'standard', '承重：500kg/m,2.5倍速', '工装板宽度540mm,线体长度3000mm', '速度：15~20M/min, 功率750W', 'active', '2026-07-13 07:30:56.360303', 'SX30020003', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (132, '倍速线', 'PARTNERS  H220727-CM02-3.9m', '', 'pcs', 423.40, 'standard', '承重：500kg/m,2.5倍速', '工装板宽度540mm,线体长度3900mm', '速度：15~20M/min, 功率750W', 'active', '2026-07-13 07:30:56.362504', 'SX30020008', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (133, '倍速线', 'PARTNERS  H220727-CM02-5.5m', '', 'pcs', 1991.40, 'standard', '承重：500kg/m,2.5倍速', '工装板宽度540mm,线体长度5500mm', '速度：15~20M/min, 功率750W', 'active', '2026-07-13 07:30:56.364424', 'SX30020009', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (134, '倍速线', 'PARTNERS  SP2-1-Wp480-L3000-M700-V16-OL-D1-E', '', 'pcs', 1677.80, 'standard', '承重700kg,  2.5倍速', '工装板宽度480mm,线体长度3000mm', '速度：5~16M/min, 功率750W', 'active', '2026-07-13 07:30:56.365689', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (135, '皮带线', 'MODULAR-B1100-M10-L2000-W200-H800-A-I-220-20-V-C-N2-S1-P1', '', 'pcs', 1070.20, 'standard', '承重：10kg/m,', '皮带宽度200mm,线体长度2000mm', '速度：20M/min,', 'active', '2026-07-13 07:30:56.366889', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (136, '皮带线', 'MODULAR-B3100-M20-L2000-W400-H800-A-I-220-20-V-C-N2-S1-P1', '', 'pcs', 2211.90, 'standard', '承重：20kg/m,', '皮带宽度400mm,线体长度2000mm', '速度：20M/min,', 'active', '2026-07-13 07:30:56.36804', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (137, '皮带线', 'PARTNERS SBC2-W558-L700-H995-M10-N2', '', 'pcs', 3936.70, 'standard', '承重：10KG', '扭矩9.2NM', '速度：15~20M/min', 'active', '2026-07-13 07:30:56.36983', 'SX30025714', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (138, '标准电夹爪', 'SCHUNK EGA-W 40-050-P-N-B', '', 'pcs', 560.60, 'standard', '夹持力：1300N', '开合行程：50mm(单边)', '手指最大长度：500mm', 'active', '2026-07-13 07:30:56.371003', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (139, '标准电夹爪', 'ZIMMER GEH6040IL-03-B', '', 'pcs', 4059.20, 'standard', '夹持力：1000N', '开合行程：40mm(单边)', '手指最大长度：100mm', 'active', '2026-07-13 07:30:56.372725', 'SX30030774', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (140, '标准电夹爪', 'ZIMMER KAG500IL', '', 'pcs', 3383.00, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.374416', 'SX30030776', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (141, '标准电夹爪', 'ZIMMER SCM-C-00-00-A', '', 'pcs', 766.40, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.376101', 'SX30030778', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (142, '标准电夹爪', 'ZIMMER GEH6040IL-31-B', '', 'pcs', 2481.40, 'standard', '夹持力：180N', '开合行程：40mm(单边)', '手指最大长度：100mm', 'active', '2026-07-13 07:30:56.377924', 'SX30018202', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (143, '电缸模组', '费斯托 :Festo ESBF-40-250-5P-A', '', 'pcs', 4098.40, 'standard', '额定推力900N', '有效行程：250mm', '运行速度V：Max.330mm/s', 'active', '2026-07-13 07:30:56.379046', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (144, '电缸模组', '艾卫迈: IAI RCS2-SRA7BD-I-150-4-250-T2-M', '', 'pcs', 3711.30, 'standard', '额定推力916N', '有效行程：250mm', '运行速度V：Max.200mm/s', 'active', '2026-07-13 07:30:56.380683', 'SX30019852', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (145, '电缸模组', '汇川： LY-40-05-250（+MS1H 400W + SV660N）', '', 'pcs', 4093.50, 'standard', '额定推力1000N', '有效行程：250mm', '运行速度V：Max.250mm/s', 'active', '2026-07-13 07:30:56.381796', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (146, '伺服电机', 'SIEMENS IFL2203-2AG10-1MC0', '', 'pcs', 2148.20, 'standard', '额定转矩：0.64 N·m', '转速：3000 rpm', '功率：200W', 'active', '2026-07-13 07:30:56.383474', 'SX30031991', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (147, '伺服电机', 'SIEMENS IFL2203-4AG10-1MC0', '', 'pcs', 2236.40, 'standard', '额定转矩：1.27 N·m', '转速：3000 rpm', '功率：400W', 'active', '2026-07-13 07:30:56.385073', 'SX30031993', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (148, '伺服电机', 'SIEMENS IFL2204-2AG10-1MC0', '', 'pcs', 1971.80, 'standard', '额定转矩：2.4 N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.386746', 'SX30031994', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (149, '伺服电机', 'AB(客指) MPL-A1520U-VJ72AA', '', 'pcs', 1668.00, 'standard', '额定转矩：0.46 N·m', '转速：3000 rpm', '功率：150W', 'active', '2026-07-13 07:30:56.387857', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (150, '伺服电机', 'AB(客指)  MPL-A4530F-MJ74AA', '', 'pcs', 1819.90, 'standard', '额定转矩：1.24 N·m', '转速：3000 rpm', '功率：390W', 'active', '2026-07-13 07:30:56.389103', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (151, '伺服电机', 'AB(客指)  MPL-A4540F-MK74AA', '', 'pcs', 4113.10, 'standard', '额定转矩：2.4 N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.39029', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (152, '伺服电机', 'Beckhoff AM3022', '', 'pcs', 2461.80, 'standard', '额定转矩：0.84 N·m', '转速：3000 rpm', '功率：220W', 'active', '2026-07-13 07:30:56.391644', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (153, '伺服电机', 'Beckhoff AM1022', '', 'pcs', 2564.70, 'standard', '额定转矩：1.34 N·m', '转速：3000 rpm', '功率：400W', 'active', '2026-07-13 07:30:56.393161', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (154, '伺服电机', 'Beckhoff AM1032', '', 'pcs', 590.00, 'standard', '额定转矩：2.55 N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.395405', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (155, '伺服电机', 'FESTO EMMS-AS-40-SK-LS-AMB-S1', '', 'pcs', 4637.40, 'standard', '额定转矩：1.91N·m', '转速：3000 rpm', '功率：200W', 'active', '2026-07-13 07:30:56.396781', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (156, '伺服电机', 'Festo EMMS-AS-40-M-LS-RMB', '', 'pcs', 4990.20, 'standard', '额定转矩：1.5N·m', '转速：3000 rpm', '功率：400W', 'active', '2026-07-13 07:30:56.398243', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (157, '伺服电机', 'Festo EMMS-AS-55-M-LS-RMB', '', 'pcs', 1016.30, 'standard', '额定转矩：1.4N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.400067', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (158, '伺服电机', 'ABB ESM06X-201-302-T2B1A00', '', 'pcs', 1717.00, 'standard', '额定转矩：0.64N·m', '转速：3000 rpm', '功率：200W', 'active', '2026-07-13 07:30:56.401555', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (159, '伺服电机', 'ABB ESM06X-401-302-T2B1A00', '', 'pcs', 2643.10, 'standard', '额定转矩：1.27N·m', '转速：3000 rpm', '功率：400W', 'active', '2026-07-13 07:30:56.403199', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (160, '伺服电机', 'ABB ESM06X-751-302-T2B1A00', '', 'pcs', 4020.00, 'standard', '额定转矩：2.39N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.404857', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (161, '伺服电机', '汇川： INOVANCE MS1H4-20B30CB-A334R', '', 'pcs', 3647.60, 'standard', '额定转矩：0.64N·m', '转速：3000 rpm', '功率：200W', 'active', '2026-07-13 07:30:56.407533', 'SX30028546', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (162, '伺服电机', '汇川： INOVANCE MS1H4-40B30CB-A334R', '', 'pcs', 4985.30, 'standard', '额定转矩：1.27N·m', '转速：3000 rpm', '功率：400W', 'active', '2026-07-13 07:30:56.410065', 'SX30031088', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (163, '伺服电机', '汇川： INOVANCE MS1H4-75B30CB-A334R', '', 'pcs', 129.40, 'standard', '额定转矩：2.39N·m', '转速：3000 rpm', '功率：750W', 'active', '2026-07-13 07:30:56.412717', 'SX30032234', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (164, '直线导轨', 'Rexroth R160510431（ R1605 Size15 N级精度，切600mm）', '', 'pcs', 2314.80, 'standard', '轨道宽度:15mm', '长度：600', '精度等级：N级', 'active', '2026-07-13 07:30:56.414511', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (165, '直线导轨', 'Rexroth R160520331（ R1605 Size20, N级精度，切600mm）', '', 'pcs', 4676.60, 'standard', '轨道宽度:20mm', '长度：600', '精度等级：N级', 'active', '2026-07-13 07:30:56.416318', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (166, '直线导轨', 'Rexroth R160520431 （R1605 Size25, N级精度,切600mm）', '', 'pcs', 4230.70, 'standard', '轨道宽度:25mm', '长度：650', '精度等级：N级', 'active', '2026-07-13 07:30:56.418014', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (167, '直线导轨', 'Rexroth R160570431 （R1605 Size30, N级精度,切700mm）', '', 'pcs', 4167.00, 'standard', '轨道宽度:30mm', '长度：700', '精度等级：N级', 'active', '2026-07-13 07:30:56.419742', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (168, '直线导轨', 'THK SSR15XW2SS+750LG=15', '', 'pcs', 2084.50, 'standard', '轨道宽度:15mm', '长度：750', '精度等级：普通', 'active', '2026-07-13 07:30:56.422221', '30302642', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (169, '直线导轨', 'THK SSR20XW2UUC1-800LP-II G1=G2=10', '', 'pcs', 2265.80, 'standard', '轨道宽度:20mm', '长度：800', '精度等级：普通', 'active', '2026-07-13 07:30:56.42492', 'SX30005710', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (170, '直线导轨', 'THK SSR25XV2UUM-1060LF  G1=G2=20', '', 'pcs', 3216.40, 'standard', '轨道宽度:25mm', '长度：1060', '精度等级：普通', 'active', '2026-07-13 07:30:56.427652', 'SX30004052', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (171, '直线导轨', 'THK SSR30XV2UUM-1420L G1=G2=30', '', 'pcs', 732.10, 'standard', '轨道宽度:30mm', '长度：1420', '精度等级：普通', 'active', '2026-07-13 07:30:56.430178', 'SX30005372', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (172, '直线导轨', 'HIWIN HGH15CA2R600Z0C E1=E2=30', '', 'pcs', 2437.30, 'standard', '轨道宽度:15mm', '长度：600', '精度等级：C', 'active', '2026-07-13 07:30:56.433421', 'SX30013601', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (173, '直线导轨', 'HIWIN HGH20CA2R600ZAH E1=E2=30', '', 'pcs', 3275.20, 'standard', '轨道宽度:20mm', '长度：600', '精度等级：H', 'active', '2026-07-13 07:30:56.435929', 'SX30011704', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (174, '直线导轨', 'HIWIN HGH25CA2R650Z0C E=25', '', 'pcs', 2226.60, 'standard', '轨道宽度:25mm', '长度：650', '精度等级：C', 'active', '2026-07-13 07:30:56.438196', 'SX30028995', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (175, '直线导轨', 'HIWIN HGW30HC2R700Z0C E1=30 E2=30', '', 'pcs', 4211.10, 'standard', '轨道宽度:30mm', '长度：700', '精度等级：C', 'active', '2026-07-13 07:30:56.439851', 'SX30018145', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (176, '直线导轨', 'HIWIN EGH15CA2R600Z0C E1=E2=30', '', 'pcs', 4862.80, 'standard', '轨道宽度:15mm', '长度：600', '精度等级：C', 'active', '2026-07-13 07:30:56.441638', 'SX30028579', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (177, '直线导轨', 'HIWIN EGH20CA2R600ZAH E1=20 E2=40', '', 'pcs', 820.30, 'standard', '轨道宽度:20mm', '长度：600', '精度等级：H', 'active', '2026-07-13 07:30:56.443274', 'SX30004802', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (178, '直线导轨', 'HIWIN EGH25CA2R640ZAH', '', 'pcs', 4176.80, 'standard', '轨道宽度:25mm', '长度：640', '精度等级：H', 'active', '2026-07-13 07:30:56.444913', 'SX30002340', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (179, '直线导轨', 'HIWIN EGH30SA2R500Z0C E1=E2=10', '', 'pcs', 1829.70, 'standard', '轨道宽度:30mm', '长度：500', '精度等级：C', 'active', '2026-07-13 07:30:56.446507', 'SX30014424', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (180, '坦克链', 'IGUS E6.29.070.100.0-EE.290.070.12.A 946mm', '', 'pcs', 3686.80, 'standard', '内腔尺寸：高29mm,宽70mm', '弯曲半径:R100mm', '行程长度:946mm', 'active', '2026-07-13 07:30:56.448144', 'SX30003402', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (181, '坦克链', 'IGUS E6.29.070.100.0-EE.290.070.12.A 1518mm', '', 'pcs', 859.50, 'standard', '内腔尺寸：高29mm,宽70mm', '弯曲半径:R100mm', '行程长度:946mm', 'active', '2026-07-13 07:30:56.449786', 'SX30003401', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (182, '坦克链', 'IGUS 14040.27.150.0X20-141400.27.12.C.A2-56.1.1.1X50-3075.ZCX8', '', 'pcs', 668.40, 'standard', '内腔尺寸：高27mm,宽150mm', '弯曲半径:R150mm', '行程长度:1820mm', 'active', '2026-07-13 07:30:56.451433', 'SX30029142', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (183, '坦克链', 'KODUCT CDP028W50R38-L1000', '', 'pcs', 1888.50, 'standard', '内腔尺寸：高19mm,宽50mm', '弯曲半径:R38mm', '行程长度:1000mm', 'active', '2026-07-13 07:30:56.453179', 'SX30023222', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (184, '坦克链', 'KODUCT KDP040W80R50-L1000', '', 'pcs', 1276.00, 'standard', '内腔尺寸：高25mm,宽80mm', '弯曲半径:R50mm', '行程长度:1000mm', 'active', '2026-07-13 07:30:56.454845', 'SX30023223', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (185, '坦克链', 'KODUCT CDPS070W120R200-L7000', '', 'pcs', 4010.20, 'standard', '内腔尺寸：高49mm,宽120mm', '弯曲半径:R200mm', '行程长度:7000mm', 'active', '2026-07-13 07:30:56.456496', 'SX30005030', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (186, '直线模组', 'THK KR2602A-0160-0-00A0', '', 'pcs', 2354.00, 'standard', '丝杆外径φ8mm', '导程2mm', '轨道长250mm,行程160mm', 'active', '2026-07-13 07:30:56.458084', '30332851', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (187, '直线模组', 'THK KR2606A-0110-0-00A0', '', 'pcs', 1756.20, 'standard', '丝杆外径φ8mm', '导程6mm', '轨道长200mm,行程110mm', 'active', '2026-07-13 07:30:56.459741', 'SX30004753', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (188, '直线模组', 'THK KR3306A-0500-0-00A0', '', 'pcs', 4436.50, 'standard', '丝杆外径φ10mm', '导程6mm', '轨道长600mm,行程500mm', 'active', '2026-07-13 07:30:56.461365', '30304124', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (189, '直线模组', 'THK KR3310A-0600-0-10A0', '', 'pcs', 2412.80, 'standard', '丝杆外径φ10mm', '导程10mm', '轨道长700mm,行程600mm', 'active', '2026-07-13 07:30:56.462999', '30304451', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (190, '直线模组', 'THK KR4610A-0490-0-00A0', '', 'pcs', 4470.80, 'standard', '丝杆外径φ12mm', '导程10mm', '轨道长640mm,行程490mm', 'active', '2026-07-13 07:30:56.464584', '30324457', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (191, '直线模组', 'THK KR4620A-0790-0-00A0', '', 'pcs', 1427.90, 'standard', '丝杆外径φ12mm', '导程20mm', '轨道长940mm,行程790mm', 'active', '2026-07-13 07:30:56.466191', '30324458', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (192, '直线模组', 'THK KR6525A-1490-0-00A0', '', 'pcs', 2442.20, 'standard', '丝杆外径φ20mm', '导程25mm', '轨道长1680mm,行程1490mm', 'active', '2026-07-13 07:30:56.468017', 'SX30004756', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (193, '直线模组', 'HIWIN  KK4001P-150A1-F0CS2', '', 'pcs', 1957.10, 'standard', '丝杆外径φ8mm', '导程1mm', '轨道长150mm,行程86mm', 'active', '2026-07-13 07:30:56.469579', 'SX30028538', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (194, '直线模组', 'HIWIN  KK4001C-150A1-F0CS2', '', 'pcs', 4225.80, 'standard', '丝杆外径φ8mm', '导程1mm', '轨道长150mm,行程86mm', 'active', '2026-07-13 07:30:56.471187', 'SX30012266', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (195, '直线模组', 'HIWIN  KK5002P-200A1-F0', '', 'pcs', 1089.80, 'standard', '丝杆外径φ8mm', '导程2mm', '轨道长200mm,行程120mm', 'active', '2026-07-13 07:30:56.472822', '30307890', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (196, '直线模组', 'HIWIN  KK5002C-200A1-F0', '', 'pcs', 232.30, 'standard', '丝杆外径φ8mm', '导程2mm', '轨道长200mm,行程120mm', 'active', '2026-07-13 07:30:56.474631', '30307819', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (197, '直线模组', 'HIWIN KK60D10P-300A1-H0CS2', '', 'pcs', 3628.00, 'standard', '丝杆外径φ12mm（出轴φ8）', '导程10mm', '轨道长300mm,行程210mm', 'active', '2026-07-13 07:30:56.476612', 'SX30011149', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (198, '直线模组', 'HIWIN KK6010C-300A1-H0CS2', '', 'pcs', 4647.20, 'standard', '丝杆外径φ12mm（出轴φ8）', '导程10mm', '轨道长300mm,行程210mm', 'active', '2026-07-13 07:30:56.478439', '30301511', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (199, '直线模组', 'HIWIN KK86D10C-940A1-F0CS2', '', 'pcs', 207.80, 'standard', '丝杆外径φ14mm', '导程10mm', '轨道长940mm,行程810mm', 'active', '2026-07-13 07:30:56.480261', 'SX30018190', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (200, '直线模组', 'HIWIN KK8610P-540A1-F0CS2', '', 'pcs', 2648.00, 'standard', '丝杆外径φ14mm', '导程10mm', '轨道长540mm,行程410mm', 'active', '2026-07-13 07:30:56.482008', 'SX30028525', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (201, '直线模组', 'HIWIN KK86D20C-940A1-F0CS2', '', 'pcs', 3824.00, 'standard', '丝杆外径φ16mm', '导程20mm', '轨道长940mm,行程810mm', 'active', '2026-07-13 07:30:56.484345', '30330476', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (202, '直线模组', 'HIWIN KK86D20C-540A1-F0CS2', '', 'pcs', 634.10, 'standard', '丝杆外径φ16mm', '导程20mm', '轨道长540mm,行程410mm', 'active', '2026-07-13 07:30:56.486748', 'SX30020733', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (203, '直线模组', 'HIWIN KK10020C-1180A1-F0CS2', '', 'pcs', 3897.50, 'standard', '丝杆外径φ20mm', '导程20mm', '轨道长1180mm,行程1028mm', 'active', '2026-07-13 07:30:56.488998', 'SX30004666', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (204, '直线模组', 'HIWIN KK13025C-1680A1-F0CS2', '', 'pcs', 4882.40, 'standard', '丝杆外径φ25mm', '导程25mm', '轨道长1680mm,行程1510mm', 'active', '2026-07-13 07:30:56.491232', 'SX30004977', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (205, '直线模组', 'HIWIN KK13025C-980A1-F0CS2', '', 'pcs', 3436.90, 'standard', '丝杆外径φ25mm', '导程25mm', '轨道长980mm,行程811mm', 'active', '2026-07-13 07:30:56.493624', 'SX30011304', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (206, '直线模组', 'LIMON  KS40-01P-150A1-F0CS1', '', 'pcs', 1060.40, 'standard', '丝杆外径φ8mm', '导程1mm', '轨道长150mm,行程86mm', 'active', '2026-07-13 07:30:56.496252', 'SX30028539', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (207, '直线模组', 'LIMON  KS60D10C-300A1-F0CS2', '', 'pcs', 3750.50, 'standard', '丝杆外径φ12mm', '导程10mm', '轨道长300mm,行程210mm', 'active', '2026-07-13 07:30:56.498824', 'SX30011910', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (208, '直线模组', 'LIMON  KS86D-10-C-540-A-1-F0-C-S1', '', 'pcs', 4034.70, 'standard', '丝杆外径φ15mm', '导程10mm', '轨道长540mm,行程410mm', 'active', '2026-07-13 07:30:56.501414', 'SX30024935', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (209, '直线模组', 'LIMON  KS86D20C-540A1-F0CS2', '', 'pcs', 149.00, 'standard', '丝杆外径φ15mm', '导程20mm', '轨道长540mm,行程410mm', 'active', '2026-07-13 07:30:56.504021', 'SX30011912', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (210, '直线模组', 'LIMON  KS86D20C-940A1-F0CS2', '', 'pcs', 3926.90, 'standard', '丝杆外径φ15mm', '导程20mm', '轨道长940mm,行程810mm', 'active', '2026-07-13 07:30:56.506638', 'SX30011914', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (299, 'PLC控制器', 'AB 1769-IQ32', '', 'pcs', 2726.40, 'standard', NULL, NULL, '32位输入', 'active', '2026-07-13 07:30:56.711004', '30203661', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (211, '直线模组', 'LIMON  KS10020C-980A2-T0C ML', '', 'pcs', 4299.30, 'standard', '丝杆外径φ20mm', '导程20mm', '轨道长980mm,行程828mm', 'active', '2026-07-13 07:30:56.5094', 'SX30024131', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (212, '直线模组', 'LIMON  YSO100-L10-250-2P-MR-M40-P3', '', 'pcs', 2667.60, 'standard', '丝杆外径φ16mm', '导程10mm', '轨道长365mm,行程250mm', 'active', '2026-07-13 07:30:56.512723', 'SX30023277', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (213, '直线模组', 'LIMON  YSO100-L10-700-1P-ML-M40-P3', '', 'pcs', 4093.50, 'standard', '丝杆外径φ16mm', '导程10mm', '轨道长810mm,行程700mm', 'active', '2026-07-13 07:30:56.515623', 'SX30023278', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (214, '直线模组', 'LIMON  YSO100-L20-250-2P-MR-M40-P3', '', 'pcs', 3324.20, 'standard', '丝杆外径φ16mm', '导程20mm', '轨道长365mm,行程250mm', 'active', '2026-07-13 07:30:56.518327', 'SX30023320', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (215, '直线模组', 'LIMON  YSO100-L20-1050-2P-MS-M40-P3', '', 'pcs', 1815.00, 'standard', '丝杆外径φ16mm', '导程20mm', '轨道长1160mm,行程1050mm', 'active', '2026-07-13 07:30:56.521234', 'SX30025849', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (216, '直线模组', 'LIMON  YSO135-L10-300-4P-ML-M20-P3', '', 'pcs', 1138.80, 'standard', '丝杆外径φ16mm', '导程10mm', '轨道长430mm,行程300mm', 'active', '2026-07-13 07:30:56.523855', 'SX30023322', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (307, 'PLC控制器', 'AB 1756-IB32', '', 'pcs', 1864.00, 'standard', NULL, NULL, '32位输入', 'active', '2026-07-13 07:30:56.732442', '30209278', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (217, '直线模组', 'LIMON  YSO135-L10-700-4P-ML-M20-P3', '', 'pcs', 3485.90, 'standard', '丝杆外径φ16mm', '导程10mm', '轨道长830mm,行程700mm', 'active', '2026-07-13 07:30:56.526571', 'SX30022748', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (218, '直线模组', 'LIMON  YSO135-L20-700-4P-ML-M40-P3', '', 'pcs', 247.00, 'standard', '丝杆外径φ16mm', '导程20mm', '轨道长830mm,行程700mm', 'active', '2026-07-13 07:30:56.529219', 'SX30023323', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (219, '直线模组', 'LIMON  YSO170-L10-400-4P-ML-M40-P3', '', 'pcs', 751.70, 'standard', '丝杆外径φ20mm', '导程10mm', '轨道长530mm,行程400mm', 'active', '2026-07-13 07:30:56.531771', 'SX30022749', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (220, '直线模组', 'LIMON  YSO170-L10-700-4P-ML-M40-P3', '', 'pcs', 3642.70, 'standard', '丝杆外径φ20mm', '导程10mm', '轨道长830mm,行程700mm', 'active', '2026-07-13 07:30:56.534364', 'SX30028722', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (221, '直线模组', 'LIMON  YSO220-L10-650-4P-MS-M40-P3', '', 'pcs', 830.10, 'standard', '丝杆外径φ25mm', '导程10mm', '轨道长800mm,行程650mm', 'active', '2026-07-13 07:30:56.536881', 'SX30023215', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (222, '直线模组', 'LIMON  YSO220-L10-1000-4P-ML-M75-P3', '', 'pcs', 1109.40, 'standard', '丝杆外径φ25mm', '导程10mm', '轨道长1150mm,行程1000mm', 'active', '2026-07-13 07:30:56.539412', 'SX30028681', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (223, '直线模组', 'LIMON  YSO220-L25-650-4P-MS-VB090-P3', '', 'pcs', 261.70, 'standard', '丝杆外径φ25mm', '导程10mm', '轨道长800mm,行程650mm', 'active', '2026-07-13 07:30:56.541961', 'SX30023346', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (224, '直线模组', 'LIMON  YSC170-L10-350-4P-ML-M75-P3', '', 'pcs', 2403.00, 'standard', '丝杆外径φ20mm', '导程10mm', '轨道长500mm,行程30mm', 'active', '2026-07-13 07:30:56.544455', 'SX30024674', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (225, '直线模组', 'LIMON  YSC170-L10-900-4P-ML-M75-P3', '', 'pcs', 364.60, 'standard', '丝杆外径φ20mm', '导程10mm', '轨道长1050mm,行程900mm', 'active', '2026-07-13 07:30:56.547297', 'SX30022985', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (226, '直线模组', 'LIMON  YTO135-800-4P-D01-M40-P3', '', 'pcs', 4284.60, 'standard', '同步带（HTD 5M高刚性闭合带）', '最高速度1.5M/s', '轨道长950mm,行程800mm', 'active', '2026-07-13 07:30:56.549845', 'SX30011832', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (227, '直线模组', 'LIMON  YTO135-1150-4P-D01-M20-P3', '', 'pcs', 3005.70, 'standard', '同步带（HTD 5M高刚性闭合带）', '最高速度1.5M/s', '轨道长1300mm,行程1150mm', 'active', '2026-07-13 07:30:56.552439', 'SX30022722', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (228, '直线模组', 'LIMON  YTO170-800-4P-D01-M40-P3', '', 'pcs', 4461.00, 'standard', '同步带（HTD 5M高刚性闭合带）', '最高速度1.5M/s', '轨道长950mm,行程800mm', 'active', '2026-07-13 07:30:56.554963', 'SX30011824', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (229, '直线模组', 'LIMON  YTO170-1300-4P-D01-M40-P3', '', 'pcs', 3368.30, 'standard', '同步带（HTD 5M高刚性闭合带）', '最高速度1.5M/s', '轨道长1460mm,行程1300mm', 'active', '2026-07-13 07:30:56.557543', 'SX30023179', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (230, '直线模组', 'LIMON  YTO220-1350-4P-D01-M75-P3', '', 'pcs', 2971.40, 'standard', '同步带（HTD 5M高刚性闭合带）', '最高速度2M/s', '轨道长1510mm,行程1350mm', 'active', '2026-07-13 07:30:56.560028', 'SX30023316', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (231, '丝杆', 'THK BNK1520-3G0-421LC5Y', '', 'pcs', 3476.10, 'standard', '外径φ15mm', '导程20mm', '总长421mm', 'active', '2026-07-13 07:30:56.562597', 'SX30003349', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (232, '丝杆', 'THK BNK1520-3G0-908.5LC5Y', '', 'pcs', 3373.20, 'standard', '外径φ15mm', '导程20mm', '总长908.5mm', 'active', '2026-07-13 07:30:56.56505', 'SX30003346', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (233, '丝杆', 'THK BNK1510-5.6G0-778LC5Y', '', 'pcs', 3936.70, 'standard', '外径φ15mm', '导程10mm', '总长371mm', 'active', '2026-07-13 07:30:56.567081', 'SX30005110', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (234, '丝杆', 'THK BLK1616-3.6UU+255LC7-60-0', '', 'pcs', 3877.90, 'standard', '外径φ16mm', '导程16mm', '总长255mm', 'active', '2026-07-13 07:30:56.568836', 'SX30020671', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (235, '丝杆', 'THK BLK1616-3.6ZZ-800LT', '', 'pcs', 3789.70, 'standard', '外径φ16mm', '导程16mm', '总长800mm', 'active', '2026-07-13 07:30:56.570515', 'SX30005408', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (236, '丝杆', 'THK BLK2020-3.6ZZ-1407L-C7T', '', 'pcs', 913.40, 'standard', '外径φ20mm', '导程20mm', '总长1407mm', 'active', '2026-07-13 07:30:56.572312', 'SX30005373', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (237, '丝杆', 'THK BNF2505-5RRG0-500LC3-J2K', '', 'pcs', 4764.80, 'standard', '外径φ25mm', '导程5mm', '总长500mm', 'active', '2026-07-13 07:30:56.57395', 'SX30009123', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (238, '丝杆', 'THK BLK2525-3.6G0-797LC7', '', 'pcs', 3868.10, 'standard', '外径φ25mm', '导程25mm', '总长797mm', 'active', '2026-07-13 07:30:56.576437', 'SX30010195', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (239, '丝杆', 'HIWIN R16-10T3-FSI-400-460-0.05', '', 'pcs', 2305.00, 'standard', '外径φ16mm', '导程10mm', '总长460mm(螺纹长400)', 'active', '2026-07-13 07:30:56.578248', '30323752', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (240, '丝杆', 'HIWIN R20-5T3-FSI-600-700-0.05', '', 'pcs', 2368.70, 'standard', '外径φ20mm', '导程5mm', '总长700mm(螺纹长600)', 'active', '2026-07-13 07:30:56.580017', 'SX30013487', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (241, '丝杆', 'HIWIN R20-10T3-FSI-944-1000-0.05', '', 'pcs', 634.10, 'standard', '外径φ20mm', '导程10mm', '总长1000mm(螺纹长944)', 'active', '2026-07-13 07:30:56.58199', 'SX30021676', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (242, '丝杆', 'HIWIN R25-10K3-FSI-950-1049-0.05', '', 'pcs', 1011.40, 'standard', '外径φ25mm', '导程10mm', '总长1049mm(螺纹长950)', 'active', '2026-07-13 07:30:56.584589', 'SX30028762', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (243, '丝杆', 'HIWIN R25-10T3-FSI-1640-1757-0.05', '', 'pcs', 2427.50, 'standard', '外径φ25mm', '导程10mm', '总长1757mm(螺纹长1640)', 'active', '2026-07-13 07:30:56.587152', 'SX30011078', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (244, '丝杆', 'HIWIN R32-5T3-FSI-1073-1189-0.05', '', 'pcs', 1677.80, 'standard', '外径φ32mm', '导程5mm', '总长1189mm(螺纹长1073)', 'active', '2026-07-13 07:30:56.589717', 'SX30010986', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (245, '丝杆', 'TBI BSHR1002-FCA-400-P0-348.5-1', '', 'pcs', 1329.90, 'standard', '外径φ10mm', '导程2mm', '总长400mm(螺纹长348.5)', 'active', '2026-07-13 07:30:56.592293', 'SX30003519', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (246, '丝杆', 'TBI SFNIR1605-DFCA-555-P1', '', 'pcs', 4412.00, 'standard', '外径φ16mm', '导程5mm', '总长555mm', 'active', '2026-07-13 07:30:56.594821', 'SX30008996', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (247, '丝杆', 'TBI SFNHR1610B1-DFCA-610-P0', '', 'pcs', 188.20, 'standard', '外径φ16mm', '导程10mm', '总长610mm', 'active', '2026-07-13 07:30:56.597355', 'SX30002559', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (248, '丝杆', 'TBI  SFVR2005D1D-DFC7-L499-P0.5', '', 'pcs', 1790.50, 'standard', '外径φ20mm', '导程5mm', '总长499mm', 'active', '2026-07-13 07:30:56.600021', 'SX30001108', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (249, '丝杆', 'TBI RS SFBR02010C1DFC7-795-P0', '', 'pcs', 2285.40, 'standard', '外径φ20mm', '导程10mm', '总长795mm', 'active', '2026-07-13 07:30:56.602912', 'SX30031733', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (250, '丝杆', 'TBI GSFHR02510DS-L949-P1', '', 'pcs', 2236.40, 'standard', '外径φ25mm', '导程10mm', '总长949mm', 'active', '2026-07-13 07:30:56.605516', 'SX30023205', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (251, '丝杆', 'TBI GSFHR02510DS-L1224-P1', '', 'pcs', 2893.00, 'standard', '外径φ25mm', '导程10mm', '总长1224mm', 'active', '2026-07-13 07:30:56.608052', 'SX30023204', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (252, '丝杆', 'TBI GSFHR02525DS-L1224-P1', '', 'pcs', 2501.00, 'standard', '外径φ25mm', '导程25mm', '总长1224mm', 'active', '2026-07-13 07:30:56.610633', 'SX30023347', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (253, '丝杆', 'TBI GSFHR03210DS-L902-P1', '', 'pcs', 3569.20, 'standard', '外径φ32mm', '导程10mm', '总长902mm', 'active', '2026-07-13 07:30:56.613242', 'SX30023206', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (254, '丝杆', 'TBI SFHR03220BDF-C7-982-P1', '', 'pcs', 3598.60, 'standard', '外径φ32mm', '导程20mm', '总长982mm', 'active', '2026-07-13 07:30:56.615859', 'SX30023435', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (255, '丝杆', 'TBI RS SFURL3210-L298.5-R298.5-DFC7-799', '', 'pcs', 2162.90, 'standard', '外径φ32mm', '导程10mm', '总长799mm（左螺纹长298.5，右螺纹长298.5）', 'active', '2026-07-13 07:30:56.619072', 'SX30028675', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (256, '丝杆', 'TBI RS SFURL3210-L298.5-R298.5-DFC7-772', '', 'pcs', 849.70, 'standard', '外径φ32mm', '导程10mm', '总长772mm（左螺纹长298.5，右螺纹长298.5）', 'active', '2026-07-13 07:30:56.621651', 'SX30028664', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (257, '2D相机', 'COGNEX CAM-CIC-5000-20', '', 'pcs', 3044.90, 'standard', '5M, 24fps,', '全局', '2/3"， 2448 x 2048， 3.45 x 3.45', 'active', '2026-07-13 07:30:56.624225', 'SX20000711', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (258, '2D相机', 'COGNEX CAM-CIC-12MR', '', 'pcs', 3187.00, 'standard', '12.4M, 8fps, 黑白', '卷帘', '1/1.7"，  4000 x 3000 ， 1.85 x 1.85', 'active', '2026-07-13 07:30:56.626847', 'SX20000712', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (259, '2D相机', 'OPT OPT-FJM200G-4L', '', 'pcs', 3035.10, 'standard', '20M,  5.9fps,黑白', '卷帘', '1＂,5472 × 3648,2.4u × 2.4u', 'active', '2026-07-13 07:30:56.629461', 'SX20003427', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (260, '2D相机', 'OPT OPT-FJM120G-4M', '', 'pcs', 844.80, 'standard', '12M，9.6fps, 黑白', '全局', '1.1＂，4096 × 3072，3.4u × 3.4u', 'active', '2026-07-13 07:30:56.6322', 'SX20003967', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (261, '2D相机', 'OPT OPT-FJC200G-4L', '', 'pcs', 629.20, 'standard', '20M， 5.9fps, 彩色', '卷帘', '1＂,5472 × 3648,2.4u × 2.4u', 'active', '2026-07-13 07:30:56.634805', 'SX20005950', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (262, '2D相机', 'OPT OPT-FJC650G-4M', '', 'pcs', 4706.00, 'standard', '65M, 18fps, 彩色', '全局', '29.9 mm × 22.4 mm， 9344 × 7000，3.2 µm × 3.2 µm', 'active', '2026-07-13 07:30:56.637412', 'SX20006087', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (263, '2D相机', 'HIKVISION MV-CE100-30GM', '', 'pcs', 232.30, 'standard', '10M,30fps, 黑白', '卷帘', '1/2.3”， 3840×2748，1.67 µm × 1.67 µm', 'active', '2026-07-13 07:30:56.639879', '30502050', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (264, '2D相机', 'HIKVISION MV-CU120-10GM', '', 'pcs', 2314.80, 'standard', '12M, 10fps, 黑白', '卷帘', '1/1.7''''，  4024 × 3036，  1.85 μm × 1.85 μm', 'active', '2026-07-13 07:30:56.64268', 'SX20006545', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (265, '2D相机', 'HIKVISION MV-CE200-10GM', '', 'pcs', 2427.50, 'standard', '20M, 10fps, 黑白', '卷帘', '1”，  5472 × 3648， 2.4 μm × 2.4 μm', 'active', '2026-07-13 07:30:56.645308', 'SX20000800', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (266, '2D相机', 'basler basler-acA3800-10gm', '', 'pcs', 3079.20, 'standard', '10M, 10fps, 黑白', '卷帘', '1/2.3", 3840 × 2748，1.67um×1.67um', 'active', '2026-07-13 07:30:56.647521', '30501482', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (267, '2D相机', 'BASLER acA2500-20gm', '', 'pcs', 996.70, 'standard', '5M，20fps, 黑白', '全局', '1"， 2590× 2048， 4.8 μm × 4.8 μm', 'active', '2026-07-13 07:30:56.649249', '30501727', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (268, '2D相机', 'BASLER basler-ala3800-8gm', '', 'pcs', 4549.20, 'standard', '10M, 8fps, 黑白', '卷帘', '1/2.3", 3840 × 2748，1.67um×1.67um', 'active', '2026-07-13 07:30:56.650983', 'SX20003101', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (269, '条码枪', '康耐视 DMR-262X-1120', '', 'pcs', 3476.10, 'standard', '1DMax, 2DMax, PowerGrid', 'RS-232 and Ethernet Interface', '1280x960, 45fps, 24VDC', 'active', '2026-07-13 07:30:56.652665', '30203435', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (270, '条码枪', 'COGNEX DM262Q', '', 'pcs', 3054.70, 'standard', '1DMax, 2DMax, Hotbars', 'RS-232 and Ethernet Interface', '752 x 480，60 fps，45/sec', 'active', '2026-07-13 07:30:56.654573', '30212079', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (271, '条码枪', '康耐视 DMR-262X-1540-P', '', 'pcs', 800.70, 'standard', '1DMax, 2DMax, PowerGrid', 'RS-232 and Ethernet Interface', '1280x960, 45fps, 24VDC', 'active', '2026-07-13 07:30:56.656578', '30500859', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (272, '条码枪', 'HONEYWELL 3320GHD Ethernet communication', '', 'pcs', 825.20, 'standard', '识读标准的一维、PDF、2D、邮政和 OCR字符。注：解码能力视套件配置而定。', 'USB，RS232', '二维影像(838x640像素) 焦点：127mm', 'active', '2026-07-13 07:30:56.658537', 'SX20003537', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (273, '条码枪', 'HONEYWELL HF800', '', 'pcs', 4843.20, 'standard', '一维条形码，PDF417
二维码：QR Code， Datamatrix，Maxicode,Aztec', 'RS232，RS485和以太网接口', '60fps', 'active', '2026-07-13 07:30:56.6605', 'SX20002407', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (274, '条码枪', 'KEYENCE SR-1000', '', 'pcs', 2868.50, 'standard', '二维码，条形码', 'Ethernet, 串行通信，USB', '110-1000mm，122X97mm【400mm时】', 'active', '2026-07-13 07:30:56.662459', '30200685', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (275, '条码枪', 'KEYENCE SR-2000', '', 'pcs', 3843.60, 'standard', '二维码，条形码', 'Ethernet, 串行通信，USB', '100-2000mm, 800 mm 时:263 x 197 mm', 'active', '2026-07-13 07:30:56.664388', '30502342', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (276, '条码枪', 'KEYENCE SR-X300', '', 'pcs', 3446.70, 'standard', '二维码，条形码', 'Ethernet, 串行通信，USB', '70-1000mm,SR-X300: 104 mm x 65 mm(距离为300mm时)', 'active', '2026-07-13 07:30:56.667855', 'SX20004012', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (277, '条码枪', '', '', 'pcs', 815.40, 'standard', '类型', '通讯接口', NULL, 'active', '2026-07-13 07:30:56.667859', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (278, '条码枪', 'SHIJIE ICW9-8100N-HD', '', 'pcs', 2305.00, 'standard', '一维码，二维码', 'USB COM', NULL, 'active', '2026-07-13 07:30:56.670999', 'SX20001465', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (279, '条码枪', 'SHIJIE ICW70-ER', '', 'pcs', 4103.30, 'standard', '一维码，二维码', 'RS232, USB-virtual-COM, USB-keyboard,
Ethernet', '读码距离：30mm,70mm, 100mm, 150mm,640*480, 60fps', 'active', '2026-07-13 07:30:56.673116', 'SX20001464', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (280, '条码枪', 'SHIJIE ICW-75V-C', '', 'pcs', 1158.40, 'standard', '一维码，二维码，Vericode', 'RS232,RS485,Ethernet,Modbus,Profinet', '读码距离：70mm, 100mm, 150mm, 1280*800, 60fps', 'active', '2026-07-13 07:30:56.67502', 'SX20001439', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (281, 'PLC控制器', 'SIEMENS 6ES7217-1AG40-0XB0', '', 'pcs', 1124.10, 'standard', '紧凑型 CPU', '2 个 PROFINET 接口', '10 DI 24V DC；
4 DI RS-422/485；
 6 DO 24V DC', 'active', '2026-07-13 07:30:56.676893', 'SX20002505', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (282, 'PLC控制器', 'SIEMENS 6ES7223-1BL32-0XB0', '', 'pcs', 2858.70, 'standard', NULL, NULL, '16位输入输出模块', 'active', '2026-07-13 07:30:56.678715', 'SX20002436', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (283, 'PLC控制器', 'SIEMENS 6ES7221-1BH30-0XB0', '', 'pcs', 1374.00, 'standard', NULL, NULL, '16位输入模块', 'active', '2026-07-13 07:30:56.680579', 'SX20003330', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (284, 'PLC控制器', 'SIEMENS 6ES7 222-1BH32-0XB0', '', 'pcs', 536.10, 'standard', NULL, NULL, '16位输出模块', 'active', '2026-07-13 07:30:56.68242', 'SX20004444', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (285, 'PLC控制器', 'SIEMENS S7 1215FC 6ES7215-1AF40-0XB0', '', 'pcs', 1462.20, 'standard', '紧凑型 安全CPU', '2个 PROFINET 接口', '14 个 24VDC 数字输入；
10 个 24VDC 数字输出', 'active', '2026-07-13 07:30:56.683583', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (286, 'PLC控制器', 'SIEMENS 6ES7226-6BA32-0XB0', '', 'pcs', 2986.10, 'standard', NULL, NULL, '16位安全输入模块', 'active', '2026-07-13 07:30:56.684787', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (287, 'PLC控制器', 'SIEMENS 6ES7226-6DA32-0XB0', '', 'pcs', 247.00, 'standard', NULL, NULL, '4位安全输出模块', 'active', '2026-07-13 07:30:56.685918', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (288, 'PLC控制器', 'SIEMENS S7 1513-1 PN 6ES7513-1AM03-0AB0', '', 'pcs', 3833.80, 'standard', '中端标准CPU（必选SD存储卡，安全控制器另配）', '无法组态 F 模块', '无独立 F 程序区', 'active', '2026-07-13 07:30:56.688209', 'SX20002560', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (289, 'PLC控制器', 'SIEMENS 6ES7 505-OKAOO-OABO', '', 'pcs', 3196.80, 'standard', NULL, NULL, '直流24V电源模块', 'active', '2026-07-13 07:30:56.68982', 'SX20003453', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (290, 'PLC控制器', 'SINAMICS S7-1500安装导轨：482mm（6ES7590-1AE80-0AA0）', '', 'pcs', 4265.00, 'standard', NULL, NULL, '482MM安装导轨', 'active', '2026-07-13 07:30:56.691441', '30205971', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (291, 'PLC控制器', 'SIEMENS 6ES7954-8LE04-0AA0', '', 'pcs', 4402.20, 'standard', NULL, NULL, '12M存储卡', 'active', '2026-07-13 07:30:56.693316', 'SX20003786', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (292, 'PLC控制器', 'SIEMENS DI32 BA 6ES7521-1BL10-0AA0', '', 'pcs', 3672.10, 'standard', NULL, NULL, '32位输入模块', 'active', '2026-07-13 07:30:56.695842', 'SX20002563', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (293, 'PLC控制器', 'SIEMENS DQ32 BA 6ES7522-1BL10-0AA0', '', 'pcs', 2231.50, 'standard', NULL, NULL, '32位输出模块', 'active', '2026-07-13 07:30:56.698043', 'SX20002565', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (294, 'PLC控制器', 'SIEMENS S7 1513F-1 PN 6ES7 513-1FL02-0AB0', '', 'pcs', 4020.00, 'standard', '中端安全 CPU（必选SD存储卡，含安全控制器）', '可配套全部安全 IO', '独立安全逻辑分区、CRC 校验', 'active', '2026-07-13 07:30:56.700225', 'SX20005199', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (295, 'PLC控制器', 'SIEMENS 6ES7526-1BH00-0AB0', '', 'pcs', 3412.40, 'standard', NULL, NULL, '16位安全输入模块', 'active', '2026-07-13 07:30:56.701821', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (296, 'PLC控制器', 'SIEMENS 6ES7526-2BF00-0AB0', '', 'pcs', 2569.60, 'standard', NULL, NULL, '8位安全输出模块', 'active', '2026-07-13 07:30:56.70354', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (297, 'PLC控制器', 'AB 1769-L36ERM', '', 'pcs', 1408.30, 'standard', '双百兆网口（支持 DLR）', '16 轴', NULL, 'active', '2026-07-13 07:30:56.705979', '30203658', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (300, 'PLC控制器', 'AB 1769-OB32', '', 'pcs', 4833.40, 'standard', NULL, NULL, '32位输出', 'active', '2026-07-13 07:30:56.713694', '30203662', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (301, 'PLC控制器', 'AB 1769-IF4', '', 'pcs', 1334.80, 'standard', NULL, NULL, '4路模拟量输入', 'active', '2026-07-13 07:30:56.716982', '30203663', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (302, 'PLC控制器', 'AB 1769-ECR', '', 'pcs', 3549.60, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.719716', '30203938', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (303, 'PLC控制器', 'AB 1756-L84E', '', 'pcs', 3794.60, 'standard', '双千兆网口（DLR / 环网）', '24 轴', NULL, 'active', '2026-07-13 07:30:56.722327', '30206050', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (304, 'PLC控制器', 'AB 1756-N2', '', 'pcs', 898.70, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.724776', '30209280', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (305, 'PLC控制器', 'AB 1756-A7', '', 'pcs', 4299.30, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.727327', '30206052', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (308, 'PLC控制器', 'AB 1756-OB32', '', 'pcs', 153.90, 'standard', NULL, NULL, '32位输出', 'active', '2026-07-13 07:30:56.734971', '30209279', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (309, 'PLC控制器', 'AB 5069-L350ERM', '', 'pcs', 986.90, 'standard', '单千兆网口（可扩展 EN2T/EN4T 模块）', '最多256轴', NULL, 'active', '2026-07-13 07:30:56.737534', '30208337', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (310, 'PLC控制器', 'AB 5069-RTB64-SPRING', '', 'pcs', 4911.80, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.740578', '30208338', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (311, 'PLC控制器', 'AB 5069-IB16', '', 'pcs', 2697.00, 'standard', NULL, NULL, '16位输入', 'active', '2026-07-13 07:30:56.743482', '30208339', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (312, 'PLC控制器', 'AB 5069-OB16', '', 'pcs', 2716.60, 'standard', NULL, NULL, '16位输出', 'active', '2026-07-13 07:30:56.746167', '30208340', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (313, 'PLC控制器', 'AB 5069-RTB18-SPRING', '', 'pcs', 4539.40, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.748735', '30208341', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (314, 'PLC控制器', 'KEYENCE KV8000', '', 'pcs', 3971.00, 'standard', '使用定位模块最多64轴', '\', NULL, 'active', '2026-07-13 07:30:56.750698', 'SX20002296', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (315, 'PLC控制器', 'KEYENCE KV-XH16EC', '', 'pcs', 3902.40, 'standard', NULL, NULL, '16轴轴控模块', 'active', '2026-07-13 07:30:56.75238', '30209525', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (316, 'PLC控制器', 'KEYENCE KV-C32XC', '', 'pcs', 3848.50, 'standard', NULL, NULL, '32位输入', 'active', '2026-07-13 07:30:56.753989', '30203450', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (317, 'PLC控制器', 'KEYENCE KV-C32TD', '', 'pcs', 2094.30, 'standard', NULL, NULL, '32位输出', 'active', '2026-07-13 07:30:56.755676', '30501697', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (318, 'PLC控制器', 'N KEYENCE KV-C32XTD', '', 'pcs', 575.30, 'standard', NULL, NULL, '32 输入 + 32输出，', 'active', '2026-07-13 07:30:56.757298', 'SX20006228', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (319, 'PLC控制器', 'KEYENCE KV-AD40V', '', 'pcs', 3378.10, 'standard', NULL, NULL, '4路模拟量输入', 'active', '2026-07-13 07:30:56.759032', '30205358', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (320, 'PLC控制器', 'KEYENCE KV-DA40V', '', 'pcs', 4808.90, 'standard', NULL, NULL, '4路模拟量输出', 'active', '2026-07-13 07:30:56.76078', '30205359', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (321, 'PLC控制器', 'N KEYENCE KV-X310', '', 'pcs', 3005.70, 'standard', '12轴', '输入 16 点 / 输出 16 点', NULL, 'active', '2026-07-13 07:30:56.762478', 'SX20007033', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (322, 'PLC控制器', 'OMRON NX102-1200', '', 'pcs', 3461.40, 'standard', '12轴', '\', '用于EtherNet/IP通信的RJ45×2
用于EtherCAT通信的RJ45×1', 'active', '2026-07-13 07:30:56.764079', '30211966', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (323, 'PLC控制器', 'OMRON NX-ID5342', '', 'pcs', 3799.50, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.765721', 'SX20001367', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (324, 'PLC控制器', 'OMRON NX-OD5121', '', 'pcs', 692.90, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.767391', 'SX20001374', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (325, 'PLC控制器', 'OMRON NX1P2-1140DT', '', 'pcs', 3201.70, 'standard', '8轴', '24点输入，16点NPN晶体管输出', 'EtherNet/IP通信用RJ45×1 
EtherCAT通信用RJ45×1', 'active', '2026-07-13 07:30:56.769107', '30203202', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (326, 'PLC控制器', 'OMRON NJ501-1500', '', 'pcs', 1491.60, 'standard', '64轴', '\', 'EtherNet/IP通信用RJ45×1 
EtherCAT通信用RJ45×1', 'active', '2026-07-13 07:30:56.770734', 'SX20002523', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (327, 'PLC控制器', 'OMRON NJ-PA3001', '', 'pcs', 800.70, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.772353', '30207487', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (328, 'PLC控制器', 'OMRON CJ1W-ID231', '', 'pcs', 4990.20, 'standard', NULL, NULL, '16位输入', 'active', '2026-07-13 07:30:56.775086', '30200093', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (329, 'PLC控制器', 'OMRON CJ1W-OD231', '', 'pcs', 3226.20, 'standard', NULL, NULL, '16位输出', 'active', '2026-07-13 07:30:56.776641', '30200098', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (330, 'PLC控制器', 'OMRON CJ1W-MD263', '', 'pcs', 227.40, 'standard', NULL, NULL, '16 输入 + 16输出，', 'active', '2026-07-13 07:30:56.779058', '30208001', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (331, 'HMI操作面板', '西门子 6AV2124-OGC01-OAXO', '', 'pcs', 4960.80, 'standard', '精智面板  7" 宽屏 TFT 显示屏', 'PROFINET 接口，
MPI/PROFIBUS-DP 接口', NULL, 'active', '2026-07-13 07:30:56.780605', '30204434', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (332, 'HMI操作面板', 'SIEMENS 6AV2123-2JB03-0AX0', '', 'pcs', 580.20, 'standard', '精简面板  9" TFT 显示屏', 'PROFINET 接口，', NULL, 'active', '2026-07-13 07:30:56.782281', 'SX20004349', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (333, 'HMI操作面板', 'SIEMENS HMI 6AV2 124-0MC01-0AX0', '', 'pcs', 2403.00, 'standard', '精智面板 12" 宽屏幕 TFT 显示屏', 'PROFINET 接口，
MPI/PROFIBUS-DP 接口', NULL, 'active', '2026-07-13 07:30:56.783835', 'SX20003940', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (334, 'HMI操作面板', 'AB 2711P-T12W22D8S', '', 'pcs', 545.90, 'standard', '12寸电阻式触摸屏', '以太网, RS-232', NULL, 'active', '2026-07-13 07:30:56.785507', '30208350', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (335, 'HMI操作面板', 'AB 2711P-T15C22D9P', '', 'pcs', 4534.50, 'standard', '15寸电阻式触摸屏', 'RS-232, RS-485, USB', NULL, 'active', '2026-07-13 07:30:56.787073', '30206056', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (336, 'HMI操作面板', 'WEINVIEW TK8072IP', '', 'pcs', 1962.00, 'standard', '7寸电阻式触控面板', 'COM × 2 , 以太网接口 × 1 ,  
USB Host × 1', NULL, 'active', '2026-07-13 07:30:56.788814', 'SX20005652', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (337, 'HMI操作面板', 'N WEINVIEW MT8106iE', '', 'pcs', 2510.80, 'standard', '10寸电阻式触控面板', 'COM × 3 , 以太网接口 × 1 ,  
USB Host × 1', NULL, 'active', '2026-07-13 07:30:56.790692', 'SX20005944', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (338, 'HMI操作面板', 'WEINVIEW CMT2167X', '', 'pcs', 4005.30, 'standard', '15.6寸强化玻璃电容式触控面板', 'COM × 2 , 以太网接口 × 1 ,  
USB Host × 1', NULL, 'active', '2026-07-13 07:30:56.792351', 'SX20006213', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (339, 'HMI操作面板', 'Mitsubishi  GS2110-WTBD', '', 'pcs', 1055.50, 'standard', '10"', '网口、RS422/485、RS232、Mini-USB、SD 卡槽', NULL, 'active', '2026-07-13 07:30:56.793927', 'SX20000195', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (340, 'HMI操作面板', 'MITSUBISHI GT2512-STBA', '', 'pcs', 727.20, 'standard', '12"', '双 USB、网口、RS422/232、SD、可扩展通信模块', NULL, 'active', '2026-07-13 07:30:56.795584', 'SX30001089', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (341, 'HMI操作面板', 'MITSUBISHI GT2715-XTBD', '', 'pcs', 3329.10, 'standard', '15"', '双 USB、双网口、串口、SD、多媒体扩展插槽', NULL, 'active', '2026-07-13 07:30:56.79753', '30206233', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (342, 'RFID', 'SIEMENS RF240R', '', 'pcs', 2991.00, 'standard', '65MM', '不能紧贴金属，四周需预留≥30mm 非金属空间；
金属会大幅衰减读写距离', NULL, 'active', '2026-07-13 07:30:56.798734', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (343, 'RFID', 'SIEMENS RF260R', '', 'pcs', 4059.20, 'standard', '100MM', '支持金属埋入式安装，仅四周预留≥20mm 非金属区即可，
金属干扰抑制更强', NULL, 'active', '2026-07-13 07:30:56.799919', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (344, 'RFID', 'SUPERISYS RF-HZ40L-TP-L', '', 'pcs', 2623.50, 'standard', 'MODBUS TCP', '0~105mm', NULL, 'active', '2026-07-13 07:30:56.801528', 'SX20005168', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (345, 'RFID', 'SUPERISYS RF-HZ40L-R4', '', 'pcs', 2226.60, 'standard', 'MODBUS RTU', '0~105mm', NULL, 'active', '2026-07-13 07:30:56.803536', 'SX20005897', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (346, 'RFID', 'Balluff BIS V-6107-039-C005', '', 'pcs', 2608.80, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.805659', 'SX20000282', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (347, 'RFID', 'Balluff BIS VM-300-001-S4', '', 'pcs', 1878.70, 'standard', NULL, '5～40mm', NULL, 'active', '2026-07-13 07:30:56.807813', 'SX20000283', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (348, 'RFID', 'Balluff BIS V-6108-048-C002', '', 'pcs', 614.50, 'standard', 'EtherCAT', NULL, NULL, 'active', '2026-07-13 07:30:56.80996', 'SX20000289', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (349, 'RFID', 'Balluff BIS VM-332-401-S4', '', 'pcs', 2554.90, 'standard', NULL, '10～70mm', NULL, 'active', '2026-07-13 07:30:56.812176', 'SX20000290', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (351, 'RFID', 'IFM DTI213', '', 'pcs', 1344.60, 'standard', NULL, '18mm', NULL, 'active', '2026-07-13 07:30:56.815704', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (352, 'RFID', 'IFM DTE101', '', 'pcs', 3466.30, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.817515', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (353, 'RFID', 'IFM ANT513', '', 'pcs', 3221.30, 'standard', NULL, '静态读写最大 60mm', NULL, 'active', '2026-07-13 07:30:56.819291', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (354, '分布式网关（柜内）', 'SIEMENS IM 157-1 PN', '', 'pcs', 4725.60, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.821155', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (355, '分布式网关（柜内）', 'SIEMENS IM 157-1 MF', '', 'pcs', 4348.30, 'standard', 'PROFINET、EtherNet/IP 和 Modbus TCP', NULL, NULL, 'active', '2026-07-13 07:30:56.822852', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (356, '分布式网关（柜内）', 'SIEMENS 6ES7155-6AR00-0AN0', '', 'pcs', 2726.40, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.825371', 'SX20004833', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (357, '分布式网关（柜内）', '西门子 6ES7131-6BH01-0BA0', '', 'pcs', 2236.40, 'standard', NULL, NULL, '16位输入', 'active', '2026-07-13 07:30:56.828017', '30209475', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (358, '分布式网关（柜内）', '西门子 6ES7132-6BH01-0BA0', '', 'pcs', 4510.00, 'standard', NULL, NULL, '16位输出', 'active', '2026-07-13 07:30:56.83148', '30209476', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (359, '分布式网关（柜内）', 'SIEMENS 6ES7136-6DC00-0CA0', '', 'pcs', 3334.00, 'standard', NULL, NULL, '16位安全输入', 'active', '2026-07-13 07:30:56.833209', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (360, '分布式网关（柜内）', 'SIEMENS 6ES7136-6BA01-0CA0', '', 'pcs', 3593.70, 'standard', NULL, NULL, '16位安全输出', 'active', '2026-07-13 07:30:56.834942', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (361, '分布式网关（柜内）', '西门子 6ES7193-6BP00-0DA0', '', 'pcs', 2652.90, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.837447', '30210074', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (362, '分布式网关（柜内）', '西门子 6ES7193-6BP00-0BA0', '', 'pcs', 590.00, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:56.839992', '30209477', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (363, '分布式网关（柜内）', 'SVLEC PNM16DN', '', 'pcs', 874.20, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.841761', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (364, '分布式网关（柜内）', 'SVLEC EPM16DN', '', 'pcs', 4666.80, 'standard', 'EtherNet/IP', NULL, NULL, 'active', '2026-07-13 07:30:56.843604', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (365, '分布式网关（柜内）', 'DECOWELL SDPN-8IOL-M12-00', '', 'pcs', 3093.90, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.845391', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (366, '分布式网关（柜内）', 'DECOWELL  SDEC-8IOL-M12-00', '', 'pcs', 3500.60, 'standard', 'EtherCAT', NULL, NULL, 'active', '2026-07-13 07:30:56.847117', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (367, '分布式网关（柜内）', 'DECOWELL SDEI-8IOL-M12-00', '', 'pcs', 2510.80, 'standard', 'EtherNet/IP', NULL, NULL, 'active', '2026-07-13 07:30:56.849107', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (368, '分布式网关（柜内）', 'SDOT IOL7A-PN01B-8A', '', 'pcs', 1271.10, 'standard', 'PROFINET', NULL, NULL, 'active', '2026-07-13 07:30:56.851068', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (369, '分布式网关（柜内）', 'SDOT IOL7A-EC01B-8A', '', 'pcs', 2403.00, 'standard', 'EtherCAT', NULL, NULL, 'active', '2026-07-13 07:30:56.852443', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (370, '分布式站点（柜外）', 'SIEMENS 6ES7141-5BF00-0BA0', '', 'pcs', 4314.00, 'standard', 'PNP输入', '8', NULL, 'active', '2026-07-13 07:30:56.853655', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (371, '分布式站点（柜外）', 'SVLEC DK0808DI', '', 'pcs', 3838.70, 'standard', '输入', '8', NULL, 'active', '2026-07-13 07:30:56.854942', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (372, '分布式站点（柜外）', 'SVLEC DK0816DI', '', 'pcs', 1158.40, 'standard', '输入', '16', NULL, 'active', '2026-07-13 07:30:56.856074', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (373, '分布式站点（柜外）', 'SVLEC DK0808DO', '', 'pcs', 266.60, 'standard', '输出', '8', NULL, 'active', '2026-07-13 07:30:56.857182', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (374, '分布式站点（柜外）', 'DECOWELL SDIOL-801N-M12', '', 'pcs', 2819.50, 'standard', 'PNP输入', '8', NULL, 'active', '2026-07-13 07:30:56.859216', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (375, '分布式站点（柜外）', 'DECOWELL SDIOL-800N-M12', '', 'pcs', 898.70, 'standard', 'NPN输入', '8', NULL, 'active', '2026-07-13 07:30:56.860371', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (376, '分布式站点（柜外）', 'DECOWELL SDIOL-08N1-M12', '', 'pcs', 2692.10, 'standard', 'PNP输出', '8', NULL, 'active', '2026-07-13 07:30:56.861434', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (377, '分布式站点（柜外）', 'DECOWELL SDIOL-08N0-M12', '', 'pcs', 2873.40, 'standard', 'NPN输出', '8', NULL, 'active', '2026-07-13 07:30:56.862708', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (378, '分布式站点（柜外）', 'SDOT PN7A-1600B', '', 'pcs', 1320.10, 'standard', 'PNP输入', '16', NULL, 'active', '2026-07-13 07:30:56.863977', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (379, '分布式站点（柜外）', 'SDOT PN7A-1600A', '', 'pcs', 3432.00, 'standard', 'NPN输入', '16', NULL, 'active', '2026-07-13 07:30:56.865248', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (380, '分布式站点（柜外）', 'SDOT PN7A-0016B', '', 'pcs', 3946.50, 'standard', 'PNP输出', '16', NULL, 'active', '2026-07-13 07:30:56.866458', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (381, '分布式站点（柜外）', 'SDOT PN7A-0016A', '', 'pcs', 1192.70, 'standard', 'NPN输出', '16', NULL, 'active', '2026-07-13 07:30:56.867567', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (382, '安全器件模块', 'SICK UE48-2OS2D2  2开1闭', '', 'pcs', 4069.00, 'standard', '2 路安全常开（安全切断主回路）+1 路非安全常闭报警信号', '供电电压：24 V AC/DC', NULL, 'active', '2026-07-13 07:30:56.869156', '30208108', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (383, '安全器件模块', 'SICK FX3-CPU000000', '', 'pcs', 2594.10, 'standard', '主机无自带 IO，需搭配 FX3 输入 / 输出扩展模块', '供电电压：24 V DC', NULL, 'active', '2026-07-13 07:30:56.870772', '30208409', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (384, '安全器件模块', 'OMRON G9SA-TH301 AC DC24V', '', 'pcs', 3730.90, 'standard', '24 V AC/DC', '1NC+1NO', '3PST-NO', 'active', '2026-07-13 07:30:56.872452', '30205842', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (385, '安全器件模块', 'OMRON G7SA-4A2B DC24', '', 'pcs', 1721.90, 'standard', '24 VDC', '4 NO+2NC', '\', 'active', '2026-07-13 07:30:56.874179', '30206433', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (386, '安全器件模块', 'PILZ PNOZ S4C 24VDC 751104', '', 'pcs', 815.40, 'standard', '24VDC', '3PST-常开', NULL, 'active', '2026-07-13 07:30:56.876272', 'SX20003227', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (387, '安全器件模块', 'PILZ PONZ-S7C-24VDC-751107', '', 'pcs', 4608.00, 'standard', '24VDC', '4PST-常开, SPST-常闭', NULL, 'active', '2026-07-13 07:30:56.878429', 'SX20005279', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (388, '安全器件模块', 'PNOZ m B0', '', 'pcs', 2574.50, 'standard', NULL, NULL, '控制器', 'active', '2026-07-13 07:30:56.879801', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (389, '安全器件模块', 'PNOZ m ES Profinet', '', 'pcs', 511.60, 'standard', NULL, NULL, '通讯模块', 'active', '2026-07-13 07:30:56.88112', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (390, '安全器件模块', 'PNOZ m EF 8DI4DO', '', 'pcs', 4377.70, 'standard', NULL, NULL, '扩展8DI/4DO', 'active', '2026-07-13 07:30:56.882509', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (391, '安全器件模块', 'PNOZ m EF 16DI', '', 'pcs', 4265.00, 'standard', NULL, NULL, '扩展16DI', 'active', '2026-07-13 07:30:56.883774', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (392, '安全器件模块', 'IFM G1501S', '', 'pcs', 3338.90, 'standard', '继电器触点输出', '2 路无源常开安全触点', '1 路常规信号输出', 'active', '2026-07-13 07:30:56.884917', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (393, '安全器件模块', 'IFM G1502S', '', 'pcs', 3814.20, 'standard', '继电器触点输出', '3 路无延时 + 2 路延时安全常开触点', '2 路非安全触点 + 1 路延时信号输出', 'active', '2026-07-13 07:30:56.886103', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (394, '安全器件模块', 'IFM G1503S', '', 'pcs', 3383.00, 'standard', '半导体 (PNP) 输出', '2 路半导体安全输出', '1 路半导体信号输出', 'active', '2026-07-13 07:30:56.887258', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (395, '安全门锁', 'OMRON D4NL-1HFG-B', '', 'pcs', 893.80, 'standard', '电磁锁定 机械释放', '3NC+2NC', NULL, 'active', '2026-07-13 07:30:56.888874', 'SX20000714', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (396, '安全门锁', 'OMRON D4SL-N2FFG-D', '', 'pcs', 2873.40, 'standard', '电磁锁定/
机械释放', '2NC/1NO+2NC', NULL, 'active', '2026-07-13 07:30:56.890523', 'SX20003772', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (397, '安全门锁', 'OMRON D4SL-NSK10-LK', '', 'pcs', 4750.10, 'standard', NULL, NULL, '安全防护网选件', 'active', '2026-07-13 07:30:56.892176', 'SX30018391', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (398, '安全门锁', 'PILZ PSEN me5M NC-NO NC-NO 1switch', '', 'pcs', 3123.30, 'standard', '磁力', '1 N/C, 1 N/O', '1 N/C, 1 N/O', 'active', '2026-07-13 07:30:56.893593', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (399, '安全门锁', 'PILZ PSEN me5S NC-NO NC-NO 1switch', '', 'pcs', 2074.70, 'standard', '弹簧力', '1 N/C, 1 N/O', '1 N/C, 1 N/O', 'active', '2026-07-13 07:30:56.894869', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (400, '安全门锁', 'BOE MSL-2AEP', '', 'pcs', 3481.00, 'standard', 'DC24V电磁锁定/ 机械释放', '1NO(缓动触点) + 1NC(缓动触点)', NULL, 'active', '2026-07-13 07:30:56.896056', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (401, '安全门锁', 'BOE MSL-6AEF1', '', 'pcs', 1378.90, 'standard', 'DC24V电磁锁定/ 机械释放', '2NC/1NO(缓动触点） + 2NC/1NO (缓动触点）', NULL, 'active', '2026-07-13 07:30:56.897112', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (402, '安全门锁', 'WONSOR DSQ-EAM', '', 'pcs', 1550.40, 'standard', '电磁锁定 机械释放', '1NC/1NO+1NC/1NO', NULL, 'active', '2026-07-13 07:30:56.898221', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (403, '安全门锁', 'WONSOR DSQ-EEM-B', '', 'pcs', 2780.30, 'standard', '电磁锁定/
机械释放', '1NC/2NO+1NC', NULL, 'active', '2026-07-13 07:30:56.899977', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (404, '安全光幕', 'SICK C4C-SA-EA-03030A10000-含5M弯头线缆和固定支架', '', 'pcs', 4093.50, 'standard', '15M', '300MM', NULL, 'active', '2026-07-13 07:30:56.901603', 'SX20001112', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (405, '安全光幕', 'SICK C2C-SA10530A10000+C2C-EA10530A10000', '', 'pcs', 2795.00, 'standard', '15M', '1050MM', NULL, 'active', '2026-07-13 07:30:56.903824', 'SX20001223', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (406, '安全光幕', 'KEYENCE GL-R40H', '', 'pcs', 3481.00, 'standard', '40', '780mm', '825mm', 'active', '2026-07-13 07:30:56.906004', '30306708', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (407, '安全光幕', 'KEYENCE GL-R80H', '', 'pcs', 1775.80, 'standard', '80', '1580mm', '1625mm', 'active', '2026-07-13 07:30:56.907925', '30314732', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (408, '安全光幕', 'KEYENCE SL-V36L', '', 'pcs', 2447.10, 'standard', '36', '1440mm', '1485mm', 'active', '2026-07-13 07:30:56.909755', '30314525', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (409, '安全光幕', 'KEYENCE SL-V40L', '', 'pcs', 3397.70, 'standard', '40', '1600mm', '1645mm', 'active', '2026-07-13 07:30:56.911749', '30314526', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (410, '安全光幕', '', '', 'pcs', 4073.90, 'standard', '光轴距', '有效保护高度', '光幕高度', 'active', '2026-07-13 07:30:56.911753', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (411, '安全光幕', '新洲 XZGM2D-24-40 配附件', '', 'pcs', 4382.60, 'standard', '40', '920', '985', 'active', '2026-07-13 07:30:56.913969', '30321066', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (412, '安全光幕', 'XINZHOU XZGM2D-24-20', '', 'pcs', 810.50, 'standard', '20', '460', '520', 'active', '2026-07-13 07:30:56.915839', 'SX30004583', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (413, '安全光幕', 'IFM OYA0510-02-4-12-P-1', '', 'pcs', 408.70, 'standard', '510mm', '2', NULL, 'active', '2026-07-13 07:30:56.917077', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (414, '安全光幕', 'IFM OYA0810-03-4-12-P-1', '', 'pcs', 2417.70, 'standard', '810mm', '3', NULL, 'active', '2026-07-13 07:30:56.918272', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (415, '安全光幕', 'IFM OYA0910-04-4-12-P-1', '', 'pcs', 149.00, 'standard', '910mm', '4', NULL, 'active', '2026-07-13 07:30:56.919391', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (416, '管理型交换机', 'SIEMENS 6GK5208-0BA00-2TB2', '', 'pcs', 521.40, 'standard', '8个 10/100 Mbit/s RJ45 接口 
1个 控制台接口', '默认 EtherNet/IP 协议', NULL, 'active', '2026-07-13 07:30:56.920515', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (417, '管理型交换机', 'SIEMENS 6GK5208-0BA00-2AB2', '', 'pcs', 4514.90, 'standard', '8个 10/100 Mbit/s RJ45 端口
 1个 终端端口', '默认 PROFINET协议', NULL, 'active', '2026-07-13 07:30:56.92166', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (418, '管理型交换机', 'ADVANTECH EKI-7706E-2FI', '', 'pcs', 3912.20, 'standard', '4', '2', 'IEEE 802.1p, 802.3ad, 802.1x, 802.1D, 802.1s, 802.1w', 'active', '2026-07-13 07:30:56.922983', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (419, '管理型交换机', 'ADVANTECH EKI-5708E-2FI', '', 'pcs', 624.30, 'standard', '6', '2', 'IEEE 802.1p, 802.3ad, 802.1x, 802.1D, 802.1s, 802.1w', 'active', '2026-07-13 07:30:56.924214', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (420, '管理型交换机', 'ADVANTECH EKI-5710E-2FI', '', 'pcs', 149.00, 'standard', '8', '2', 'IEEE 802.1p, 802.3ad, 802.1x,802.1D, 802.1s, 802.1w', 'active', '2026-07-13 07:30:56.925546', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (421, '管理型交换机', 'TP-LINK TL-SG2005', '', 'pcs', 4617.80, 'standard', '5', NULL, '支持802.1Q VLAN、MTU VLAN、端口VLAN', 'active', '2026-07-13 07:30:56.926996', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (422, '管理型交换机', 'TP-LINK TL-SG2210', '', 'pcs', 1672.90, 'standard', '8', '2', '支持802.1Q VLAN、MTU VLAN、端口VLAN', 'active', '2026-07-13 07:30:56.928543', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (423, '管理型交换机', 'TP-LINK TL-SL2108', '', 'pcs', 1369.10, 'standard', '1', NULL, 'IEEE 802.3,802.3i,802.3u,802.3x
兼容Modbus TCP、Ethernet/IP、Profinet等协议', 'active', '2026-07-13 07:30:56.930003', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (424, '管理型交换机', 'MOXA  EDS-508A-MM-ST', '', 'pcs', 2672.50, 'standard', '6', '多模 ST 接头：2', 'EtherNet/IP、Modbus TCP', 'active', '2026-07-13 07:30:56.931517', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (425, '管理型交换机', 'MOXA EDS-510A-3GT', '', 'pcs', 1295.60, 'standard', '7', '10/100/1000BaseT(X) 端口（RJ45 接头）：3', 'EtherNet/IP、Modbus TCP', 'active', '2026-07-13 07:30:56.933049', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (426, '管理型交换机', 'MOXA EDS-505A-MM-SC', '', 'pcs', 4367.90, 'standard', '3', '多模 SC 接头：2', 'EtherNet/IP、Modbus TCP', 'active', '2026-07-13 07:30:56.934592', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (427, '普通交换机', 'SIEMENS 6GK5005-0BA00-1AB2', '', 'pcs', 884.00, 'standard', '5', '10/100 Mbit/s', NULL, 'active', '2026-07-13 07:30:56.936827', 'SX20004846', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (428, '普通交换机', 'SIEMENS 6GK5008-0BA10-1AB2', '', 'pcs', 3608.40, 'standard', '8', '10/100 Mbit/s', NULL, 'active', '2026-07-13 07:30:56.939105', 'SX20001221', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (429, '普通交换机', 'SIEMENS 6GK5116-0BA00-2AB2', '', 'pcs', 1393.60, 'standard', '16', '10/100 Mbit/s', NULL, 'active', '2026-07-13 07:30:56.940698', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (430, '普通交换机', '研华 EKI-2525', '', 'pcs', 4049.40, 'standard', '5', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.943091', '30201566', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (431, '普通交换机', '研华 EKI-2528', '', 'pcs', 1589.60, 'standard', '8', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.945594', '30203445', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (432, '普通交换机', 'ADVANTECH EKI-2725', '', 'pcs', 477.30, 'standard', '5', '10/100/1000 Mbps', NULL, 'active', '2026-07-13 07:30:56.948683', '30205227', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (433, '普通交换机', '研华 EKI-2728', '', 'pcs', 3520.20, 'standard', '8', '10/100/1000 Mbps', NULL, 'active', '2026-07-13 07:30:56.95174', '30201852', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (434, '普通交换机', 'TP-LINK SG1005D', '', 'pcs', 472.40, 'standard', '5', '10/100/1000 Mbps', NULL, 'active', '2026-07-13 07:30:56.954875', '30201756', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (435, '普通交换机', 'TP-LINK SG1008D', '', 'pcs', 2863.60, 'standard', '8', '10/100/1000 Mbps', NULL, 'active', '2026-07-13 07:30:56.958028', '30207466', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (436, '普通交换机', '普联 TL-SF1008工业级', '', 'pcs', 2015.90, 'standard', '8', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.960892', '30211116', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (437, '普通交换机', 'MOXA EDS-205', '', 'pcs', 3044.90, 'standard', '5', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.963665', '30200083', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (438, '普通交换机', 'MOXA EDS-316', '', 'pcs', 913.40, 'standard', '16', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.966224', '30201032', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (439, '普通交换机', 'MOXA EDS208A-T', '', 'pcs', 820.30, 'standard', '8', '10/100 Mbps', NULL, 'active', '2026-07-13 07:30:56.968813', '30207979', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (440, '网关', 'SIEMENS GK1503-2CB00', '', 'pcs', 1525.90, 'standard', '2 路独立隔离 RS485（Modbus RTU 主站）', '1 路 RJ45 PROFINET 以太网口', NULL, 'active', '2026-07-13 07:30:56.970624', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (441, '网关', 'ADVANTECH ECU-1051', '', 'pcs', 4980.40, 'standard', '2× 百兆 10/100M', '2 路隔离 RS232/485', '无', 'active', '2026-07-13 07:30:56.972413', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (442, '网关', 'ADVANTECH ECU-1052', '', 'pcs', 4612.90, 'standard', '2× 千兆 10/100/1000M', '2 路隔离 RS232/485', '2 路 CAN 2.0B', 'active', '2026-07-13 07:30:56.974071', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (443, '网关', 'ADVANTECH EKI-1524', '', 'pcs', 3108.60, 'standard', '2× 千兆 10/100/1000M', '2 路隔离 RS232/485 + USB3.0', '无', 'active', '2026-07-13 07:30:56.975877', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (444, '网关', 'TP-LINK TL-DU3002', '', 'pcs', 844.80, 'standard', '2× 百兆 RJ45 (10/100M)', '不支持无线通信', NULL, 'active', '2026-07-13 07:30:56.977691', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (445, '网关', 'TP-LINK TL-IG4022', '', 'pcs', 2270.70, 'standard', '2× 千兆 RJ45 (10/100/1000M，WAN+LAN 分离)', '支持 4G/5G 模组扩展，双 Nano-SIM 卡冗余', NULL, 'active', '2026-07-13 07:30:56.979549', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (446, '网关', 'MOXA MGate 5105-MB-EIP', '', 'pcs', 1717.00, 'standard', '1 路隔离 RS485/232；
2× 百兆网口', 'Modbus 主站、EtherNet/IP Scanner', NULL, 'active', '2026-07-13 07:30:56.981349', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (447, '网关', 'MOXA MGate 5119-T', '', 'pcs', 2167.80, 'standard', '1 路隔离 RS485/232；
2× 百兆网口', 'IEC101/DNP3 主站、IEC61850 MMS 服务器', NULL, 'active', '2026-07-13 07:30:56.983095', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (448, '网关', 'MOXA MGate 5003', '', 'pcs', 1971.80, 'standard', '1 路 CAN 总线（CAN2.0A/B）；
2× 百兆网口', 'CANopen 主站、J1939 采集主站', NULL, 'active', '2026-07-13 07:30:56.98524', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (449, '高精密检测传感器', 'KEYENCE LR-XH100', '', 'pcs', 3598.60, 'standard', '25.0 至 100.0 mm', '1.0 mm', '配套放大器可选 NPN/PNP', 'active', '2026-07-13 07:30:56.98749', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (450, '高精密检测传感器', 'KEYENCE LR-XH250', '', 'pcs', 1398.50, 'standard', '30 至 250 mm', '30 至 180 mm : 9 mm
180 至 250 mm : 18 mm', '配套放大器可选 NPN/PNP', 'active', '2026-07-13 07:30:56.989394', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (451, '高精密检测传感器', 'KEYENCE LR-ZH500P', '', 'pcs', 1996.30, 'standard', '35 至 500 mm', '35 至 180 mm：9 mm
180 至 300 mm：25 mm
300 至 400 mm：40 mm
400 至 500 mm：50 mm', 'PNP', 'active', '2026-07-13 07:30:56.991112', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (452, '高精密检测传感器', 'KEYENCE LR-ZB250AP', '', 'pcs', 4451.20, 'standard', '35 至 250 mm', '35 至 180 mm：9 mm
180 至 250 mm：25 mm', 'PNP', 'active', '2026-07-13 07:30:56.992844', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (453, '高精密检测传感器', 'SICK OD1000-6001R15', '', 'pcs', 3074.30, 'standard', '200～1000mm', '0.4mm', '模拟量 4-20mA', 'active', '2026-07-13 07:30:56.994613', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (454, '高精密检测传感器', 'SICK WTT2SL-2P3292', '', 'pcs', 4867.70, 'standard', '50～800mm', '2～5mm', '仅 PNP 开关量输出', 'active', '2026-07-13 07:30:56.996425', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (455, '高精密检测传感器', 'OMRON E3AS-HF6000SMT', '', 'pcs', 810.50, 'standard', '50～6,000mm', '原生支持 IO-Link V1.1，可上传实时距离值、诊断、参数远程读写', 'PNP，Light-ON/Dark-ON 可切换', 'active', '2026-07-13 07:30:56.998101', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (456, '高精密检测传感器', 'OMRON E3ZG-LS81-LO 2M', '', 'pcs', 1099.60, 'standard', '50～900mm', '仅开关量 IO，无 IO-Link，无法上传测距数值', 'PNP，固定 Light-ON', 'active', '2026-07-13 07:30:56.999902', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (457, '高精密检测传感器', 'PANASONIC HG-C1200-P', '', 'pcs', 1677.80, 'standard', '±80mm', '200μm', '±0.2%F.S.', 'active', '2026-07-13 07:30:57.00167', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (458, '高精密检测传感器', 'PANASONIC HG-C1400-P', '', 'pcs', 604.70, 'standard', '±200mm', '300μm', '±0.2%F.S.', 'active', '2026-07-13 07:30:57.003577', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (459, '检测传感器', 'SICK  KTM-WN11181P', '', 'pcs', 3157.60, 'standard', '感应距离 :≤ 12.5 mm', '感应距离公差 :± 3 mm', '开关量输出: NPN', 'active', '2026-07-13 07:30:57.005892', '30206201', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (460, '检测传感器', 'SICK CSS-WBG4C4115AA10Z', '', 'pcs', 2055.10, 'standard', '检测距离：50 mm ~ 150 mm', '总线接口：IO-Link', NULL, 'active', '2026-07-13 07:30:57.008434', 'SX20006003', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (461, '检测传感器', 'OMRON E52-CA1DY-M6-4M', '', 'pcs', 1040.80, 'standard', '测温范围：0～+400℃ ： K(CA)
                    0～+350℃ ： J(IC)', '导线：0～+180℃', NULL, 'active', '2026-07-13 07:30:57.011276', 'SX20006184', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (462, '检测传感器', 'OMRON TL-W20ME1 2M', '', 'pcs', 501.80, 'standard', '检测距离: 20MM', '输出形式：NPN集电极开路NO', NULL, 'active', '2026-07-13 07:30:57.014405', 'SX30017087', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (463, '检测传感器', 'KEYENCE LR-W500', '', 'pcs', 3412.40, 'standard', '检测距离：30 至 500 mm', NULL, NULL, 'active', '2026-07-13 07:30:57.017187', 'SX20001347', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (464, '检测传感器', 'KEYENCE TF-C31', '', 'pcs', 330.30, 'standard', '测温范围：0至+800°C', NULL, NULL, 'active', '2026-07-13 07:30:57.019745', 'SX20000459', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (465, '检测传感器', 'KEYENCE KV-TF40', '', 'pcs', 2496.10, 'standard', NULL, NULL, NULL, 'active', '2026-07-13 07:30:57.022391', 'SX20003070', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (466, '检测传感器', 'KEYENCE AP-C31', '', 'pcs', 4701.10, 'standard', '量程：0 ~ -101.3 kPa', '输出：标准款 NPN', NULL, 'active', '2026-07-13 07:30:57.02487', '30312546', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (467, '检测传感器', 'KEYENCE FD-XS8', '', 'pcs', 335.20, 'standard', '适配管径：Φ6/Φ8 小管，最大额定流量 8L/min', '重复精度 ±0.1% FS', NULL, 'active', '2026-07-13 07:30:57.027291', 'SX30001281', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (468, '检测传感器', 'PANASONIC DP-102-E-P', '', 'pcs', 1050.60, 'standard', '‘-100.0~+100.0KPa', '数显PNP', NULL, 'active', '2026-07-13 07:30:57.028846', 'SX20004143', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (469, '检测传感器', 'Panasonic DP-101', '', 'pcs', 1560.20, 'standard', '’-0.100～+1.000MPa', '数显NPN', NULL, 'active', '2026-07-13 07:30:57.030456', 'SX30026482', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (470, '位移传感器', 'KEYENCE GT-A10', '', 'pcs', 4211.10, 'standard', '10 mm', '3 µm', '\', 'active', '2026-07-13 07:30:57.032921', '30501374', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (471, '位移传感器', 'KEYENCE IL-S065', '', 'pcs', 2643.10, 'standard', '55 到 75 mm', '2μm', '±0.05% F.S. (55 到 65 mm)
±0.075% F.S. (55 到 75 mm)', 'active', '2026-07-13 07:30:57.035392', '30503040', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (472, '位移传感器', 'KEYENCE IL-100', '', 'pcs', 2731.30, 'standard', '75 到 130 mm', '4 µm', '±0.15% F.S.', 'active', '2026-07-13 07:30:57.037826', 'SX20007052', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (473, '位移传感器', 'SICK OD1-B035C15I25', '', 'pcs', 2834.20, 'standard', '20毫米......50毫米', '6微米', '± 30 微米', 'active', '2026-07-13 07:30:57.040499', '30208558', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (474, '位移传感器', 'SICK OD2-N250W150U2', '', 'pcs', 3775.00, 'standard', '100毫米......400毫米', '75微米', '± 750 微米', 'active', '2026-07-13 07:30:57.04215', '30210963', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (475, '位移传感器', 'SICK OD5000-C30T05', '', 'pcs', 3534.90, 'standard', '25 mm ... 35 mm', '0.05 µm', '漫反射 ± 3 µm 
镜面反射 ± 4 µm', 'active', '2026-07-13 07:30:57.043814', 'SX20003910', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (476, '位移传感器', 'OMRON ZX1-LD300A61', '', 'pcs', 3951.40, 'standard', '100 ± 35 mm', '电流输出： 4～20mA', NULL, 'active', '2026-07-13 07:30:57.045447', 'SX20002424', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (477, '位移传感器', 'OMRON ZX1-LD300A81', '', 'pcs', 310.70, 'standard', '100 ± 35 mm', '电流输出： 4～20mA', NULL, 'active', '2026-07-13 07:30:57.047297', 'SX20003100', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (478, '位移传感器', 'OMRON D5VA-3F1', '', 'pcs', 815.40, 'standard', '5mm', '电流输出： 4～20mA', NULL, 'active', '2026-07-13 07:30:57.049642', '30200562', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (479, '位移传感器', 'OMRON D5VA-3B1', '', 'pcs', 3074.30, 'standard', '5mm', '电流输出： 4～20mA', NULL, 'active', '2026-07-13 07:30:57.052769', '30203525', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (480, '位移传感器', 'PANASONIC HG-C1050', '', 'pcs', 893.80, 'standard', '±15mm', '30μm', NULL, 'active', '2026-07-13 07:30:57.055106', '30205411', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (481, '位移传感器', '松下 HG-C1200', '', 'pcs', 1408.30, 'standard', '±80mm', '200μm', NULL, 'active', '2026-07-13 07:30:57.05758', '30207943', NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (482, '超声波传感器', 'SICK UM12-1172251', '', 'pcs', 3966.10, 'standard', '20毫米......150毫米', '± 0.15%', '± 1%', 'active', '2026-07-13 07:30:57.05928', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (483, '超声波传感器', 'SICK UM12-1192251', '', 'pcs', 178.40, 'standard', '40毫米......240毫米', '± 0.15%', '± 1%', 'active', '2026-07-13 07:30:57.060921', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (484, '超声波传感器', 'SICK UC4-11345', '', 'pcs', 658.60, 'standard', '13毫米......100毫米', '± 0.15%', '± 1%', 'active', '2026-07-13 07:30:57.062661', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (485, '超声波传感器', 'OMRON E4E2-TS50C1 2M', '', 'pcs', 4887.30, 'standard', '500mm', 'NPN集电极开路NO', NULL, 'active', '2026-07-13 07:30:57.064445', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (486, '超声波传感器', 'KEYENCE FW-H02', '', 'pcs', 4294.40, 'standard', '50 到 200 mm', '±0.25%FS/℃', NULL, 'active', '2026-07-13 07:30:57.066194', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (487, '超声波传感器', 'KEYENCE FW-H07', '', 'pcs', 4833.40, 'standard', '150 到 700 mm', '±0.25%FS/℃', NULL, 'active', '2026-07-13 07:30:57.068009', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (488, '超声波传感器', 'KEYENCE FW-H10R', '', 'pcs', 2589.20, 'standard', '150 到 1000 mm', '±0.06% FS/℃', NULL, 'active', '2026-07-13 07:30:57.069782', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (489, '超声波传感器', 'BOE US-M18-020', '', 'pcs', 4661.90, 'standard', '50 到 200 mm', '±0.25%FS/℃', '不支持', 'active', '2026-07-13 07:30:57.071737', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (490, '超声波传感器', 'BOE US-M18-070', '', 'pcs', 2844.00, 'standard', '150 到 700 mm', '±0.25%FS/℃', '不支持', 'active', '2026-07-13 07:30:57.073779', NULL, NULL, NULL, NULL, NULL);
INSERT INTO public.materials VALUES (491, '超声波传感器', 'BOE US-M18-100R', '', 'pcs', 2976.30, 'standard', '150 到 1000 mm', '±0.07% FS/℃', '支持 IO-Link V1.1', 'active', '2026-07-13 07:30:57.075496', NULL, NULL, NULL, NULL, NULL);


ALTER TABLE public.materials ENABLE TRIGGER ALL;

--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.messages DISABLE TRIGGER ALL;



ALTER TABLE public.messages ENABLE TRIGGER ALL;

--
-- Data for Name: module_materials; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.module_materials DISABLE TRIGGER ALL;

INSERT INTO public.module_materials VALUES (1, 1, 98, false, 1, NULL, 1, '2026-07-13 07:56:50.661232');
INSERT INTO public.module_materials VALUES (2, 1, 97, false, 1, NULL, 1, '2026-07-13 07:56:50.709182');
INSERT INTO public.module_materials VALUES (3, 1, 96, false, 1, NULL, 1, '2026-07-13 07:56:50.752689');
INSERT INTO public.module_materials VALUES (4, 1, 95, false, 1, NULL, 1, '2026-07-13 07:56:50.844776');
INSERT INTO public.module_materials VALUES (5, 1, 94, false, 1, NULL, 1, '2026-07-13 07:56:50.866457');
INSERT INTO public.module_materials VALUES (6, 1, 93, false, 1, NULL, 1, '2026-07-13 07:56:50.888712');
INSERT INTO public.module_materials VALUES (7, 1, 92, false, 1, NULL, 1, '2026-07-13 07:56:50.926424');
INSERT INTO public.module_materials VALUES (8, 1, 91, false, 1, NULL, 1, '2026-07-13 07:56:50.970514');
INSERT INTO public.module_materials VALUES (9, 1, 90, false, 1, NULL, 1, '2026-07-13 07:56:50.992027');
INSERT INTO public.module_materials VALUES (10, 1, 89, false, 1, NULL, 1, '2026-07-13 07:56:51.014306');
INSERT INTO public.module_materials VALUES (11, 1, 88, false, 1, NULL, 1, '2026-07-13 07:56:51.037256');
INSERT INTO public.module_materials VALUES (12, 1, 87, false, 1, NULL, 1, '2026-07-13 07:56:51.198377');
INSERT INTO public.module_materials VALUES (13, 1, 86, false, 1, NULL, 1, '2026-07-13 07:56:51.221298');
INSERT INTO public.module_materials VALUES (14, 1, 85, false, 1, NULL, 1, '2026-07-13 07:56:51.246377');
INSERT INTO public.module_materials VALUES (15, 1, 84, false, 1, NULL, 1, '2026-07-13 07:56:51.275852');
INSERT INTO public.module_materials VALUES (16, 1, 83, false, 1, NULL, 1, '2026-07-13 07:56:51.304006');
INSERT INTO public.module_materials VALUES (17, 1, 82, false, 1, NULL, 1, '2026-07-13 07:56:51.323419');
INSERT INTO public.module_materials VALUES (18, 1, 81, false, 1, NULL, 1, '2026-07-13 07:56:51.344897');
INSERT INTO public.module_materials VALUES (19, 1, 80, false, 1, NULL, 1, '2026-07-13 07:56:51.370758');
INSERT INTO public.module_materials VALUES (20, 1, 79, false, 1, NULL, 1, '2026-07-13 07:56:51.390051');
INSERT INTO public.module_materials VALUES (21, 1, 78, false, 1, NULL, 1, '2026-07-13 07:56:51.410653');
INSERT INTO public.module_materials VALUES (22, 1, 77, false, 1, NULL, 1, '2026-07-13 07:56:51.433958');
INSERT INTO public.module_materials VALUES (23, 1, 76, false, 1, NULL, 1, '2026-07-13 07:56:51.456982');
INSERT INTO public.module_materials VALUES (24, 1, 75, false, 1, NULL, 1, '2026-07-13 07:56:51.479515');
INSERT INTO public.module_materials VALUES (25, 1, 74, false, 1, NULL, 1, '2026-07-13 07:56:51.504055');
INSERT INTO public.module_materials VALUES (26, 1, 73, false, 1, NULL, 1, '2026-07-13 07:56:51.526243');
INSERT INTO public.module_materials VALUES (27, 1, 72, false, 1, NULL, 1, '2026-07-13 07:56:51.546533');
INSERT INTO public.module_materials VALUES (28, 1, 71, false, 1, NULL, 1, '2026-07-13 07:56:51.56751');
INSERT INTO public.module_materials VALUES (29, 1, 70, false, 1, NULL, 1, '2026-07-13 07:56:51.589164');
INSERT INTO public.module_materials VALUES (30, 1, 69, false, 1, NULL, 1, '2026-07-13 07:56:51.610979');
INSERT INTO public.module_materials VALUES (31, 1, 68, false, 1, NULL, 1, '2026-07-13 07:56:51.629182');
INSERT INTO public.module_materials VALUES (32, 1, 67, false, 1, NULL, 1, '2026-07-13 07:56:51.648352');
INSERT INTO public.module_materials VALUES (33, 1, 66, false, 1, NULL, 1, '2026-07-13 07:56:51.670869');
INSERT INTO public.module_materials VALUES (34, 1, 65, false, 1, NULL, 1, '2026-07-13 07:56:51.707926');
INSERT INTO public.module_materials VALUES (35, 1, 64, false, 1, NULL, 1, '2026-07-13 07:56:51.729568');
INSERT INTO public.module_materials VALUES (36, 1, 63, false, 1, NULL, 1, '2026-07-13 07:56:51.747071');
INSERT INTO public.module_materials VALUES (37, 1, 62, false, 1, NULL, 1, '2026-07-13 07:56:51.764489');
INSERT INTO public.module_materials VALUES (38, 1, 61, false, 1, NULL, 1, '2026-07-13 07:56:51.781341');
INSERT INTO public.module_materials VALUES (39, 1, 60, false, 1, NULL, 1, '2026-07-13 07:56:51.802836');
INSERT INTO public.module_materials VALUES (40, 1, 59, false, 1, NULL, 1, '2026-07-13 07:56:51.821747');
INSERT INTO public.module_materials VALUES (41, 1, 58, false, 1, NULL, 1, '2026-07-13 07:56:51.841868');
INSERT INTO public.module_materials VALUES (42, 1, 57, false, 1, NULL, 1, '2026-07-13 07:56:51.859382');
INSERT INTO public.module_materials VALUES (43, 1, 56, false, 1, NULL, 1, '2026-07-13 07:56:51.874957');
INSERT INTO public.module_materials VALUES (44, 1, 55, false, 1, NULL, 1, '2026-07-13 07:56:51.892212');
INSERT INTO public.module_materials VALUES (45, 1, 54, false, 1, NULL, 1, '2026-07-13 07:56:51.911048');
INSERT INTO public.module_materials VALUES (46, 1, 53, false, 1, NULL, 1, '2026-07-13 07:56:51.938668');
INSERT INTO public.module_materials VALUES (47, 1, 52, false, 1, NULL, 1, '2026-07-13 07:56:51.984646');
INSERT INTO public.module_materials VALUES (48, 1, 51, false, 1, NULL, 1, '2026-07-13 07:56:52.007061');
INSERT INTO public.module_materials VALUES (49, 1, 50, false, 1, NULL, 1, '2026-07-13 07:56:52.022836');
INSERT INTO public.module_materials VALUES (50, 1, 49, false, 1, NULL, 1, '2026-07-13 07:56:52.036289');
INSERT INTO public.module_materials VALUES (51, 2, 491, false, 1, NULL, 1, '2026-07-13 07:57:06.546806');
INSERT INTO public.module_materials VALUES (52, 2, 490, false, 1, NULL, 1, '2026-07-13 07:57:06.581897');
INSERT INTO public.module_materials VALUES (53, 2, 489, false, 1, NULL, 1, '2026-07-13 07:57:06.626467');
INSERT INTO public.module_materials VALUES (54, 2, 488, false, 1, NULL, 1, '2026-07-13 07:57:06.650453');
INSERT INTO public.module_materials VALUES (55, 2, 487, false, 1, NULL, 1, '2026-07-13 07:57:06.683558');
INSERT INTO public.module_materials VALUES (56, 2, 486, false, 1, NULL, 1, '2026-07-13 07:57:06.712413');
INSERT INTO public.module_materials VALUES (57, 2, 485, false, 1, NULL, 1, '2026-07-13 07:57:06.738363');
INSERT INTO public.module_materials VALUES (58, 2, 484, false, 1, NULL, 1, '2026-07-13 07:57:06.768233');
INSERT INTO public.module_materials VALUES (59, 2, 483, false, 1, NULL, 1, '2026-07-13 07:57:06.794574');
INSERT INTO public.module_materials VALUES (60, 2, 482, false, 1, NULL, 1, '2026-07-13 07:57:06.817565');
INSERT INTO public.module_materials VALUES (61, 2, 481, false, 1, NULL, 1, '2026-07-13 07:57:06.844872');
INSERT INTO public.module_materials VALUES (62, 2, 480, false, 1, NULL, 1, '2026-07-13 07:57:06.86719');
INSERT INTO public.module_materials VALUES (63, 2, 479, false, 1, NULL, 1, '2026-07-13 07:57:06.893949');
INSERT INTO public.module_materials VALUES (64, 2, 478, false, 1, NULL, 1, '2026-07-13 07:57:07.01444');
INSERT INTO public.module_materials VALUES (65, 2, 477, false, 1, NULL, 1, '2026-07-13 07:57:07.097843');
INSERT INTO public.module_materials VALUES (66, 2, 476, false, 1, NULL, 1, '2026-07-13 07:57:07.123584');
INSERT INTO public.module_materials VALUES (67, 2, 475, false, 1, NULL, 1, '2026-07-13 07:57:07.16208');
INSERT INTO public.module_materials VALUES (68, 2, 474, false, 1, NULL, 1, '2026-07-13 07:57:07.187438');
INSERT INTO public.module_materials VALUES (69, 2, 473, false, 1, NULL, 1, '2026-07-13 07:57:07.213097');
INSERT INTO public.module_materials VALUES (70, 2, 472, false, 1, NULL, 1, '2026-07-13 07:57:07.264767');
INSERT INTO public.module_materials VALUES (71, 3, 341, false, 1, NULL, 1, '2026-07-13 07:57:17.651872');
INSERT INTO public.module_materials VALUES (72, 3, 340, false, 1, NULL, 1, '2026-07-13 07:57:17.737676');
INSERT INTO public.module_materials VALUES (73, 3, 339, false, 1, NULL, 1, '2026-07-13 07:57:17.882199');
INSERT INTO public.module_materials VALUES (74, 3, 338, false, 1, NULL, 1, '2026-07-13 07:57:17.95863');
INSERT INTO public.module_materials VALUES (75, 3, 337, false, 1, NULL, 1, '2026-07-13 07:57:18.004923');
INSERT INTO public.module_materials VALUES (76, 3, 336, false, 1, NULL, 1, '2026-07-13 07:57:18.030601');
INSERT INTO public.module_materials VALUES (77, 3, 335, false, 1, NULL, 1, '2026-07-13 07:57:18.217691');
INSERT INTO public.module_materials VALUES (78, 3, 334, false, 1, NULL, 1, '2026-07-13 07:57:18.241201');
INSERT INTO public.module_materials VALUES (79, 3, 333, false, 1, NULL, 1, '2026-07-13 07:57:18.26202');
INSERT INTO public.module_materials VALUES (80, 3, 332, false, 1, NULL, 1, '2026-07-13 07:57:18.280595');
INSERT INTO public.module_materials VALUES (81, 3, 331, false, 1, NULL, 1, '2026-07-13 07:57:18.312084');
INSERT INTO public.module_materials VALUES (82, 3, 330, false, 1, NULL, 1, '2026-07-13 07:57:18.337677');
INSERT INTO public.module_materials VALUES (83, 3, 329, false, 1, NULL, 1, '2026-07-13 07:57:18.35966');
INSERT INTO public.module_materials VALUES (84, 3, 328, false, 1, NULL, 1, '2026-07-13 07:57:18.380173');
INSERT INTO public.module_materials VALUES (85, 3, 327, false, 1, NULL, 1, '2026-07-13 07:57:18.403694');
INSERT INTO public.module_materials VALUES (86, 3, 326, false, 1, NULL, 1, '2026-07-13 07:57:18.423806');
INSERT INTO public.module_materials VALUES (87, 3, 325, false, 1, NULL, 1, '2026-07-13 07:57:18.449193');
INSERT INTO public.module_materials VALUES (88, 3, 324, false, 1, NULL, 1, '2026-07-13 07:57:18.467519');
INSERT INTO public.module_materials VALUES (89, 3, 323, false, 1, NULL, 1, '2026-07-13 07:57:18.485292');
INSERT INTO public.module_materials VALUES (90, 3, 322, false, 1, NULL, 1, '2026-07-13 07:57:18.503492');
INSERT INTO public.module_materials VALUES (91, 3, 321, false, 1, NULL, 1, '2026-07-13 07:57:18.524254');
INSERT INTO public.module_materials VALUES (92, 3, 320, false, 1, NULL, 1, '2026-07-13 07:57:18.539831');
INSERT INTO public.module_materials VALUES (93, 3, 319, false, 1, NULL, 1, '2026-07-13 07:57:18.558212');
INSERT INTO public.module_materials VALUES (94, 3, 318, false, 1, NULL, 1, '2026-07-13 07:57:18.585698');
INSERT INTO public.module_materials VALUES (95, 3, 317, false, 1, NULL, 1, '2026-07-13 07:57:18.603851');
INSERT INTO public.module_materials VALUES (96, 3, 316, false, 1, NULL, 1, '2026-07-13 07:57:18.622568');
INSERT INTO public.module_materials VALUES (97, 3, 315, false, 1, NULL, 1, '2026-07-13 07:57:18.644283');
INSERT INTO public.module_materials VALUES (98, 3, 314, false, 1, NULL, 1, '2026-07-13 07:57:18.665388');
INSERT INTO public.module_materials VALUES (99, 3, 313, false, 1, NULL, 1, '2026-07-13 07:57:18.691798');
INSERT INTO public.module_materials VALUES (100, 3, 312, false, 1, NULL, 1, '2026-07-13 07:57:18.713963');
INSERT INTO public.module_materials VALUES (101, 3, 311, false, 1, NULL, 1, '2026-07-13 07:57:18.734726');
INSERT INTO public.module_materials VALUES (102, 3, 310, false, 1, NULL, 1, '2026-07-13 07:57:18.75192');
INSERT INTO public.module_materials VALUES (103, 3, 309, false, 1, NULL, 1, '2026-07-13 07:57:18.771581');
INSERT INTO public.module_materials VALUES (104, 3, 308, false, 1, NULL, 1, '2026-07-13 07:57:18.794082');
INSERT INTO public.module_materials VALUES (105, 3, 307, false, 1, NULL, 1, '2026-07-13 07:57:18.815253');
INSERT INTO public.module_materials VALUES (106, 3, 306, false, 1, NULL, 1, '2026-07-13 07:57:18.839631');
INSERT INTO public.module_materials VALUES (107, 3, 305, false, 1, NULL, 1, '2026-07-13 07:57:18.859519');
INSERT INTO public.module_materials VALUES (108, 3, 304, false, 1, NULL, 1, '2026-07-13 07:57:18.884293');
INSERT INTO public.module_materials VALUES (109, 3, 303, false, 1, NULL, 1, '2026-07-13 07:57:18.920286');
INSERT INTO public.module_materials VALUES (110, 3, 302, false, 1, NULL, 1, '2026-07-13 07:57:18.956206');
INSERT INTO public.module_materials VALUES (111, 3, 301, false, 1, NULL, 1, '2026-07-13 07:57:19.005375');
INSERT INTO public.module_materials VALUES (112, 3, 300, false, 1, NULL, 1, '2026-07-13 07:57:19.074858');
INSERT INTO public.module_materials VALUES (113, 3, 299, false, 1, NULL, 1, '2026-07-13 07:57:19.100388');
INSERT INTO public.module_materials VALUES (114, 3, 298, false, 1, NULL, 1, '2026-07-13 07:57:19.119629');
INSERT INTO public.module_materials VALUES (115, 3, 297, false, 1, NULL, 1, '2026-07-13 07:57:19.136465');
INSERT INTO public.module_materials VALUES (116, 3, 296, false, 1, NULL, 1, '2026-07-13 07:57:19.153784');
INSERT INTO public.module_materials VALUES (117, 3, 295, false, 1, NULL, 1, '2026-07-13 07:57:19.185082');
INSERT INTO public.module_materials VALUES (118, 3, 294, false, 1, NULL, 1, '2026-07-13 07:57:19.209166');
INSERT INTO public.module_materials VALUES (119, 3, 293, false, 1, NULL, 1, '2026-07-13 07:57:19.229835');
INSERT INTO public.module_materials VALUES (120, 3, 292, false, 1, NULL, 1, '2026-07-13 07:57:19.254342');
INSERT INTO public.module_materials VALUES (121, 4, 392, false, 1, NULL, 1, '2026-07-13 07:57:36.656856');
INSERT INTO public.module_materials VALUES (122, 4, 391, false, 1, NULL, 1, '2026-07-13 07:57:36.732586');
INSERT INTO public.module_materials VALUES (123, 4, 390, false, 1, NULL, 1, '2026-07-13 07:57:37.115869');
INSERT INTO public.module_materials VALUES (124, 4, 389, false, 1, NULL, 1, '2026-07-13 07:57:37.207496');
INSERT INTO public.module_materials VALUES (125, 4, 388, false, 1, NULL, 1, '2026-07-13 07:57:37.235696');
INSERT INTO public.module_materials VALUES (126, 4, 387, false, 1, NULL, 1, '2026-07-13 07:57:37.258736');
INSERT INTO public.module_materials VALUES (127, 4, 386, false, 1, NULL, 1, '2026-07-13 07:57:37.27827');
INSERT INTO public.module_materials VALUES (128, 4, 385, false, 1, NULL, 1, '2026-07-13 07:57:37.298473');
INSERT INTO public.module_materials VALUES (129, 4, 384, false, 1, NULL, 1, '2026-07-13 07:57:37.320525');
INSERT INTO public.module_materials VALUES (130, 4, 383, false, 1, NULL, 1, '2026-07-13 07:57:37.348263');
INSERT INTO public.module_materials VALUES (131, 4, 382, false, 1, NULL, 1, '2026-07-13 07:57:37.370841');
INSERT INTO public.module_materials VALUES (132, 4, 381, false, 1, NULL, 1, '2026-07-13 07:57:37.420383');
INSERT INTO public.module_materials VALUES (133, 4, 380, false, 1, NULL, 1, '2026-07-13 07:57:37.478388');
INSERT INTO public.module_materials VALUES (134, 4, 379, false, 1, NULL, 1, '2026-07-13 07:57:37.583288');
INSERT INTO public.module_materials VALUES (135, 4, 378, false, 1, NULL, 1, '2026-07-13 07:57:37.59981');
INSERT INTO public.module_materials VALUES (136, 4, 377, false, 1, NULL, 1, '2026-07-13 07:57:37.614806');
INSERT INTO public.module_materials VALUES (137, 4, 376, false, 1, NULL, 1, '2026-07-13 07:57:37.629191');
INSERT INTO public.module_materials VALUES (139, 4, 374, false, 1, NULL, 1, '2026-07-13 07:57:37.671165');
INSERT INTO public.module_materials VALUES (138, 4, 375, false, 1, NULL, 1, '2026-07-13 07:57:37.645923');
INSERT INTO public.module_materials VALUES (140, 4, 373, false, 1, NULL, 1, '2026-07-13 07:57:37.706558');


ALTER TABLE public.module_materials ENABLE TRIGGER ALL;

--
-- Data for Name: module_participants; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.module_participants DISABLE TRIGGER ALL;



ALTER TABLE public.module_participants ENABLE TRIGGER ALL;

--
-- Data for Name: operation_logs; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.operation_logs DISABLE TRIGGER ALL;

INSERT INTO public.operation_logs VALUES (1, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 06:32:43.245254');
INSERT INTO public.operation_logs VALUES (2, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 06:32:43.441059');
INSERT INTO public.operation_logs VALUES (3, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 06:32:56.509792');
INSERT INTO public.operation_logs VALUES (4, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 06:32:56.510934');
INSERT INTO public.operation_logs VALUES (5, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 06:33:00.440388');
INSERT INTO public.operation_logs VALUES (6, 1, 'admin', 'logout', 'auth', 'user', '1', '用户 "admin" 登出', '127.0.0.1', 'system', '2026-07-13 07:19:58.723428');
INSERT INTO public.operation_logs VALUES (7, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:20:05.671956');
INSERT INTO public.operation_logs VALUES (8, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:20:05.672816');
INSERT INTO public.operation_logs VALUES (9, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:21:36.644458');
INSERT INTO public.operation_logs VALUES (10, 1, 'admin', 'delete', 'travel', 'travel_mode', '4', '删除 差旅/运输费用配置 轮船 (类型=出行方式)', '127.0.0.1', 'system', '2026-07-13 07:24:07.532432');
INSERT INTO public.operation_logs VALUES (11, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:24:29.425607');
INSERT INTO public.operation_logs VALUES (12, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:24:33.595187');
INSERT INTO public.operation_logs VALUES (13, 1, 'admin', 'create', 'ai', 'ai_conversation', 'cf7ca637-e89a-40', '创建 AI 会话 "新对话"', '127.0.0.1', 'system', '2026-07-13 07:24:47.863686');
INSERT INTO public.operation_logs VALUES (14, 1, 'admin', 'delete', 'role', 'participant_type', 'supplier', '删除参与类型: supplier (清理 3 条权限配置)', '127.0.0.1', 'system', '2026-07-13 07:28:02.649749');
INSERT INTO public.operation_logs VALUES (15, 1, 'admin', 'import', 'material', 'material', NULL, '导入物料 491/491 条 (创建 491, 更新 0, 失败 0)', '127.0.0.1', 'system', '2026-07-13 07:30:57.079759');
INSERT INTO public.operation_logs VALUES (16, 1, 'admin', 'create', 'material', 'material', '492', '创建物料 其他 (编码=其他, 分类=other)', '127.0.0.1', 'system', '2026-07-13 07:31:20.363683');
INSERT INTO public.operation_logs VALUES (17, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:37:53.453549');
INSERT INTO public.operation_logs VALUES (18, 1, '1', 'create', 'quotation', 'quotation', 'CS26005', '创建报价单 "自动折盒机"', '127.0.0.1', 'system', '2026-07-13 07:40:34.057614');
INSERT INTO public.operation_logs VALUES (19, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:41:04.923268');
INSERT INTO public.operation_logs VALUES (20, 1, '1', 'create', 'quotation', 'quotation', '2', '创建报价单 "测试报价单"', '127.0.0.1', 'system', '2026-07-13 07:41:04.970789');
INSERT INTO public.operation_logs VALUES (21, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:41:10.225725');
INSERT INTO public.operation_logs VALUES (22, 1, '1', 'create', 'quotation', 'quotation', '3', '创建报价单 "测试报价单"', '127.0.0.1', 'system', '2026-07-13 07:41:10.281643');
INSERT INTO public.operation_logs VALUES (23, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:42:15.838346');
INSERT INTO public.operation_logs VALUES (24, 1, '1', 'create', 'quotation', 'quotation_participant', '1', '添加报价单参与人 admin 为 机构 角色 (报价单: 自动折盒机)', '127.0.0.1', 'system', '2026-07-13 07:42:26.753035');
INSERT INTO public.operation_logs VALUES (25, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:43:29.72056');
INSERT INTO public.operation_logs VALUES (26, 1, 'admin', 'create', 'module', 'module', NULL, '推断模块类型: mechanical (来源=quotation_id, 数量=1)', '127.0.0.1', 'system', '2026-07-13 07:43:55.199333');
INSERT INTO public.operation_logs VALUES (27, 1, 'admin', 'create', 'module', 'module', '1', '创建模块 机构01 (代码=-, 报价单ID=1)', '127.0.0.1', 'system', '2026-07-13 07:44:11.844533');
INSERT INTO public.operation_logs VALUES (28, 1, 'admin', 'create', 'module', 'module', NULL, '推断模块类型: mechanical (来源=quotation_id, 数量=1)', '127.0.0.1', 'system', '2026-07-13 07:44:21.059778');
INSERT INTO public.operation_logs VALUES (29, 1, 'admin', 'create', 'module', 'module', '2', '创建模块 机构02 (代码=-, 报价单ID=1)', '127.0.0.1', 'system', '2026-07-13 07:44:28.571771');
INSERT INTO public.operation_logs VALUES (30, 1, 'admin', 'create', 'module', 'module', NULL, '推断模块类型: mechanical (来源=quotation_id, 数量=1)', '127.0.0.1', 'system', '2026-07-13 07:44:30.212053');
INSERT INTO public.operation_logs VALUES (31, 1, 'admin', 'create', 'module', 'module', '3', '创建模块 电气01 (代码=-, 报价单ID=1)', '127.0.0.1', 'system', '2026-07-13 07:44:40.071991');
INSERT INTO public.operation_logs VALUES (32, 1, 'admin', 'create', 'module', 'module', NULL, '推断模块类型: mechanical (来源=quotation_id, 数量=1)', '127.0.0.1', 'system', '2026-07-13 07:44:42.670318');
INSERT INTO public.operation_logs VALUES (33, 1, 'admin', 'create', 'module', 'module', '4', '创建模块 其他 (代码=-, 报价单ID=1)', '127.0.0.1', 'system', '2026-07-13 07:44:52.596723');
INSERT INTO public.operation_logs VALUES (34, 1, 'admin', 'create', 'fee', 'other_fee', '1', '创建费用 20000.0元 (认证费)', '127.0.0.1', 'system', '2026-07-13 07:45:00.450647');
INSERT INTO public.operation_logs VALUES (35, 1, 'admin', 'create', 'fee', 'other_fee', '2', '创建费用 25000.0元 (项目管理费)', '127.0.0.1', 'system', '2026-07-13 07:45:10.284038');
INSERT INTO public.operation_logs VALUES (36, 1, 'admin', 'create', 'labor_hours', 'labor_hour', '1', '创建 人力工时 "机械设计" (类型=design, 工时=80.0, 单价=0.0, 小计=0.0)', '127.0.0.1', 'system', '2026-07-13 07:45:18.391057');
INSERT INTO public.operation_logs VALUES (37, 1, 'admin', 'create', 'labor_hours', 'labor_hour', '2', '创建 人力工时 "生产装配" (类型=assembly, 工时=160.0, 单价=0.0, 小计=0.0)', '127.0.0.1', 'system', '2026-07-13 07:45:27.242282');
INSERT INTO public.operation_logs VALUES (38, 1, 'admin', 'create', 'labor_hours', 'labor_hour', '3', '创建 人力工时 "软件编程厂外调试（C#&Vision&robot）" (类型=debug, 工时=80.0, 单价=0.0, 小计=0.0)', '127.0.0.1', 'system', '2026-07-13 07:45:33.132061');
INSERT INTO public.operation_logs VALUES (39, 1, 'admin', 'create', 'travel', 'person_days', '1', '添加 差旅人天 (报价单#1, 差旅类别#8, 人天=10, 单价=0.0)', '127.0.0.1', 'system', '2026-07-13 07:45:46.438864');
INSERT INTO public.operation_logs VALUES (40, 1, 'admin', 'create', 'travel', 'person_trips', '1', '添加 差旅人次 (报价单#1, 差旅类别#8, 出行方式#5, 人次=10, 单价=1200.0, 签证费=0.0)', '127.0.0.1', 'system', '2026-07-13 07:45:57.516731');
INSERT INTO public.operation_logs VALUES (41, 1, '1', 'delete', 'quotation', 'quotation', '3', '删除报价单 "测试报价单" (3)', '127.0.0.1', 'system', '2026-07-13 07:56:26.208693');
INSERT INTO public.operation_logs VALUES (42, 1, '1', 'delete', 'quotation', 'quotation', '2', '删除报价单 "测试报价单" (2)', '127.0.0.1', 'system', '2026-07-13 07:56:34.228067');
INSERT INTO public.operation_logs VALUES (43, 1, 'admin', 'create', 'module', 'module_material', '1', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.667985');
INSERT INTO public.operation_logs VALUES (44, 1, 'admin', 'create', 'module', 'module_material', '2', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.711985');
INSERT INTO public.operation_logs VALUES (45, 1, 'admin', 'create', 'module', 'module_material', '3', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.756643');
INSERT INTO public.operation_logs VALUES (46, 1, 'admin', 'create', 'module', 'module_material', '4', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.849514');
INSERT INTO public.operation_logs VALUES (47, 1, 'admin', 'create', 'module', 'module_material', '5', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.870427');
INSERT INTO public.operation_logs VALUES (48, 1, 'admin', 'create', 'module', 'module_material', '6', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.891702');
INSERT INTO public.operation_logs VALUES (49, 1, 'admin', 'create', 'module', 'module_material', '7', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.939709');
INSERT INTO public.operation_logs VALUES (50, 1, 'admin', 'create', 'module', 'module_material', '8', '添加物料 彩色相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.97369');
INSERT INTO public.operation_logs VALUES (51, 1, 'admin', 'create', 'module', 'module_material', '9', '添加物料 3D相机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:50.996109');
INSERT INTO public.operation_logs VALUES (52, 1, 'admin', 'create', 'module', 'module_material', '10', '添加物料 线激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.017047');
INSERT INTO public.operation_logs VALUES (53, 1, 'admin', 'create', 'module', 'module_material', '11', '添加物料 线激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.041517');
INSERT INTO public.operation_logs VALUES (54, 1, 'admin', 'create', 'module', 'module_material', '12', '添加物料 线激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.201674');
INSERT INTO public.operation_logs VALUES (56, 1, 'admin', 'create', 'module', 'module_material', '14', '添加物料 线激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.252212');
INSERT INTO public.operation_logs VALUES (58, 1, 'admin', 'create', 'module', 'module_material', '16', '添加物料 点激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.306887');
INSERT INTO public.operation_logs VALUES (60, 1, 'admin', 'create', 'module', 'module_material', '18', '添加物料 点激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.350694');
INSERT INTO public.operation_logs VALUES (62, 1, 'admin', 'create', 'module', 'module_material', '20', '添加物料 振动盘 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.392785');
INSERT INTO public.operation_logs VALUES (64, 1, 'admin', 'create', 'module', 'module_material', '22', '添加物料 振动盘 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.438098');
INSERT INTO public.operation_logs VALUES (66, 1, 'admin', 'create', 'module', 'module_material', '24', '添加物料 氦气检测仪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.48454');
INSERT INTO public.operation_logs VALUES (68, 1, 'admin', 'create', 'module', 'module_material', '26', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.531395');
INSERT INTO public.operation_logs VALUES (70, 1, 'admin', 'create', 'module', 'module_material', '28', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.572641');
INSERT INTO public.operation_logs VALUES (72, 1, 'admin', 'create', 'module', 'module_material', '30', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.614091');
INSERT INTO public.operation_logs VALUES (74, 1, 'admin', 'create', 'module', 'module_material', '32', '添加物料 压机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.651879');
INSERT INTO public.operation_logs VALUES (78, 1, 'admin', 'create', 'module', 'module_material', '36', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.749725');
INSERT INTO public.operation_logs VALUES (80, 1, 'admin', 'create', 'module', 'module_material', '38', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.78407');
INSERT INTO public.operation_logs VALUES (82, 1, 'admin', 'create', 'module', 'module_material', '40', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.824567');
INSERT INTO public.operation_logs VALUES (84, 1, 'admin', 'create', 'module', 'module_material', '42', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.862025');
INSERT INTO public.operation_logs VALUES (86, 1, 'admin', 'create', 'module', 'module_material', '44', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.894922');
INSERT INTO public.operation_logs VALUES (88, 1, 'admin', 'create', 'module', 'module_material', '46', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.9412');
INSERT INTO public.operation_logs VALUES (90, 1, 'admin', 'create', 'module', 'module_material', '48', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:52.009537');
INSERT INTO public.operation_logs VALUES (92, 1, 'admin', 'create', 'module', 'module_material', '50', '添加物料 协作机械手 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:52.038537');
INSERT INTO public.operation_logs VALUES (55, 1, 'admin', 'create', 'module', 'module_material', '13', '添加物料 线激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.226378');
INSERT INTO public.operation_logs VALUES (59, 1, 'admin', 'create', 'module', 'module_material', '17', '添加物料 点激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.327323');
INSERT INTO public.operation_logs VALUES (61, 1, 'admin', 'create', 'module', 'module_material', '19', '添加物料 振动盘 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.375159');
INSERT INTO public.operation_logs VALUES (63, 1, 'admin', 'create', 'module', 'module_material', '21', '添加物料 振动盘 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.415005');
INSERT INTO public.operation_logs VALUES (65, 1, 'admin', 'create', 'module', 'module_material', '23', '添加物料 氦气检测仪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.460773');
INSERT INTO public.operation_logs VALUES (73, 1, 'admin', 'create', 'module', 'module_material', '31', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.632796');
INSERT INTO public.operation_logs VALUES (75, 1, 'admin', 'create', 'module', 'module_material', '33', '添加物料 压机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.6746');
INSERT INTO public.operation_logs VALUES (79, 1, 'admin', 'create', 'module', 'module_material', '37', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.768064');
INSERT INTO public.operation_logs VALUES (81, 1, 'admin', 'create', 'module', 'module_material', '39', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.806433');
INSERT INTO public.operation_logs VALUES (83, 1, 'admin', 'create', 'module', 'module_material', '41', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.845539');
INSERT INTO public.operation_logs VALUES (85, 1, 'admin', 'create', 'module', 'module_material', '43', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.87769');
INSERT INTO public.operation_logs VALUES (89, 1, 'admin', 'create', 'module', 'module_material', '47', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.987149');
INSERT INTO public.operation_logs VALUES (91, 1, 'admin', 'create', 'module', 'module_material', '49', '添加物料 协作机械手 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:52.024975');
INSERT INTO public.operation_logs VALUES (57, 1, 'admin', 'create', 'module', 'module_material', '15', '添加物料 点激光检测 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.279193');
INSERT INTO public.operation_logs VALUES (71, 1, 'admin', 'create', 'module', 'module_material', '29', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.592836');
INSERT INTO public.operation_logs VALUES (67, 1, 'admin', 'create', 'module', 'module_material', '25', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.507619');
INSERT INTO public.operation_logs VALUES (77, 1, 'admin', 'create', 'module', 'module_material', '35', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.732988');
INSERT INTO public.operation_logs VALUES (69, 1, 'admin', 'create', 'module', 'module_material', '27', '添加物料 镭雕机 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.550251');
INSERT INTO public.operation_logs VALUES (87, 1, 'admin', 'create', 'module', 'module_material', '45', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.913905');
INSERT INTO public.operation_logs VALUES (76, 1, 'admin', 'create', 'module', 'module_material', '34', '添加物料 螺丝枪 x 1pcs (模块=机构01)', '127.0.0.1', 'system', '2026-07-13 07:56:51.713495');
INSERT INTO public.operation_logs VALUES (93, 1, 'admin', 'create', 'module', 'module_material', '51', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.552736');
INSERT INTO public.operation_logs VALUES (94, 1, 'admin', 'create', 'module', 'module_material', '52', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.586579');
INSERT INTO public.operation_logs VALUES (95, 1, 'admin', 'create', 'module', 'module_material', '53', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.631225');
INSERT INTO public.operation_logs VALUES (96, 1, 'admin', 'create', 'module', 'module_material', '54', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.653324');
INSERT INTO public.operation_logs VALUES (97, 1, 'admin', 'create', 'module', 'module_material', '55', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.68884');
INSERT INTO public.operation_logs VALUES (98, 1, 'admin', 'create', 'module', 'module_material', '56', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.716212');
INSERT INTO public.operation_logs VALUES (99, 1, 'admin', 'create', 'module', 'module_material', '57', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.741026');
INSERT INTO public.operation_logs VALUES (100, 1, 'admin', 'create', 'module', 'module_material', '58', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.774157');
INSERT INTO public.operation_logs VALUES (101, 1, 'admin', 'create', 'module', 'module_material', '59', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.797098');
INSERT INTO public.operation_logs VALUES (102, 1, 'admin', 'create', 'module', 'module_material', '60', '添加物料 超声波传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.823602');
INSERT INTO public.operation_logs VALUES (103, 1, 'admin', 'create', 'module', 'module_material', '61', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.847441');
INSERT INTO public.operation_logs VALUES (104, 1, 'admin', 'create', 'module', 'module_material', '62', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.873186');
INSERT INTO public.operation_logs VALUES (105, 1, 'admin', 'create', 'module', 'module_material', '63', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:06.896912');
INSERT INTO public.operation_logs VALUES (106, 1, 'admin', 'create', 'module', 'module_material', '64', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.018102');
INSERT INTO public.operation_logs VALUES (107, 1, 'admin', 'create', 'module', 'module_material', '65', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.101503');
INSERT INTO public.operation_logs VALUES (108, 1, 'admin', 'create', 'module', 'module_material', '66', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.127173');
INSERT INTO public.operation_logs VALUES (109, 1, 'admin', 'create', 'module', 'module_material', '67', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.165839');
INSERT INTO public.operation_logs VALUES (110, 1, 'admin', 'create', 'module', 'module_material', '68', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.191199');
INSERT INTO public.operation_logs VALUES (111, 1, 'admin', 'create', 'module', 'module_material', '69', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.216575');
INSERT INTO public.operation_logs VALUES (112, 1, 'admin', 'create', 'module', 'module_material', '70', '添加物料 位移传感器 x 1pcs (模块=机构02)', '127.0.0.1', 'system', '2026-07-13 07:57:07.26852');
INSERT INTO public.operation_logs VALUES (113, 1, 'admin', 'create', 'module', 'module_material', '71', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:17.657272');
INSERT INTO public.operation_logs VALUES (114, 1, 'admin', 'create', 'module', 'module_material', '72', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:17.74043');
INSERT INTO public.operation_logs VALUES (115, 1, 'admin', 'create', 'module', 'module_material', '73', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:17.887414');
INSERT INTO public.operation_logs VALUES (116, 1, 'admin', 'create', 'module', 'module_material', '74', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:17.964255');
INSERT INTO public.operation_logs VALUES (117, 1, 'admin', 'create', 'module', 'module_material', '75', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.010169');
INSERT INTO public.operation_logs VALUES (118, 1, 'admin', 'create', 'module', 'module_material', '76', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.033155');
INSERT INTO public.operation_logs VALUES (119, 1, 'admin', 'create', 'module', 'module_material', '77', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.223205');
INSERT INTO public.operation_logs VALUES (120, 1, 'admin', 'create', 'module', 'module_material', '78', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.244108');
INSERT INTO public.operation_logs VALUES (121, 1, 'admin', 'create', 'module', 'module_material', '79', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.265541');
INSERT INTO public.operation_logs VALUES (122, 1, 'admin', 'create', 'module', 'module_material', '80', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.284224');
INSERT INTO public.operation_logs VALUES (123, 1, 'admin', 'create', 'module', 'module_material', '81', '添加物料 HMI操作面板 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.315755');
INSERT INTO public.operation_logs VALUES (124, 1, 'admin', 'create', 'module', 'module_material', '82', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.342991');
INSERT INTO public.operation_logs VALUES (125, 1, 'admin', 'create', 'module', 'module_material', '83', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.362677');
INSERT INTO public.operation_logs VALUES (126, 1, 'admin', 'create', 'module', 'module_material', '84', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.385217');
INSERT INTO public.operation_logs VALUES (127, 1, 'admin', 'create', 'module', 'module_material', '85', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.406612');
INSERT INTO public.operation_logs VALUES (128, 1, 'admin', 'create', 'module', 'module_material', '86', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.427787');
INSERT INTO public.operation_logs VALUES (129, 1, 'admin', 'create', 'module', 'module_material', '87', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.452442');
INSERT INTO public.operation_logs VALUES (130, 1, 'admin', 'create', 'module', 'module_material', '88', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.470374');
INSERT INTO public.operation_logs VALUES (131, 1, 'admin', 'create', 'module', 'module_material', '89', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.489793');
INSERT INTO public.operation_logs VALUES (132, 1, 'admin', 'create', 'module', 'module_material', '90', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.506383');
INSERT INTO public.operation_logs VALUES (133, 1, 'admin', 'create', 'module', 'module_material', '91', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.527093');
INSERT INTO public.operation_logs VALUES (134, 1, 'admin', 'create', 'module', 'module_material', '92', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.542611');
INSERT INTO public.operation_logs VALUES (135, 1, 'admin', 'create', 'module', 'module_material', '93', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.56317');
INSERT INTO public.operation_logs VALUES (136, 1, 'admin', 'create', 'module', 'module_material', '94', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.588665');
INSERT INTO public.operation_logs VALUES (137, 1, 'admin', 'create', 'module', 'module_material', '95', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.606619');
INSERT INTO public.operation_logs VALUES (138, 1, 'admin', 'create', 'module', 'module_material', '96', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.625934');
INSERT INTO public.operation_logs VALUES (139, 1, 'admin', 'create', 'module', 'module_material', '97', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.647096');
INSERT INTO public.operation_logs VALUES (140, 1, 'admin', 'create', 'module', 'module_material', '98', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.668946');
INSERT INTO public.operation_logs VALUES (141, 1, 'admin', 'create', 'module', 'module_material', '99', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.69516');
INSERT INTO public.operation_logs VALUES (142, 1, 'admin', 'create', 'module', 'module_material', '100', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.71812');
INSERT INTO public.operation_logs VALUES (143, 1, 'admin', 'create', 'module', 'module_material', '101', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.737199');
INSERT INTO public.operation_logs VALUES (145, 1, 'admin', 'create', 'module', 'module_material', '103', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.775425');
INSERT INTO public.operation_logs VALUES (147, 1, 'admin', 'create', 'module', 'module_material', '105', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.818684');
INSERT INTO public.operation_logs VALUES (148, 1, 'admin', 'create', 'module', 'module_material', '106', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.844958');
INSERT INTO public.operation_logs VALUES (149, 1, 'admin', 'create', 'module', 'module_material', '107', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.864781');
INSERT INTO public.operation_logs VALUES (151, 1, 'admin', 'create', 'module', 'module_material', '109', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.924934');
INSERT INTO public.operation_logs VALUES (153, 1, 'admin', 'create', 'module', 'module_material', '111', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.00832');
INSERT INTO public.operation_logs VALUES (155, 1, 'admin', 'create', 'module', 'module_material', '113', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.102807');
INSERT INTO public.operation_logs VALUES (158, 1, 'admin', 'create', 'module', 'module_material', '116', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.156536');
INSERT INTO public.operation_logs VALUES (163, 1, 'admin', 'create', 'module', 'module_material', '121', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:36.66006');
INSERT INTO public.operation_logs VALUES (180, 1, 'admin', 'create', 'module', 'module_material', '138', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.648494');
INSERT INTO public.operation_logs VALUES (182, 1, 'admin', 'create', 'module', 'module_material', '140', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.709289');
INSERT INTO public.operation_logs VALUES (144, 1, 'admin', 'create', 'module', 'module_material', '102', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.754784');
INSERT INTO public.operation_logs VALUES (150, 1, 'admin', 'create', 'module', 'module_material', '108', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.88791');
INSERT INTO public.operation_logs VALUES (160, 1, 'admin', 'create', 'module', 'module_material', '118', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.214346');
INSERT INTO public.operation_logs VALUES (169, 1, 'admin', 'create', 'module', 'module_material', '127', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.280862');
INSERT INTO public.operation_logs VALUES (146, 1, 'admin', 'create', 'module', 'module_material', '104', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.79963');
INSERT INTO public.operation_logs VALUES (152, 1, 'admin', 'create', 'module', 'module_material', '110', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:18.959058');
INSERT INTO public.operation_logs VALUES (162, 1, 'admin', 'create', 'module', 'module_material', '120', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.258548');
INSERT INTO public.operation_logs VALUES (154, 1, 'admin', 'create', 'module', 'module_material', '112', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.079917');
INSERT INTO public.operation_logs VALUES (156, 1, 'admin', 'create', 'module', 'module_material', '114', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.122148');
INSERT INTO public.operation_logs VALUES (165, 1, 'admin', 'create', 'module', 'module_material', '123', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.11877');
INSERT INTO public.operation_logs VALUES (167, 1, 'admin', 'create', 'module', 'module_material', '125', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.238002');
INSERT INTO public.operation_logs VALUES (171, 1, 'admin', 'create', 'module', 'module_material', '129', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.322878');
INSERT INTO public.operation_logs VALUES (173, 1, 'admin', 'create', 'module', 'module_material', '131', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.373167');
INSERT INTO public.operation_logs VALUES (175, 1, 'admin', 'create', 'module', 'module_material', '133', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.480685');
INSERT INTO public.operation_logs VALUES (177, 1, 'admin', 'create', 'module', 'module_material', '135', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.601979');
INSERT INTO public.operation_logs VALUES (179, 1, 'admin', 'create', 'module', 'module_material', '137', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.632073');
INSERT INTO public.operation_logs VALUES (181, 1, 'admin', 'create', 'module', 'module_material', '139', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.675067');
INSERT INTO public.operation_logs VALUES (157, 1, 'admin', 'create', 'module', 'module_material', '115', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.13893');
INSERT INTO public.operation_logs VALUES (159, 1, 'admin', 'create', 'module', 'module_material', '117', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.190328');
INSERT INTO public.operation_logs VALUES (161, 1, 'admin', 'create', 'module', 'module_material', '119', '添加物料 PLC控制器 x 1pcs (模块=电气01)', '127.0.0.1', 'system', '2026-07-13 07:57:19.234666');
INSERT INTO public.operation_logs VALUES (164, 1, 'admin', 'create', 'module', 'module_material', '122', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:36.735506');
INSERT INTO public.operation_logs VALUES (166, 1, 'admin', 'create', 'module', 'module_material', '124', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.210668');
INSERT INTO public.operation_logs VALUES (168, 1, 'admin', 'create', 'module', 'module_material', '126', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.262513');
INSERT INTO public.operation_logs VALUES (170, 1, 'admin', 'create', 'module', 'module_material', '128', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.300763');
INSERT INTO public.operation_logs VALUES (172, 1, 'admin', 'create', 'module', 'module_material', '130', '添加物料 安全器件模块 x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.35037');
INSERT INTO public.operation_logs VALUES (174, 1, 'admin', 'create', 'module', 'module_material', '132', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.42271');
INSERT INTO public.operation_logs VALUES (176, 1, 'admin', 'create', 'module', 'module_material', '134', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.585503');
INSERT INTO public.operation_logs VALUES (178, 1, 'admin', 'create', 'module', 'module_material', '136', '添加物料 分布式站点（柜外） x 1pcs (模块=其他)', '127.0.0.1', 'system', '2026-07-13 07:57:37.617086');
INSERT INTO public.operation_logs VALUES (183, 1, 'admin', 'login', 'auth', 'user', '1', '用户 "admin" 登录成功', '127.0.0.1', 'system', '2026-07-13 07:58:16.119102');
INSERT INTO public.operation_logs VALUES (184, 1, 'admin', 'update', 'labor_hours', 'labor_hour', '1', '更新 人力工时 "机械设计" (字段: name, hours, unit_price, labor_type) (工时=80.0, 单价=200.0, 小计=16000.0)', '127.0.0.1', 'system', '2026-07-13 08:03:04.826113');
INSERT INTO public.operation_logs VALUES (185, 1, 'admin', 'update', 'labor_hours', 'labor_hour', '3', '更新 人力工时 "软件编程厂外调试（C#&Vision&robot）" (字段: name, hours, unit_price, labor_type) (工时=80.0, 单价=200.0, 小计=16000.0)', '127.0.0.1', 'system', '2026-07-13 08:03:12.083803');
INSERT INTO public.operation_logs VALUES (186, 1, 'admin', 'update', 'labor_hours', 'labor_hour', '2', '更新 人力工时 "生产装配" (字段: name, hours, unit_price, labor_type) (工时=160.0, 单价=200.0, 小计=32000.0)', '127.0.0.1', 'system', '2026-07-13 08:03:16.011858');
INSERT INTO public.operation_logs VALUES (187, 1, 'admin', 'update', 'travel', 'person_days', '1', '更新 差旅人天 #1 (人天=60, 单价=600.0)', '127.0.0.1', 'system', '2026-07-13 08:11:59.750511');
INSERT INTO public.operation_logs VALUES (188, 1, 'admin', 'create', 'travel', 'travel_packing', '1', '添加 运输包装 (报价单#1, 包装类型#2, 数量=6, 单价=None)', '127.0.0.1', 'system', '2026-07-13 08:14:07.064255');
INSERT INTO public.operation_logs VALUES (189, 1, 'admin', 'view', 'ai', 'ai_query', '940f377c-8cb4-4d', 'AI 咨询: 你好 (报价单=无)', '127.0.0.1', 'system', '2026-07-13 08:14:55.104545');
INSERT INTO public.operation_logs VALUES (190, 1, 'admin', 'view', 'ai', 'ai_query', '940f377c-8cb4-4d', 'AI 咨询: 你能作甚恶魔 (报价单=无)', '127.0.0.1', 'system', '2026-07-13 08:15:04.796371');
INSERT INTO public.operation_logs VALUES (191, 1, '1', 'create', 'quotation', 'quotation', 'C2568', '创建报价单 "JOT流线组件"', '127.0.0.1', 'system', '2026-07-13 08:15:56.032383');
INSERT INTO public.operation_logs VALUES (192, 1, '1', 'delete', 'quotation', 'quotation', '4', '删除报价单 "JOT流线组件" (C2568)', '127.0.0.1', 'system', '2026-07-13 08:16:02.146952');
INSERT INTO public.operation_logs VALUES (193, 1, 'admin', 'update', 'travel', 'packing_type', '1', '更新 差旅/运输费用配置 框架箱海运费 (类型=包装类型) (字段: name, name_en) (单价=50.0)', '127.0.0.1', 'system', '2026-07-13 08:29:34.855634');
INSERT INTO public.operation_logs VALUES (194, 1, 'admin', 'update', 'travel', 'packing_type', '1', '更新 差旅/运输费用配置 框架箱海运 (类型=包装类型) (字段: name, name_en) (单价=50.0)', '127.0.0.1', 'system', '2026-07-13 08:29:47.675097');
INSERT INTO public.operation_logs VALUES (195, 1, 'admin', 'update', 'travel', 'packing_type', '2', '更新 差旅/运输费用配置 40HQ海运费 (类型=包装类型) (字段: name, name_en) (单价=200.0)', '127.0.0.1', 'system', '2026-07-13 08:29:54.605852');
INSERT INTO public.operation_logs VALUES (196, 1, 'admin', 'update', 'travel', 'packing_type', '3', '更新 差旅/运输费用配置 货物空运 (类型=包装类型) (字段: name, name_en) (单价=500.0)', '127.0.0.1', 'system', '2026-07-13 08:30:06.262777');
INSERT INTO public.operation_logs VALUES (197, 1, 'admin', 'update', 'travel', 'packing_type', '4', '更新 差旅/运输费用配置 路面货车 (类型=包装类型) (字段: name, name_en) (单价=30.0)', '127.0.0.1', 'system', '2026-07-13 08:30:14.779113');
INSERT INTO public.operation_logs VALUES (198, 1, 'admin', 'delete', 'travel', 'packing_type', '5', '删除 差旅/运输费用配置 其他 (类型=包装类型)', '127.0.0.1', 'system', '2026-07-13 08:31:01.733108');
INSERT INTO public.operation_logs VALUES (199, 1, 'admin', 'create', 'travel', 'packing_type', '6', '创建 差旅/运输费用配置 框架箱提货报关港口费 (类型=包装类型, 单价=1000.0)', '127.0.0.1', 'system', '2026-07-13 08:31:33.563894');
INSERT INTO public.operation_logs VALUES (200, 1, 'admin', 'create', 'travel', 'packing_type', '7', '创建 差旅/运输费用配置 40HQ提货报关港口费 (类型=包装类型, 单价=500.0)', '127.0.0.1', 'system', '2026-07-13 08:31:52.694082');
INSERT INTO public.operation_logs VALUES (201, 1, 'admin', 'create', 'travel', 'packing_type', '8', '创建 差旅/运输费用配置 货物空运提货报关港口费 (类型=包装类型, 单价=800.0)', '127.0.0.1', 'system', '2026-07-13 08:32:02.862272');


ALTER TABLE public.operation_logs ENABLE TRIGGER ALL;

--
-- Data for Name: other_fees; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.other_fees DISABLE TRIGGER ALL;

INSERT INTO public.other_fees VALUES (1, 1, NULL, '认证费', 'external', 20000.00, '', '2026-07-13 07:45:00.446231', 1);
INSERT INTO public.other_fees VALUES (2, 1, NULL, '项目管理费', 'external', 25000.00, '', '2026-07-13 07:45:10.279436', 2);


ALTER TABLE public.other_fees ENABLE TRIGGER ALL;

--
-- Data for Name: packing_types; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.packing_types DISABLE TRIGGER ALL;

INSERT INTO public.packing_types VALUES (1, '框架箱海运', '框架箱海运', 50.00, NULL, true, '2026-07-13 06:39:51.685454', '2026-07-13 08:29:47.652909');
INSERT INTO public.packing_types VALUES (2, '40HQ海运费', '40HQ海运费', 200.00, NULL, true, '2026-07-13 06:39:51.687141', '2026-07-13 08:29:54.601536');
INSERT INTO public.packing_types VALUES (3, '货物空运', '货物空运', 500.00, NULL, true, '2026-07-13 06:39:51.688177', '2026-07-13 08:30:06.259336');
INSERT INTO public.packing_types VALUES (4, '路面货车', '路面货车', 30.00, NULL, true, '2026-07-13 06:39:51.689168', '2026-07-13 08:30:14.774866');
INSERT INTO public.packing_types VALUES (5, '其他', NULL, 0.00, NULL, false, '2026-07-13 06:39:51.689987', '2026-07-13 08:31:01.729842');
INSERT INTO public.packing_types VALUES (6, '框架箱提货报关港口费', '框架箱提货报关港口费', 1000.00, '', true, '2026-07-13 08:31:33.559677', '2026-07-13 08:31:33.559689');
INSERT INTO public.packing_types VALUES (7, '40HQ提货报关港口费', '40HQ提货报关港口费', 500.00, '', true, '2026-07-13 08:31:52.6899', '2026-07-13 08:31:52.689904');
INSERT INTO public.packing_types VALUES (8, '货物空运提货报关港口费', '货物空运提货报关港口费', 800.00, '', true, '2026-07-13 08:32:02.856567', '2026-07-13 08:32:02.856578');


ALTER TABLE public.packing_types ENABLE TRIGGER ALL;

--
-- Data for Name: packing_entries; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.packing_entries DISABLE TRIGGER ALL;

INSERT INTO public.packing_entries VALUES (1, 1, 2, 6, NULL, '', '2026-07-13 08:14:07.060566', '2026-07-13 08:14:07.06057');


ALTER TABLE public.packing_entries ENABLE TRIGGER ALL;

--
-- Data for Name: participant_type_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.participant_type_permissions DISABLE TRIGGER ALL;

INSERT INTO public.participant_type_permissions VALUES (1, 'project', 'modules', '模块管理', '添加、编辑、删除模块', '项目', 1, false, '2026-07-13 07:27:29.976979', '2026-07-13 07:27:29.976984');
INSERT INTO public.participant_type_permissions VALUES (2, 'project', 'participants', '参与人员', '管理报价单参与人员', '项目', 2, false, '2026-07-13 07:27:29.979508', '2026-07-13 07:27:29.979511');
INSERT INTO public.participant_type_permissions VALUES (3, 'project', 'coefficients', '费用系数', '调整大件/核心部件/其他件系数', '项目', 3, false, '2026-07-13 07:27:29.98064', '2026-07-13 07:27:29.980644');
INSERT INTO public.participant_type_permissions VALUES (4, 'project', 'materials', '物料清单', '物料选择与报价', '项目', 4, false, '2026-07-13 07:27:29.981651', '2026-07-13 07:27:29.981654');
INSERT INTO public.participant_type_permissions VALUES (5, 'project', 'fees', '费用', '附加费用配置', '项目', 5, false, '2026-07-13 07:27:29.982612', '2026-07-13 07:27:29.982615');
INSERT INTO public.participant_type_permissions VALUES (6, 'project', 'labor', '人力工时', '人力工时统计', '项目', 6, false, '2026-07-13 07:27:29.983555', '2026-07-13 07:27:29.983558');
INSERT INTO public.participant_type_permissions VALUES (7, 'project', 'summary', '汇总', '查看费用汇总', '项目', 7, false, '2026-07-13 07:27:29.984459', '2026-07-13 07:27:29.984462');
INSERT INTO public.participant_type_permissions VALUES (8, 'project', 'export', '导出', '导出 Excel/PDF', '项目', 8, false, '2026-07-13 07:27:29.98536', '2026-07-13 07:27:29.985363');
INSERT INTO public.participant_type_permissions VALUES (9, 'project', 'packing', '运输包装', '运输包装配置', '项目', 9, false, '2026-07-13 07:27:29.986233', '2026-07-13 07:27:29.986236');
INSERT INTO public.participant_type_permissions VALUES (10, 'project', 'travel_person_days', '差旅人天', '差旅人天统计', '项目', 10, false, '2026-07-13 07:27:29.987113', '2026-07-13 07:27:29.987116');
INSERT INTO public.participant_type_permissions VALUES (11, 'project', 'travel_person_trips', '差旅人次', '差旅人次统计', '项目', 11, false, '2026-07-13 07:27:29.987982', '2026-07-13 07:27:29.987985');
INSERT INTO public.participant_type_permissions VALUES (12, 'agency', 'modules', '模块管理', '查看模块', '机构', 1, false, '2026-07-13 07:27:29.988903', '2026-07-13 07:27:29.988906');
INSERT INTO public.participant_type_permissions VALUES (13, 'agency', 'materials', '物料清单', '物料选择与报价', '机构', 2, false, '2026-07-13 07:27:29.989791', '2026-07-13 07:27:29.989794');
INSERT INTO public.participant_type_permissions VALUES (14, 'agency', 'fees', '费用', '附加费用配置', '机构', 3, false, '2026-07-13 07:27:29.990686', '2026-07-13 07:27:29.990689');
INSERT INTO public.participant_type_permissions VALUES (15, 'agency', 'labor', '人力工时', '人力工时统计', '机构', 4, false, '2026-07-13 07:27:29.99159', '2026-07-13 07:27:29.991593');
INSERT INTO public.participant_type_permissions VALUES (16, 'agency', 'summary', '汇总', '查看费用汇总', '机构', 5, false, '2026-07-13 07:27:29.992465', '2026-07-13 07:27:29.992468');
INSERT INTO public.participant_type_permissions VALUES (17, 'agency', 'export', '导出', '导出 Excel/PDF', '机构', 6, false, '2026-07-13 07:27:29.993335', '2026-07-13 07:27:29.993338');
INSERT INTO public.participant_type_permissions VALUES (18, 'agency', 'packing', '运输包装', '运输包装配置', '机构', 7, false, '2026-07-13 07:27:29.994218', '2026-07-13 07:27:29.994221');
INSERT INTO public.participant_type_permissions VALUES (19, 'agency', 'travel_person_days', '差旅人天', '差旅人天统计', '机构', 8, false, '2026-07-13 07:27:29.995092', '2026-07-13 07:27:29.995095');
INSERT INTO public.participant_type_permissions VALUES (20, 'agency', 'travel_person_trips', '差旅人次', '差旅人次统计', '机构', 9, false, '2026-07-13 07:27:29.995979', '2026-07-13 07:27:29.995982');
INSERT INTO public.participant_type_permissions VALUES (21, 'electrical', 'modules', '模块管理', '查看模块', '电气', 1, false, '2026-07-13 07:27:29.996846', '2026-07-13 07:27:29.996848');
INSERT INTO public.participant_type_permissions VALUES (22, 'electrical', 'materials', '物料清单', '物料选择与报价', '电气', 2, false, '2026-07-13 07:27:29.997722', '2026-07-13 07:27:29.997724');
INSERT INTO public.participant_type_permissions VALUES (23, 'electrical', 'fees', '费用', '附加费用配置', '电气', 3, false, '2026-07-13 07:27:29.998633', '2026-07-13 07:27:29.998636');
INSERT INTO public.participant_type_permissions VALUES (24, 'electrical', 'labor', '人力工时', '人力工时统计', '电气', 4, false, '2026-07-13 07:27:29.999663', '2026-07-13 07:27:29.999666');
INSERT INTO public.participant_type_permissions VALUES (25, 'electrical', 'summary', '汇总', '查看费用汇总', '电气', 5, false, '2026-07-13 07:27:30.000815', '2026-07-13 07:27:30.000817');
INSERT INTO public.participant_type_permissions VALUES (26, 'electrical', 'export', '导出', '导出 Excel/PDF', '电气', 6, false, '2026-07-13 07:27:30.00198', '2026-07-13 07:27:30.001983');
INSERT INTO public.participant_type_permissions VALUES (27, 'electrical', 'packing', '运输包装', '运输包装配置', '电气', 7, false, '2026-07-13 07:27:30.003165', '2026-07-13 07:27:30.003168');
INSERT INTO public.participant_type_permissions VALUES (28, 'electrical', 'travel_person_days', '差旅人天', '差旅人天统计', '电气', 8, false, '2026-07-13 07:27:30.004328', '2026-07-13 07:27:30.004331');
INSERT INTO public.participant_type_permissions VALUES (29, 'electrical', 'travel_person_trips', '差旅人次', '差旅人次统计', '电气', 9, false, '2026-07-13 07:27:30.005467', '2026-07-13 07:27:30.00547');


ALTER TABLE public.participant_type_permissions ENABLE TRIGGER ALL;

--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.permissions DISABLE TRIGGER ALL;

INSERT INTO public.permissions VALUES (1, 'dashboard.view', '查看首页', '首页', NULL);
INSERT INTO public.permissions VALUES (2, 'quotation.view', '查看报价单', '报价单', NULL);
INSERT INTO public.permissions VALUES (3, 'quotation.create', '创建报价单', '报价单', NULL);
INSERT INTO public.permissions VALUES (4, 'quotation.edit', '编辑报价单', '报价单', NULL);
INSERT INTO public.permissions VALUES (5, 'quotation.delete', '删除报价单', '报价单', NULL);
INSERT INTO public.permissions VALUES (6, 'quotation.export', '导出报价单', '报价单', NULL);
INSERT INTO public.permissions VALUES (7, 'material.view', '查看物料', '原材料', NULL);
INSERT INTO public.permissions VALUES (8, 'material.create', '创建物料', '原材料', NULL);
INSERT INTO public.permissions VALUES (9, 'material.edit', '编辑物料', '原材料', NULL);
INSERT INTO public.permissions VALUES (10, 'material.delete', '删除物料', '原材料', NULL);
INSERT INTO public.permissions VALUES (11, 'material.import', '导入物料', '原材料', NULL);
INSERT INTO public.permissions VALUES (12, 'fee_type.view', '查看费用类型', '费用类型', NULL);
INSERT INTO public.permissions VALUES (13, 'fee_type.create', '创建费用类型', '费用类型', NULL);
INSERT INTO public.permissions VALUES (14, 'fee_type.edit', '编辑费用类型', '费用类型', NULL);
INSERT INTO public.permissions VALUES (15, 'fee_type.delete', '删除费用类型', '费用类型', NULL);
INSERT INTO public.permissions VALUES (16, 'fee_rate.view', '查看系数', '费用系数', NULL);
INSERT INTO public.permissions VALUES (17, 'fee_rate.edit', '编辑系数', '费用系数', NULL);
INSERT INTO public.permissions VALUES (18, 'exchange_rate.view', '查看汇率', '汇率', NULL);
INSERT INTO public.permissions VALUES (19, 'exchange_rate.edit', '编辑汇率', '汇率', NULL);
INSERT INTO public.permissions VALUES (20, 'module.view', '查看模块', '模块', NULL);
INSERT INTO public.permissions VALUES (21, 'module.create', '创建模块', '模块', NULL);
INSERT INTO public.permissions VALUES (22, 'module.edit', '编辑模块', '模块', NULL);
INSERT INTO public.permissions VALUES (23, 'module.delete', '删除模块', '模块', NULL);
INSERT INTO public.permissions VALUES (24, 'version.view', '查看版本', '版本', NULL);
INSERT INTO public.permissions VALUES (25, 'version.create', '创建版本', '版本', NULL);
INSERT INTO public.permissions VALUES (26, 'version.edit', '编辑版本', '版本', NULL);
INSERT INTO public.permissions VALUES (27, 'user.view', '查看用户', '用户', NULL);
INSERT INTO public.permissions VALUES (28, 'user.create', '创建用户', '用户', NULL);
INSERT INTO public.permissions VALUES (29, 'user.edit', '编辑用户', '用户', NULL);
INSERT INTO public.permissions VALUES (30, 'user.delete', '删除用户', '用户', NULL);
INSERT INTO public.permissions VALUES (31, 'user.reset_password', '重置密码', '用户', NULL);
INSERT INTO public.permissions VALUES (32, 'role.view', '查看角色', '角色', NULL);
INSERT INTO public.permissions VALUES (33, 'role.create', '创建角色', '角色', NULL);
INSERT INTO public.permissions VALUES (34, 'role.edit', '编辑角色', '角色', NULL);
INSERT INTO public.permissions VALUES (35, 'role.delete', '删除角色', '角色', NULL);
INSERT INTO public.permissions VALUES (36, 'log.view', '查看日志', '日志', NULL);
INSERT INTO public.permissions VALUES (37, 'system.view', '查看设置', '系统', NULL);
INSERT INTO public.permissions VALUES (38, 'system.edit', '编辑设置', '系统', NULL);
INSERT INTO public.permissions VALUES (39, 'module_assignment.view', '查看我的分配', '我的分配', NULL);
INSERT INTO public.permissions VALUES (40, 'module_assignment.edit', '编辑我的分配', '我的分配', NULL);
INSERT INTO public.permissions VALUES (41, 'participant_type_permission.view', '查看参与人权限', '参与人权限', NULL);
INSERT INTO public.permissions VALUES (42, 'participant_type_permission.edit', '编辑参与人权限', '参与人权限', NULL);
INSERT INTO public.permissions VALUES (43, 'travel_fee_config.view', '查看运输差旅配置', '运输差旅', NULL);
INSERT INTO public.permissions VALUES (44, 'travel_fee_config.edit', '编辑运输差旅配置', '运输差旅', NULL);
INSERT INTO public.permissions VALUES (45, 'ai.query', '使用 AI 助手', 'AI 助手', NULL);


ALTER TABLE public.permissions ENABLE TRIGGER ALL;

--
-- Data for Name: quotation_participants; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.quotation_participants DISABLE TRIGGER ALL;

INSERT INTO public.quotation_participants VALUES (1, 1, 1, 'agency', '2026-07-13 07:42:26.747453');


ALTER TABLE public.quotation_participants ENABLE TRIGGER ALL;

--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.roles DISABLE TRIGGER ALL;

INSERT INTO public.roles VALUES (1, '系统管理员', 'admin', '拥有所有权限', '2026-07-13 06:32:20.877018');
INSERT INTO public.roles VALUES (2, '经理', 'manager', '业务管理', '2026-07-13 06:32:20.879303');
INSERT INTO public.roles VALUES (3, '业务员', 'business', '报价单业务', '2026-07-13 06:32:20.880759');
INSERT INTO public.roles VALUES (4, '采购员', 'purchaser', '物料管理', '2026-07-13 06:32:20.882177');
INSERT INTO public.roles VALUES (5, '查看者', 'viewer', '只读', '2026-07-13 06:32:20.883385');


ALTER TABLE public.roles ENABLE TRIGGER ALL;

--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.role_permissions DISABLE TRIGGER ALL;

INSERT INTO public.role_permissions VALUES (3, 1);
INSERT INTO public.role_permissions VALUES (3, 2);
INSERT INTO public.role_permissions VALUES (3, 3);
INSERT INTO public.role_permissions VALUES (3, 4);
INSERT INTO public.role_permissions VALUES (3, 5);
INSERT INTO public.role_permissions VALUES (3, 6);
INSERT INTO public.role_permissions VALUES (3, 7);
INSERT INTO public.role_permissions VALUES (3, 12);
INSERT INTO public.role_permissions VALUES (3, 16);
INSERT INTO public.role_permissions VALUES (3, 18);
INSERT INTO public.role_permissions VALUES (3, 23);
INSERT INTO public.role_permissions VALUES (3, 20);
INSERT INTO public.role_permissions VALUES (3, 21);
INSERT INTO public.role_permissions VALUES (3, 22);
INSERT INTO public.role_permissions VALUES (3, 24);
INSERT INTO public.role_permissions VALUES (3, 25);
INSERT INTO public.role_permissions VALUES (3, 26);
INSERT INTO public.role_permissions VALUES (3, 39);
INSERT INTO public.role_permissions VALUES (3, 40);
INSERT INTO public.role_permissions VALUES (4, 8);
INSERT INTO public.role_permissions VALUES (4, 9);
INSERT INTO public.role_permissions VALUES (4, 10);
INSERT INTO public.role_permissions VALUES (4, 7);
INSERT INTO public.role_permissions VALUES (4, 11);
INSERT INTO public.role_permissions VALUES (4, 39);
INSERT INTO public.role_permissions VALUES (4, 12);
INSERT INTO public.role_permissions VALUES (4, 1);
INSERT INTO public.role_permissions VALUES (5, 1);
INSERT INTO public.role_permissions VALUES (5, 39);


ALTER TABLE public.role_permissions ENABLE TRIGGER ALL;

--
-- Data for Name: travel_categories; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_categories DISABLE TRIGGER ALL;

INSERT INTO public.travel_categories VALUES (8, '国内出差', 'domestic', '中国大陆境内出差', 1, true, '2026-07-13 07:36:07.437653', '2026-07-13 07:36:07.43766');
INSERT INTO public.travel_categories VALUES (9, '东南亚出差', 'southeast_asia', '泰国/越南/印尼/马来西亚等', 2, true, '2026-07-13 07:36:07.437663', '2026-07-13 07:36:07.437665');
INSERT INTO public.travel_categories VALUES (10, '欧洲出差', 'europe', '欧盟/英国/瑞士等', 3, true, '2026-07-13 07:36:07.437668', '2026-07-13 07:36:07.43767');
INSERT INTO public.travel_categories VALUES (11, '美洲出差', 'americas', '美国/加拿大/巴西等', 4, true, '2026-07-13 07:36:07.437672', '2026-07-13 07:36:07.437674');


ALTER TABLE public.travel_categories ENABLE TRIGGER ALL;

--
-- Data for Name: travel_day_rates; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_day_rates DISABLE TRIGGER ALL;

INSERT INTO public.travel_day_rates VALUES (1, 8, 600.00, 'CNY', '国内出差人天单价', true, '2026-07-13 07:36:07.459281', '2026-07-13 07:36:07.459285');
INSERT INTO public.travel_day_rates VALUES (2, 9, 900.00, 'CNY', '东南亚出差人天单价', true, '2026-07-13 07:36:07.459287', '2026-07-13 07:36:07.459288');
INSERT INTO public.travel_day_rates VALUES (3, 10, 1500.00, 'CNY', '欧洲出差人天单价', true, '2026-07-13 07:36:07.45929', '2026-07-13 07:36:07.459291');
INSERT INTO public.travel_day_rates VALUES (4, 11, 1800.00, 'CNY', '美洲出差人天单价', true, '2026-07-13 07:36:07.459293', '2026-07-13 07:36:07.459294');


ALTER TABLE public.travel_day_rates ENABLE TRIGGER ALL;

--
-- Data for Name: travel_modes; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_modes DISABLE TRIGGER ALL;

INSERT INTO public.travel_modes VALUES (5, '飞机', 'Airplane', 'plane', '民航客机', true, '2026-07-13 07:36:07.450089', '2026-07-13 07:36:07.450094');
INSERT INTO public.travel_modes VALUES (6, '高铁', 'High-speed Rail', 'train', '高铁/动车', true, '2026-07-13 07:36:07.450096', '2026-07-13 07:36:07.450097');
INSERT INTO public.travel_modes VALUES (7, '汽车', 'Car', 'car', '长途汽车/自驾', true, '2026-07-13 07:36:07.450099', '2026-07-13 07:36:07.4501');
INSERT INTO public.travel_modes VALUES (8, '轮船', 'Ship', 'ship', '客船/渡轮', true, '2026-07-13 07:36:07.450102', '2026-07-13 07:36:07.450103');


ALTER TABLE public.travel_modes ENABLE TRIGGER ALL;

--
-- Data for Name: travel_person_days; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_person_days DISABLE TRIGGER ALL;

INSERT INTO public.travel_person_days VALUES (1, 1, 8, 60.00, 600.00, '', '2026-07-13 07:45:46.432885', '2026-07-13 08:11:59.746995');


ALTER TABLE public.travel_person_days ENABLE TRIGGER ALL;

--
-- Data for Name: travel_person_trip_fees; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_person_trip_fees DISABLE TRIGGER ALL;

INSERT INTO public.travel_person_trip_fees VALUES (1, 8, 5, 1200.00, 0.00, 'CNY', '国内出差-飞机人次单价', true, '2026-07-13 07:36:07.467985', '2026-07-13 07:36:07.467989');
INSERT INTO public.travel_person_trip_fees VALUES (2, 8, 6, 600.00, 0.00, 'CNY', '国内出差-高铁人次单价', true, '2026-07-13 07:36:07.46799', '2026-07-13 07:36:07.467992');
INSERT INTO public.travel_person_trip_fees VALUES (3, 8, 7, 800.00, 0.00, 'CNY', '国内出差-汽车人次单价', true, '2026-07-13 07:36:07.467993', '2026-07-13 07:36:07.467994');
INSERT INTO public.travel_person_trip_fees VALUES (4, 9, 5, 3000.00, 500.00, 'CNY', '东南亚出差-飞机人次单价', true, '2026-07-13 07:36:07.467996', '2026-07-13 07:36:07.467997');
INSERT INTO public.travel_person_trip_fees VALUES (5, 10, 5, 8000.00, 1000.00, 'CNY', '欧洲出差-飞机人次单价', true, '2026-07-13 07:36:07.467998', '2026-07-13 07:36:07.467999');
INSERT INTO public.travel_person_trip_fees VALUES (6, 11, 5, 10000.00, 1500.00, 'CNY', '美洲出差-飞机人次单价', true, '2026-07-13 07:36:07.468', '2026-07-13 07:36:07.468002');


ALTER TABLE public.travel_person_trip_fees ENABLE TRIGGER ALL;

--
-- Data for Name: travel_person_trips; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.travel_person_trips DISABLE TRIGGER ALL;

INSERT INTO public.travel_person_trips VALUES (1, 1, 8, 5, 10, 1200.00, 0.00, '', '2026-07-13 07:45:57.511306', '2026-07-13 07:45:57.51131');


ALTER TABLE public.travel_person_trips ENABLE TRIGGER ALL;

--
-- Data for Name: version_snapshots; Type: TABLE DATA; Schema: public; Owner: -
--

ALTER TABLE public.version_snapshots DISABLE TRIGGER ALL;



ALTER TABLE public.version_snapshots ENABLE TRIGGER ALL;

--
-- Name: ai_knowledge_base_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ai_knowledge_base_id_seq', 1, false);


--
-- Name: ai_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ai_messages_id_seq', 4, true);


--
-- Name: archive_approvals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.archive_approvals_id_seq', 1, false);


--
-- Name: change_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.change_requests_id_seq', 1, false);


--
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.departments_id_seq', 1, false);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_id_seq', 1, false);


--
-- Name: exchange_rates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exchange_rates_id_seq', 166, true);


--
-- Name: fee_rates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.fee_rates_id_seq', 3, true);


--
-- Name: fee_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.fee_types_id_seq', 2, true);


--
-- Name: labor_hours_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labor_hours_id_seq', 3, true);


--
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.materials_id_seq', 492, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messages_id_seq', 1, true);


--
-- Name: module_materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.module_materials_id_seq', 140, true);


--
-- Name: module_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.module_participants_id_seq', 1, false);


--
-- Name: modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.modules_id_seq', 4, true);


--
-- Name: operation_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.operation_logs_id_seq', 201, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.organizations_id_seq', 1, false);


--
-- Name: other_fees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.other_fees_id_seq', 2, true);


--
-- Name: packing_entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.packing_entries_id_seq', 1, true);


--
-- Name: packing_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.packing_types_id_seq', 8, true);


--
-- Name: participant_type_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.participant_type_permissions_id_seq', 32, true);


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permissions_id_seq', 45, true);


--
-- Name: positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.positions_id_seq', 1, false);


--
-- Name: quotation_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.quotation_participants_id_seq', 1, true);


--
-- Name: quotations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.quotations_id_seq', 4, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_seq', 5, true);


--
-- Name: travel_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_categories_id_seq', 11, true);


--
-- Name: travel_day_rates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_day_rates_id_seq', 4, true);


--
-- Name: travel_modes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_modes_id_seq', 8, true);


--
-- Name: travel_person_days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_person_days_id_seq', 1, true);


--
-- Name: travel_person_trip_fees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_person_trip_fees_id_seq', 6, true);


--
-- Name: travel_person_trips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.travel_person_trips_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 285, true);


--
-- Name: version_snapshots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.version_snapshots_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict tb7q5TikvxwMTaFQ3CGnnYT0tSl8CcWpbKZK9wbzPUdUaD36khHz1glX8jWZY30

