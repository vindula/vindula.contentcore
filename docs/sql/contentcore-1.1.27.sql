use vindula_myvindulaDB;

ALTER TABLE `vindula_myvindulaDB`.`vin_contentcore_forms` ADD COLUMN `uid_form` VARCHAR(255) DEFAULT NULL AFTER `description_form`;