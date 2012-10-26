
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

