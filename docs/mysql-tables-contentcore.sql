SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `myvindulaDB` DEFAULT CHARACTER SET latin1 ;
USE `myvindulaDB` ;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_forms`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_forms` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_forms` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name_form` VARCHAR(45) NOT NULL ,
  `date_creation` VARCHAR(45) NOT NULL ,
  `description_form` VARCHAR(45) NULL ,
  `campo_label` VARCHAR(45) NULL DEFAULT NULL,
  `campo_chave` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_fields`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_fields` ;

CREATE TABLE  `vin_contentcore_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_field` varchar(45) NOT NULL,
  `type_fields` varchar(45) NOT NULL,
  `list_values` text,
  `date_creation` varchar(45) NOT NULL,
  `title` text NOT NULL,
  `value_default` text,
  `flag_multi` tinyint(1) DEFAULT NULL,
  `field_ref` varchar(45) DEFAULT NULL,
  `description_fields` text,
  `mascara` varchar(45) DEFAULT NULL,
  `ordenacao` int(11) NOT NULL,
  `required` tinyint(1) DEFAULT '0',
  `flag_ativo` tinyint(1) DEFAULT '1',
  `forms_id` int(11) NOT NULL,
  `form_ref` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_contentcore_fields_vin_contentcore_forms1` (`forms_id`),
  KEY `name_field_idx` (`forms_id`,`name_field`) USING BTREE,
  CONSTRAINT `fk_vin_contentcore_fields_vin_contentcore_forms1` FOREIGN KEY (`forms_id`) REFERENCES `vin_contentcore_forms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1



-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_form_instance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_form_instance` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_form_instance` (
  `instance_id` INT NOT NULL AUTO_INCREMENT ,
  `forms_id` INT NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  PRIMARY KEY (`instance_id`, `forms_id`) ,
  INDEX `fk_vin_contentcore_form_instance_vin_contentcore_forms1` (`forms_id` ASC) ,
  CONSTRAINT `fk_vin_contentcore_form_instance_vin_contentcore_forms1`
    FOREIGN KEY (`forms_id` )
    REFERENCES `myvindulaDB`.`vin_contentcore_forms` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_form_values`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_form_values` ;

CREATE TABLE `vin_contentcore_form_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` text,
  `value_blob` longblob,
  `date_creation` datetime NOT NULL,
  `forms_id` int(11) NOT NULL,
  `instance_id` int(11) NOT NULL,
  `fields` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_helpdesk_from_values_vin_helpdesk_forms1` (`forms_id`),
  KEY `fields_idx` (`forms_id`,`instance_id`,`fields`) USING BTREE,
  CONSTRAINT `fk_vin_helpdesk_from_values_vin_helpdesk_forms1` FOREIGN KEY (`forms_id`) REFERENCES `vin_contentcore_forms` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=704 DEFAULT CHARSET=latin1

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_default_value`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_default_value` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_default_value` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `value` TEXT NOT NULL ,
  `lable` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;

INSERT INTO `vin_contentcore_default_value` VALUES (3,'self.context.portal_membership.getAuthenticatedMember().getId()','usuario logado'),(4,'self.context.absolute_url()','url portal'),(5,'import datetime; datetime.datetime.now().strftime("%d-%m-%Y %H:%M")','Data atual');


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_parameters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_parameters` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_parameters` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `forms_id` INT NOT NULL ,
  `fields_id` INT NULL ,
  `parameters` VARCHAR(45) NULL ,
  `value_parameters` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`, `forms_id`) ,
  INDEX `fk_vin_contentcore_parameters_vin_contentcore_forms1` (`forms_id` ASC) ,
  INDEX `fk_vin_contentcore_parameters_vin_contentcore_fields1` (`fields_id` ASC) ,
  CONSTRAINT `fk_vin_contentcore_parameters_vin_contentcore_forms1`
    FOREIGN KEY (`forms_id` )
    REFERENCES `myvindulaDB`.`vin_contentcore_forms` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_vin_contentcore_parameters_vin_contentcore_fields1`
    FOREIGN KEY (`fields_id` )
    REFERENCES `myvindulaDB`.`vin_contentcore_fields` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_log` ;

CREATE TABLE  `myvindulaDB`.`vin_contentcore_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `valor_old` text,
  `valor_new` text,
  `date_creation` datetime NOT NULL,
  `instance_id` int(11) NOT NULL,
  `forms_id` int(11) NOT NULL,
  `fields` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_configImport`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_configImport` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_configImport` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `forms_id` INT(11) NOT NULL ,
  `fields` VARCHAR(45) NOT NULL ,
  `campo_csv` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vin_contentcore_configImport_vin_contentcore_forms1` (`forms_id` ASC) ,
  CONSTRAINT `fk_vin_contentcore_configImport_vin_contentcore_forms1`
    FOREIGN KEY (`forms_id` )
    REFERENCES `myvindulaDB_coop`.`vin_contentcore_forms` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COLLATE = latin1_swedish_ci;




SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
