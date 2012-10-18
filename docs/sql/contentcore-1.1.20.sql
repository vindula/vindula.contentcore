use myvindulaDB;

ALTER TABLE `myvindulaDB`.`vin_contentcore_forms` ADD COLUMN `campo_label` VARCHAR(45) NULL DEFAULT NULL  AFTER `description_form` , ADD COLUMN `campo_chave` VARCHAR(45) NULL DEFAULT NULL  AFTER `campo_label` ;

ALTER TABLE `myvindulaDB`.`vin_contentcore_fields` ADD COLUMN `form_ref` INT(11) NULL DEFAULT NULL  AFTER `field_ref` ,
												   CHANGE COLUMN `title` `title` VARCHAR(45) NOT NULL  , 
      											   CHANGE COLUMN `required` `required` TINYINT(1) NULL DEFAULT False ,
												   CHANGE COLUMN `flag_ativo` `flag_ativo` TINYINT(1) NULL DEFAULT True ,
												   ADD COLUMN `mascara` VARCHAR(45) NULL DEFAULT NULL  AFTER `description_fields`;


