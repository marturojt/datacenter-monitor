-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: monitoreo
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tbMediciones`
--

DROP TABLE IF EXISTS `tbMediciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbMediciones` (
  `idtbMediciones` int(11) NOT NULL AUTO_INCREMENT,
  `temperatura` float NOT NULL,
  `humedad` float NOT NULL,
  `presion` float NOT NULL,
  `altitud` float NOT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`idtbMediciones`)
) ENGINE=InnoDB AUTO_INCREMENT=3084 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tbMetodosBot`
--

DROP TABLE IF EXISTS `tbMetodosBot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbMetodosBot` (
  `idtbMetodosBot` int(11) NOT NULL AUTO_INCREMENT,
  `nombreMetodo` varchar(45) NOT NULL,
  PRIMARY KEY (`idtbMetodosBot`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'monitoreo'
--
/*!50003 DROP PROCEDURE IF EXISTS `spInsertaMediciones` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ajimenez`@`%` PROCEDURE `spInsertaMediciones`( IN xTemp FLOAT, IN xHumi FLOAT, IN xPres FLOAT, IN xAlti FLOAT )
BEGIN

INSERT INTO tbMediciones (temperatura, humedad, presion, altitud) VALUES (xTemp, xHumi, xPres, xAlti);

DELETE FROM tbMediciones WHERE LEFT(timestamp,10) = DATE_SUB(CURDATE(), INTERVAL 30 DAY);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spMetodosBOT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`ajimenez`@`%` PROCEDURE `spMetodosBOT`(IN xMetodo INT)
BEGIN

SELECT
CASE
	WHEN xMetodo = 1 THEN (SELECT ROUND(temperatura,1) as temperatura FROM tbMediciones ORDER BY idtbMediciones DESC LIMIT 1)
    WHEN xMetodo = 2 THEN (SELECT ROUND(AVG(temperatura),1) as temperatura FROM tbMediciones WHERE LEFT(timestamp,10) = curdate())
    WHEN xMetodo = 3 THEN (SELECT ROUND(MAX(temperatura),1) as temperatura FROM tbMediciones WHERE LEFT(timestamp,10) = curdate())
    ELSE "error: método no valido"
END as temperatura,
(SELECT nombreMetodo FROM tbMetodosBot WHERE idtbMetodosBot = xMetodo) as "metodo";
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-14 16:29:31
