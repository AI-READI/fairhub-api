-- --------------------------------------------------------
-- Host:                         7hg.h.filess.io
-- Server version:               PostgreSQL 14.4 on x86_64-pc-linux-musl, compiled by gcc (Alpine 11.2.1_git20220219) 11.2.1 20220219, 64-bit
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

-- Dumping structure for table public.dataset
CREATE TABLE IF NOT EXISTS "dataset" (
	"id" CHAR(36) NOT NULL,
	"updated_on" TIMESTAMP NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset: 4 rows
/*!40000 ALTER TABLE "dataset" DISABLE KEYS */;
INSERT INTO "dataset" ("id", "updated_on", "created_at", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000005', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "dataset" ENABLE KEYS */;

-- Dumping structure for table public.dataset_access
CREATE TABLE IF NOT EXISTS "dataset_access" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"url" VARCHAR NOT NULL,
	"url_last_checked" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_access_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_access: -1 rows
/*!40000 ALTER TABLE "dataset_access" DISABLE KEYS */;
INSERT INTO "dataset_access" ("id", "type", "description", "url", "url_last_checked", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'main', 'Clinical research studies ', 'https://aireadi.org', '1st August', NULL),
	('badac1ab-26fd-4f94-b2b4-b198365a198f', 'none', '', '', '', NULL),
	('6d2c020f-71b1-48d2-8532-89a563868fa4', 'none', '', '', '', NULL),
	('f8f3bf91-2eb9-49b8-a8f0-1c92def99bcf', 'none', '', '', '', NULL),
	('395d37d9-e3cf-4989-81f6-21dd2202d1ca', 'none', '', '', '', NULL),
	('fdc10b6d-2dc6-41c1-b43e-202a24abc80a', 'none', '', '', '', NULL);
/*!40000 ALTER TABLE "dataset_access" ENABLE KEYS */;

-- Dumping structure for table public.dataset_alternate_identifier
CREATE TABLE IF NOT EXISTS "dataset_alternate_identifier" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_identifier_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_alternate_identifier: 3 rows
/*!40000 ALTER TABLE "dataset_alternate_identifier" DISABLE KEYS */;
INSERT INTO "dataset_alternate_identifier" ("id", "identifier", "identifier_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'N/A', 'N/A', NULL),
	('00000000-0000-0000-0000-000000000002', '126543GF3', 'GRID', NULL),
	('77df307c-eb87-450b-b5d5-7d75bfb88cf7', 'N/A', 'N/A', NULL);
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_consent_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_consent: -1 rows
/*!40000 ALTER TABLE "dataset_consent" DISABLE KEYS */;
INSERT INTO "dataset_consent" ("id", "type", "noncommercial", "geog_restrict", "research_type", "genetic_only", "no_methods", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'none', 'true', 'true', 'true', 'false', 'false', 'na', NULL),
	('f38a6bae-8724-411d-999a-f587cfdd32bf', 'none', 'true', 'true', 'true', 'false', 'false', 'na', NULL);
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_contributor_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_contributor" DISABLE KEYS */;
INSERT INTO "dataset_contributor" ("id", "first_name", "last_name", "name_type", "name_identifier", "name_identifier_scheme", "name_identifier_scheme_uri", "creator", "contributor_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh', 'patel', 'type_name', 'identifier', 'scheme', 'scheme uri', 'true', 'type', NULL);
/*!40000 ALTER TABLE "dataset_contributor" ENABLE KEYS */;

-- Dumping structure for table public.dataset_contributor_affiliation
CREATE TABLE IF NOT EXISTS "dataset_contributor_affiliation" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_scheme" VARCHAR NOT NULL,
	"identifier_scheme_uri" VARCHAR NOT NULL,
	"dataset_contributor_id" VARCHAR NULL DEFAULT NULL,
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_date_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_date: -1 rows
/*!40000 ALTER TABLE "dataset_date" DISABLE KEYS */;
INSERT INTO "dataset_date" ("id", "date", "date_type", "data_information", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '2023', 'day', 'none', '00000000-0000-0000-0000-000000000005'),
	('00000000-0000-0000-0000-000000000001', '2023', 'day', 'none', NULL),
	('00000000-0000-0000-0000-000000000004', '2023', 'day', 'none', NULL),
	('0b1775e5-d110-482f-a1c4-2aa3947b8db8', '', 'na', 'none', NULL),
	('dc090dbd-6fa3-4b61-829e-2f139bdbd116', '', 'na', 'none', NULL);
/*!40000 ALTER TABLE "dataset_date" ENABLE KEYS */;

-- Dumping structure for table public.dataset_description
CREATE TABLE IF NOT EXISTS "dataset_description" (
	"id" CHAR(36) NOT NULL,
	"description" VARCHAR NOT NULL,
	"description_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_description_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_description: -1 rows
/*!40000 ALTER TABLE "dataset_description" DISABLE KEYS */;
INSERT INTO "dataset_description" ("id", "description", "description_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'AI-READI is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program.', 'object', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000001', '', '', NULL),
	('78f2b774-2f5a-4096-b82e-9923ca04395b', '', '', NULL);
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_de_ident_level_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_de_ident_level: -1 rows
/*!40000 ALTER TABLE "dataset_de_ident_level" DISABLE KEYS */;
INSERT INTO "dataset_de_ident_level" ("id", "type", "direct", "hipaa", "dates", "nonarr", "k_anon", "details", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'NA', 'false', 'true', 'false', 'true', 'false', 'none', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', '', 'false', 'true', 'false', 'true', 'false', '', NULL),
	('1bc4eeb0-dcdf-41af-b8e9-d05923ba45fa', '', 'true', 'true', 'true', 'true', 'true', '', NULL),
	('a3f40ca7-4f34-43b5-9e44-fc20e8f50eef', '', 'true', 'true', 'true', 'true', 'true', '', NULL);
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_funder_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_funder: -1 rows
/*!40000 ALTER TABLE "dataset_funder" DISABLE KEYS */;
INSERT INTO "dataset_funder" ("id", "name", "identifier", "identifier_type", "identifier_scheme_uri", "award_number", "award_uri", "award_title", "dataset_id") VALUES
	('8ef6d41f-2f59-492c-9f28-8c1c10bcc4e8', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', '', NULL);
/*!40000 ALTER TABLE "dataset_funder" ENABLE KEYS */;

-- Dumping structure for table public.dataset_managing_organization
CREATE TABLE IF NOT EXISTS "dataset_managing_organization" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"ror_id" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_managing_organization_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_managing_organization: -1 rows
/*!40000 ALTER TABLE "dataset_managing_organization" DISABLE KEYS */;
INSERT INTO "dataset_managing_organization" ("id", "name", "ror_id", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'UCSD', '354grhji5', NULL),
	('c5d5a32a-c072-4594-989a-4b55acc5d11b', 'UCD', '354grhji5', NULL);
/*!40000 ALTER TABLE "dataset_managing_organization" ENABLE KEYS */;

-- Dumping structure for table public.dataset_other
CREATE TABLE IF NOT EXISTS "dataset_other" (
	"id" CHAR(36) NOT NULL,
	"language" VARCHAR NOT NULL,
	"managing_organization_name" VARCHAR NOT NULL,
	"managing_organization_ror_id" VARCHAR NOT NULL,
	"size" UNKNOWN NOT NULL,
	"standards_followed" VARCHAR NOT NULL,
	"acknowledgement" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_other_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_other: -1 rows
/*!40000 ALTER TABLE "dataset_other" DISABLE KEYS */;
INSERT INTO "dataset_other" ("id", "language", "managing_organization_name", "managing_organization_ror_id", "size", "standards_followed", "acknowledgement", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000003', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org/other', 'NA', NULL),
	('00000000-0000-0000-0000-000000000002', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'none', 'NA', NULL),
	('2fca4640-6f0e-406c-8c7a-e93a0740b9c6', 'eng', 'Research Organisation Registry', 'https://ror.org', '{1}', 'https://ror.org', 'NA', NULL);
/*!40000 ALTER TABLE "dataset_other" ENABLE KEYS */;

-- Dumping structure for table public.dataset_readme
CREATE TABLE IF NOT EXISTS "dataset_readme" (
	"id" CHAR(36) NOT NULL,
	"content" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_readme_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_readme: -1 rows
/*!40000 ALTER TABLE "dataset_readme" DISABLE KEYS */;
INSERT INTO "dataset_readme" ("id", "content", "dataset_id") VALUES
	('6473a133-af27-4b6c-a8a0-3fc850d3ab91', 'none', NULL);
/*!40000 ALTER TABLE "dataset_readme" ENABLE KEYS */;

-- Dumping structure for table public.dataset_record_keys
CREATE TABLE IF NOT EXISTS "dataset_record_keys" (
	"id" CHAR(36) NOT NULL,
	"key_type" VARCHAR NOT NULL,
	"key_details" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_record_keys_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_record_keys: -1 rows
/*!40000 ALTER TABLE "dataset_record_keys" DISABLE KEYS */;
INSERT INTO "dataset_record_keys" ("id", "key_type", "key_details", "dataset_id") VALUES
	('46867b5a-9eb1-4f0e-98ba-5b453c2c9ff2', 'test', 'test', NULL),
	('59c1b98d-876f-49f6-aeb0-f32d4fde6c3f', 'test1', 'test1', NULL),
	('82fbb094-74c5-4dd1-9248-9e219c0b70f5', 'test1', 'test1', NULL),
	('bb834d3c-b59a-4968-b31c-51bd22c11c4f', 'test', 'test', NULL);
/*!40000 ALTER TABLE "dataset_record_keys" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item
CREATE TABLE IF NOT EXISTS "dataset_related_item" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"relation_type" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_related_item_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_related_item: -1 rows
/*!40000 ALTER TABLE "dataset_related_item" DISABLE KEYS */;
INSERT INTO "dataset_related_item" ("id", "type", "relation_type", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'main', 'main', '00000000-0000-0000-0000-000000000002'),
	('f55af3f0-16f9-4049-8beb-f6673d32bef0', '', '', NULL);
/*!40000 ALTER TABLE "dataset_related_item" ENABLE KEYS */;

-- Dumping structure for table public.dataset_related_item_contributor
CREATE TABLE IF NOT EXISTS "dataset_related_item_contributor" (
	"id" CHAR(36) NOT NULL,
	"name" VARCHAR NOT NULL,
	"name_type" VARCHAR NOT NULL,
	"creator" BOOLEAN NOT NULL,
	"contributor_type" VARCHAR NOT NULL,
	"dataset_related_item_id" CHAR(36) NULL DEFAULT NULL,
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
	"dataset_related_item_id" CHAR(36) NULL DEFAULT NULL,
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
	"dataset_related_item_id" CHAR(36) NULL DEFAULT NULL,
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
	"dataset_related_item_id" CHAR(36) NULL DEFAULT NULL,
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
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_rights_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_rights: -1 rows
/*!40000 ALTER TABLE "dataset_rights" DISABLE KEYS */;
INSERT INTO "dataset_rights" ("id", "rights", "uri", "identifier", "identifier_scheme", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'NA', 'https://orcid.org', 'none', 'ORCID', NULL),
	('e9fd3c26-843b-465a-b950-8d23005df384', 'NA', 'https://orcid.org', 'none', 'ORCID', NULL);
/*!40000 ALTER TABLE "dataset_rights" ENABLE KEYS */;

-- Dumping structure for table public.dataset_subject
CREATE TABLE IF NOT EXISTS "dataset_subject" (
	"id" CHAR(36) NOT NULL,
	"subject" VARCHAR NOT NULL,
	"scheme" VARCHAR NOT NULL,
	"scheme_uri" VARCHAR NOT NULL,
	"value_uri" VARCHAR NOT NULL,
	"classification_code" VARCHAR NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_subject_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_subject: -1 rows
/*!40000 ALTER TABLE "dataset_subject" DISABLE KEYS */;
INSERT INTO "dataset_subject" ("id", "subject", "scheme", "scheme_uri", "value_uri", "classification_code", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', '', '', '', '', 'NLM''s Medical Subject', NULL),
	('5ce2ba12-e536-4858-8913-7de2225cecc3', '', '', '', '', 'NLM''s Medical Subject', NULL);
/*!40000 ALTER TABLE "dataset_subject" ENABLE KEYS */;

-- Dumping structure for table public.dataset_title
CREATE TABLE IF NOT EXISTS "dataset_title" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"dataset_id" VARCHAR NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_title_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.dataset_title: -1 rows
/*!40000 ALTER TABLE "dataset_title" DISABLE KEYS */;
INSERT INTO "dataset_title" ("id", "title", "type", "dataset_id") VALUES
	('02937b58-268d-486d-ad63-55a79b39ea9c', 'title', 'na', NULL);
/*!40000 ALTER TABLE "dataset_title" ENABLE KEYS */;

-- Dumping structure for table public.invited_study_contributor
CREATE TABLE IF NOT EXISTS "invited_study_contributor" (
	"email_address" VARCHAR NOT NULL,
	"permission" VARCHAR NOT NULL,
	"invited_on" TIMESTAMP NOT NULL,
	"study_id" CHAR(36) NOT NULL,
	PRIMARY KEY ("email_address", "study_id"),
	CONSTRAINT "invited_study_contributor_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.invited_study_contributor: -1 rows
/*!40000 ALTER TABLE "invited_study_contributor" DISABLE KEYS */;
INSERT INTO "invited_study_contributor" ("email_address", "permission", "invited_on", "study_id") VALUES
	('aydan.gasimova@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000001'),
	('bhavesh.patel@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000003'),
	('sanjay.soundarajan@@gmail.com', 'owner', '2023-08-13 16:34:16', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "invited_study_contributor" ENABLE KEYS */;

-- Dumping structure for table public.participant
CREATE TABLE IF NOT EXISTS "participant" (
	"id" CHAR(36) NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"address" VARCHAR NOT NULL,
	"age" VARCHAR NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"updated_on" TIMESTAMP NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "participant_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study
CREATE TABLE IF NOT EXISTS "study" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"image" VARCHAR NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"updated_on" TIMESTAMP NOT NULL,
	PRIMARY KEY ("id")
);

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

-- Dumping structure for table public.study_arm
CREATE TABLE IF NOT EXISTS "study_arm" (
	"id" CHAR(36) NOT NULL,
	"label" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"intervention_list" UNKNOWN NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_arm_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study_available_ipd
CREATE TABLE IF NOT EXISTS "study_available_ipd" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"url" VARCHAR NOT NULL,
	"comment" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_available_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_available_ipd: -1 rows
/*!40000 ALTER TABLE "study_available_ipd" DISABLE KEYS */;
INSERT INTO "study_available_ipd" ("id", "identifier", "type", "url", "comment", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', ' for intermediate-size patient populations', 'available', 'https://json-schema.org/draft/2020-12/schema', 'none', '00000000-0000-0000-0000-000000000003');
/*!40000 ALTER TABLE "study_available_ipd" ENABLE KEYS */;

-- Dumping structure for table public.study_contact
CREATE TABLE IF NOT EXISTS "study_contact" (
	"id" CHAR(36) NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"affiliation" VARCHAR NOT NULL,
	"role" VARCHAR NOT NULL,
	"phone" VARCHAR NOT NULL,
	"phone_ext" VARCHAR NOT NULL,
	"email_address" VARCHAR NOT NULL,
	"central_contact" BOOLEAN NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_contact_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_contact: -1 rows
/*!40000 ALTER TABLE "study_contact" DISABLE KEYS */;
INSERT INTO "study_contact" ("id", "first_name", "last_name", "affiliation", "role", "phone", "phone_ext", "email_address", "central_contact", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'holly', 'sienna', 'calmi2', 'editor', '4056074345', 'ext', 'holly.sienna@gmail.com', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'billy', 'brown', 'calmi2', 'editor', '4056074345', 'ext', 'billy.sanders@gmail.com', 'true', '00000000-0000-0000-0000-000000000001'),
	('81e71d41-2c93-47cb-9fac-00d94ab1c1a2', 'billy', 'brown', 'calmi2', 'editor', '4056074345', 'ext', 'billy.sanders@gmail.com', 'true', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_contact" ENABLE KEYS */;

-- Dumping structure for table public.study_contributor
CREATE TABLE IF NOT EXISTS "study_contributor" (
	"permission" VARCHAR NOT NULL,
	"user_id" CHAR(36) NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("user_id"),
	CONSTRAINT "study_contributor_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "study_contributor_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_contributor: -1 rows
/*!40000 ALTER TABLE "study_contributor" DISABLE KEYS */;
INSERT INTO "study_contributor" ("permission", "user_id", "study_id") VALUES
	('editor', '00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001'),
	('owner', '00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002'),
	('owner', '00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000004'),
	('editor', '00000000-0000-0000-0000-000000000004', '00000000-0000-0000-0000-000000000006');
/*!40000 ALTER TABLE "study_contributor" ENABLE KEYS */;

-- Dumping structure for table public.study_description
CREATE TABLE IF NOT EXISTS "study_description" (
	"id" CHAR(36) NOT NULL,
	"brief_summary" VARCHAR NOT NULL,
	"detailed_description" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_description_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_description: -1 rows
/*!40000 ALTER TABLE "study_description" DISABLE KEYS */;
INSERT INTO "study_description" ("id", "brief_summary", "detailed_description", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000003'),
	('f51a772e-373a-452a-8106-822840a76339', 'study summary', 'This is one of the data generation projects of the National Institutes of Health (NIH) funded Bridge2AI Program', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_description" ENABLE KEYS */;

-- Dumping structure for table public.study_design
CREATE TABLE IF NOT EXISTS "study_design" (
	"id" CHAR(36) NOT NULL,
	"design_allocation" VARCHAR NOT NULL,
	"study_type" VARCHAR NOT NULL,
	"design_interventional_model" VARCHAR NOT NULL,
	"design_intervention_model_description" VARCHAR NOT NULL,
	"design_primary_purpose" VARCHAR NOT NULL,
	"design_masking" VARCHAR NOT NULL,
	"design_masking_description" VARCHAR NOT NULL,
	"design_who_masked_list" UNKNOWN NOT NULL,
	"phase_list" UNKNOWN NOT NULL,
	"enrollment_count" INTEGER NOT NULL,
	"enrollment_type" VARCHAR NOT NULL,
	"number_arms" INTEGER NOT NULL,
	"design_observational_model_list" UNKNOWN NOT NULL,
	"design_time_perspective_list" UNKNOWN NOT NULL,
	"bio_spec_retention" VARCHAR NOT NULL,
	"bio_spec_description" VARCHAR NOT NULL,
	"target_duration" VARCHAR NOT NULL,
	"number_groups_cohorts" INTEGER NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_design_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_design: -1 rows
/*!40000 ALTER TABLE "study_design" DISABLE KEYS */;
INSERT INTO "study_design" ("id", "design_allocation", "study_type", "design_interventional_model", "design_intervention_model_description", "design_primary_purpose", "design_masking", "design_masking_description", "design_who_masked_list", "phase_list", "enrollment_count", "enrollment_type", "number_arms", "design_observational_model_list", "design_time_perspective_list", "bio_spec_retention", "bio_spec_description", "target_duration", "number_groups_cohorts", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'Randomized', 'type', 'treatment of cancer', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '1 years', 10, '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'Randomized', 'type', 'treatment', 'description', 'Single Group Assignment', 'Blinded', 'description', '{Participant}', '{Trials}', 1, 'enrollmentInfo', 2, '{casecontrol}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3 months', 10, '00000000-0000-0000-0000-000000000002'),
	('2b1312ef-338b-454a-9e17-5db84e17d97c', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{[,'',P,a,r,t,i,c,i,p,a,n,t,'',]}', '{Trials}', 1, 'enrollmentInfo', 2, '{[,'',C,a,s,e,C,o,n,t,r,o,l,'',]}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001'),
	('ca5500a4-cbce-454a-a767-653461d59397', 'Randomized', 'type', 'biomedical chemistry', 'description', 'Single Group Assignment', 'Blinded', 'description', '{CaseControl}', '{Trials}', 1, 'enrollmentInfo', 2, '{CaseControl}', '{Retrospective}', 'Samples With DNA', 'Specify all types', '3years', 10, '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_design" ENABLE KEYS */;

-- Dumping structure for table public.study_eligibility
CREATE TABLE IF NOT EXISTS "study_eligibility" (
	"id" CHAR(36) NOT NULL,
	"gender" VARCHAR NOT NULL,
	"gender_based" VARCHAR NOT NULL,
	"gender_description" VARCHAR NOT NULL,
	"healthy_volunteers" BOOLEAN NOT NULL,
	"inclusion_criteria" UNKNOWN NOT NULL,
	"exclusion_criteria" UNKNOWN NOT NULL,
	"study_population" VARCHAR NOT NULL,
	"sampling_method" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	"minimum_age_value" INTEGER NOT NULL,
	"minimum_age_unit" VARCHAR NOT NULL,
	"maximum_age_value" INTEGER NOT NULL,
	"maximum_age_unit" VARCHAR NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_eligibility_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study_identification
CREATE TABLE IF NOT EXISTS "study_identification" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"identifier_type" VARCHAR NOT NULL,
	"identifier_domain" VARCHAR NOT NULL,
	"identifier_link" VARCHAR NOT NULL,
	"secondary" BOOLEAN NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_identification_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_identification: -1 rows
/*!40000 ALTER TABLE "study_identification" DISABLE KEYS */;
INSERT INTO "study_identification" ("id", "identifier", "identifier_type", "identifier_domain", "identifier_link", "secondary", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001'),
	('cfc1b66c-882a-4eee-a6d7-01a7cb018ac2', 'Screening', 'Registry Identifier', 'registry Identifier', 'https://reporter.nih.gov/quickSearch/K01HL147713', 'true', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_identification" ENABLE KEYS */;

-- Dumping structure for table public.study_intervention
CREATE TABLE IF NOT EXISTS "study_intervention" (
	"id" CHAR(36) NOT NULL,
	"type" VARCHAR NOT NULL,
	"name" VARCHAR NOT NULL,
	"description" VARCHAR NOT NULL,
	"arm_group_label_list" UNKNOWN NOT NULL,
	"other_name_list" UNKNOWN NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_intervention_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study_ipdsharing
CREATE TABLE IF NOT EXISTS "study_ipdsharing" (
	"id" CHAR(36) NOT NULL,
	"ipd_sharing" VARCHAR NOT NULL,
	"ipd_sharing_description" VARCHAR NOT NULL,
	"ipd_sharing_info_type_list" UNKNOWN NOT NULL,
	"ipd_sharing_time_frame" VARCHAR NOT NULL,
	"ipd_sharing_access_criteria" VARCHAR NOT NULL,
	"ipd_sharing_url" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_ipdsharing_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_ipdsharing: -1 rows
/*!40000 ALTER TABLE "study_ipdsharing" DISABLE KEYS */;
INSERT INTO "study_ipdsharing" ("id", "ipd_sharing", "ipd_sharing_description", "ipd_sharing_info_type_list", "ipd_sharing_time_frame", "ipd_sharing_access_criteria", "ipd_sharing_url", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000003'),
	('ebfe1211-763e-4b10-8e15-7ccb29cb21f5', 'IPDSharing', 'unplanned', '{"Statistical Analysis Plan (SAP)"}', 'January 2025', 'No criteria', 'https://orcid.org/', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_ipdsharing" ENABLE KEYS */;

-- Dumping structure for table public.study_link
CREATE TABLE IF NOT EXISTS "study_link" (
	"id" CHAR(36) NOT NULL,
	"url" VARCHAR NOT NULL,
	"title" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_link_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study_location
CREATE TABLE IF NOT EXISTS "study_location" (
	"id" CHAR(36) NOT NULL,
	"facility" VARCHAR NOT NULL,
	"status" VARCHAR NOT NULL,
	"city" VARCHAR NOT NULL,
	"state" VARCHAR NOT NULL,
	"zip" VARCHAR NOT NULL,
	"country" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_location_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

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

-- Dumping structure for table public.study_other
CREATE TABLE IF NOT EXISTS "study_other" (
	"id" CHAR(36) NOT NULL,
	"oversight_has_dmc" BOOLEAN NOT NULL,
	"conditions" UNKNOWN NOT NULL,
	"keywords" UNKNOWN NOT NULL,
	"size" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_other_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_other: -1 rows
/*!40000 ALTER TABLE "study_other" DISABLE KEYS */;
INSERT INTO "study_other" ("id", "oversight_has_dmc", "conditions", "keywords", "size", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000003', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000001', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000001'),
	('cd440fa9-988b-4d51-8b66-8c2e42c630b3', 'false', '{conditional}', '{none}', '1', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_other" ENABLE KEYS */;

-- Dumping structure for table public.study_overall_official
CREATE TABLE IF NOT EXISTS "study_overall_official" (
	"id" CHAR(36) NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"affiliation" VARCHAR NOT NULL,
	"role" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_overall_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_overall_official: -1 rows
/*!40000 ALTER TABLE "study_overall_official" DISABLE KEYS */;
INSERT INTO "study_overall_official" ("id", "first_name", "last_name", "affiliation", "role", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'firstname', 'lastname', 'affiliation', 'Study Chair, Study Director', '00000000-0000-0000-0000-000000000003'),
	('a0806089-6602-48b0-b870-1d5e91b956a5', 'firstname', 'lastname', 'affiliation', 'Study Chair', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_overall_official" ENABLE KEYS */;

-- Dumping structure for table public.study_reference
CREATE TABLE IF NOT EXISTS "study_reference" (
	"id" CHAR(36) NOT NULL,
	"identifier" VARCHAR NOT NULL,
	"type" VARCHAR NOT NULL,
	"citation" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_reference_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_reference: 6 rows
/*!40000 ALTER TABLE "study_reference" DISABLE KEYS */;
INSERT INTO "study_reference" ("id", "identifier", "type", "citation", "study_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'The PubMed Unique Identifier ', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000004', 'The PubMed Unique Identifier ', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('2996e115-8c44-4914-a470-2764ff280316', 'The PubMed Unique Identifier ', 'false', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000001', 'The PubMed Unique Identifier ', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'The PubMed Unique Identifier ', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000005', 'The PubMed Unique Identifier ', 'type', 'A bibliographic reference', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "study_reference" ENABLE KEYS */;

-- Dumping structure for table public.study_sponsors_collaborators
CREATE TABLE IF NOT EXISTS "study_sponsors_collaborators" (
	"id" CHAR(36) NOT NULL,
	"responsible_party_type" VARCHAR NOT NULL,
	"responsible_party_investigator_name" VARCHAR NOT NULL,
	"responsible_party_investigator_title" VARCHAR NOT NULL,
	"responsible_party_investigator_affiliation" VARCHAR NOT NULL,
	"lead_sponsor_name" VARCHAR NOT NULL,
	"collaborator_name" UNKNOWN NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_sponsors_collaborators_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_sponsors_collaborators: -1 rows
/*!40000 ALTER TABLE "study_sponsors_collaborators" DISABLE KEYS */;
INSERT INTO "study_sponsors_collaborators" ("id", "responsible_party_type", "responsible_party_investigator_name", "responsible_party_investigator_title", "responsible_party_investigator_affiliation", "lead_sponsor_name", "collaborator_name", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000004', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000005', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001'),
	('687dea6a-4dbf-45dc-867e-de7b303d4b0c', 'San Diego', 'firstname', 'title', 'affiliation', 'name', '{"clinical study"}', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_sponsors_collaborators" ENABLE KEYS */;

-- Dumping structure for table public.study_status
CREATE TABLE IF NOT EXISTS "study_status" (
	"id" CHAR(36) NOT NULL,
	"overall_status" VARCHAR NOT NULL,
	"why_stopped" VARCHAR NOT NULL,
	"start_date" TIMESTAMP NOT NULL,
	"start_date_type" VARCHAR NOT NULL,
	"completion_date" TIMESTAMP NOT NULL,
	"completion_date_type" VARCHAR NOT NULL,
	"study_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "study_status_study_id_fkey" FOREIGN KEY ("study_id") REFERENCES "study" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.study_status: -1 rows
/*!40000 ALTER TABLE "study_status" DISABLE KEYS */;
INSERT INTO "study_status" ("id", "overall_status", "why_stopped", "start_date", "start_date_type", "completion_date", "completion_date_type", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Suspended', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'anticipated', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2021-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000003', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2020-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000004', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Terminated', '2020-08-21 12:57:34', 'anticipated', '2022-08-21 12:57:44', 'Actual', '00000000-0000-0000-0000-000000000001'),
	('8100ce8e-406d-4483-bc47-634e97c34713', 'Overall Recruitment Status for the study must be ''Recruiting''', 'Suspended', '2021-08-21 12:57:34', 'Actual', '2022-08-21 12:57:44', 'anticipated', '00000000-0000-0000-0000-000000000001');
/*!40000 ALTER TABLE "study_status" ENABLE KEYS */;

-- Dumping structure for table public.user
CREATE TABLE IF NOT EXISTS "user" (
	"id" CHAR(36) NOT NULL,
	"email_address" VARCHAR NOT NULL,
	"username" VARCHAR NOT NULL,
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"orcid" VARCHAR NOT NULL,
	"hash" VARCHAR NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"institution" VARCHAR NOT NULL,
	PRIMARY KEY ("id")
);

-- Dumping data for table public.user: -1 rows
/*!40000 ALTER TABLE "user" DISABLE KEYS */;
INSERT INTO "user" ("id", "email_address", "username", "first_name", "last_name", "orcid", "hash", "created_at", "institution") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh.patel@gmail.com', 'bhavesh', 'Bhavesh', 'Patel', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000002', 'sanjay.soundarajan@gmail.com', 'sanjay', 'sanjay', 'soundarajan', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000003', 'billy.sanders@gmail.com', 'billy', 'billy', 'sanders', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000004', 'james.lilly@gmail.com', 'james', 'james', 'lilly', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2');
/*!40000 ALTER TABLE "user" ENABLE KEYS */;

-- Dumping structure for table public.version
CREATE TABLE IF NOT EXISTS "version" (
	"id" CHAR(36) NOT NULL,
	"title" VARCHAR NOT NULL,
	"published" BOOLEAN NOT NULL,
	"changelog" VARCHAR NOT NULL,
	"updated_on" TIMESTAMP NOT NULL,
	"doi" VARCHAR NOT NULL,
	"created_at" TIMESTAMP NOT NULL,
	"published_on" TIMESTAMP NOT NULL,
	"dataset_id" CHAR(36) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "dataset_version_dataset_id_fkey" FOREIGN KEY ("dataset_id") REFERENCES "dataset" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Dumping data for table public.version: -1 rows
/*!40000 ALTER TABLE "version" DISABLE KEYS */;
INSERT INTO "version" ("id", "title", "published", "changelog", "updated_on", "doi", "created_at", "published_on", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000002', 'AIREADI1', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'AIREADI4', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000003', 'AIREADI3', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000001', 'AIREADI', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', NULL);
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

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
