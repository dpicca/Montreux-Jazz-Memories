-- MySQL Script generated by MySQL Workbench
-- Mon Apr 18 15:58:08 2022
-- Model: New Model    Version: 1.0
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
  `idInterview` INT NOT NULL,
  `Text` LONGTEXT NOT NULL,
  `Audio` BLOB NOT NULL,
  PRIMARY KEY (`idInterview`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Technical MetaData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Technical MetaData` (
  `idTechnical MetaData` INT NOT NULL,
  `File Name` VARCHAR(45) NOT NULL,
  `Audio File Length` TIME NOT NULL,
  `Quality Control` VARCHAR(45) NOT NULL,
  `Format` VARCHAR(45) NOT NULL,
  `MediaInfo` BLOB NOT NULL,
  `Language` VARCHAR(45) NOT NULL,
  `Transcriptive MetaData_idTranscriptive MetaDatas` INT NOT NULL,
  `Log` BLOB NULL,
  PRIMARY KEY (`idTechnical MetaData`, `Transcriptive MetaData_idTranscriptive MetaDatas`),
  INDEX `fk_Technical MetaData_Transcriptive MetaData1_idx` (`Transcriptive MetaData_idTranscriptive MetaDatas` ASC) VISIBLE,
  CONSTRAINT `fk_Technical MetaData_Transcriptive MetaData1`
    FOREIGN KEY (`Transcriptive MetaData_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Descriptive MetaData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Descriptive MetaData` (
  `idDescriptive MetatData` INT NOT NULL,
  `Name Interviewee.s` VARCHAR(45) NOT NULL,
  `Name Interviewer.s` VARCHAR(45) NULL,
  `Location` VARCHAR(45) NULL,
  `Date` DATE NOT NULL,
  `Context` VARCHAR(45) NULL,
  `Transcriptive MetaData_idTranscriptive MetaDatas` INT NOT NULL,
  PRIMARY KEY (`idDescriptive MetatData`, `Transcriptive MetaData_idTranscriptive MetaDatas`),
  INDEX `fk_Descriptive MetaData_Transcriptive MetaData1_idx` (`Transcriptive MetaData_idTranscriptive MetaDatas` ASC) VISIBLE,
  CONSTRAINT `fk_Descriptive MetaData_Transcriptive MetaData1`
    FOREIGN KEY (`Transcriptive MetaData_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment Text`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment Text` (
  `idSegmentText` INT NOT NULL,
  `Character Start` INT NOT NULL,
  `Character Stop` INT NOT NULL,
  `Summary` MEDIUMTEXT NULL,
  `Transcriptive MetaDatas_idTranscriptive MetaDatas` INT NOT NULL,
  PRIMARY KEY (`idSegmentText`, `Transcriptive MetaDatas_idTranscriptive MetaDatas`),
  INDEX `fk_Segment_Transcriptive MetaDatas1_idx` (`Transcriptive MetaDatas_idTranscriptive MetaDatas` ASC) VISIBLE,
  CONSTRAINT `fk_Segment_Transcriptive MetaDatas1`
    FOREIGN KEY (`Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`NER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`NER` (
  `idNER` INT NOT NULL COMMENT 'Named Entity Recognized',
  `EntityName` VARCHAR(45) NOT NULL,
  `WikipediaPage` VARCHAR(100) BINARY NULL,
  `Type` VARCHAR(45) NULL,
  PRIMARY KEY (`idNER`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment_has_Entity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment_has_Entity` (
  `Segment_idSegment` INT NOT NULL,
  `Entity_idEntity` INT NOT NULL,
  PRIMARY KEY (`Segment_idSegment`, `Entity_idEntity`),
  INDEX `fk_Segment_has_Entity_Entity1_idx` (`Entity_idEntity` ASC) VISIBLE,
  INDEX `fk_Segment_has_Entity_Segment_idx` (`Segment_idSegment` ASC) VISIBLE,
  CONSTRAINT `fk_Segment_has_Entity_Segment`
    FOREIGN KEY (`Segment_idSegment`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Segment_has_Entity_Entity1`
    FOREIGN KEY (`Entity_idEntity`)
    REFERENCES `mydb`.`NER` (`idNER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment Audio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Segment Audio` (
  `idSegment Audio` INT NOT NULL,
  `TimeCode In` TIMESTAMP(2) NOT NULL,
  `TimeCode Out` TIMESTAMP(2) NOT NULL,
  `Transcriptive MetaData_idTranscriptive MetaDatas` INT NOT NULL,
  `Segment Text_idSegmentText` INT NOT NULL,
  `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` INT NOT NULL,
  PRIMARY KEY (`idSegment Audio`, `Transcriptive MetaData_idTranscriptive MetaDatas`, `Segment Text_idSegmentText`, `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`),
  INDEX `fk_Segment Audio_Transcriptive MetaData1_idx` (`Transcriptive MetaData_idTranscriptive MetaDatas` ASC) VISIBLE,
  INDEX `fk_Segment Audio_Segment Text1_idx` (`Segment Text_idSegmentText` ASC, `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` ASC) VISIBLE,
  CONSTRAINT `fk_Segment Audio_Transcriptive MetaData1`
    FOREIGN KEY (`Transcriptive MetaData_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Interview` (`idInterview`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Segment Audio_Segment Text1`
    FOREIGN KEY (`Segment Text_idSegmentText` , `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText` , `Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tag` (
  `idTag` INT NOT NULL,
  `Coding variable` VARCHAR(45) NOT NULL,
  `Keywords` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTag`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tag_has_Segment Audio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tag_has_Segment Audio` (
  `Tag_idTag` INT NOT NULL,
  `Segment Audio_idSegment Audio` INT NOT NULL,
  `Segment Audio_Transcriptive MetaData_idTranscriptive MetaDatas` INT NOT NULL,
  `Segment Audio_Segment Text_idSegmentText` INT NOT NULL,
  `Segment Audio_Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` INT NOT NULL,
  PRIMARY KEY (`Tag_idTag`, `Segment Audio_idSegment Audio`, `Segment Audio_Transcriptive MetaData_idTranscriptive MetaDatas`, `Segment Audio_Segment Text_idSegmentText`, `Segment Audio_Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`),
  INDEX `fk_Tag_has_Segment Audio_Segment Audio1_idx` (`Segment Audio_idSegment Audio` ASC, `Segment Audio_Transcriptive MetaData_idTranscriptive MetaDatas` ASC, `Segment Audio_Segment Text_idSegmentText` ASC, `Segment Audio_Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` ASC) VISIBLE,
  INDEX `fk_Tag_has_Segment Audio_Tag1_idx` (`Tag_idTag` ASC) VISIBLE,
  CONSTRAINT `fk_Tag_has_Segment Audio_Tag1`
    FOREIGN KEY (`Tag_idTag`)
    REFERENCES `mydb`.`Tag` (`idTag`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tag_has_Segment Audio_Segment Audio1`
    FOREIGN KEY (`Segment Audio_idSegment Audio` , `Segment Audio_Transcriptive MetaData_idTranscriptive MetaDatas` , `Segment Audio_Segment Text_idSegmentText` , `Segment Audio_Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Segment Audio` (`idSegment Audio` , `Transcriptive MetaData_idTranscriptive MetaDatas` , `Segment Text_idSegmentText` , `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tag_has_Segment Text`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tag_has_Segment Text` (
  `Tag_idTag` INT NOT NULL,
  `Segment Text_idSegmentText` INT NOT NULL,
  `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` INT NOT NULL,
  PRIMARY KEY (`Tag_idTag`, `Segment Text_idSegmentText`, `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`),
  INDEX `fk_Tag_has_Segment Text_Segment Text1_idx` (`Segment Text_idSegmentText` ASC, `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas` ASC) VISIBLE,
  INDEX `fk_Tag_has_Segment Text_Tag1_idx` (`Tag_idTag` ASC) VISIBLE,
  CONSTRAINT `fk_Tag_has_Segment Text_Tag1`
    FOREIGN KEY (`Tag_idTag`)
    REFERENCES `mydb`.`Tag` (`idTag`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tag_has_Segment Text_Segment Text1`
    FOREIGN KEY (`Segment Text_idSegmentText` , `Segment Text_Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    REFERENCES `mydb`.`Segment Text` (`idSegmentText` , `Transcriptive MetaDatas_idTranscriptive MetaDatas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`SocioDem Data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`SocioDem Data` (
  `idSocioDem Data` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Gender` VARCHAR(45) NULL,
  `Place of Origin` VARCHAR(45) NULL,
  `Place of Residence` VARCHAR(45) NULL,
  `Marital Status` VARCHAR(45) NULL,
  `Profession` VARCHAR(45) NULL,
  PRIMARY KEY (`idSocioDem Data`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Taste and Musical Practice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Taste and Musical Practice` (
  `idTaste and Musical Practice` INT NOT NULL,
  `Music practiced` VARCHAR(45) NULL,
  `Music Taste` VARCHAR(45) NULL,
  `Relation to Music` VARCHAR(45) NULL,
  `Artists (listened to?)` VARCHAR(45) NULL,
  `Musical Performances` VARCHAR(45) NULL,
  `Discussing different festivals` VARCHAR(45) NULL,
  `Festival as  a spectactor` VARCHAR(45) NULL,
  `Musician as a hobby` VARCHAR(45) NULL,
  `Taste and Musical Practicecol` VARCHAR(45) NULL,
  PRIMARY KEY (`idTaste and Musical Practice`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Articulating life spheres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Articulating life spheres` (
  `idArticulating life spheres` INT NOT NULL,
  `Personal organisation (private)` VARCHAR(45) NULL,
  `Personal organisation (professional)` VARCHAR(45) NULL,
  `Compromise (private)` VARCHAR(45) NULL,
  `Compromise (professional)` VARCHAR(45) NULL,
  PRIMARY KEY (`idArticulating life spheres`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Infrastructure use`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Infrastructure use` (
  `idInfrastructure use` INT NOT NULL,
  `MJF monney` VARCHAR(45) NULL,
  `Logistic` VARCHAR(45) NULL,
  `Security` VARCHAR(45) NULL,
  `Bars` VARCHAR(45) NULL,
  `Restaurants` VARCHAR(45) NULL,
  `Festival In & Off` VARCHAR(45) NULL,
  `Rooms` VARCHAR(45) NULL,
  PRIMARY KEY (`idInfrastructure use`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Encounter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Encounter` (
  `idEncounter` INT NOT NULL,
  `Friendship` VARCHAR(45) NULL,
  `Love` VARCHAR(45) NULL,
  `Artist` VARCHAR(45) NULL,
  `Leading to a new activity` VARCHAR(45) NULL,
  PRIMARY KEY (`idEncounter`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Staff Career: Getting In`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Staff Career: Getting In` (
  `idStaff Career: Getting In` INT NOT NULL,
  `antecedent` VARCHAR(45) NULL,
  `Access` VARCHAR(45) NULL,
  `1st impression` VARCHAR(45) NULL,
  PRIMARY KEY (`idStaff Career: Getting In`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Staff Career: current`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Staff Career: current` (
  `idStaff Career: current` INT NOT NULL,
  `roles` VARCHAR(45) NULL,
  `link between activities` VARCHAR(45) NULL,
  `Impression` VARCHAR(45) NULL,
  PRIMARY KEY (`idStaff Career: current`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Activities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Activities` (
)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
