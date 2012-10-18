use myvindulaDB;

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


