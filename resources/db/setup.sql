DROP SCHEMA IF EXISTS `object_detection`;

CREATE SCHEMA IF NOT EXISTS `object_detection`;

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
  PRIMARY KEY (`id`))
;

DROP TABLE IF EXISTS `object_detection`.`image`;

CREATE TABLE IF NOT EXISTS `object_detection`.`image` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `image` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
;

DROP TABLE IF EXISTS `object_detection`.`image_prediction`;

CREATE TABLE IF NOT EXISTS `object_detection`.`image_prediction` (
  `image_id` INT NOT NULL,
  `prediction_id` INT NOT NULL,
  PRIMARY KEY (`image_id`, `prediction_id`),
  CONSTRAINT `img_pred_image`
    FOREIGN KEY (`image_id`)
    REFERENCES `object_detection`.`image` (`id`),
  CONSTRAINT `img_pred_prediction`
    FOREIGN KEY (`prediction_id`)
    REFERENCES `object_detection`.`prediction` (`id`))
;