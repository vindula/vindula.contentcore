-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_contentcore_fields`
--

DROP TABLE IF EXISTS `vin_contentcore_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_contentcore_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_field` varchar(45) NOT NULL,
  `type_fields` varchar(45) NOT NULL,
  `list_values` text,
  `date_creation` varchar(45) NOT NULL,
  `title` varchar(45) NOT NULL,
  `value_default` text,
  `description_fields` text,
  `ordenacao` int(11) NOT NULL,
  `required` tinyint(1) DEFAULT '0',
  `flag_ativo` tinyint(1) DEFAULT '1',
  `forms_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_contentcore_fields_vin_contentcore_forms1` (`forms_id`),
  CONSTRAINT `fk_vin_contentcore_fields_vin_contentcore_forms1` FOREIGN KEY (`forms_id`) REFERENCES `vin_contentcore_forms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_contentcore_fields`
--

LOCK TABLES `vin_contentcore_fields` WRITE;
/*!40000 ALTER TABLE `vin_contentcore_fields` DISABLE KEYS */;
INSERT INTO `vin_contentcore_fields` VALUES (4,'nome','text','','2011-12-19 09:46:11','Nome do usuario',NULL,'digite o nome do usuário',0,0,1,3),(5,'endereco','text','','2011-12-19 10:47:16','Endereço do usuario - aqui',NULL,'digite o endereço do usuário',1,1,1,3);
/*!40000 ALTER TABLE `vin_contentcore_fields` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:15:20
-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_contentcore_form_instance`
--

DROP TABLE IF EXISTS `vin_contentcore_form_instance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_contentcore_form_instance` (
  `instance_id` int(11) NOT NULL AUTO_INCREMENT,
  `forms_id` int(11) NOT NULL,
  `date_creation` datetime NOT NULL,
  PRIMARY KEY (`instance_id`,`forms_id`),
  KEY `fk_vin_contentcore_form_instance_vin_contentcore_forms1` (`forms_id`),
  CONSTRAINT `fk_vin_contentcore_form_instance_vin_contentcore_forms1` FOREIGN KEY (`forms_id`) REFERENCES `vin_contentcore_forms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_contentcore_form_instance`
--

LOCK TABLES `vin_contentcore_form_instance` WRITE;
/*!40000 ALTER TABLE `vin_contentcore_form_instance` DISABLE KEYS */;
INSERT INTO `vin_contentcore_form_instance` VALUES (2,3,'2011-12-19 11:15:41'),(9,3,'2011-12-21 09:42:16'),(10,3,'2011-12-21 09:45:19'),(11,3,'2011-12-21 09:46:47'),(12,3,'2011-12-21 09:53:07'),(13,3,'2011-12-21 09:53:56');
/*!40000 ALTER TABLE `vin_contentcore_form_instance` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:15:20
-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_contentcore_forms`
--

DROP TABLE IF EXISTS `vin_contentcore_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_contentcore_forms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_form` varchar(45) NOT NULL,
  `date_creation` varchar(45) NOT NULL,
  `description_form` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_contentcore_forms`
--

LOCK TABLES `vin_contentcore_forms` WRITE;
/*!40000 ALTER TABLE `vin_contentcore_forms` DISABLE KEYS */;
INSERT INTO `vin_contentcore_forms` VALUES (3,'formulário cadastro','2011-12-16 18:38:30','formulário cadastro para teste do vindula');
/*!40000 ALTER TABLE `vin_contentcore_forms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:15:20
-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_contentcore_default_value`
--

DROP TABLE IF EXISTS `vin_contentcore_default_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_contentcore_default_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` text NOT NULL,
  `lable` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_contentcore_default_value`
--

LOCK TABLES `vin_contentcore_default_value` WRITE;
/*!40000 ALTER TABLE `vin_contentcore_default_value` DISABLE KEYS */;
INSERT INTO `vin_contentcore_default_value` VALUES (3,'self.context.portal_membership.getAuthenticatedMember().getId()','usuario logado'),(4,'self.context.absolute_url()','url portal');
/*!40000 ALTER TABLE `vin_contentcore_default_value` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:15:20
-- MySQL dump 10.13  Distrib 5.1.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myvindulaDB
-- ------------------------------------------------------
-- Server version	5.1.41-3ubuntu12.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `vin_contentcore_from_values`
--

DROP TABLE IF EXISTS `vin_contentcore_from_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_contentcore_from_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` text,
  `value_blob` longblob,
  `date_creation` datetime NOT NULL,
  `forms_id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `fields` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_helpdesk_from_values_vin_helpdesk_forms1` (`forms_id`),
  CONSTRAINT `fk_vin_helpdesk_from_values_vin_helpdesk_forms1` FOREIGN KEY (`forms_id`) REFERENCES `vin_contentcore_forms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin_contentcore_from_values`
--

LOCK TABLES `vin_contentcore_from_values` WRITE;
/*!40000 ALTER TABLE `vin_contentcore_from_values` DISABLE KEYS */;
INSERT INTO `vin_contentcore_from_values` VALUES (17,'mau mau maum amua KKKKKKK',NULL,'2011-12-21 09:42:16',3,9,'endereco'),(18,'maumau',NULL,'2011-12-21 09:42:16',3,9,'nome'),(21,'mau mau maum amua KKKKKKK',NULL,'2011-12-21 09:46:47',3,11,'endereco'),(22,'cesar',NULL,'2011-12-21 09:46:47',3,11,'nome'),(23,'tes tetetet mau maumau',NULL,'2011-12-21 09:53:07',3,12,'endereco'),(24,'cesar',NULL,'2011-12-21 09:53:07',3,12,'nome'),(25,'asmdkadjksdjkdmsakdm',NULL,'2011-12-21 09:53:56',3,13,'endereco'),(26,'jef jjeff',NULL,'2011-12-21 09:53:56',3,13,'nome');
/*!40000 ALTER TABLE `vin_contentcore_from_values` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-12-23 10:15:20
