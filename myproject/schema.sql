-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: stmtflask
-- ------------------------------------------------------
-- Server version	8.0.32

-- /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
-- /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
-- /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
-- /*!50503 SET NAMES utf8 */;
-- /*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
-- /*!40103 SET TIME_ZONE='+00:00' */;
-- /*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
-- /*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
-- /*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
-- /*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- ----------------------------------------------------------------
-- The commnet only support by '-- '
-- ----------------------------------------------------------------



SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

-- ----------------------------
-- Table structure for tb_test
-- ----------------------------
DROP TABLE IF EXISTS `tb_test`;
CREATE TABLE `tb_test` (
   `idtest` int NOT NULL AUTO_INCREMENT,
   `name` varchar(45) NOT NULL DEFAULT 'unknown',
   `address` varchar(100) NOT NULL DEFAULT 'unkonw',
   `notes` varchar(200) NOT NULL DEFAULT 'unkonw',
   PRIMARY KEY (`idtest`)
 ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of tb_test
-- ----------------------------
insert into `tb_test` values(1,'unkown', '未知', '未知');
insert into `tb_test` values(2,'小泉彩', '东京', '著名AV女优');
insert into `tb_test` values(3,'苍井空', '东京', '著名AV女优');
insert into `tb_test` values(4,'周杰伦', '台湾', '著名歌手');
insert into `tb_test` values(5,'Will Smith', 'USA', 'Actor');
insert into `tb_test` values(6,'Kayden Kross', 'USA', 'Actress');

-- ----------------------------
-- Table structure for tb_student
-- ----------------------------
DROP TABLE IF EXISTS `tb_student`;
CREATE TABLE `tb_student` (
   `student_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Student No',
   `student_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Name',
   `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Self Label',
   `id_card` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ID',
   `age` int DEFAULT NULL COMMENT 'Age',
   `gender` tinyint DEFAULT NULL COMMENT 'Gender，1M，2F',
   `year` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Enrollment Year',
   `create_time` datetime DEFAULT (CURRENT_TIMESTAMP),
   `update_time` datetime DEFAULT (CURRENT_TIMESTAMP),
   PRIMARY KEY (`student_no`) USING BTREE,
   UNIQUE KEY `id_card_UNIQUE` (`id_card`),
   UNIQUE KEY `student_name_UNIQUE` (`student_name`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
-- ----------------------------
-- Records of tb_student
-- ----------------------------
INSERT INTO `tb_student` VALUES ('S001', 'DayRain', '明天会更好！', '450481197804234431', 20, 1, '2020', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S002', '小明同学', NULL, '360830197604012922', 18, 1, '2020', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S003', '小红同学', NULL, '522601199210248092', 20, 2, '1997', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S004', '小李同学', NULL, '53042219880104926X', 20, 1, '2019', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S005', '测试同学', NULL, '140501198111035371', 18, 1, '2020', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S006', '小小', NULL, '220802198107141182', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S007', 'Kayden', NULL, '330183198504077335', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S008', '曾欣彤', NULL, '610701199012217629', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S009', '国姝好', NULL, '350823199102140928', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S010', '钱初露', NULL, '411525198805116966', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_student` VALUES ('S011', '六一帮', NULL, '220112197712157203', 18, 1, '2022', '2020-12-02 00:00:00', '2020-12-02 00:00:00');
-- test id
-- 陆堂诞 450481197804234431
-- 邱谷兰 360830197604012922
-- 郎康焕 522601199210248092
-- 裘诗翠 53042219880104926X
-- 杨儒熙 140501198111035371
-- 章以晴 220802198107141182
-- 房枝迟 330183198504077335
-- 唐静槐 610701199012217629
-- 马南珍 350823199102140928
-- 皮悦欣 411525198805116966
-- 咎梦玉 220112197712157203

-- available id
-- 薛梦菲 44090119760311922X
-- 高先伊 621022199002015237
-- 嵇开梦 360730199110167653
-- 阮琪霏 610582197504156576
-- 贺剑佛 410611198308045737
-- 姚文冲 410327198006137139
-- 元羿谆 451023199010043419
-- 宣芷珊 530926198611154467
-- 危志承 420104198912285551
-- 祁落兴 410927199112015570
-- 咎琅升 610625197909191976
-- 周吉钟 320100198912195637
-- 乐颢锵 211005197607069877
-- 吉灵上 445122198011048058
-- 邹凡睦 623021197501077471
-- 凌寒显 422827199112135538
-- 危觅双 320100197910062940
-- 尹夏瑶 511321198312224288
-- 钟乐儿 511181199105134124
-- 酆诗珊 450421198908219082
-- 顾淳雅 532628198308103753
-- 耿语梦 152530199401036428
-- 梁超南 620800199410081561
-- 芮蒙蒙 652301198112064829


-- ----------------------------
-- Table structure for tb_teacher
-- ----------------------------
DROP TABLE IF EXISTS `tb_teacher`;
CREATE TABLE `tb_teacher`  (
  `teacher_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gender` tinyint NULL DEFAULT NULL COMMENT 'Gender: 1M，2F',
  `create_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  `update_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  PRIMARY KEY (`teacher_no`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_teacher
-- ----------------------------
INSERT INTO `tb_teacher` VALUES ('T001', '李老师', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T002', '吴老师', 2, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T003', '王老师', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T004', '苍井空', 2, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T005', '外星人', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T006', '小泉彩', 2, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T007', 'kiwi', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T008', 'Code', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T009', 'Fxxk', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T010', '毛静枫', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_teacher` VALUES ('T011', '赵婧学', 1, '2023-12-02 00:00:00', '2020-12-02 00:00:00');

-- ----------------------------
-- Table structure for tb_course
-- ----------------------------
DROP TABLE IF EXISTS `tb_course`;
CREATE TABLE `tb_course`  (
  `course_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Course id',
  `course_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Course',
  `teacher_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Teacher',
  `student_num` int NULL DEFAULT NULL COMMENT 'Student num',
  `create_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  `update_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  PRIMARY KEY (`course_no`) USING BTREE,
  CONSTRAINT `fk_course_teacher` FOREIGN KEY (teacher_no) REFERENCES tb_teacher (teacher_no) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_course
-- ----------------------------
INSERT INTO `tb_course` VALUES ('C001', '高等数学（上）', 'T001', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C002', '高等数学（下）', 'T001', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C003', '大学物理', 'T002', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C004', '语文', 'T003', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C005', '数电', 'T004', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C006', '模电', 'T005', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C007', '机电', 'T006', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C008', '美术', 'T007', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C009', '光电', 'T008', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C010', '微积分', 'T009', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C011', '艺术', 'T010', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_course` VALUES ('C012', '音乐', 'T010', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

-- ----------------------------
-- Table structure for tb_score
-- ----------------------------
DROP TABLE IF EXISTS `tb_score`;
CREATE TABLE `tb_score`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID autoincrement',
  `course_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Course no',
  `student_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'student id',
  `score` float NULL DEFAULT NULL COMMENT 'Score',
  `create_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  `update_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `fk_score_course` FOREIGN KEY (course_no) REFERENCES tb_course (course_no) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_score_student` FOREIGN KEY (student_no) REFERENCES tb_student (student_no) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_score
-- ----------------------------
INSERT INTO `tb_score` VALUES (1, 'C001', 'S001', 65, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (2, 'C001', 'S002', 84, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (3, 'C001', 'S003', 35, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (4, 'C001', 'S004', 100, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (5, 'C001', 'S005', 115, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (6, 'C001', 'S006', 125, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (7, 'C001', 'S007', 155, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (8, 'C001', 'S008', 15, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (9, 'C001', 'S009', 6, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (10, 'C001', 'S010', 78, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (11, 'C002', 'S001', 93, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (12, 'C002', 'S002', 76, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (13, 'C002', 'S003', 96, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (14, 'C002', 'S004', 86, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (15, 'C002', 'S005', 37, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (16, 'C002', 'S006', 15, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (17, 'C002', 'S007', 95, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (18, 'C002', 'S008', 85, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (19, 'C002', 'S009', 56, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (20, 'C002', 'S010', 45, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (21, 'C003', 'S001', 76, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (22, 'C003', 'S002', 78, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (23, 'C003', 'S003', 97, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (24, 'C003', 'S004', 74, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (25, 'C003', 'S005', 36, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (26, 'C003', 'S006', 83, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (27, 'C003', 'S007', 86, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (28, 'C003', 'S008', 40, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (29, 'C003', 'S009', 10, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (30, 'C003', 'S010', 39, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (31, 'C004', 'S001', 47, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (32, 'C004', 'S002', 58, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (33, 'C004', 'S003', 69, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (34, 'C004', 'S004', 81, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (35, 'C004', 'S005', 92, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (36, 'C004', 'S006', 103, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (37, 'C004', 'S007', 38, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (38, 'C004', 'S008', 25, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (39, 'C004', 'S009', 85, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (40, 'C004', 'S010', 93, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (41, 'C005', 'S001', 24, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (42, 'C005', 'S002', 92, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (43, 'C005', 'S003', 94, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (44, 'C005', 'S004', 74, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (45, 'C005', 'S005', 83, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (46, 'C005', 'S006', 45, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (47, 'C005', 'S007', 39, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (48, 'C005', 'S008', 48, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (49, 'C005', 'S009', 57, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (50, 'C005', 'S010', 95, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (51, 'C004', 'S001', 46, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (52, 'C004', 'S002', 72, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (53, 'C004', 'S003', 14, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (54, 'C004', 'S004', 91, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (55, 'C004', 'S005', 0, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (56, 'C005', 'S006', 59, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (57, 'C006', 'S007', 65, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (58, 'C007', 'S008', 111, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (59, 'C008', 'S009', 121, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (60, 'C009', 'S010', 124, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (61, 'C007', 'S001', 35, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (62, 'C007', 'S002', 64, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (63, 'C007', 'S003', 75, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (64, 'C007', 'S004', 34, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (65, 'C007', 'S005', 98, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (66, 'C007', 'S006', 97, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (67, 'C007', 'S007', 45, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (68, 'C007', 'S008', 85, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (69, 'C007', 'S009', 75, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (70, 'C007', 'S010', 85, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (71, 'C008', 'S001', 87, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (72, 'C008', 'S002', 67, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (73, 'C008', 'S003', 34, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (74, 'C008', 'S004', 58, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (75, 'C008', 'S005', 93, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (76, 'C008', 'S006', 26, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (77, 'C008', 'S007', 47, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (78, 'C008', 'S008', 69, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (79, 'C008', 'S009', 97, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (80, 'C008', 'S010', 72, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (81, 'C009', 'S001', 94, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (82, 'C009', 'S002', 89, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (83, 'C009', 'S003', 29, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (84, 'C009', 'S004', 68, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (85, 'C009', 'S005', 90, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (86, 'C009', 'S006', 1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (87, 'C009', 'S007', 70, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (88, 'C009', 'S008', 60, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (89, 'C009', 'S009', 50, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (90, 'C009', 'S010', 30, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (91, 'C010', 'S001', 96, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (92, 'C010', 'S002', 84, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (93, 'C010', 'S003', 86, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (94, 'C010', 'S004', 85, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (95, 'C010', 'S005', 95, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (96, 'C010', 'S006', 49, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (97, 'C010', 'S007', 67, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (98, 'C010', 'S008', 58, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (99, 'C010', 'S009', 49, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (100, 'C010', 'S010', 29, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (101, 'C011', 'S001', 19, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (102, 'C011', 'S002', 78, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (103, 'C011', 'S003', 83, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (104, 'C011', 'S004', 68, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (105, 'C011', 'S005', 94, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (106, 'C011', 'S006', -1, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (107, 'C011', 'S007', 98, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (108, 'C011', 'S008', 67, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (109, 'C011', 'S009', 45, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (110, 'C011', 'S010', 92, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

INSERT INTO `tb_score` VALUES (111, 'C012', 'S001', 70, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (112, 'C012', 'S002', 80, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (113, 'C012', 'S003', 90, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (114, 'C012', 'S004', 75, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (115, 'C012', 'S005', 76, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (116, 'C012', 'S006', 94, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (117, 'C012', 'S007', 67, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (118, 'C012', 'S008', 34, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (119, 'C012', 'S009', 82, '2020-12-02 00:00:00', '2020-12-02 00:00:00');
INSERT INTO `tb_score` VALUES (120, 'C012', 'S010', 17, '2020-12-02 00:00:00', '2020-12-02 00:00:00');

-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
   `user_id` int NOT NULL AUTO_INCREMENT,
   `user_type` tinyint DEFAULT NULL COMMENT '1admin，0student',
   `username` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Account name',
   `password` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'password',
   `student_no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'student_No',
   `display_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'display name',
   `status` tinyint NOT NULL DEFAULT '1' COMMENT 'Status，1enabled，2disabled',
   `create_time` datetime DEFAULT (CURRENT_TIMESTAMP),
   `update_time` datetime DEFAULT (CURRENT_TIMESTAMP),
   PRIMARY KEY (`user_id`) USING BTREE,
   UNIQUE KEY `username_UNIQUE` (`username`)
 ) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
-- ----------------------------
-- Records of tb_user
-- Default password: admin/admin
--                   user/user
-- ----------------------------
INSERT INTO `tb_user` VALUES (1, 1, 'admin', 'pbkdf2:sha256:600000$niCdhX16oJGhTUUK$1b82e7ce0574ac99acba5ecd5f4e96c020091a38854fcf8233189a42296a445c', '0', '管理员', 1, '2023-06-17 10:48:24', '2023-06-17 10:48:26');
INSERT INTO `tb_user` VALUES (2, 1, 'user', 'pbkdf2:sha256:600000$sZ6nWXm79fRegWWy$8fd2786398657c64aad2f29e8019525ef4eb926a299addc6adb20162ff153b04', 'user', '管理员user', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (3, 0, 'user1', 'pbkdf2:sha256:600000$BMWxPKxMJD2EUgT5$f8a088284e0d2ecfd52223ead5672db2cb01431cd9f879793cd26bfe9d2ee979', 'S001', 'S001', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (4, 0, 'user2', 'pbkdf2:sha256:600000$xUmzHPcbg37YswfI$c7bc0c5842733010aabe61528ecd6999af0c80f25933beb01644fbe71a48267f', 'S002', 'S002', 2, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (5, 0, 'user3', 'pbkdf2:sha256:600000$OxnAFDigvUEoGl8p$7e8c6249fefed3717372b1c4f938326b7f603121c7e21a5b235a14de19b419fe', 'S003', 'S003', 2, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (6, 0, 'user4', 'pbkdf2:sha256:600000$8k8mf8kAchySTSWa$f37e28be03bb99542632bc1c9c9d97c694a048eb708f9528b001bac03a932cd9', 'S004', 'S004', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (7, 0, 'user5', 'pbkdf2:sha256:600000$H50P7fJNkl5sFUOO$c9022f80b032877a792da18fc791f5dd3dee73e5a66202dcb5e543fc1393ea85', 'S005', 'S005', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (8, 0, 'user6', 'pbkdf2:sha256:600000$C6vSedX66mHjP1lH$33e89bddea9426765114bc5eeb7aef6c542899a422996f961cefa3b0465be9ba', 'S006', 'S006', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (9, 0, 'user7', 'pbkdf2:sha256:600000$W9vBwCyGzy0stJN4$79a1d0492402806e7a9d9a0eda97896392600b2b6f4cae414ab206679ee0737b', 'S007', 'S007', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (10, 0, 'user8', 'pbkdf2:sha256:600000$cKtvAu5CuEnxJO7l$07ee3413ea7ac69aa30e56e67cb922763d7bc19ec66319406f6cb1422bd72cad', 'S008', 'S008', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (11, 0, 'user9', 'pbkdf2:sha256:600000$BmH4aQNUnnudV4AJ$18502fee17b6c7fda67c1aa26c68ef9220b055db2bc4fb569f78ab5a04a4413e', 'S009', 'S009', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (12, 0, 'user10', 'pbkdf2:sha256:600000$A0IiQ0eEVK7oDelc$7a91bbfa9f05738a4d1bf172a45bf8c4855efc48cf096d8da70f834f990cfc68', 'S010', 'S010', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');
INSERT INTO `tb_user` VALUES (13, 0, 'user11', 'pbkdf2:sha256:600000$mOWJbmKOwhBBK2yh$5862454d98ae5a8b83023f2f5816fafb1f46908932a3f17591841b5957572fcd', 'S011', 'S011', 1, '2023-06-17 00:00:00', '2023-06-17 00:00:00');


-- ----------------------------
-- Table structure for tb_login_history
-- ----------------------------
DROP TABLE IF EXISTS `tb_login_history`;
CREATE TABLE `tb_login_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `ip` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT (CURRENT_TIMESTAMP),
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `fk_login-history_user` FOREIGN KEY (user_id) REFERENCES tb_user (user_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_login_history
-- ----------------------------
INSERT INTO `tb_login_history` VALUES (3, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (4, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (5, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (6, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (7, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (8, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (9, 1, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');
INSERT INTO `tb_login_history` VALUES (10, 7, '0:0:0:0:0:0:0:1', '2020-12-02 00:00:00');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

