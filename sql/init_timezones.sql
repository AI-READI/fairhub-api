BEGIN;
-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               PostgreSQL 15.4 (Debian 15.4-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
-- Server OS:
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table public.study
CREATE TABLE IF NOT EXISTS "study" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"image" VARCHAR NOT NULL,
	"created_at" BIGINT NOT NULL,
	"updated_on" BIGINT NOT NULL,
	PRIMARY KEY ("id")
);

-- Dumping data for table public.study: 11 rows
/*!40000 ALTER TABLE "study" DISABLE KEYS */;
INSERT INTO "study" ("id", "title", "image", "created_at", "updated_on") VALUES
	('ec0064ca-4f34-48a8-9dcc-1377c7ca0a59', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1693953573, 1693953573),
	('995d703e-a6d0-4dc2-95e7-3ce868eb9fb7', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1693953609, 1693953609),
	('f154f7c2-58a9-4b2e-808c-3d9a71dc99d2', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1693953736, 1693953736),
	('22910241-051c-4f42-9a58-890704df32ad', 'Small Cotton Shoes', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=8', 1693805470, 1693805470),
	('af2f9f5e-24eb-4b54-8fe1-ec76391b9af6', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694017629, 1694017629),
	('cb24e1c9-b4b2-451a-89b7-e73556d50ca2', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694023951, 1694023951),
	('e5a2a1d2-850f-465a-8fc1-6a1aec6d9e5a', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1693953512, 1694028729),
	('39a913b7-daad-4c86-ba07-9f6400c73a28', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694031647, 1694031647),
	('61ac1bdb-1809-4d20-8e29-22d3f2d85252', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694032751, 1694032751),
	('626f2a7e-fa8f-459e-9076-a3b2082a00d2', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694032781, 1694032781),
	('ee3012e5-3c51-4d21-b16c-5ace1c80cf72', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1694035574, 1694035574),
	('00000000-0000-0000-0000-000000000008', 'study 8', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=8', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000007', 'study 7', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=7', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000006', 'study 6', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=6', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000005', 'study 5', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=5', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000001', 'study 1', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=1', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000002', 'study 1', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=1', 1693805470, 1693805470),
	('d925991e-af73-4fa2-ab2a-7040140a57df', 'study 1', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=1', 1693805470, 1693805470),
	('b32ca9d9-9656-49b5-9707-bd157dff0ffb', 'study 1', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=1', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000003', 'study 3', 'https://api.dicebear.com/7.x/fun-emoji/svg?seed=3', 1693805470, 1693805470),
	('95711a87-16ee-4ebd-bc37-1b79b104bff3', 'Recycled Cotton Shirt', 'https://www.svgrepo.com/show/213127/image-warning.svg', 1693805470, 1693805470);
/*!40000 ALTER TABLE "study" ENABLE KEYS */;


-- Dumping structure for table public.dataset
CREATE TABLE IF NOT EXISTS "dataset" (
	"id" CHAR(36) NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"updated_on" BIGINT NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset: -1 rows
/*!40000 ALTER TABLE "dataset" DISABLE KEYS */;
INSERT INTO "dataset" ("id", "study_id", "updated_on", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 1693957896, 1693957896),
	('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 1693957896, 1693957896),
	('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001', 1693957896, 1693957896),
	('00000000-0000-0000-0000-000000000005', '00000000-0000-0000-0000-000000000002', 1693957896, 1693957896),
	('00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000002', 1693957896, 1693957896),
	('00000000-0000-0000-0000-000000000006', '00000000-0000-0000-0000-000000000003', 1693957896, 1693957896),
	('c8b5eb7a-f939-44a3-86c1-7746e73329c4', '00000000-0000-0000-0000-000000000001', 1694031716, 1694031716);
/*!40000 ALTER TABLE "dataset" ENABLE KEYS */;

-- Dumping structure for table public.dataset_access
CREATE TABLE IF NOT EXISTS "dataset_access" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"url" VARCHAR NOT NULL,
	"url_last_checked" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_access_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_access: -1 rows
/*!40000 ALTER TABLE "dataset_access" DISABLE KEYS */;
INSERT INTO "dataset_access" ("id", "type", "description", "url", "url_last_checked", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'PublicOnScreenAccess', '', '', '', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'PublicOnScreenAccess', '', '', '', '00000000-0000-0000-0000-000000000002');
/*!40000 ALTER TABLE "dataset_access" ENABLE KEYS */;

-- Dumping structure for table public.dataset_alternate_identifier
CREATE TABLE IF NOT EXISTS "dataset_alternate_identifier" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_alternate_identifier_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_alternate_identifier: -1 rows
/*!40000 ALTER TABLE "dataset_alternate_identifier" DISABLE KEYS */;
INSERT INTO "dataset_alternate_identifier" ("id", "identifier", "identifier_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'N/A', 'N/A', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '126543GF3', 'GRID', '00000000-0000-0000-0000-000000000001'),
	('77df307c-eb87-450b-b5d5-7d75bfb88cf7', 'N/A', 'N/A', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_alternate_identifier" ENABLE KEYS */;

-- Dumping structure for table public.dataset_consent
CREATE TABLE IF NOT EXISTS "dataset_consent" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"noncommercial" BOOLEAN NOT NULL,
	"geog_restrict" BOOLEAN NOT NULL,
	"research_type" BOOLEAN NOT NULL,
	"genetic_only" BOOLEAN NOT NULL,
	"no_methods" BOOLEAN NOT NULL,
	"details" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_consent_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_consent: -1 rows
/*!40000 ALTER TABLE "dataset_consent" DISABLE KEYS */;
INSERT INTO "dataset_consent" ("id", "type", "noncommercial", "geog_restrict", "research_type", "genetic_only", "no_methods", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'none', 'true', 'true', 'true', 'false', 'false', 'na', '00000000-0000-0000-0000-000000000001'),
	('f38a6bae-8724-411d-999a-f587cfdd32bf', 'none', 'true', 'true', 'true', 'false', 'false', 'na', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_consent" ENABLE KEYS */;

-- Dumping structure for table public.dataset_contributor
CREATE TABLE IF NOT EXISTS "dataset_contributor" (
	"id" CHAR(36) NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"name_type" VARCHAR NOT NULL,
	"name_identifier" VARCHAR NOT NULL,
	"name_identifier_scheme" VARCHAR NOT NULL,
	"name_identifier_scheme_uri" VARCHAR NOT NULL,
	"creator" BOOLEAN NOT NULL,
	"contributor_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_contributor_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_contributor" DISABLE KEYS */;
INSERT INTO "dataset_contributor" ("id", "first_name", "last_name", "name_type", "name_identifier", "name_identifier_scheme", "name_identifier_scheme_uri", "creator", "contributor_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh', 'patel', 'type_name', 'identifier', 'scheme', 'scheme uri', 'true', 'type', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_contributor" ENABLE KEYS */;

-- Dumping structure for table public.dataset_contributor_affiliation
CREATE TABLE IF NOT EXISTS "dataset_contributor_affiliation" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_scheme" VARCHAR NOT NULL,
	"identifier_scheme_uri" VARCHAR NOT NULL,
	"dataset_contributor_id" VARCHAR NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_contributor_affiliation_dataset_contributor_id_fkey" FOREIGN KEY ("dataset_contributor_id") REFERENCES "dataset_contributor" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_contributor_affiliation: -1 rows
/*!40000 ALTER TABLE "dataset_contributor_affiliation" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_contributor_affiliation" ENABLE KEYS */;

-- Dumping structure for table public.dataset_date
CREATE TABLE IF NOT EXISTS "dataset_date" (
	"id" CHAR(36) NOT NULL,
	"date" VARCHAR NOT NULL,
	"date_type" VARCHAR NOT NULL,
	"data_information" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_date_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.dataset_description
CREATE TABLE IF NOT EXISTS "dataset_description" (
	"id" CHAR(36) NOT NULL,
	"description" VARCHAR NOT NULL,
	"description_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_description_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_description: -1 rows
/*!40000 ALTER TABLE "dataset_description" DISABLE KEYS */;
INSERT INTO "dataset_description" ("id", "description", "description_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000004'),
	('78f2b774-2f5a-4096-b82e-9923ca04395b', '', '', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', '', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_description" ENABLE KEYS */;

-- Dumping structure for table public.dataset_de_ident_level
CREATE TABLE IF NOT EXISTS "dataset_de_ident_level" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"direct" BOOLEAN NOT NULL,
	"hipaa" BOOLEAN NOT NULL,
	"dates" BOOLEAN NOT NULL,
	"nonarr" BOOLEAN NOT NULL,
	"k_anon" BOOLEAN NOT NULL,
	"details" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_de_ident_level_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_de_ident_level: -1 rows
/*!40000 ALTER TABLE "dataset_de_ident_level" DISABLE KEYS */;
INSERT INTO "dataset_de_ident_level" ("id", "type", "direct", "hipaa", "dates", "nonarr", "k_anon", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '', 'false', 'true', 'false', 'true', 'false', '', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'NA', 'false', 'true', 'false', 'true', 'false', 'none', '00000000-0000-0000-0000-000000000002'),
	('1bc4eeb0-dcdf-41af-b8e9-d05923ba45fa', '', 'true', 'true', 'true', 'true', 'true', '', '00000000-0000-0000-0000-000000000001'),
	('a3f40ca7-4f34-43b5-9e44-fc20e8f50eef', '', 'true', 'true', 'true', 'true', 'true', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_de_ident_level" ENABLE KEYS */;

-- Dumping structure for table public.dataset_funder
CREATE TABLE IF NOT EXISTS "dataset_funder" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_type" VARCHAR NOT NULL,
	"identifier_scheme_uri" VARCHAR NOT NULL,
	"award_number" VARCHAR NOT NULL,
	"award_uri" VARCHAR NOT NULL,
	"award_title" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_funder_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_funder: -1 rows
/*!40000 ALTER TABLE "dataset_funder" DISABLE KEYS */;
INSERT INTO "dataset_funder" ("id", "name", "identifier", "identifier_type", "identifier_scheme_uri", "award_number", "award_uri", "award_title", "dataset_id") VALUES
	('8ef6d41f-2f59-492c-9f28-8c1c10bcc4e8', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_funder" ENABLE KEYS */;

-- Dumping structure for table public.dataset_managing_organization
CREATE TABLE IF NOT EXISTS "dataset_managing_organization" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"ror_id" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_managing_organization_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_managing_organization: -1 rows
/*!40000 ALTER TABLE "dataset_managing_organization" DISABLE KEYS */;
INSERT INTO "dataset_managing_organization" ("id", "name", "ror_id", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'UCSD', '354grhji5', '00000000-0000-0000-0000-000000000001'),
	('c5d5a32a-c072-4594-989a-4b55acc5d11b', 'UCD', '354grhji5', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_managing_organization" ENABLE KEYS */;

-- Dumping structure for table public.dataset_other
CREATE TABLE IF NOT EXISTS "dataset_other" (
	"id" CHAR(36) NOT NULL,
	"language" VARCHAR NOT NULL,
	"managing_organization_name" VARCHAR NOT NULL,
	"managing_organization_ror_id" VARCHAR NOT NULL,
	"size" VARCHAR[] NOT NULL,
	"standards_followed" VARCHAR NOT NULL,
	"acknowledgement" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_other_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_other: -1 rows
/*!40000 ALTER TABLE "dataset_other" DISABLE KEYS */;
INSERT INTO "dataset_other" ("id", "language", "managing_organization_name", "managing_organization_ror_id", "size", "standards_followed", "acknowledgement", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', '00000000-0000-0000-0000-000000000002'),
	('2fca4640-6f0e-406c-8c7a-e93a0740b9c6', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org', 'NA', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org/other', 'NA', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_other" ENABLE KEYS */;

-- Dumping structure for table public.dataset_readme
CREATE TABLE IF NOT EXISTS "dataset_readme" (
	"id" CHAR(36) NOT NULL,
	"content" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_readme_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_readme: -1 rows
/*!40000 ALTER TABLE "dataset_readme" DISABLE KEYS */;
INSERT INTO "dataset_readme" ("id", "content", "dataset_id") VALUES
	('6473a133-af27-4b6c-a8a0-3fc850d3ab91', 'none', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_readme" ENABLE KEYS */;

-- Dumping structure for table public.dataset_record_keys
CREATE TABLE IF NOT EXISTS "dataset_record_keys" (
	"id" CHAR(36) NOT NULL,
	"key_type" VARCHAR NOT NULL,
	"key_details" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_record_keys_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_record_keys: -1 rows
/*!40000 ALTER TABLE "dataset_record_keys" DISABLE KEYS */;
INSERT INTO "dataset_record_keys" ("id", "key_type", "key_details", "dataset_id") VALUES
	('46867b5a-9eb1-4f0e-98ba-5b453c2c9ff2', 'test', 'test', '00000000-0000-0000-0000-000000000001'),
	('bb834d3c-b59a-4968-b31c-51bd22c11c4f', 'test', 'test', '00000000-0000-0000-0000-000000000001'),
	('82fbb094-74c5-4dd1-9248-9e219c0b70f5', 'test1', 'test1', '00000000-0000-0000-0000-000000000001'),
	('59c1b98d-876f-49f6-aeb0-f32d4fde6c3f', 'test1', 'test1', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_record_keys" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item
CREATE TABLE IF NOT EXISTS "dataset_related_item" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"relation_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item: -1 rows
/*!40000 ALTER TABLE "dataset_related_item" DISABLE KEYS */;
INSERT INTO "dataset_related_item" ("id", "type", "relation_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'main', 'main', '00000000-0000-0000-0000-000000000002'),
	('f55af3f0-16f9-4049-8beb-f6673d32bef0', '', '', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_related_item" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item_contributor
CREATE TABLE IF NOT EXISTS "dataset_related_item_contributor" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"name_type" VARCHAR NOT NULL,
	"creator" BOOLEAN NOT NULL,
	"contributor_type" VARCHAR NOT NULL,
	"dataset_related_item_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_contributor_dataset_related_item_id_fkey" FOREIGN KEY ("dataset_related_item_id") REFERENCES "dataset_related_item" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_contributor" DISABLE KEYS */;
INSERT INTO "dataset_related_item_contributor" ("id", "name", "name_type", "creator", "contributor_type", "dataset_related_item_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'AIREADI', 'string', 'true', 'owner', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_related_item_contributor" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item_identifier
CREATE TABLE IF NOT EXISTS "dataset_related_item_identifier" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"metadata_scheme" VARCHAR NOT NULL,
	"scheme_uri" VARCHAR NOT NULL,
	"scheme_type" VARCHAR NOT NULL,
	"dataset_related_item_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_identifier_dataset_related_item_id_fkey" FOREIGN KEY ("dataset_related_item_id") REFERENCES "dataset_related_item" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item_identifier: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_identifier" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_identifier" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item_other
CREATE TABLE IF NOT EXISTS "dataset_related_item_other" (
	"id" CHAR(36) NOT NULL,
	"publication_year" VARCHAR NOT NULL,
	"volume" VARCHAR NOT NULL,
	"issue" VARCHAR NOT NULL,
	"number_value" VARCHAR NOT NULL,
	"number_type" VARCHAR NOT NULL,
	"first_page" VARCHAR NOT NULL,
	"last_page" BOOLEAN NOT NULL,
	"publisher" VARCHAR NOT NULL,
	"edition" VARCHAR NOT NULL,
	"dataset_related_item_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_other_dataset_related_item_id_fkey" FOREIGN KEY ("dataset_related_item_id") REFERENCES "dataset_related_item" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item_other: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_other" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_other" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item_title
CREATE TABLE IF NOT EXISTS "dataset_related_item_title" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"title" VARCHAR NOT NULL,
	"dataset_related_item_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_title_dataset_related_item_id_fkey" FOREIGN KEY ("dataset_related_item_id") REFERENCES "dataset_related_item" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item_title: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_title" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item_title" ENABLE KEYS */;

-- Dumping structure for table public.dataset_rights
CREATE TABLE IF NOT EXISTS "dataset_rights" (
	"id" CHAR(36) NOT NULL,
	"rights" VARCHAR NOT NULL,
	"uri" VARCHAR NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_scheme" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_rights_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_rights: -1 rows
/*!40000 ALTER TABLE "dataset_rights" DISABLE KEYS */;
INSERT INTO "dataset_rights" ("id", "rights", "uri", "identifier", "identifier_scheme", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'NA', 'https://orcid.org', 'none', 'ORCID', '00000000-0000-0000-0000-000000000001'),
	('e9fd3c26-843b-465a-b950-8d23005df384', 'NA', 'https://orcid.org', 'none', 'ORCID', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_rights" ENABLE KEYS */;

-- Dumping structure for table public.dataset_subject
CREATE TABLE IF NOT EXISTS "dataset_subject" (
	"id" CHAR(36) NOT NULL,
	"subject" VARCHAR NOT NULL,
	"scheme" VARCHAR NOT NULL,
	"scheme_uri" VARCHAR NOT NULL,
	"value_uri" VARCHAR NOT NULL,
	"classification_code" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_subject_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_subject: -1 rows
/*!40000 ALTER TABLE "dataset_subject" DISABLE KEYS */;
INSERT INTO "dataset_subject" ("id", "subject", "scheme", "scheme_uri", "value_uri", "classification_code", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '', '', '', '', 'NLM''s Medical Subject', '00000000-0000-0000-0000-000000000001'),
	('5ce2ba12-e536-4858-8913-7de2225cecc3', '', '', '', '', 'NLM''s Medical Subject', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_subject" ENABLE KEYS */;

-- Dumping structure for table public.dataset_title
CREATE TABLE IF NOT EXISTS "dataset_title" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"dataset_id" VARCHAR NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_title_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_title: -1 rows
/*!40000 ALTER TABLE "dataset_title" DISABLE KEYS */;
INSERT INTO "dataset_title" ("id", "title", "type", "dataset_id") VALUES
	('02937b58-268d-486d-ad63-55a79b39ea9c', 'title', 'na', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "dataset_title" ENABLE KEYS */;

-- Dumping structure for table public.invited_study_contributor
CREATE TABLE IF NOT EXISTS "invited_study_contributor" (
	"email_address" VARCHAR NOT NULL,
	"permission" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"invited_on" BIGINT NOT NULL,
	PRIMARY KEY ("email_address", "study_id"),
	CONSTRAINT "invited_study_contributor_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.invited_study_contributor: -1 rows
/*!40000 ALTER TABLE "invited_study_contributor" DISABLE KEYS */;
INSERT INTO "invited_study_contributor" ("email_address", "permission", "study_id", "invited_on") VALUES
	('Aliya_Herman@yahoo.com', 'editor', '00000000-0000-0000-0000-000000000001', 1693805470),
	('Anastacio50@hotmail.com', 'viewer', '00000000-0000-0000-0000-000000000001', 1693805470),
	('Edward0@gmail.com', 'viewer', '00000000-0000-0000-0000-000000000001', 1693805470),
	('Jailyn17@gmail.com', 'viewer', '00000000-0000-0000-0000-000000000002', 1693805470);
/*!40000 ALTER TABLE "invited_study_contributor" ENABLE KEYS */;

-- Dumping structure for table public.participant
CREATE TABLE IF NOT EXISTS "participant" (
	"id" CHAR(36) NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"address" VARCHAR NOT NULL,
	"age" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"created_at" BIGINT NOT NULL,
	"updated_on" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "participant_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.participant: -1 rows
/*!40000 ALTER TABLE "participant" DISABLE KEYS */;
INSERT INTO "participant" ("id", "first_name", "last_name", "address", "age", "study_id", "created_at", "updated_on") VALUES
	('00000000-0000-0000-0000-000000000002', 'bhavesh', 'patel', '3904 university ave', '20', '00000000-0000-0000-0000-000000000002', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000003', 'sanjay', 'soundarajan', '123 gold coast', '27', '00000000-0000-0000-0000-000000000003', 1693805470, 1693805470),
	('921ba857-dd08-4149-8f5c-245c6c93ef84', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('458d2c15-6ed8-4f70-a47d-70b42f2f1b86', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('35750167-40c5-4f4a-9d8e-ebe89c2efcfc', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('43c54d45-2f63-41da-8d18-6d3ef06ba476', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('b444520d-0eac-4065-a86d-004481f68d8a', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('88c7592a-4382-4d6b-a197-e880e49db3c0', 'aydan1', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('ba73ed99-6ec2-46e0-acdb-4a00c31dd572', 'aydan', 'gasimova', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000001', 'aydan', 'gasimova1', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('006306a7-0ddb-4163-952d-2939712e190d', 'aydan', 'gasimova1', '1221d kibler drive', '20', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('c1f24707-e909-45e5-9b44-fd35c0ad62be', 'bhavesh', 'patel', '3904 university ave', '20', '00000000-0000-0000-0000-000000000001', 1694032113, 1694032113);
/*!40000 ALTER TABLE "participant" ENABLE KEYS */;



-- Dumping structure for table public.user
CREATE TABLE IF NOT EXISTS "user" (
	"id" CHAR(36) NOT NULL,
	"email_address" VARCHAR NOT NULL,
	"username" VARCHAR NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"orcid" VARCHAR NOT NULL,
	"hash" VARCHAR NOT NULL,
	"institution" VARCHAR NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id")
);

-- Dumping data for table public.user: -1 rows
/*!40000 ALTER TABLE "user" DISABLE KEYS */;
INSERT INTO "user" ("id", "email_address", "username", "first_name", "last_name", "orcid", "hash", "institution", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'Ervin_Lindgren@hotmail.com', 'Ervin79', 'Ervin', 'Lindgren', 'd348206e-b1e2-4f99-9157-44b1321ecb4c', 'hashed', 'Schinner, Kuvalis and Beatty', 1693805470),
	('00000000-0000-0000-0000-000000000002', 'Camila.Pacocha@hotmail.com', 'Camila_Pacocha', 'Camila', 'Pacocha', '699e9977-5d86-40fc-bf1a-a5083f0cdc95', 'hashed', 'Schmitt Inc', 1693805470),
	('00000000-0000-0000-0000-000000000003', 'Alaina.Hammes@hotmail.com', 'Alaina_Hammes', 'Alaina', 'Hammes', '0b39872c-a1d6-44c0-88c2-7ea1b3a33dcf', 'hashed', 'Stracke, Leuschke and Kuvalis', 1693805470),
	('00000000-0000-0000-0000-000000000004', 'Brady_Anderson@gmail.com', 'Brady_Anderson', 'Brady', 'Anderson', '779d42d2-4743-43d3-980b-fcf1a962b485', 'hashed', 'Heidenreich, Wilkinson and Mitchell', 1693805470),
	('00000000-0000-0000-0000-000000000005', 'Brycen78@hotmail.com', 'Brycen_OReilly64', 'Brycen', 'O''Reilly', '529053dc-a755-4819-bdd2-a593d41e7f73', 'hashed', 'Heaney, Russel and Turner', 1693805470);
/*!40000 ALTER TABLE "user" ENABLE KEYS */;


-- Dumping structure for table public.study_arm
CREATE TABLE IF NOT EXISTS "study_arm" (
	"id" CHAR(36) NOT NULL,
	"label" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"intervention_list" VARCHAR[] NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_arm_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_arm: -1 rows
/*!40000 ALTER TABLE "study_arm" DISABLE KEYS */;
INSERT INTO "study_arm" ("id", "label", "type", "description", "intervention_list", "study_id", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'arm1', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'arm1', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('3fa464ca-6701-4a75-ab84-c26f3d3f49be', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('527b87cc-55e5-4e39-ada6-1ed738cdde47', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('3d2189e8-e95b-4d1b-ac1e-b0716bbe9eb4', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('47c1c51b-f145-4b7a-af99-f05eb0feb133', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('50278410-a4ca-4e0b-bff0-632f9a1c447a', 'arm1', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('cb555a08-5387-4d34-b397-1ddd10fec0b9', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000002', 1694326095),
	('038bb56d-2b8b-483a-a974-3612fc52b2a3', 'arm2', 'Experimental', 'Lorem Ipsum', '{inter1,"intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('173c6350-ba74-47fd-ae34-f39e2c4901ab', 'arm1', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('91dca128-d30d-41e3-8115-2a548b029e04', 'arm2', 'Experimental', 'Lorem Ipsum', '{"intervention 1","intervention 2"}', '00000000-0000-0000-0000-000000000001', 1694326095);
/*!40000 ALTER TABLE "study_arm" ENABLE KEYS */;

-- Dumping structure for table public.study_available_ipd
CREATE TABLE IF NOT EXISTS "study_available_ipd" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"url" VARCHAR NOT NULL,
	"comment" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
    "created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_available_ipd_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_available_ipd: -1 rows
/*!40000 ALTER TABLE "study_available_ipd" DISABLE KEYS */;
INSERT INTO "study_available_ipd" ("id", "identifier", "type", "url", "comment", "study_id", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'AS25AF', 'Study Protocol', 'https://someurl.io', '', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'AS2655AF', 'Study Protocol', 'https://someurl.io', '', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'AS625AF', 'Study Protocol', 'https://someurl.io', '', '00000000-0000-0000-0000-000000000002', 1694326095);
/*!40000 ALTER TABLE "study_available_ipd" ENABLE KEYS */;

-- Dumping structure for table public.study_contact
CREATE TABLE IF NOT EXISTS "study_contact" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"affiliation" VARCHAR NOT NULL,
	"role" VARCHAR NULL DEFAULT NULL,
	"phone" VARCHAR NOT NULL,
	"phone_ext" VARCHAR NOT NULL,
	"email_address" VARCHAR NOT NULL,
	"central_contact" BOOLEAN NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_contact_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_contact: -1 rows
/*!40000 ALTER TABLE "study_contact" DISABLE KEYS */;
INSERT INTO "study_contact" ("id", "name", "affiliation", "role", "phone", "phone_ext", "email_address", "central_contact", "study_id", "created_at"
) VALUES
	('00000000-0000-0000-0000-000000000001', 'Dejah', 'Erdman Inc', NULL, '501-039-841', '', 'Dejah83@hotmail.com', 'true', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000004', 'Lela', 'Metz LLC', NULL, '501-039-841', '', 'Lela84@hotmail.com', 'true', '00000000-0000-0000-0000-000000000002', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'Verner', 'Monahan and Sons', NULL, '501-039-841', '', 'Verner19@yahoo.com', 'false', '00000000-0000-0000-0000-000000000002', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'Reanna', 'Schowalter, Ullrich and Reichert', NULL, '501-039-841', '', 'Reanna79@hotmail.com', 'false', '00000000-0000-0000-0000-000000000001', 1694326095);
/*!40000 ALTER TABLE "study_contact" ENABLE KEYS */;

-- Dumping structure for table public.study_contributor
CREATE TABLE IF NOT EXISTS "study_contributor" (
	"permission" VARCHAR NOT NULL,
	"user_id" CHAR(36) NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("user_id", "study_id"),
	CONSTRAINT "study_contributor_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "study_contributor_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_contributor: -1 rows
/*!40000 ALTER TABLE "study_contributor" DISABLE KEYS */;
INSERT INTO "study_contributor" ("permission", "user_id", "study_id") VALUES
	('owner', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001'),
	('editor', '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001'),
	('editor', '00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001'),
	('viewer', '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000001'),
	('owner', '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002'),
	('viewer', '00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000002'),
	('viewer', '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000002'),
	('owner', '00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000003'),
	('viewer', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000003'),
	('editor', '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000003'),
	('owner', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000005'),
	('owner', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000006'),
	('owner', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000007'),
	('owner', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000008');
/*!40000 ALTER TABLE "study_contributor" ENABLE KEYS */;

-- Dumping structure for table public.study_description
CREATE TABLE IF NOT EXISTS "study_description" (
	"id" CHAR(36) NOT NULL,
	"brief_summary" VARCHAR NOT NULL,
	"detailed_description" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_description_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_description: -1 rows
/*!40000 ALTER TABLE "study_description" DISABLE KEYS */;
INSERT INTO "study_description" ("id", "brief_summary", "detailed_description", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'study summary', 'big description', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'study summary', 'big description', '00000000-0000-0000-0000-000000000003'),
	('d083b544-b359-4210-9f5f-d5de7b3dce1e', 'study summary', 'big description', '00000000-0000-0000-0000-000000000002'),
	('bfc385dc-4391-41a5-9f93-65d96e60bfe4', '', '', 'e5a2a1d2-850f-465a-8fc1-6a1aec6d9e5a'),
	('052fe6d3-bb46-478c-b680-77f342594258', '', '', 'ec0064ca-4f34-48a8-9dcc-1377c7ca0a59'),
	('3ebd87eb-f790-41b9-9a73-9ba51a39f429', '', '', '995d703e-a6d0-4dc2-95e7-3ce868eb9fb7'),
	('58f8ee80-9d2b-4828-addf-03e072702423', '', '', 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('e6256c6b-138a-438b-b6f3-916767dfb051', '', '', 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('b66dae93-ca0e-4d8c-8078-d504b5ed6038', '', '', 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('3ca6a722-479c-4e79-b79a-702fe8f5ed06', '', '', '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('e8a2b389-781d-4e10-94a3-0a04b59771d7', '', '', '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('ab7a024f-c9f2-4021-b86c-1516025c4cc4', '', '', '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('a75786cc-06d8-4793-ae09-1a85a3cb4d26', '', '', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_description" ENABLE KEYS */;

-- Dumping structure for table public.study_design
CREATE TABLE IF NOT EXISTS "study_design" (
	"id" CHAR(36) NOT NULL,
	"design_allocation" VARCHAR NULL DEFAULT NULL,
	"study_type" VARCHAR NOT NULL,
	"design_intervention_model" VARCHAR NULL DEFAULT NULL,
	"design_intervention_model_description" VARCHAR NULL DEFAULT NULL,
	"design_primary_purpose" VARCHAR NULL DEFAULT NULL,
	"design_masking" VARCHAR NULL DEFAULT NULL,
	"design_masking_description" VARCHAR NULL DEFAULT NULL,
	"design_who_masked_list" VARCHAR[] NULL DEFAULT NULL,
	"phase_list" VARCHAR[] NULL DEFAULT NULL,
	"enrollment_count" INTEGER NOT NULL,
	"enrollment_type" VARCHAR NOT NULL,
	"number_arms" INTEGER NULL DEFAULT NULL,
	"design_observational_model_list" VARCHAR[] NULL DEFAULT NULL,
	"design_time_perspective_list" VARCHAR[] NULL DEFAULT NULL,
	"bio_spec_retention" VARCHAR NULL DEFAULT NULL,
	"bio_spec_description" VARCHAR NULL DEFAULT NULL,
	"target_duration" VARCHAR NULL DEFAULT NULL,
	"number_groups_cohorts" INTEGER NULL DEFAULT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_design_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_design: -1 rows
/*!40000 ALTER TABLE "study_design" DISABLE KEYS */;
INSERT INTO "study_design" ("id", "design_allocation", "study_type", "design_intervention_model", "design_intervention_model_description", "design_primary_purpose", "design_masking", "design_masking_description", "design_who_masked_list", "phase_list", "enrollment_count", "enrollment_type", "number_arms", "design_observational_model_list", "design_time_perspective_list", "bio_spec_retention", "bio_spec_description", "target_duration", "number_groups_cohorts", "study_id") VALUES
	('56228349-b6bb-45e3-8877-0ade34016bd9', NULL, 'Observational', NULL, NULL, NULL, NULL, NULL, '{"Billy sanders"}', NULL, 20, 'Actual', NULL, '{Cohort}', '{Retrospective}', 'None Retained', 'description', '5 Days', 30, '00000000-0000-0000-0000-000000000005'),
	('d1a85ba2-2f1b-4360-b60d-4d2996b57aa4', NULL, 'Interventional', NULL, NULL, NULL, NULL, NULL, '{"Billy sanders"}', NULL, 20, 'Actual', NULL, '{Cohort}', '{Retrospective}', 'None Retained', 'description', '5 Days', 30, '00000000-0000-0000-0000-000000000001'),
	('1258a00d-5c9a-4e8a-907f-79a39f4b21e8', NULL, 'Observational', NULL, NULL, NULL, NULL, NULL, '{"Billy sanders"}', NULL, 20, 'Actual', NULL, '{Cohort}', '{Retrospective}', 'None Retained', 'description', '5 Days', 30, 'd925991e-af73-4fa2-ab2a-7040140a57df'),
	('00000000-0000-0000-0000-000000000002', NULL, 'Interventional', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 20, 'Actual', NULL, '{Cohort}', '{Retrospective}', 'None Retained', 'description', '5 Days', 30, '00000000-0000-0000-0000-000000000007'),
	('764cb716-a9fa-49b8-a9eb-7b948ff1d835', NULL, 'Interventional', NULL, NULL, NULL, NULL, NULL, '{"Billy sanders"}', NULL, 20, 'Actual', NULL, '{Cohort}', '{Retrospective}', 'None Retained', 'description', '5 Days', 30, '00000000-0000-0000-0000-000000000002'),
	('efa13194-2320-42d6-8348-0db63de6696b', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('a6d0f1ba-2f9d-4ce4-a0c8-c12315975d04', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('0966fc6a-0e32-4989-bd59-63956cfec02e', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('a4dcaf28-8d81-4fcb-a69e-0ca664b5a84d', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('8ced9a54-e88c-4f74-90c8-2d84c6401dda', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('1f886857-2094-4f2c-8d5d-55ee1805db11', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('f0902357-928c-47a7-8263-97985bc344be', '', '', '', '', '', '', '', '{}', '{}', 0, '', 0, '{}', '{}', '', '', '', 0, 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_design" ENABLE KEYS */;

-- Dumping structure for table public.study_eligibility
CREATE TABLE IF NOT EXISTS "study_eligibility" (
	"id" CHAR(36) NOT NULL,
	"gender" VARCHAR NOT NULL,
	"gender_based" VARCHAR NOT NULL,
	"gender_description" VARCHAR NOT NULL,
	"minimum_age_value" INTEGER NOT NULL,
	"maximum_age_value" INTEGER NOT NULL,
	"minimum_age_unit" VARCHAR NOT NULL,
	"maximum_age_unit" VARCHAR NOT NULL,
	"healthy_volunteers" VARCHAR DEFAULT NULL,
	"inclusion_criteria" VARCHAR[] NOT NULL,
	"exclusion_criteria" VARCHAR[] NOT NULL,
	"study_population" VARCHAR NULL DEFAULT NULL,
	"sampling_method" VARCHAR NULL DEFAULT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_eligibility_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_eligibility: 2 rows
/*!40000 ALTER TABLE "study_eligibility" DISABLE KEYS */;
INSERT INTO "study_eligibility" ("id", "gender", "gender_based", "gender_description", "minimum_age_value", "maximum_age_value", "minimum_age_unit", "maximum_age_unit", "healthy_volunteers", "inclusion_criteria", "exclusion_criteria", "study_population", "sampling_method", "study_id") VALUES
	('aa2de03c-d062-4e2a-93a7-4e3ac0ed2629', 'All', 'Yes', 'Description', 24, 34, 'Years', 'Years', 'selected', '{"inclusion 1"}', '{"exclusion 1"}', 'Description', 'Probability Sample', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'All', 'Yes', 'Description', 24, 34, 'Years', 'Years', 'selected', '{"inclusion 1"}', '{"exclusion 1"}', 'Description', 'Probability Sample', '00000000-0000-0000-0000-000000000001'),
	('abace007-f4d5-470d-b60e-b947c0b8a28a', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', '995d703e-a6d0-4dc2-95e7-3ce868eb9fb7'),
	('e0778c32-9097-453e-836f-4d7f0fc30d01', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('ea3f8c85-bfa1-4cf6-81d3-bde9d79bf0c2', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('5fbae118-430d-4d1a-b88b-61b2feed08fe', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('a41f2a42-2372-4bbb-9aea-83298b3fc855', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('23df9c4f-c939-4548-88b6-111f95bb2ed0', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('b3be3fff-eeec-4c2c-91dc-9bce6dff1fc7', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('624a91d1-980b-4bf0-b2e6-dbdd1e5ec2c2', '', '', '', 18, 60, '', '', '', '{}', '{}', '', '', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_eligibility" ENABLE KEYS */;

-- Dumping structure for table public.study_identification
CREATE TABLE IF NOT EXISTS "study_identification" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_type" VARCHAR NOT NULL,
	"identifier_domain" VARCHAR NOT NULL,
	"identifier_link" VARCHAR NOT NULL,
	"secondary" BOOLEAN NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_identification_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_identification: -1 rows
/*!40000 ALTER TABLE "study_identification" DISABLE KEYS */;
INSERT INTO "study_identification" ("id", "identifier", "identifier_type", "identifier_domain", "identifier_link", "secondary", "study_id", "created_at"
) VALUES
	('00000000-0000-0000-0000-000000000001', 'ADF89ADS', 'NIH Grant Number', '', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'false', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'ADF8934ADS', 'NIH Grant Number', '', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'AD6F89ADS', 'NIH Grant Number', '', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000004', 'ADF897ADS', 'NIH Grant Number', '', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002', 1694326095),
	('00000000-0000-0000-0000-000000000005', 'ADF897ADS', 'NIH Grant Number', 'domain', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'false', '00000000-0000-0000-0000-000000000002', 1694326095),
	('d70c6003-1a9d-4ee2-adca-3250dd1ae50a', 'ADF897ADS', 'NIH Grant Number', '', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002', 1694326095);
/*!40000 ALTER TABLE "study_identification" ENABLE KEYS */;

-- Dumping structure for table public.study_intervention
CREATE TABLE IF NOT EXISTS "study_intervention" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"name" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"arm_group_label_list" VARCHAR[] NOT NULL,
	"other_name_list" VARCHAR[] NOT NULL,
	"study_id" CHAR(36) NOT NULL,
    "created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_intervention_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_intervention: -1 rows
/*!40000 ALTER TABLE "study_intervention" DISABLE KEYS */;
INSERT INTO "study_intervention" ("id", "type", "name", "description", "arm_group_label_list", "other_name_list", "study_id", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'Drug', 'Test Name1', 'Lorem Ipsum', '{"name 1"}', '{"name 1"}', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'Drug', 'Test Name2', 'Lorem Ipsum', '{"name 1"}', '{"name 1"}', '00000000-0000-0000-0000-000000000001', 1694326095);
/*!40000 ALTER TABLE "study_intervention" ENABLE KEYS */;

-- Dumping structure for table public.study_ipdsharing
CREATE TABLE IF NOT EXISTS "study_ipdsharing" (
	"id" CHAR(36) NOT NULL,
	"ipd_sharing" VARCHAR NOT NULL,
	"ipd_sharing_description" VARCHAR NOT NULL,
	"ipd_sharing_info_type_list" VARCHAR[] NOT NULL,
	"ipd_sharing_time_frame" VARCHAR NOT NULL,
	"ipd_sharing_access_criteria" VARCHAR NOT NULL,
	"ipd_sharing_url" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_ipdsharing_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_ipdsharing: -1 rows
/*!40000 ALTER TABLE "study_ipdsharing" DISABLE KEYS */;
INSERT INTO "study_ipdsharing" ("id", "ipd_sharing", "ipd_sharing_description", "ipd_sharing_info_type_list", "ipd_sharing_time_frame", "ipd_sharing_access_criteria", "ipd_sharing_url", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'Yes', 'Lorem Ipsum', '{"Study Protocol"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000001'),
	('54ba9f80-106e-4dda-a507-cbc66a6b6b48', 'Yes', 'Lorem Ipsum', '{"Study Protocol"}', 'January 2025', 'No criteria updated', 'https://orcid.org/', '00000000-0000-0000-0000-000000000002'),
	('dd98f3a8-76e6-4cd5-9d7f-9a274dc8edff', '', '', '{}', '', '', '', 'ec0064ca-4f34-48a8-9dcc-1377c7ca0a59'),
	('02ac873b-7cc0-4725-a307-182ccbe3eadd', '', '', '{}', '', '', '', '995d703e-a6d0-4dc2-95e7-3ce868eb9fb7'),
	('45bccc13-add0-4fc4-ab85-58c94ce27247', '', '', '{}', '', '', '', 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('b8b90e0c-058e-4c26-a587-5bb3f6782a8c', '', '', '{}', '', '', '', 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('cd263b0d-03e8-4f2d-b6c2-7ef1944015ab', '', '', '{}', '', '', '', 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('2be4bdfa-e187-4767-a903-a6e45d349a94', '', '', '{}', '', '', '', '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('d71f1e8b-42a7-4814-a80c-27418f76b79d', '', '', '{}', '', '', '', '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('c98e3f78-89f8-48d4-b974-6ac1e80bc44e', '', '', '{}', '', '', '', '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('b37f781e-55d2-47e9-8f7e-6d1ab21ce96b', '', '', '{}', '', '', '', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_ipdsharing" ENABLE KEYS */;

-- Dumping structure for table public.study_link
CREATE TABLE IF NOT EXISTS "study_link" (
	"id" CHAR(36) NOT NULL,
	"url" VARCHAR NOT NULL,
	"title" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
    "created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_link_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_link: -1 rows
/*!40000 ALTER TABLE "study_link" DISABLE KEYS */;
INSERT INTO "study_link" ("id", "url", "title", "study_id", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'https://schema.aireadi.org/', 'schema1', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'https://schema.aireadi.org/', 'schema2', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'https://schema.aireadi.org/', 'schema3', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000004', 'https://schema.aireadi.org/', 'schema1', '00000000-0000-0000-0000-000000000002', 1694326095);
/*!40000 ALTER TABLE "study_link" ENABLE KEYS */;

-- Dumping structure for table public.study_location
CREATE TABLE IF NOT EXISTS "study_location" (
	"id" CHAR(36) NOT NULL,
	"facility" VARCHAR NOT NULL,
	"status" VARCHAR NOT NULL,
	"city" VARCHAR NOT NULL,
	"state" VARCHAR NOT NULL,
	"zip" VARCHAR NOT NULL,
	"country" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
    "created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_location_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_location: -1 rows
/*!40000 ALTER TABLE "study_location" DISABLE KEYS */;
INSERT INTO "study_location" ("id", "facility", "status", "city", "state", "zip", "country", "study_id", , "created_at"
) VALUES
	('00000000-0000-0000-0000-000000000001', 'facility1', 'Recruting', 'San Diego', 'CA', '92121', 'USA', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'facility2', 'Recruting', 'San Diego', 'CA', '92121', 'USA', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'facility1', 'Recruting', 'San Diego', 'CA', '92121', 'USA', '00000000-0000-0000-0000-000000000002', 1694326095);
/*!40000 ALTER TABLE "study_location" ENABLE KEYS */;

-- Dumping structure for table public.study_other
CREATE TABLE IF NOT EXISTS "study_other" (
	"id" CHAR(36) NOT NULL,
	"oversight_has_dmc" BOOLEAN NOT NULL,
	"conditions" VARCHAR[] NOT NULL,
	"keywords" VARCHAR[] NOT NULL,
	"size" BIGINT NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_other_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_other: -1 rows
/*!40000 ALTER TABLE "study_other" DISABLE KEYS */;
INSERT INTO "study_other" ("id", "oversight_has_dmc", "conditions", "keywords", "size", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'true', '{"condition 1"}', '{"keyword 1"}', 32, '00000000-0000-0000-0000-000000000001'),
	('7a1217d6-6e58-432d-b747-36e1dec81499', 'true', '{conditionupdate}', '{"keyword 1"}', 32, '00000000-0000-0000-0000-000000000002'),
	('837dce97-4073-4c4a-8d65-d1b7c87f92c6', 'false', '{}', '{}', '', 'e5a2a1d2-850f-465a-8fc1-6a1aec6d9e5a'),
	('a651f9b1-3db4-4dae-a486-e9f7f7b5a5cb', 'false', '{}', '{}', '', 'ec0064ca-4f34-48a8-9dcc-1377c7ca0a59'),
	('ccd3e31d-9e45-4329-9c89-2e7c7fa0d53b', 'false', '{}', '{}', '', '995d703e-a6d0-4dc2-95e7-3ce868eb9fb7'),
	('b2176d5e-6c1e-4b4d-91a4-b271b042c88c', 'false', '{}', '{}', '', 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('43bcce4d-92d9-4b0f-9844-1885796a295f', 'false', '{}', '{}', '', 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('22195a93-d2cd-4a0b-80d0-f1da5bcfd215', 'false', '{}', '{}', '', 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('5fd15009-c8ff-4070-bcef-ae969713bfd4', 'false', '{}', '{}', '', '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('6f759a30-742b-4c8a-9eca-a52efdb279e6', 'false', '{}', '{}', '', '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('2f1197a1-bd0c-42fb-a680-46242ebf8e80', 'false', '{}', '{}', '', '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('dfa22eea-c4d7-4cdc-84b7-5023a145354e', 'false', '{}', '{}', '', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_other" ENABLE KEYS */;

-- Dumping structure for table public.study_overall_official
CREATE TABLE IF NOT EXISTS "study_overall_official" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"affiliation" VARCHAR NOT NULL,
	"role" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
    "created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_overall_official_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_overall_official: -1 rows
/*!40000 ALTER TABLE "study_overall_official" DISABLE KEYS */;
INSERT INTO "study_overall_official" ("id", "name", "affiliation", "role", "study_id", "created_at"
) VALUES
	('00000000-0000-0000-0000-000000000001', 'Zoey', 'Lowe, Kshlerin and Ward', 'Study Director', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'Ashlynn', 'Kuhic - Towne', 'Study Chair', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'Maiya', 'Medhurst - Marks', 'Study Chair', '00000000-0000-0000-0000-000000000002', 1694326095),
	('b1683ba3-26ca-42c5-a257-1974dbbf4f8b', 'Maiya', 'Medhurst - Marks', 'Study Chair', '00000000-0000-0000-0000-000000000002', 1694326095),
	('319c21f2-9441-48ec-a64c-ab839a1da2a3', 'Maiya', 'Medhurst - Marks', 'Study Chair', '00000000-0000-0000-0000-000000000002', 1694326095);
/*!40000 ALTER TABLE "study_overall_official" ENABLE KEYS */;

-- Dumping structure for table public.study_reference
CREATE TABLE IF NOT EXISTS "study_reference" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"citation" VARCHAR NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_reference_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_reference: -1 rows
/*!40000 ALTER TABLE "study_reference" DISABLE KEYS */;
INSERT INTO "study_reference" ("id", "identifier", "type", "citation", "study_id", "created_at"
) VALUES
	('00000000-0000-0000-0000-000000000001', 'PMID1234 ', 'Yes', 'Lorem Ipsum', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000002', 'PMID12234 ', 'No', 'Lorem Ipsum', '00000000-0000-0000-0000-000000000001', 1694326095),
	('00000000-0000-0000-0000-000000000003', 'PMID1A2234 ', 'No', 'Lorem Ipsum', '00000000-0000-0000-0000-000000000002',1694326095);
/*!40000 ALTER TABLE "study_reference" ENABLE KEYS */;

-- Dumping structure for table public.study_sponsors_collaborators
CREATE TABLE IF NOT EXISTS "study_sponsors_collaborators" (
	"id" CHAR(36) NOT NULL,
	"responsible_party_type" VARCHAR NOT NULL,
	"responsible_party_investigator_name" VARCHAR NOT NULL,
	"responsible_party_investigator_title" VARCHAR NOT NULL,
	"responsible_party_investigator_affiliation" VARCHAR NOT NULL,
	"lead_sponsor_name" VARCHAR NOT NULL,
	"collaborator_name" VARCHAR[] NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_sponsors_collaborators_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_sponsors_collaborators: -1 rows
/*!40000 ALTER TABLE "study_sponsors_collaborators" DISABLE KEYS */;
INSERT INTO "study_sponsors_collaborators" ("id", "responsible_party_type", "responsible_party_investigator_name", "responsible_party_investigator_title", "responsible_party_investigator_affiliation", "lead_sponsor_name", "collaborator_name", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'Principal Investigator', 'Sean West', 'Title 1', 'Wyman Inc', 'Kurtis Daniel', '{UCSD}', '00000000-0000-0000-0000-000000000001'),
	('9b92a2db-e864-4a5d-8a88-91a3d8a48b74', 'Principal Investigatorup updated version', 'Sean West', 'Title 1', 'Wyman Inc', 'Kurtis Daniel', '{"UCSD updated"}', '00000000-0000-0000-0000-000000000002'),
	('9fcde425-1d11-4d31-bfc2-edc022871876', '', '', '', '', '', '{}', 'f154f7c2-58a9-4b2e-808c-3d9a71dc99d2'),
	('cbb8562c-ac36-481d-b67c-5d69d7ae83cd', '', '', '', '', '', '{}', 'af2f9f5e-24eb-4b54-8fe1-ec76391b9af6'),
	('4d5361ab-ce94-4f94-92ed-0fe6c47b2f3a', '', '', '', '', '', '{}', 'cb24e1c9-b4b2-451a-89b7-e73556d50ca2'),
	('51e75430-25cd-42fa-953e-3724090942f5', '', '', '', '', '', '{}', '39a913b7-daad-4c86-ba07-9f6400c73a28'),
	('75f7e616-4565-44e9-99de-a7e4afeaa06d', '', '', '', '', '', '{}', '61ac1bdb-1809-4d20-8e29-22d3f2d85252'),
	('41f99b90-3a02-49e3-af56-c29074e28cef', '', '', '', '', '', '{}', '626f2a7e-fa8f-459e-9076-a3b2082a00d2'),
	('ee92b6a8-f840-4db0-9184-54a488006227', '', '', '', '', '', '{}', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_sponsors_collaborators" ENABLE KEYS */;

-- Dumping structure for table public.study_status
CREATE TABLE IF NOT EXISTS "study_status" (
	"id" CHAR(36) NOT NULL,
	"overall_status" VARCHAR NULL DEFAULT NULL,
	"why_stopped" VARCHAR NOT NULL,
	"start_date" VARCHAR NULL DEFAULT NULL,
	"start_date_type" VARCHAR NULL DEFAULT NULL,
	"completion_date" VARCHAR NULL DEFAULT NULL,
	"completion_date_type" VARCHAR NULL DEFAULT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_status_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_status: 2 rows
/*!40000 ALTER TABLE "study_status" DISABLE KEYS */;
INSERT INTO "study_status" ("id", "overall_status", "why_stopped", "start_date", "start_date_type", "completion_date", "completion_date_type", "study_id") VALUES
	('b25cc3e6-f9b2-4c20-ba57-d82313d41df5', 'Suspended', 'Lorem Ipsum', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'Recruiting new', 'Lorem Ipsum', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'Anticipated', '00000000-0000-0000-0000-000000000001'),
	('30f39019-ff68-4b7e-b058-23ac64172e1d', '', '', NULL, '', NULL, '', 'ee3012e5-3c51-4d21-b16c-5ace1c80cf72');
/*!40000 ALTER TABLE "study_status" ENABLE KEYS */;

-- Dumping structure for table public.version
CREATE TABLE IF NOT EXISTS "version" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"published" BOOLEAN NOT NULL,
	"changelog" VARCHAR NOT NULL,
	"doi" VARCHAR NOT NULL,
	"published_on" TIMESTAMP NOT NULL,
	"dataset_id" CHAR(36) NOT NULL,
	"updated_on" BIGINT NOT NULL,
	"created_at" BIGINT NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "version_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.version: -1 rows
/*!40000 ALTER TABLE "version" DISABLE KEYS */;
INSERT INTO "version" ("id", "title", "published", "changelog", "doi", "published_on", "dataset_id", "updated_on", "created_at") VALUES
	('00000000-0000-0000-0000-000000000001', 'Version 1', 'true', 'lorem ipsum', '2435464e643', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000002', 'Version 2', 'false', 'lorem ipsum', '2435464e643', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000001', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000003', 'Version 1', 'false', 'lorem ipsum', '2435464e643', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000002', 1693805470, 1693805470),
	('00000000-0000-0000-0000-000000000004', 'Version 1', 'false', 'lorem ipsum', '2435464e643', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000003', 1693805470, 1693805470);
/*!40000 ALTER TABLE "version" ENABLE KEYS */;

-- Dumping structure for table public.version_participants
CREATE TABLE IF NOT EXISTS "version_participants" (
	"dataset_version_id" CHAR(36) NOT NULL,
	"participant_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("dataset_version_id", "participant_id"),
	CONSTRAINT "version_participants_dataset_version_id_fkey" FOREIGN KEY ("dataset_version_id") REFERENCES "version" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "version_participants_participant_id_fkey" FOREIGN KEY ("participant_id") REFERENCES "participant" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.version_participants: -1 rows
/*!40000 ALTER TABLE "version_participants" DISABLE KEYS */;
INSERT INTO "version_participants" ("dataset_version_id", "participant_id") VALUES
	('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "version_participants" ENABLE KEYS */;

-- Dumping structure for table public.study_redcap_project_api
CREATE TABLE IF NOT EXISTS "study_redcap_project_api" (
	"study_id" CHAR(36) NOT NULL,
	"project_id" BIGINT NOT NULL,
	"project_title" VARCHAR NOT NULL,
	"project_api_url" VARCHAR NOT NULL,
	"project_api_key" CHAR(32) NOT NULL,
	"created_at" BIGINT NOT NULL,
	"updated_on" BIGINT NOT NULL,
	PRIMARY KEY ("study_id", "project_id"),
	CONSTRAINT "study_redcap_project_api_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_redcap_project_api: 1 rows
/*!40000 ALTER TABLE "study_redcap_project_api" DISABLE KEYS */;
INSERT INTO "study_redcap_project_api" ("study_id", "project_id", "project_title", "project_api_url", "project_api_key", "created_at", "updated_on") VALUES
	('00000000-0000-0000-0000-000000000006', '666666', 'other-stuff', 'https://redcap.university.org/api', '0000000000000000AAAAAAAAAAAAAAA6', '2023-08-13 16:23:48', '2023-08-14 16:23:49');
/*!40000 ALTER TABLE "study_redcap_project_api" ENABLE KEYS */;

-- Dumping structure for table public.study_redcap_project_dashboard
CREATE TABLE IF NOT EXISTS "study_redcap_project_dashboard" (
	"study_id" CHAR(36) NOT NULL,
	"project_id" BIGINT NOT NULL,
	"dashboard_id" CHAR(36) NOT NULL,
	"dashboard_name" VARCHAR NOT NULL,
	"dashboard_modules" VARCHAR[] NOT NULL,
	"created_at" BIGINT NOT NULL,
	"updated_on" BIGINT NOT NULL,
	PRIMARY KEY ("study_id", "project_id", "dashboard_id"),
	CONSTRAINT "study_redcap_project_dashboard_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "study_redcap_project_dashboard_project_id_fkey" FOREIGN KEY ("project_id") REFERENCES "study_redcap_project_api" ("project_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_redcap_project_dashboard: 1 rows
/*!40000 ALTER TABLE "study_redcap_project_dashboard" DISABLE KEYS */;
INSERT INTO "study_redcap_project_dashboard" ("study_id", "project_id", "dashboard_id", "dashboard_name", "dashboard_modules", "created_at", "updated_on") VALUES
	('00000000-0000-0000-0000-000000000006', '666666', '00000000-0000-0000-0000-000000000006', 'other-stuff', '{}', '2023-08-13 16:23:48', '2023-08-14 16:23:49');
/*!40000 ALTER TABLE "study_redcap_project_dashboard" ENABLE KEYS */;


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

COMMIT;
