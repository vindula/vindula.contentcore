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
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_contentcore_fields`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_fields` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_fields` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name_field` VARCHAR(45) NOT NULL ,
  `type_fields` VARCHAR(45) NOT NULL ,
  `list_values` TEXT NULL ,
  `date_creation` VARCHAR(45) NOT NULL ,
  `title` VARCHAR(45) NOT NULL ,
  `value_default` TEXT NULL DEFAULT NULL ,
  `description_fields` TEXT NULL DEFAULT NULL ,
  `ordenacao` INT NOT NULL ,
  `required` TINYINT(1)  NULL DEFAULT False ,
  `flag_ativo` TINYINT(1)  NULL DEFAULT True ,
  `forms_id` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vin_contentcore_fields_vin_contentcore_forms1` (`forms_id` ASC) ,
  CONSTRAINT `fk_vin_contentcore_fields_vin_contentcore_forms1`
    FOREIGN KEY (`forms_id` )
    REFERENCES `myvindulaDB`.`vin_contentcore_forms` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


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
-- Table `myvindulaDB`.`vin_contentcore_from_values`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_contentcore_from_values` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_contentcore_from_values` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `value` TEXT NULL DEFAULT NULL ,
  `value_blob` LONGBLOB NULL DEFAULT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `forms_id` INT NOT NULL ,
  `instance_id` INT NOT NULL ,
  `fields` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vin_helpdesk_from_values_vin_helpdesk_forms1` (`forms_id` ASC) ,
  CONSTRAINT `fk_vin_helpdesk_from_values_vin_helpdesk_forms1`
    FOREIGN KEY (`forms_id` )
    REFERENCES `myvindulaDB`.`vin_contentcore_forms` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


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



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

