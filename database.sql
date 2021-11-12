/*
 Navicat Premium Data Transfer

 Source Server         : Remote Codecool
 Source Server Type    : PostgreSQL
 Source Server Version : 140000
 Source Host           : mainserver.brolake.ro:5432
 Source Catalog        : askmate
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140000
 File Encoding         : 65001

 Date: 12/11/2021 11:24:51
*/


-- ----------------------------
-- Sequence structure for answer_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."answer_id_seq";
CREATE SEQUENCE "public"."answer_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for comment_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."comment_id_seq";
CREATE SEQUENCE "public"."comment_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for question_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."question_id_seq";
CREATE SEQUENCE "public"."question_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tag_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tag_id_seq";
CREATE SEQUENCE "public"."tag_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq1";
CREATE SEQUENCE "public"."users_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for answer
-- ----------------------------
DROP TABLE IF EXISTS "public"."answer";
CREATE TABLE "public"."answer" (
  "id" int4 NOT NULL DEFAULT nextval('answer_id_seq'::regclass),
  "submission_time" timestamp(6) DEFAULT now(),
  "vote_number" int4 DEFAULT 0,
  "question_id" int4,
  "message" text COLLATE "pg_catalog"."default",
  "user_id" int4 NOT NULL,
  "bow" bool NOT NULL DEFAULT false
)
;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS "public"."comment";
CREATE TABLE "public"."comment" (
  "id" int4 NOT NULL DEFAULT nextval('comment_id_seq'::regclass),
  "question_id" int4,
  "answer_id" int4,
  "message" text COLLATE "pg_catalog"."default",
  "submission_time" timestamp(6) DEFAULT now(),
  "edited_count" int4 DEFAULT 0,
  "user_id" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS "public"."question";
CREATE TABLE "public"."question" (
  "id" int4 NOT NULL DEFAULT nextval('question_id_seq'::regclass),
  "submission_time" timestamp(6) DEFAULT now(),
  "view_number" int4 DEFAULT 0,
  "vote_number" int4 DEFAULT 0,
  "title" text COLLATE "pg_catalog"."default",
  "message" text COLLATE "pg_catalog"."default",
  "image" text COLLATE "pg_catalog"."default",
  "user_id" int4 NOT NULL,
  "bonus_question" bool NOT NULL DEFAULT false
)
;

-- ----------------------------
-- Table structure for question_tag
-- ----------------------------
DROP TABLE IF EXISTS "public"."question_tag";
CREATE TABLE "public"."question_tag" (
  "question_id" int4 NOT NULL,
  "tag_id" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS "public"."tag";
CREATE TABLE "public"."tag" (
  "id" int4 NOT NULL DEFAULT nextval('tag_id_seq'::regclass),
  "name" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL GENERATED ALWAYS AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
),
  "username" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "password" bytea NOT NULL,
  "registered" date NOT NULL DEFAULT now(),
  "administrator" bool NOT NULL DEFAULT false
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."answer_id_seq"
OWNED BY "public"."answer"."id";
SELECT setval('"public"."answer_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."comment_id_seq"
OWNED BY "public"."comment"."id";
SELECT setval('"public"."comment_id_seq"', 12, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."question_id_seq"
OWNED BY "public"."question"."id";
SELECT setval('"public"."question_id_seq"', 58, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."tag_id_seq"
OWNED BY "public"."tag"."id";
SELECT setval('"public"."tag_id_seq"', 7, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 8, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq1"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq1"', 4, true);

-- ----------------------------
-- Primary Key structure for table answer
-- ----------------------------
ALTER TABLE "public"."answer" ADD CONSTRAINT "pk_answer_id" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table comment
-- ----------------------------
ALTER TABLE "public"."comment" ADD CONSTRAINT "pk_comment_id" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table question
-- ----------------------------
ALTER TABLE "public"."question" ADD CONSTRAINT "pk_question_id" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table question_tag
-- ----------------------------
ALTER TABLE "public"."question_tag" ADD CONSTRAINT "pk_question_tag_id" PRIMARY KEY ("question_id", "tag_id");

-- ----------------------------
-- Primary Key structure for table tag
-- ----------------------------
ALTER TABLE "public"."tag" ADD CONSTRAINT "pk_tag_id" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table answer
-- ----------------------------
ALTER TABLE "public"."answer" ADD CONSTRAINT "answer_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."answer" ADD CONSTRAINT "fk_question_id" FOREIGN KEY ("question_id") REFERENCES "public"."question" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table comment
-- ----------------------------
ALTER TABLE "public"."comment" ADD CONSTRAINT "comment_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."comment" ADD CONSTRAINT "fk_answer_id" FOREIGN KEY ("answer_id") REFERENCES "public"."answer" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."comment" ADD CONSTRAINT "fk_question_id" FOREIGN KEY ("question_id") REFERENCES "public"."question" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table question
-- ----------------------------
ALTER TABLE "public"."question" ADD CONSTRAINT "question_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table question_tag
-- ----------------------------
ALTER TABLE "public"."question_tag" ADD CONSTRAINT "fk_question_id" FOREIGN KEY ("question_id") REFERENCES "public"."question" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."question_tag" ADD CONSTRAINT "fk_tag_id" FOREIGN KEY ("tag_id") REFERENCES "public"."tag" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
