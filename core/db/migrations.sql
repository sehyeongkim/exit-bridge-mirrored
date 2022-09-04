--  companies
CREATE TABLE `companies` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`gp_id`	int	NOT NULL,
	`name`	varchar(20)	NULL,
	`logo_img_url`	text	NULL,
	`product_name`	varchar(20)	NULL,
	`investment_stage`	varchar(20)	NULL,
	`investment_method`	varchar(20)	NULL,
	`total_capital`	float	NULL,
	`total_investment`	float	NULL,
	`company_classification`	varchar(20)	NULL,
	`corporate_classification`	varchar(20)	NULL,
	`establishment_date`	date	NULL,
	`homepage_url`	text	NULL,
	`business_category`	varchar(20)	NULL,
	`skill`	varchar(30)	NULL,
	`business_number`	varchar(30)	NULL,
	`venture_registration_number`	varchar(30)	NULL,
	`bond_issue_date`	date	NULL,
	`main_banner_img_url`	text	NULL
);

ALTER TABLE `companies` ADD CONSTRAINT `PK_COMPANIES` PRIMARY KEY (
	`id`
);


-- users
CREATE TABLE `users` (
	`id`	varchar(20)	NOT NULL,
	`email`	varchar(40)	NULL,
	`name`	varchar(20)	NULL,
	`phone_number`	varchar(20)	NULL,
	`type`	varchar(10)	NOT NULL,
	`access_token`	text	NULL,
	`refresh_token`	text	NULL,
	`profile_img_url`	text	NULL,
	`is_verified`	bool	NULL,
	`zip_code`	varchar(10)	NULL,
	`road_name_address`	varchar(100)	NULL,
	`detailed_address`	varchar(100)	NULL,
	`kakao_user_id`	varchar(50)	NULL,
	`created_at`	datetime	NOT NULL,
	`updated_at`	datetime	NOT NULL,
	`registration_number`	varchar(100)	NULL
);

ALTER TABLE `users` ADD CONSTRAINT `PK_USERS` PRIMARY KEY (
	`id`
);

-- main_posts
CREATE TABLE `main_posts` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`company_id`	int	NOT NULL,
	`gp_id`	int	NOT NULL,
	`intro`	text	NULL,
	`title`	varchar(100)	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`deleted_at`	datetime	NULL,
	`main_post_detail_id`	int	NULL,
	`recruitment_start_date`	datetime	NULL,
	`recruitment_end_date`	datetime	NULL,
	`recruitment_status`	varchar(10)	NULL,
	`is_open_to_public`	bool	NULL,
	`Field`	VARCHAR(255)	NULL
);

ALTER TABLE `main_posts` ADD CONSTRAINT `PK_MAIN_POSTS` PRIMARY KEY (
	`id`
);


-- main_post_qna
CREATE TABLE `main_post_qna` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`main_post_id`	int	NOT NULL,
	`user_id`	varchar(20)	NOT NULL,
	`title`	varchar(100)	NULL,
	`content`	text	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`is_answered`	bool	NULL,
	`answer`	text	NULL
);

ALTER TABLE `main_post_qna` ADD CONSTRAINT `PK_MAIN_POST_QNA` PRIMARY KEY (
	`id`
);


-- lp_application_forms
CREATE TABLE `lp_application_forms` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`user_id`	varchar(20)	NOT NULL,
	`union_id`	int	NOT NULL,
	`company_id`	int	NOT NULL,
	`signature_img_url`	text	NULL,
	`decision_date`	datetime	NULL,
	`total_share_number`	int	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`is_personal_info_checked`	bool	NULL,
	`is_agenda_checked`	bool	NULL,
	`is_application_checked`	bool	NULL,
	`income_deduction_applied_date`	date	NULL,
	`confirmation_status`	varchar(10)	NULL,
	`reject_reason`	text	NULL
);

ALTER TABLE `lp_application_forms` ADD CONSTRAINT `PK_LP_APPLICATION_FORMS` PRIMARY KEY (
	`id`
);


-- unions
CREATE TABLE `unions` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`gp_id`	int	NOT NULL,
	`company_id`	int	NULL,
	`name`	varchar(20)	NULL	COMMENT 'unique',
	`unit_share_price`	float	NULL,
	`total_share_number`	float	NULL,
	`total_share_price`	float	NULL,
	`establishment_date`	datetime	NULL,
	`expire_date`	datetime	NULL,
	`status`	varchar(10)	NULL	COMMENT '결성 진행중/ 운용중 / 해산',
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL
);

ALTER TABLE `unions` ADD CONSTRAINT `PK_UNIONS` PRIMARY KEY (
	`id`
);


-- unions_limited_partners
CREATE TABLE `unions_limited_partners` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`lp_id`	int	NOT NULL,
	`union_id`	int	NOT NULL
);


-- unions_limited_partners
ALTER TABLE `unions_limited_partners` ADD CONSTRAINT `PK_UNIONS_LIMITED_PARTNERS` PRIMARY KEY (
	`id`
);


-- companies_limited_partners
CREATE TABLE `companies_limited_partners` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`company_id`	int	NOT NULL,
	`lp_id`	int	NOT NULL
);

ALTER TABLE `companies_limited_partners` ADD CONSTRAINT `PK_COMPANIES_LIMITED_PARTNERS` PRIMARY KEY (
	`id`
);


