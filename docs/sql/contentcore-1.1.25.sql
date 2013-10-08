use myvindulaDB;

ALTER TABLE `vindula_myvindulaDB`.`vin_contentcore_log` ADD COLUMN `username` VARCHAR(100) DEFAULT NULL AFTER `valor_new`;
