-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Cliente` (
  `cpf` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `dataNasc` DATE NOT NULL,
  `endereço` VARCHAR(100) NULL,
  `qtdeCartao` INT NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Cartao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Cartao` (
  `numCartao` INT NOT NULL,
  `vencimento` DATE NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `saldo` DOUBLE NULL,
  `codSeguranca` INT NOT NULL,
  `Cliente_cpf` INT NOT NULL,
  PRIMARY KEY (`numCartao`, `Cliente_cpf`),
  INDEX `fk_Cartao_Cliente_idx` (`Cliente_cpf` ASC),
  CONSTRAINT `fk_Cartao_Cliente`
    FOREIGN KEY (`Cliente_cpf`)
    REFERENCES `mydb`.`Cliente` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`movimentacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`movimentacao` (
  `id` INT NOT NULL,
  `data` DATE NULL,
  `valor` DOUBLE NULL,
  `Cartao_numCartao` INT NOT NULL,
  `Cartao_Cliente_cpf` INT NOT NULL,
  PRIMARY KEY (`id`, `Cartao_numCartao`, `Cartao_Cliente_cpf`),
  INDEX `fk_movimentacao_Cartao1_idx` (`Cartao_numCartao` ASC, `Cartao_Cliente_cpf` ASC),
  CONSTRAINT `fk_movimentacao_Cartao1`
    FOREIGN KEY (`Cartao_numCartao` , `Cartao_Cliente_cpf`)
    REFERENCES `mydb`.`Cartao` (`numCartao` , `Cliente_cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`extrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`extrato` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `data` DATETIME NOT NULL,
  `saldo` DOUBLE NOT NULL,
  `Cartao_numCartao` INT NOT NULL,
  `Cartao_Cliente_cpf` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_extrato_Cartao1_idx` (`Cartao_numCartao` ASC, `Cartao_Cliente_cpf` ASC),
  CONSTRAINT `fk_extrato_Cartao1`
    FOREIGN KEY (`Cartao_numCartao` , `Cartao_Cliente_cpf`)
    REFERENCES `mydb`.`Cartao` (`numCartao` , `Cliente_cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