-- feeds
CREATE TABLE `feeds` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`gp_id`	int	NOT NULL,
	`union_id`	int	NOT NULL,
	`company_id`	int	NOT NULL,
	`content`	text	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`deleted_at`	datetime	NULL
);

ALTER TABLE `feeds` ADD CONSTRAINT `PK_FEEDS` PRIMARY KEY (
	`id`
);


-- feed_comments
CREATE TABLE `feed_comments` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`user_id`	varchar(20)	NOT NULL,
	`feed_id`	int	NOT NULL,
	`content`	varchar(100)	NULL,
	`is_secret`	bool	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`deleted_at`	datetime	NULL,
	`mentioned_at`	datetime	NULL
);

ALTER TABLE `feed_comments` ADD CONSTRAINT `PK_FEED_COMMENTS` PRIMARY KEY (
	`id`
);


-- general_partners
CREATE TABLE `general_partners` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`user_id`	varchar(20)	NOT NULL,
	`date_of_birth`	varchar(20)	NULL,
	`applied_date`	datetime	NULL,
	`confirmation_date`	datetime	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL,
	`nickname`	varchar(50)	NULL,
	`year_of_gp_experience`	int	NULL
);

ALTER TABLE `general_partners` ADD CONSTRAINT `PK_GENERAL_PARTNERS` PRIMARY KEY (
	`id`
);


-- limited_partners
CREATE TABLE `limited_partners` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`user_id`	varchar(20)	NOT NULL,
	`union_id`	int	NOT NULL,
	`company_id`	int	NOT NULL,
	`name`	varchar(20)	NULL,
	`signature_img_url`	text	NULL,
	`decision_date`	datetime	NULL,
	`number_of_shares`	int	NULL,
	`income_deduction_applied_date`	int	NULL,
	`confirmation_date`	datetime	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL
);

ALTER TABLE `limited_partners` ADD CONSTRAINT `PK_LIMITED_PARTNERS` PRIMARY KEY (
	`id`
);


-- clicks
CREATE TABLE `clicks` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`click_count`	int	NULL,
	`post_type`	varchar(20)	NOT NULL,
	`post_id`	int	NOT NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL
);

ALTER TABLE `clicks` ADD CONSTRAINT `PK_CLICKS` PRIMARY KEY (
	`id`
);


-- main_post_details
CREATE TABLE `main_post_details` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`html_text`	text	NULL,
	`inobiz_url`	text	NULL,
	`dart_url`	text	NULL,
	`attachment_json`	json	NULL,
	`article_json`	json	NULL
);

ALTER TABLE `main_post_details` ADD CONSTRAINT `PK_MAIN_POST_DETAILS` PRIMARY KEY (
	`id`
);


-- user_types
CREATE TABLE `user_types` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`user_id`	varchar(20)	NOT NULL,
	`type`	varchar(10)	NOT NULL,
	`union_id`	int	NULL
);

ALTER TABLE `user_types` ADD CONSTRAINT `PK_USER_TYPES` PRIMARY KEY (
	`id`
);


-- limited_partner_details
CREATE TABLE `limited_partner_details` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`lp_id`	int	NOT NULL,
	`signature_img_url`	text	NULL,
	`decision_date`	datetime	NULL,
	`total_share_number`	int	NULL,
	`income_deduction_applied_date`	int	NULL,
	`created_at`	datetime	NULL,
	`updated_at`	datetime	NULL
);

ALTER TABLE `limited_partner_details` ADD CONSTRAINT `PK_LIMITED_PARTNER_DETAILS` PRIMARY KEY (
	`id`
);


-- general_partner_careers
CREATE TABLE `general_partner_careers` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`gp_id`	int	NOT NULL,
	`worked_company`	varchar(50)	NULL,
	`worked_position_desciption`	text	NULL,
	`career_start_date`	date	NULL,
	`career_end_date`	date	NULL
);

ALTER TABLE `general_partner_careers` ADD CONSTRAINT `PK_GENERAL_PARTNER_CAREERS` PRIMARY KEY (
	`id`
);


-- general_partner_union_establishment_experiences
CREATE TABLE `general_partner_union_establishment_experiences` (
	`id`	int	NOT NULL AUTO_INCREMENT,
	`gp_id`	int	NOT NULL,
	`union_start_date`	date	NULL,
	`union_end_date`	date	NULL,
	`union_id_certificate_url`	text	NULL,
	`union_investment_certificate_url`	text	NULL
);

ALTER TABLE `general_partner_union_establishment_experiences` ADD CONSTRAINT `PK_GENERAL_PARTNER_UNION_ESTABLISHMENT_EXPERIENCES` PRIMARY KEY (
	`id`
);


-- s3_buckets
CREATE TABLE `s3_buckets` (
	`id`	varchar(100)	NOT NULL,
	`key_prefix`	varchar(255)	NULL,
	`filename`	varchar(255)	NULL,
	`bucket_name`	varchar(255)	NULL,
    `created_at`	datetime	NULL,
	`updated_at`	datetime	NULL
);

ALTER TABLE `s3_buckets` ADD CONSTRAINT `MULTI_PK_S3_BUCKETS` PRIMARY KEY (
	`filename`, `key_prefix`, `bucket_name`
);

CREATE UNIQUE INDEX UNIQUE_ID_S3_BUCKET
On s3_buckets (id);
