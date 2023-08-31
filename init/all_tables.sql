-- --------------------------------------------------------
-- Host:                         7hg.h.filess.io
-- Server version:               PostgreSQL 14.4 on x86_64-pc-linux-musl, compiled by gcc (Alpine 11.2.1_git20220219) 11.2.1 20220219, 64-bit
-- Server OS:                    
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

BEGIN;
-- Dumping data for table public.dataset: -1 rows
/*!40000 ALTER TABLE "dataset" DISABLE KEYS */;
INSERT INTO "dataset" ("id", "updated_on", "created_at", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000005', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000001', '2023-08-15 16:53:05.257623', '2023-08-15 16:53:05.257623', '00000000-0000-0000-0000-000000000001'),
	('b210863a-2bee-4eaf-aad8-999b7a7cae06', '2023-08-20 22:31:18.830152', '2023-08-20 22:31:18.830152', '00000000-0000-0000-0000-000000000001'),
	('89aa8ffb-48b5-49c3-92c4-9b90fbcc736f', '2023-08-29 13:46:58.847208', '2023-08-29 13:46:58.847208', '00000000-0000-0000-0000-000000000001'),
	('e6c4cde9-f769-457e-a1ee-2a6c6dd76609', '2023-08-29 13:54:00.410672', '2023-08-29 13:54:00.410672', '00000000-0000-0000-0000-000000000001'),
	('8c510e24-2fb3-4abb-8712-5b4d6c429d15', '2023-08-29 13:54:28.093018', '2023-08-29 13:54:28.093018', '00000000-0000-0000-0000-000000000001'),
	('151e9c0b-20b3-4558-9eed-51830a708899', '2023-08-29 15:02:18.766003', '2023-08-29 15:02:18.766003', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset" ENABLE KEYS */;

-- Dumping data for table public.dataset_access: -1 rows
/*!40000 ALTER TABLE "dataset_access" DISABLE KEYS */;
INSERT INTO "dataset_access" ("id", "type", "description", "url", "url_last_checked", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'main', 'Clinical research studies ', 'https://aireadi.org', '1st August', NULL),
	('badac1ab-26fd-4f94-b2b4-b198365a198f', 'none', '', '', '', NULL),
	('6d2c020f-71b1-48d2-8532-89a563868fa4', 'none', '', '', '', NULL),
	('f8f3bf91-2eb9-49b8-a8f0-1c92def99bcf', 'none', '', '', '', NULL),
	('fdc10b6d-2dc6-41c1-b43e-202a24abc80a', 'none', '', '', '', '00000000-0000-0000-0000-000000000001'),
	('395d37d9-e3cf-4989-81f6-21dd2202d1ca', 'none', '', '', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_access" ENABLE KEYS */;

-- Dumping data for table public.dataset_alternate_identifier: 3 rows
/*!40000 ALTER TABLE "dataset_alternate_identifier" DISABLE KEYS */;
INSERT INTO "dataset_alternate_identifier" ("id", "identifier", "identifier_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'N/A', 'N/A', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '126543GF3', 'GRID', '00000000-0000-0000-0000-000000000001'),
	('77df307c-eb87-450b-b5d5-7d75bfb88cf7', 'N/A', 'N/A', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_alternate_identifier" ENABLE KEYS */;

-- Dumping data for table public.dataset_consent: -1 rows
/*!40000 ALTER TABLE "dataset_consent" DISABLE KEYS */;
INSERT INTO "dataset_consent" ("id", "type", "noncommercial", "geog_restrict", "research_type", "genetic_only", "no_methods", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'none', 'true', 'true', 'true', 'false', 'false', 'na', '00000000-0000-0000-0000-000000000001'),
	('f38a6bae-8724-411d-999a-f587cfdd32bf', 'none', 'true', 'true', 'true', 'false', 'false', 'na', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_consent" ENABLE KEYS */;

-- Dumping data for table public.dataset_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_contributor" DISABLE KEYS */;
INSERT INTO "dataset_contributor" ("id", "first_name", "last_name", "name_type", "name_identifier", "name_identifier_scheme", "name_identifier_scheme_uri", "creator", "contributor_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh', 'patel', 'type_name', 'identifier', 'scheme', 'scheme uri', 'true', 'type', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_contributor" ENABLE KEYS */;

-- Dumping data for table public.dataset_contributor_affiliation: -1 rows
/*!40000 ALTER TABLE "dataset_contributor_affiliation" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_contributor_affiliation" ENABLE KEYS */;

-- Dumping data for table public.dataset_date: -1 rows
/*!40000 ALTER TABLE "dataset_date" DISABLE KEYS */;
INSERT INTO "dataset_date" ("id", "date", "date_type", "data_information", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000004', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000005'),
	('0b1775e5-d110-482f-a1c4-2aa3947b8db8', '', 'na', 'none', '00000000-0000-0000-0000-000000000001'),
	('dc090dbd-6fa3-4b61-829e-2f139bdbd116', '', 'na', 'none', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_date" ENABLE KEYS */;

-- Dumping data for table public.dataset_description: -1 rows
/*!40000 ALTER TABLE "dataset_description" DISABLE KEYS */;
INSERT INTO "dataset_description" ("id", "description", "description_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000004'),
	('78f2b774-2f5a-4096-b82e-9923ca04395b', '', '', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', '', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_description" ENABLE KEYS */;

-- Dumping data for table public.dataset_de_ident_level: -1 rows
/*!40000 ALTER TABLE "dataset_de_ident_level" DISABLE KEYS */;
INSERT INTO "dataset_de_ident_level" ("id", "type", "direct", "hipaa", "dates", "nonarr", "k_anon", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '', 'false', 'true', 'false', 'true', 'false', '', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'NA', 'false', 'true', 'false', 'true', 'false', 'none', '00000000-0000-0000-0000-000000000002'),
	('1bc4eeb0-dcdf-41af-b8e9-d05923ba45fa', '', 'true', 'true', 'true', 'true', 'true', '', '00000000-0000-0000-0000-000000000001'),
	('a3f40ca7-4f34-43b5-9e44-fc20e8f50eef', '', 'true', 'true', 'true', 'true', 'true', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_de_ident_level" ENABLE KEYS */;

-- Dumping data for table public.dataset_funder: -1 rows
/*!40000 ALTER TABLE "dataset_funder" DISABLE KEYS */;
INSERT INTO "dataset_funder" ("id", "name", "identifier", "identifier_type", "identifier_scheme_uri", "award_number", "award_uri", "award_title", "dataset_id") VALUES
	('8ef6d41f-2f59-492c-9f28-8c1c10bcc4e8', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_funder" ENABLE KEYS */;

-- Dumping data for table public.dataset_managing_organization: -1 rows
/*!40000 ALTER TABLE "dataset_managing_organization" DISABLE KEYS */;
INSERT INTO "dataset_managing_organization" ("id", "name", "ror_id", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'UCSD', '354grhji5', '00000000-0000-0000-0000-000000000001'),
	('c5d5a32a-c072-4594-989a-4b55acc5d11b', 'UCD', '354grhji5', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_managing_organization" ENABLE KEYS */;

-- Dumping data for table public.dataset_other: -1 rows
/*!40000 ALTER TABLE "dataset_other" DISABLE KEYS */;
INSERT INTO "dataset_other" ("id", "language", "managing_organization_name", "managing_organization_ror_id", "size", "standards_followed", "acknowledgement", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', '00000000-0000-0000-0000-000000000002'),
	('2fca4640-6f0e-406c-8c7a-e93a0740b9c6', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org', 'NA', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org/other', 'NA', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_other" ENABLE KEYS */;

-- Dumping data for table public.dataset_readme: -1 rows
/*!40000 ALTER TABLE "dataset_readme" DISABLE KEYS */;
INSERT INTO "dataset_readme" ("id", "content", "dataset_id") VALUES
	('6473a133-af27-4b6c-a8a0-3fc850d3ab91', 'none', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_readme" ENABLE KEYS */;

-- Dumping data for table public.dataset_record_keys: -1 rows
/*!40000 ALTER TABLE "dataset_record_keys" DISABLE KEYS */;
INSERT INTO "dataset_record_keys" ("id", "key_type", "key_details", "dataset_id") VALUES
	('46867b5a-9eb1-4f0e-98ba-5b453c2c9ff2', 'test', 'test', '00000000-0000-0000-0000-000000000001'),
	('bb834d3c-b59a-4968-b31c-51bd22c11c4f', 'test', 'test', '00000000-0000-0000-0000-000000000001'),
	('82fbb094-74c5-4dd1-9248-9e219c0b70f5', 'test1', 'test1', '00000000-0000-0000-0000-000000000001'),
	('59c1b98d-876f-49f6-aeb0-f32d4fde6c3f', 'test1', 'test1', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_record_keys" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item: -1 rows
/*!40000 ALTER TABLE "dataset_related_item" DISABLE KEYS */;
INSERT INTO "dataset_related_item" ("id", "type", "relation_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'main', 'main', '00000000-0000-0000-0000-000000000002'),
	('f55af3f0-16f9-4049-8beb-f6673d32bef0', '', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_related_item" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_contributor" DISABLE KEYS */;
INSERT INTO "dataset_related_item_contributor" ("id", "name", "name_type", "creator", "contributor_type", "dataset_related_item_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'AIREADI', 'string', 'true', 'owner', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_related_item_contributor" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item_identifier: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_identifier" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_identifier" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item_other: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_other" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_other" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item_title: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_title" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_title" ENABLE KEYS */;

-- Dumping data for table public.dataset_rights: -1 rows
/*!40000 ALTER TABLE "dataset_rights" DISABLE KEYS */;
INSERT INTO "dataset_rights" ("id", "rights", "uri", "identifier", "identifier_scheme", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'NA', 'https://orcid.org', 'none', 'ORCID', '00000000-0000-0000-0000-000000000001'),
	('e9fd3c26-843b-465a-b950-8d23005df384', 'NA', 'https://orcid.org', 'none', 'ORCID', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_rights" ENABLE KEYS */;

-- Dumping data for table public.dataset_subject: -1 rows
/*!40000 ALTER TABLE "dataset_subject" DISABLE KEYS */;
INSERT INTO "dataset_subject" ("id", "subject", "scheme", "scheme_uri", "value_uri", "classification_code", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '', '', '', '', 'NLM''s Medical Subject', '00000000-0000-0000-0000-000000000001'),
	('5ce2ba12-e536-4858-8913-7de2225cecc3', '', '', '', '', 'NLM''s Medical Subject', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_subject" ENABLE KEYS */;

-- Dumping data for table public.dataset_title: -1 rows
/*!40000 ALTER TABLE "dataset_title" DISABLE KEYS */;
INSERT INTO "dataset_title" ("id", "title", "type", "dataset_id") VALUES
	('02937b58-268d-486d-ad63-55a79b39ea9c', 'title', 'na', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_title" ENABLE KEYS */;

-- Dumping data for table public.invited_study_contributor: -1 rows
/*!40000 ALTER TABLE "invited_study_contributor" DISABLE KEYS */;
INSERT INTO "invited_study_contributor" ("email_address", "permission", "invited_on", "study_id") VALUES
	('aydan.gasimova@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000001'),
	('bhavesh.patel@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000003'),
	('sanjay.soundarajan@@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "invited_study_contributor" ENABLE KEYS */;

-- Dumping data for table public.participant: -1 rows
/*!40000 ALTER TABLE "participant" DISABLE KEYS */;
INSERT INTO "participant" ("id", "first_name", "last_name", "address", "age", "created_at", "updated_on", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'bhavesh', 'patel', '3904 university ave', '20', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'sanjay', 'soundarajan', '123 gold coast', '27', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'billy', 'sanders', '123 gold coast', '32', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000004'),
	('921ba857-dd08-4149-8f5c-245c6c93ef84', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:42:23.627034', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('458d2c15-6ed8-4f70-a47d-70b42f2f1b86', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:42:36.656094', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('35750167-40c5-4f4a-9d8e-ebe89c2efcfc', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:42:52.555088', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('43c54d45-2f63-41da-8d18-6d3ef06ba476', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:42:59.614647', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('b444520d-0eac-4065-a86d-004481f68d8a', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:45:49.495595', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('88c7592a-4382-4d6b-a197-e880e49db3c0', 'aydan1', 'gasimova', '1221d kibler drive', '20', '2023-08-29 13:46:17.682171', '2023-08-29 13:46:17.682171', '00000000-0000-0000-0000-000000000001'),
	('ba73ed99-6ec2-46e0-acdb-4a00c31dd572', 'aydan', 'gasimova', '1221d kibler drive', '20', '2023-08-29 15:08:03.758771', '2023-08-29 15:08:03.758771', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'aydan', 'gasimova1', '1221d kibler drive', '20', '2023-08-13 16:33:53', '2023-08-29 15:09:04.323914', '00000000-0000-0000-0000-000000000001'),
	('006306a7-0ddb-4163-952d-2939712e190d', 'aydan', 'gasimova1', '1221d kibler drive', '20', '2023-08-29 15:15:35.891076', '2023-08-29 15:15:35.891076', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "participant" ENABLE KEYS */;

-- Dumping data for table public.study: -1 rows
/*!40000 ALTER TABLE "study" DISABLE KEYS */;
INSERT INTO "study" ("id", "title", "image", "created_at", "updated_on") VALUES
	('00000000-0000-0000-0000-000000000001', 'study 1', 'https://loremflickr.com/640/480?lock=342651989655552', '2023-08-13 12:33:10', '2023-08-13 12:33:11'),
	('00000000-0000-0000-0000-000000000006', 'study 6', 'https://loremflickr.com/640/480?lock=342651989655552', '2019-08-03 12:33:10', '2022-08-03 12:33:11'),
	('00000000-0000-0000-0000-000000000007', 'study 7', 'https://loremflickr.com/640/480?lock=342651989655552', '2020-08-03 12:33:10', '2023-03-03 12:33:11'),
	('00000000-0000-0000-0000-000000000008', 'study 8', 'https://loremflickr.com/640/480?lock=342651989655552', '2023-08-03 12:33:10', '2023-01-03 12:33:11'),
	('00000000-0000-0000-0000-000000000003', 'study 3', 'https://loremflickr.com/640/480?lock=342651989655552', '2016-08-03 12:33:10', '2023-02-03 12:33:11'),
	('00000000-0000-0000-0000-000000000002', 'study 2', 'https://loremflickr.com/640/480?lock=342651989655552', '2022-08-03 12:33:10', '2023-07-03 12:33:11'),
	('00000000-0000-0000-0000-000000000004', 'study 4', 'https://loremflickr.com/640/480?lock=342651989655552', '2020-08-03 12:33:10', '2021-09-03 12:33:11'),
	('00000000-0000-0000-0000-000000000005', 'study 5', 'https://loremflickr.com/640/480?lock=342651989655552', '2021-08-03 12:33:10', '2023-05-03 12:33:11');
/*!40000 ALTER TABLE "study" ENABLE KEYS */;

-- Dumping data for table public.study_arm: -1 rows
/*!40000 ALTER TABLE "study_arm" DISABLE KEYS */;
INSERT INTO "study_arm" ("id", "label", "type", "description", "intervention_list", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'label', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'Active Comparator', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000003'),
	('75edc7d3-ab7c-404d-a6dd-b55f7fe6446d', 'label', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001'),
	('2b26a772-b4af-4e61-9e76-6642746b78ee', '', '', '', '{""}', '00000000-0000-0000-0000-000000000001'),
	('a82a5e49-a735-4ba3-ab2e-ba64e7fb464c', 'label1', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'label', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000002'),
	('ba03826c-b9db-4517-aeaa-031793de4a25', 'label1', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001'),
	('a11728f0-fadb-4bd0-be09-511d5fb39649', 'label1', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001'),
	('311fed5e-fd7a-4a02-8465-3b55a05cab04', 'label1', 'type', 'description', '{list}', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_arm" ENABLE KEYS */;

-- Dumping data for table public.study_available_ipd: -1 rows
/*!40000 ALTER TABLE "study_available_ipd" DISABLE KEYS */;
INSERT INTO "study_available_ipd" ("id", "identifier", "type", "url", "comment", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000003');
/*!40000 ALTER TABLE "study_available_ipd" ENABLE KEYS */;

-- Dumping data for table public.study_contact: -1 rows
/*!40000 ALTER TABLE "study_contact" DISABLE KEYS */;
INSERT INTO "study_contact" ("id", "first_name", "last_name", "affiliation", "role", "phone", "phone_ext", "email_address", "central_contact", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'holly', 'sienna', 'calmi2', 'editor', '4056074345', 'ext', 'holly.sienna@gmail.com', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'billy', 'brown', 'calmi2', 'editor', '4056074345', 'ext', 'billy.sanders@gmail.com', 'true', '00000000-0000-0000-0000-000000000001'),
	('81e71d41-2c93-47cb-9fac-00d94ab1c1a2', 'billy', 'brown', 'calmi2', 'editor', '4056074345', 'ext', 'billy.sanders@gmail.com', 'true', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_contact" ENABLE KEYS */;

-- Dumping data for table public.study_contributor: -1 rows
/*!40000 ALTER TABLE "study_contributor" DISABLE KEYS */;
INSERT INTO "study_contributor" ("permission", "user_id", "study_id") VALUES
	('editor', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001'),
	('owner', '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002'),
	('owner', '00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000004'),
	('editor', '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000006');
/*!40000 ALTER TABLE "study_contributor" ENABLE KEYS */;

-- Dumping data for table public.study_description: -1 rows
/*!40000 ALTER TABLE "study_description" DISABLE KEYS */;
INSERT INTO "study_description" ("id", "brief_summary", "detailed_description", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000003'),
	('f51a772e-373a-452a-8106-822840a76339', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_description" ENABLE KEYS */;

-- Dumping data for table public.study_design: -1 rows
/*!40000 ALTER TABLE "study_design" DISABLE KEYS */;
INSERT INTO "study_design" ("id", "design_allocation", "study_type", "design_interventional_model", "design_intervention_model_description", "design_primary_purpose", "design_masking", "design_masking_description", "design_who_masked_list", "phase_list", "enrollment_count", "enrollment_type", "number_arms", "design_observational_model_list", "design_time_perspective_list", "bio_spec_retention", "bio_spec_description", "target_duration", "number_groups_cohorts", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'Randomized', 'type', 'treatment of cancer', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '1 years', 10, '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'Randomized', 'type', 'treatment', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{casecontrol}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3 months', 10, '00000000-0000-0000-0000-000000000002'),
	('2b1312ef-338b-454a-9e17-5db84e17d97c', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{[,'',P,a,r,t,i,c,i,p,a,n,t,'',]}', '{Trials}', 1, 'enrollmentInfo', 2, '{[,'',C,a,s,e,C,o,n,t,r,o,l,'',]}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001'),
	('ca5500a4-cbce-454a-a767-653461d59397', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{CaseControl}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_design" ENABLE KEYS */;

-- Dumping data for table public.study_eligibility: 6 rows
/*!40000 ALTER TABLE "study_eligibility" DISABLE KEYS */;
INSERT INTO "study_eligibility" ("id", "gender", "gender_based", "gender_description", "healthy_volunteers", "inclusion_criteria", "exclusion_criteria", "study_population", "sampling_method", "study_id", "minimum_age_value", "minimum_age_unit", "maximum_age_value", "maximum_age_unit") VALUES
	('00000000-0000-0000-0000-000000000004', 'female', 'Correct', 'none', 'true', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 30, 'UCSD', 54, 'UW'),
	('dfac0d9e-a104-4f4b-ac1d-05f3699c72f3', 'female', 'Not given', 'none', 'true', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 23, 'UCSD', 32, 'UW'),
	('00000000-0000-0000-0000-000000000002', 'female', 'True', 'none', 'false', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 45, 'UCLA', 43, 'UCLA'),
	('00000000-0000-0000-0000-000000000001', 'female', 'True', 'none', 'true', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 24, 'UCSD', 34, 'UCLA'),
	('00000000-0000-0000-0000-000000000003', 'female', 'True', 'none', 'false', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 56, 'UCLA', 37, 'UCSD'),
	('01ac64ef-cfca-47bc-8f30-67525017461f', 'female', 'True', 'none', 'true', '{concluded}', '{none}', 'primary care clinic', 'Probability Sample', '00000000-0000-0000-0000-000000000001', 34, 'UW', 29, 'UW');
/*!40000 ALTER TABLE "study_eligibility" ENABLE KEYS */;

-- Dumping data for table public.study_identification: -1 rows
/*!40000 ALTER TABLE "study_identification" DISABLE KEYS */;
INSERT INTO "study_identification" ("id", "identifier", "identifier_type", "identifier_domain", "identifier_link", "secondary", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001'),
	('cfc1b66c-882a-4eee-a6d7-01a7cb018ac2', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_identification" ENABLE KEYS */;

-- Dumping data for table public.study_intervention: -1 rows
/*!40000 ALTER TABLE "study_intervention" DISABLE KEYS */;
INSERT INTO "study_intervention" ("id", "type", "name", "description", "arm_group_label_list", "other_name_list", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'Drug', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'Procedure/Surgery', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'Radiation', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000004'),
	('70eecc49-2c32-47a4-a176-2abb57334fab', 'Device', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000001'),
	('ede01416-9693-4095-bdae-a2c144a9ec82', 'Device', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000001'),
	('f6c68d25-8a1c-47ec-9b8d-4db36cf3fecd', 'Device', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'Device', 'intervention name updatee', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000001'),
	('65ef7ce9-4992-47a1-8a86-355792ca6fbc', 'Device', 'intervention name', 'Other current and former name', '{"Arm Group Label"}', '{"Arm other list"}', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_intervention" ENABLE KEYS */;

-- Dumping data for table public.study_ipdsharing: -1 rows
/*!40000 ALTER TABLE "study_ipdsharing" DISABLE KEYS */;
INSERT INTO "study_ipdsharing" ("id", "ipd_sharing", "ipd_sharing_description", "ipd_sharing_info_type_list", "ipd_sharing_time_frame", "ipd_sharing_access_criteria", "ipd_sharing_url", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000003'),
	('ebfe1211-763e-4b10-8e15-7ccb29cb21f5', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_ipdsharing" ENABLE KEYS */;

-- Dumping data for table public.study_link: -1 rows
/*!40000 ALTER TABLE "study_link" DISABLE KEYS */;
INSERT INTO "study_link" ("id", "url", "title", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000003'),
	('e354922c-9ab3-4b38-ba79-c4d4640737d2', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000001'),
	('040d305e-504d-433b-b5c2-7d56c24d440a', 'https://schema.aireadi.org/', 'schema', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_link" ENABLE KEYS */;

-- Dumping data for table public.study_location: -1 rows
/*!40000 ALTER TABLE "study_location" DISABLE KEYS */;
INSERT INTO "study_location" ("id", "facility", "status", "city", "state", "zip", "country", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'facility', 'active', 'San diego', 'CA', '92121', 'sAN dIEGO', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'facility', 'active', 'San diego', 'CA', '92121', 'sAN dIEGO', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'facility', 'active', 'San diego', 'CA', '92121', 'sAN dIEGO', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'facility', 'active', 'San diego', 'CA', '92121', 'sAN dIEGO', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000005', 'facility', 'active', 'San diego', 'CA', '92121', 'sAN dIEGO', '00000000-0000-0000-0000-000000000004'),
	('cda2dc03-95cf-494a-87ea-aac49ac07f0b', 'facility', 'active', 'San diego', 'CA', '92121', 'San diego', '00000000-0000-0000-0000-000000000001'),
	('72d6a140-e57b-4ba4-a57d-391cdc871c21', 'facility', 'active', 'San diego', 'CA', '92121', 'San diego', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_location" ENABLE KEYS */;

-- Dumping data for table public.study_other: -1 rows
/*!40000 ALTER TABLE "study_other" DISABLE KEYS */;
INSERT INTO "study_other" ("id", "oversight_has_dmc", "conditions", "keywords", "size", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000003', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000001'),
	('cd440fa9-988b-4d51-8b66-8c2e42c630b3', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_other" ENABLE KEYS */;

-- Dumping data for table public.study_overall_official: -1 rows
/*!40000 ALTER TABLE "study_overall_official" DISABLE KEYS */;
INSERT INTO "study_overall_official" ("id", "first_name", "last_name", "affiliation", "role", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000003'),
	('a0806089-6602-48b0-b870-1d5e91b956a5', 'firstname', 'lastname', 'affiliation', 'Study Chair', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_overall_official" ENABLE KEYS */;

-- Dumping data for table public.study_reference: 6 rows
/*!40000 ALTER TABLE "study_reference" DISABLE KEYS */;
INSERT INTO "study_reference" ("id", "identifier", "title", "type", "citation", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'The PubMed Unique Identifier ', ' bibliographic reference', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'The PubMed Unique Identifier ', ' bibliographic reference', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('2996e115-8c44-4914-a470-2764ff280316', 'The PubMed Unique Identifier ', ' bibliographic reference', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'The PubMed Unique Identifier ', ' bibliographic reference', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'The PubMed Unique Identifier ', ' bibliographic reference', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000005', 'The PubMed Unique Identifier ', ' bibliographic reference', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "study_reference" ENABLE KEYS */;

-- Dumping data for table public.study_sponsors_collaborators: -1 rows
/*!40000 ALTER TABLE "study_sponsors_collaborators" DISABLE KEYS */;
INSERT INTO "study_sponsors_collaborators" ("id", "responsible_party_type", "responsible_party_investigator_first_name", "responsible_party_investigator_last_name", "responsible_party_investigator_title", "responsible_party_investigator_affiliation", "lead_sponsor_first_name", "lead_sponsor_last_name", "collaborator_name", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000004', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000005', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('687dea6a-4dbf-45dc-867e-de7b303d4b0c', 'San Diego', 'firstname', 'lastname', 'title', 'affiliation', 'name', 'lastname', '{"clinical study"}', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_sponsors_collaborators" ENABLE KEYS */;

-- Dumping data for table public.study_status: -1 rows
/*!40000 ALTER TABLE "study_status" DISABLE KEYS */;
INSERT INTO "study_status" ("id", "overall_status", "why_stopped", "start_date", "start_date_type", "completion_date", "completion_date_type", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Suspended', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'anticipated', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2021-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2020-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000004', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2020-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('8100ce8e-406d-4483-bc47-634e97c34713', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Suspended', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'anticipated', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_status" ENABLE KEYS */;

-- Dumping data for table public.user: -1 rows
/*!40000 ALTER TABLE "user" DISABLE KEYS */;
INSERT INTO "user" ("id", "email_address", "username", "first_name", "last_name", "orcid", "hash", "created_at", "institution") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh.patel@gmail.com', 'bhavesh', 'Bhavesh', 'Patel', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000002', 'sanjay.soundarajan@gmail.com', 'sanjay', 'sanjay', 'soundarajan', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000003', 'billy.sanders@gmail.com', 'billy', 'billy', 'sanders', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000004', 'james.lilly@gmail.com', 'james', 'james', 'lilly', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2');
/*!40000 ALTER TABLE "user" ENABLE KEYS */;

-- Dumping data for table public.version: -1 rows
/*!40000 ALTER TABLE "version" DISABLE KEYS */;
-- Dumping data for table public.version_participants: -1 rows
/*!40000 ALTER TABLE "version_participants" DISABLE KEYS */;
INSERT INTO "version_participants" ("dataset_version_id", "participant_id") VALUES
	('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "version_participants" ENABLE KEYS */;

COMMIT;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
