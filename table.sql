# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 10.19.117.230 (MySQL 5.7.21-log)
# Generation Time: 2019-01-08 00:47:32 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table recommend_categorys
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_categorys`;

CREATE TABLE `recommend_categorys` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `level` int(11) NOT NULL DEFAULT '0',
  `father_id` int(11) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_level` (`name`,`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分类表';



# Dump of table recommend_categorys_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_categorys_tags`;

CREATE TABLE `recommend_categorys_tags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `tag_id` varchar(50) NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tagid_categoryid` (`tag_id`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='标签和分类对应表';



# Dump of table recommend_new_videos
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_new_videos`;

CREATE TABLE `recommend_new_videos` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `archive_id` int(11) NOT NULL DEFAULT '0' COMMENT '文章ID',
  `url` varchar(600) NOT NULL DEFAULT '' COMMENT '视频地址',
  `hash_id` varchar(64) DEFAULT '' COMMENT 'url Hash值',
  `duration` int(11) DEFAULT '0' COMMENT '视频长度',
  `width` int(11) DEFAULT '0' COMMENT '宽',
  `height` int(11) DEFAULT '0' COMMENT '高',
  `size` int(11) DEFAULT '0' COMMENT '视频大小',
  `source` varchar(600) DEFAULT '' COMMENT '视频来源',
  `source_id` int(11) DEFAULT '0' COMMENT '源表中id',
  `source_key` varchar(255) DEFAULT '''''' COMMENT '七牛源文件',
  `image` varchar(600) DEFAULT '' COMMENT '视频图片地址',
  `mime` varchar(32) DEFAULT '' COMMENT 'mime 类型',
  `is_tag` int(11) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash_id` (`hash_id`),
  KEY `archive_id_idx` (`archive_id`),
  KEY `hash_id_idx` (`hash_id`),
  KEY `source_id` (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章视频信息 目前只有微头条使用';



# Dump of table recommend_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_tags`;

CREATE TABLE `recommend_tags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='标签表';



# Dump of table recommend_video_info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_video_info`;

CREATE TABLE `recommend_video_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `origin_video_url` varchar(255) NOT NULL DEFAULT '' COMMENT '播放地址',
  `dqd_video_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'dqd地址',
  `af_video_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'af地址',
  `duration` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '时长',
  `video_width` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '视频宽',
  `video_height` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '视频高',
  `origin_thumb_url` varchar(255) NOT NULL DEFAULT '' COMMENT '封面地址',
  `dqd_thumb_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'dqd封面',
  `af_thumb_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'af封面',
  `img_width` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '图片宽',
  `img_height` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '图片高',
  `site` varchar(50) NOT NULL DEFAULT '' COMMENT '站点',
  `play_page_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'page id',
  `publish_time` varchar(50) NOT NULL DEFAULT '' COMMENT '发布时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_origin_url` (`origin_video_url`),
  KEY `idx_af_url` (`af_video_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table recommend_video_play_page
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_video_play_page`;

CREATE TABLE `recommend_video_play_page` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `origin_page_url` varchar(255) NOT NULL DEFAULT '' COMMENT '播放页地址',
  `site` varchar(50) NOT NULL DEFAULT '' COMMENT '站点',
  `seed_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'seed id',
  `publish_time` varchar(50) NOT NULL DEFAULT '' COMMENT '发布时间',
  `author` varchar(50) NOT NULL DEFAULT '' COMMENT '作者',
  `content` varchar(5000) NOT NULL DEFAULT '' COMMENT '正文',
  `view_count` bigint(20) NOT NULL DEFAULT '0',
  `up_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '点赞数',
  `down_count` int(10) unsigned NOT NULL DEFAULT '0',
  `share_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '分享数',
  `comment_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '评论数',
  `video_downloaded` smallint(5) unsigned NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_page_url` (`origin_page_url`(125)),
  KEY `idx_seed` (`seed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table recommend_video_seed
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_video_seed`;

CREATE TABLE `recommend_video_seed` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `nick` varchar(50) NOT NULL DEFAULT '' COMMENT '昵称',
  `user_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'user id',
  `avatar` varchar(255) NOT NULL DEFAULT '' COMMENT '头像地址',
  `hub_url` varchar(512) NOT NULL DEFAULT '' COMMENT 'hub 地址',
  `site` varchar(25) NOT NULL DEFAULT '' COMMENT '站点',
  `last_fetch_time` bigint(20) NOT NULL DEFAULT '0' COMMENT '上次抓取时间',
  `frequency` int(10) unsigned NOT NULL DEFAULT '3600' COMMENT '抓取频率',
  `status` smallint(5) unsigned NOT NULL DEFAULT '1' COMMENT '状态',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_site` (`site`),
  KEY `idx_uid` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table recommend_videos_tags
# ------------------------------------------------------------

DROP TABLE IF EXISTS `recommend_videos_tags`;

CREATE TABLE `recommend_videos_tags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `video_id` int(11) unsigned NOT NULL,
  `archive_id` int(11) DEFAULT NULL COMMENT '文章id',
  `tag_id` int(11) unsigned NOT NULL COMMENT '标签id',
  `weight` decimal(15,14) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `videoid_tagid` (`video_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='视频对应标签表';




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
