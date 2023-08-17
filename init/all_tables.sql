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

-- Dumping data for table public.dataset: -1 rows
/*!40000 ALTER TABLE "dataset" DISABLE KEYS */;
INSERT INTO "dataset" ("id", "updated_on", "created_at", "study_id") VALUES
	('00000000-0000-0000-0000-000000000001', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000005', '2023-08-13 16:23:48', '2023-08-13 16:23:49', '00000000-0000-0000-0000-000000000004');
/*!40000 ALTER TABLE "dataset" ENABLE KEYS */;

-- Dumping data for table public.dataset_access: -1 rows
/*!40000 ALTER TABLE "dataset_access" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_access" ENABLE KEYS */;

-- Dumping data for table public.dataset_consent: -1 rows
/*!40000 ALTER TABLE "dataset_consent" DISABLE KEYS */;
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
/*!40000 ALTER TABLE "dataset_date" ENABLE KEYS */;

-- Dumping data for table public.dataset_description: -1 rows
/*!40000 ALTER TABLE "dataset_description" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_description" ENABLE KEYS */;

-- Dumping data for table public.dataset_de_ident_level: -1 rows
/*!40000 ALTER TABLE "dataset_de_ident_level" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_de_ident_level" ENABLE KEYS */;

-- Dumping data for table public.dataset_funder: -1 rows
/*!40000 ALTER TABLE "dataset_funder" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_funder" ENABLE KEYS */;

-- Dumping data for table public.dataset_identifier: -1 rows
/*!40000 ALTER TABLE "dataset_identifier" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_identifier" ENABLE KEYS */;

-- Dumping data for table public.dataset_managing_organization: -1 rows
/*!40000 ALTER TABLE "dataset_managing_organization" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_managing_organization" ENABLE KEYS */;

-- Dumping data for table public.dataset_other: -1 rows
/*!40000 ALTER TABLE "dataset_other" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_other" ENABLE KEYS */;

-- Dumping data for table public.dataset_readme: -1 rows
/*!40000 ALTER TABLE "dataset_readme" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_readme" ENABLE KEYS */;

-- Dumping data for table public.dataset_record_keys: -1 rows
/*!40000 ALTER TABLE "dataset_record_keys" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_record_keys" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item: -1 rows
/*!40000 ALTER TABLE "dataset_related_item" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_related_item" ENABLE KEYS */;

-- Dumping data for table public.dataset_related_item_contributor: -1 rows
/*!40000 ALTER TABLE "dataset_related_item_contributor" DISABLE KEYS */;
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
/*!40000 ALTER TABLE "dataset_rights" ENABLE KEYS */;

-- Dumping data for table public.dataset_subject: -1 rows
/*!40000 ALTER TABLE "dataset_subject" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_subject" ENABLE KEYS */;

-- Dumping data for table public.dataset_title: -1 rows
/*!40000 ALTER TABLE "dataset_title" DISABLE KEYS */;
/*!40000 ALTER TABLE "dataset_title" ENABLE KEYS */;

-- Dumping data for table public.dataset_version: -1 rows
/*!40000 ALTER TABLE "dataset_version" DISABLE KEYS */;
INSERT INTO "dataset_version" ("id", "title", "published", "changelog", "updated_on", "doi", "created_at", "published_on", "dataset_id") VALUES
	('00000000-0000-0000-0000-000000000001', 'AIREADI', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'AIREADI1', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'AIREADI4', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000004'),
	('00000000-0000-0000-0000-000000000003', 'AIREADI3', 'true', 'lorem ipsum', '2023-08-13 16:24:05', '2435464e643', '2023-08-13 16:23:59', '2023-08-13 16:24:00', '00000000-0000-0000-0000-000000000003');
/*!40000 ALTER TABLE "dataset_version" ENABLE KEYS */;

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
	('00000000-0000-0000-0000-000000000001', 'aydan', 'gasimova', '1221d kibler drive', '20', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000001'),
	('00000000-0000-0000-0000-000000000002', 'bhavesh', 'patel', '3904 university ave', '20', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000002'),
	('00000000-0000-0000-0000-000000000003', 'sanjay', 'soundarajan', '123 gold coast', '27', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000003'),
	('00000000-0000-0000-0000-000000000004', 'billy', 'sanders', '123 gold coast', '32', '2023-08-13 16:33:53', '2023-08-13 16:33:54', '00000000-0000-0000-0000-000000000004');
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
/*!40000 ALTER TABLE "study_arm" ENABLE KEYS */;

-- Dumping data for table public.study_available: -1 rows
/*!40000 ALTER TABLE "study_available" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_available" ENABLE KEYS */;

-- Dumping data for table public.study_contact: -1 rows
/*!40000 ALTER TABLE "study_contact" DISABLE KEYS */;
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
/*!40000 ALTER TABLE "study_description" ENABLE KEYS */;

-- Dumping data for table public.study_design: -1 rows
/*!40000 ALTER TABLE "study_design" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_design" ENABLE KEYS */;

-- Dumping data for table public.study_eligibility: 0 rows
/*!40000 ALTER TABLE "study_eligibility" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_eligibility" ENABLE KEYS */;

-- Dumping data for table public.study_identification: -1 rows
/*!40000 ALTER TABLE "study_identification" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_identification" ENABLE KEYS */;

-- Dumping data for table public.study_intervention: -1 rows
/*!40000 ALTER TABLE "study_intervention" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_intervention" ENABLE KEYS */;

-- Dumping data for table public.study_ipdsharing: -1 rows
/*!40000 ALTER TABLE "study_ipdsharing" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_ipdsharing" ENABLE KEYS */;

-- Dumping data for table public.study_link: -1 rows
/*!40000 ALTER TABLE "study_link" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_link" ENABLE KEYS */;

-- Dumping data for table public.study_location: -1 rows
/*!40000 ALTER TABLE "study_location" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_location" ENABLE KEYS */;

-- Dumping data for table public.study_other: -1 rows
/*!40000 ALTER TABLE "study_other" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_other" ENABLE KEYS */;

-- Dumping data for table public.study_overall_official: -1 rows
/*!40000 ALTER TABLE "study_overall_official" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_overall_official" ENABLE KEYS */;

-- Dumping data for table public.study_reference: -1 rows
/*!40000 ALTER TABLE "study_reference" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_reference" ENABLE KEYS */;

-- Dumping data for table public.study_sponsors_collaborators: -1 rows
/*!40000 ALTER TABLE "study_sponsors_collaborators" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_sponsors_collaborators" ENABLE KEYS */;

-- Dumping data for table public.study_status: -1 rows
/*!40000 ALTER TABLE "study_status" DISABLE KEYS */;
/*!40000 ALTER TABLE "study_status" ENABLE KEYS */;

-- Dumping data for table public.user: -1 rows
/*!40000 ALTER TABLE "user" DISABLE KEYS */;
INSERT INTO "user" ("id", "email_address", "username", "first_name", "last_name", "orcid", "hash", "created_at", "institution") VALUES
	('00000000-0000-0000-0000-000000000001', 'bhavesh.patel@gmail.com', 'bhavesh', 'Bhavesh', 'Patel', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000002', 'sanjay.soundarajan@gmail.com', 'sanjay', 'sanjay', 'soundarajan', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000003', 'billy.sanders@gmail.com', 'billy', 'billy', 'sanders', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2'),
	('00000000-0000-0000-0000-000000000004', 'james.lilly@gmail.com', 'james', 'james', 'lilly', '1111-2222-333-444-5555', 'hashed', '2023-08-13 12:34:06', 'CALMI2');
/*!40000 ALTER TABLE "user" ENABLE KEYS */;

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
