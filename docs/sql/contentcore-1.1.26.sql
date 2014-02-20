-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: vindula_myvindulaDB_homolog
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1

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
-- Table structure for table `vin_myvindula_holerite02`
--

DROP TABLE IF EXISTS `vin_myvindula_holerite02`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_myvindula_holerite02` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `empresa` varchar(42) DEFAULT NULL,
  `cnpj_empresa` varchar(20) DEFAULT NULL,
  `competencia` varchar(7) DEFAULT NULL,
  `matricula` varchar(11) DEFAULT NULL,
  `nome` varchar(42) DEFAULT NULL,
  `data_admissao` varchar(11) DEFAULT NULL,
  `cargo` varchar(26) DEFAULT NULL,
  `setor` varchar(26) DEFAULT NULL,
  `carteira_trabalho` varchar(17) DEFAULT NULL,
  `secao` varchar(6) DEFAULT NULL,
  `dep_ir` varchar(3) DEFAULT NULL,
  `dep_sf` varchar(3) DEFAULT NULL,
  `cpf` varchar(15) DEFAULT NULL,
  `indentidade` varchar(21) DEFAULT NULL,
  `pis` varchar(15) DEFAULT NULL,
  `salario_base` varchar(11) DEFAULT NULL,
  `cod_pagamento` varchar(3) DEFAULT NULL,
  `banco_pag` varchar(26) DEFAULT NULL,
  `agencia` varchar(16) DEFAULT NULL,
  `conta_corrente` varchar(16) DEFAULT NULL,
  `date_creation` datetime NOT NULL,
  `base_fgts` varchar(11) DEFAULT NULL,
  `base_Inss` varchar(11) DEFAULT NULL,
  `base_irrf` varchar(11) DEFAULT NULL,
  `salario_contribuicao` varchar(11) DEFAULT NULL,
  `total_proventos` varchar(11) DEFAULT NULL,
  `total_desconto` varchar(11) DEFAULT NULL,
  `fgts_mes` varchar(11) DEFAULT NULL,
  `valor_liquido` varchar(11) DEFAULT NULL,
  `observacao` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1227 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vin_myvindula_descricao_holerite02`
--

DROP TABLE IF EXISTS `vin_myvindula_descricao_holerite02`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vin_myvindula_descricao_holerite02` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(4) DEFAULT NULL,
  `descricao` varchar(31) DEFAULT NULL,
  `valor` varchar(11) DEFAULT NULL,
  `status` varchar(2) DEFAULT NULL,
  `referencial` varchar(10) DEFAULT NULL,
  `vin_myvindula_holerite02_id` int(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_myvindula_descricao_holerite02_vin_myvindula_holerite021` (`vin_myvindula_holerite02_id`),
  CONSTRAINT `fk_vin_myvindula_descricao_holerite02_vin_myvindula_holerite021` FOREIGN KEY (`vin_myvindula_holerite02_id`) REFERENCES `vin_myvindula_holerite02` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12464 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-19 21:08:42
