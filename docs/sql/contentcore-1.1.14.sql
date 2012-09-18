use myvinduladb;

ALTER TABLE `myvindulaDB`.`vin_contentcore_fields` ADD COLUMN `flag_multi` TINYINT(1) NULL DEFAULT NULL  AFTER `value_default`, ADD COLUMN `field_ref` VARCHAR(45) NULL DEFAULT NULL  AFTER `value_default` , CHANGE COLUMN `required` `required` TINYINT(1) NULL DEFAULT False  , CHANGE COLUMN `flag_ativo` `flag_ativo` TINYINT(1) NULL DEFAULT True  ;


ALTER TABLE `myvindulaDB`.`vin_contentcore_fields` MODIFY COLUMN `title` TEXT  CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;

