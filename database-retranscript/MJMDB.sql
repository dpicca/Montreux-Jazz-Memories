-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`interview`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`interview` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `audio` LONGBLOB NOT NULL COMMENT 'audio file path',
  `text` LONGTEXT NOT NULL COMMENT 'text displayed on the app and changeable',
  `transcription` LONGTEXT NOT NULL COMMENT 'original traqnscription made by the app',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`descriptive_metadata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`descriptive_metadata` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name_interviewee` VARCHAR(45) NOT NULL COMMENT 'name of the interviewee',
  `name_interviewer` VARCHAR(45) NULL COMMENT 'name of the interviewer of interviewers',
  `location` VARCHAR(45) NULL COMMENT 'location of the interview',
  `date` DATE NOT NULL,
  `context` VARCHAR(45) NULL COMMENT 'context in which the interview was made\n',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_descriptive_metadata_interview`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`interview` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`segment_text`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`segment_text` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `char_start` INT NOT NULL COMMENT 'starting character of the segment\n',
  `char_stop` INT NOT NULL COMMENT 'ending character of the segment',
  `summary` MEDIUMTEXT NULL COMMENT 'summary of the segment',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_segment_text_interview`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`interview` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ner` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'Named Entity Recognized',
  `entity_name` VARCHAR(45) NOT NULL COMMENT 'name of the entity cited (can be a place, a person, an event, and so on)',
  `entity_link` VARCHAR(100) BINARY NULL COMMENT 'link to the wikipedia page, to a personal website or a particular web page regarding the entity cited',
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`segment_audio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`segment_audio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `timecode_in` TIME NOT NULL COMMENT 'timecode starting the segment',
  `timecode_out` TIME NOT NULL COMMENT 'timecode ending the segment',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_segment_audio_interview`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`interview` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_segment_audio_segment_text`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`segment_text` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tag` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `coding_variable` VARCHAR(45) NOT NULL,
  `keywords` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`technical_metadata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`technical_metadata` (
  `id` INT NOT NULL,
  `file_name` VARCHAR(400) NOT NULL COMMENT 'name of the audio file',
  `file_length` TIME NOT NULL COMMENT 'length of the audio file (retrieved from the media infop file)',
  `format` VARCHAR(45) NOT NULL COMMENT 'format of the audio file (should be wave)',
  `language` VARCHAR(45) NOT NULL,
  `log` BLOB NULL,
  `media_info` BLOB NOT NULL COMMENT 'json file path, containing all the informations extraceted via media info',
  `recording_data` VARCHAR(1000) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_Technical MetaData_Interview10`
    FOREIGN KEY (`id`)
    REFERENCES `mydb`.`interview` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`segment_audio_has_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`segment_audio_has_tag` (
  `segment_audio_id` INT NOT NULL,
  `tag_id` INT NOT NULL,
  `segment_text_id` INT NOT NULL,
  PRIMARY KEY (`segment_audio_id`, `tag_id`, `segment_text_id`),
  INDEX `fk_segment_audio_has_tag_tag1_idx` (`tag_id` ASC),
  INDEX `fk_segment_audio_has_tag_segment_audio1_idx` (`segment_audio_id` ASC),
  INDEX `fk_segment_audio_has_tag_segment_text1_idx` (`segment_text_id` ASC),
  CONSTRAINT `fk_segment_audio_has_tag_segment_audio`
    FOREIGN KEY (`segment_audio_id`)
    REFERENCES `mydb`.`segment_audio` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_segment_audio_has_tag_tag`
    FOREIGN KEY (`tag_id`)
    REFERENCES `mydb`.`tag` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_segment_audio_has_tag_segment_text`
    FOREIGN KEY (`segment_text_id`)
    REFERENCES `mydb`.`segment_text` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`segment_text_has_ner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`segment_text_has_ner` (
  `segment_text_id` INT NOT NULL,
  `ner_id` INT NOT NULL,
  PRIMARY KEY (`segment_text_id`, `ner_id`),
  INDEX `fk_segment_text_has_ner_ner1_idx` (`ner_id` ASC),
  INDEX `fk_segment_text_has_ner_segment_text1_idx` (`segment_text_id` ASC),
  CONSTRAINT `fk_segment_text_has_ner_segment_text`
    FOREIGN KEY (`segment_text_id`)
    REFERENCES `mydb`.`segment_text` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_segment_text_has_ner_ner`
    FOREIGN KEY (`ner_id`)
    REFERENCES `mydb`.`ner` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
