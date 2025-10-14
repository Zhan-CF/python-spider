/*
 Navicat Premium Dump SQL

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42)
 Source Host           : localhost:3306
 Source Schema         : weibo_topic

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42)
 File Encoding         : 65001

 Date: 13/10/2025 23:52:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for two_comments
-- ----------------------------
DROP TABLE IF EXISTS `two_comments`;
CREATE TABLE `two_comments`  (
  `reply_id` int NOT NULL AUTO_INCREMENT COMMENT '二级评论ID',
  `comment_id` int NOT NULL COMMENT '关联一级评论ID',
  `replier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二级评论人',
  `reply_time` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二级评论时间',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二级评论内容',
  `replier_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二级评论人IP',
  PRIMARY KEY (`reply_id`) USING BTREE,
  INDEX `comment_id`(`comment_id` ASC) USING BTREE,
  CONSTRAINT `two_comments_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `one_comments` (`comment_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '二级评论表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
