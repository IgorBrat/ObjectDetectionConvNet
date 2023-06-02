DROP TABLE IF EXISTS `object_detection`.`prediction`;

CREATE TABLE IF NOT EXISTS `object_detection`.`prediction` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `left_coord` INT NOT NULL,
  `top_coord` INT NOT NULL,
  `right_coord` INT NOT NULL,
  `bottom_coord` INT NOT NULL,
  `confidence` FLOAT(3) NOT NULL,
  `class` VARCHAR(20) NOT NULL,
  `depth` FLOAT(3) NOT NULL,
  `image` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
;