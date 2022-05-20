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
-- Table `mydb`.`Interview`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Interview` (
  `idInterview` INT NOT NULL AUTO_INCREMENT,
  `Audio` LONGBLOB NOT NULL,
  `Text` LONGTEXT NOT NULL,
  `Transcription` LONGTEXT NOT NULL,
  PRIMARY KEY (`idInterview`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Descriptive MetaData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Descriptive MetaData` (
  `idDescriptive_MetaData` INT NOT NULL,
  `Name_Interviewee` VARCHAR(45) NOT NULL,
  `Name Interviewer.s` VARCHAR(45) NULL,
  `Location` VARCHAR(45) NULL,
  `Date` DATE NOT NULL,
  `Context` VARCHAR(45) NULL,
  PRIMARY KEY (`idDescriptive_MetaData`),
  CONSTRAINT `fk_Descriptive MetaData_Interview1`
    FOREIGN KEY (`idDescriptive_MetaData`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment Text`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment Text` (
  `idSegmentText` INT NOT NULL AUTO_INCREMENT,
  `Character Start` INT NOT NULL,
  `Character Stop` INT NOT NULL,
  `Summary` MEDIUMTEXT NULL,
  PRIMARY KEY (`idSegmentText`),
  CONSTRAINT `fk_Segment Text_Interview1`
    FOREIGN KEY (`idSegmentText`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`NER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`NER` (
  `idNER` INT NOT NULL AUTO_INCREMENT COMMENT 'Named Entity Recognized',
  `EntityName` VARCHAR(45) NOT NULL,
  `WikipediaPage` VARCHAR(100) BINARY NULL,
  `Type` VARCHAR(45) NULL,
  PRIMARY KEY (`idNER`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment Audio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment Audio` (
  `idSegmentAudio` INT NOT NULL AUTO_INCREMENT,
  `TimeCode In` TIME NOT NULL,
  `TimeCode Out` TIME NOT NULL,
  PRIMARY KEY (`idSegmentAudio`),
  CONSTRAINT `fk_Segment Audio_Interview1`
    FOREIGN KEY (`idSegmentAudio`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Segment Audio_Segment Text1`
    FOREIGN KEY (`idSegmentAudio`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tag` (
  `idTag` INT NOT NULL AUTO_INCREMENT,
  `CodingVariable` VARCHAR(45) NOT NULL,
  `Keywords` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTag`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tag_has_Segment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tag_has_Segment` (
  `idTag` INT NOT NULL,
  `idSegmentAudio` INT NOT NULL,
  `idSegmentText` INT NOT NULL,
  PRIMARY KEY (`idTag`, `idSegmentAudio`, `idSegmentText`),
  INDEX `fk_Audio` (`idSegmentAudio` ASC),
  INDEX `fk_Tag` (`idTag` ASC),
  INDEX `fk_Text` (`idSegmentText` ASC),
  CONSTRAINT `fk_Tag`
    FOREIGN KEY (`idTag`)
    REFERENCES `mydb`.`Tag` (`idTag`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_audio`
    FOREIGN KEY (`idSegmentAudio`)
    REFERENCES `mydb`.`Segment Audio` (`idSegmentAudio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Text`
    FOREIGN KEY (`idSegmentText`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment Text_has_NER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment Text_has_NER` (
  `idSegmentText` INT NOT NULL,
  `idNER` INT NOT NULL,
  PRIMARY KEY (`idSegmentText`, `idNER`),
  INDEX `fk_NER` (`idNER` ASC),
  INDEX `fk_SegmentText` (`idSegmentText` ASC),
  CONSTRAINT `fk_SegmentText`
    FOREIGN KEY (`idSegmentText`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_NER`
    FOREIGN KEY (`idNER`)
    REFERENCES `mydb`.`NER` (`idNER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Technical MetaData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Technical MetaData` (
  `idTechnical_MetaData` INT NOT NULL,
  `FileName` VARCHAR(45) NOT NULL,
  `AudioFile_Length` TIME NOT NULL,
  `Format` VARCHAR(45) NOT NULL,
  `Language` VARCHAR(45) NOT NULL,
  `Log` BLOB NULL,
  `MediaInfo` BLOB NOT NULL,
  `RecordingData` VARCHAR(1000) NULL,
  PRIMARY KEY (`idTechnical_MetaData`),
  CONSTRAINT `fk_Technical MetaData_Interview10`
    FOREIGN KEY (`idTechnical_MetaData`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
