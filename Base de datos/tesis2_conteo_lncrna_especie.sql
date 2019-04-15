-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: tesis2
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `conteo_lncrna_especie`
--

DROP TABLE IF EXISTS `conteo_lncrna_especie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conteo_lncrna_especie` (
  `especie` varchar(100) NOT NULL,
  `fuente` varchar(45) NOT NULL,
  `conteo` int(11) DEFAULT NULL,
  PRIMARY KEY (`especie`,`fuente`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conteo_lncrna_especie`
--

LOCK TABLES `conteo_lncrna_especie` WRITE;
/*!40000 ALTER TABLE `conteo_lncrna_especie` DISABLE KEYS */;
INSERT INTO `conteo_lncrna_especie` VALUES ('Amborella trichopoda','Ensembl',27152),('Amborella trichopoda','GreeNC',5698),('Arabidopsis lyrata','CantataDB',7593),('Arabidopsis lyrata','Ensembl',32664),('Arabidopsis thaliana','CantataDB',4373),('Arabidopsis thaliana','Ensembl',48321),('Brachypodium distachyon','Ensembl',52972),('Brachypodium distachyon','GreeNC',5584),('Brassica napus','CantataDB',12010),('Brassica napus','Ensembl',101039),('Brassica oleracea','CantataDB',7338),('Brassica oleracea','Ensembl',59220),('Brassica rapa','CantataDB',8501),('Brassica rapa','Ensembl',41025),('Chlamydomonas reinhardtii','Ensembl',19525),('Chondrus crispus','Ensembl',9807),('Corchorus capsularis','CantataDB',6459),('Corchorus capsularis','Ensembl',29356),('Cucumis sativus','CantataDB',7348),('Cucumis sativus','Ensembl',23780),('Galdieria sulphuraria','Ensembl',7174),('Glycine max','Ensembl',88402),('Glycine max','GreeNC',6689),('Gossypium raimondii','Ensembl',78371),('Gossypium raimondii','GreeNC',4216),('Hordeum vulgare','CantataDB',7970),('Hordeum vulgare','Ensembl',234701),('Leersia perrieri','CantataDB',6402),('Leersia perrieri','Ensembl',38960),('Manihot esculenta','CantataDB',9504),('Manihot esculenta','Ensembl',41393),('Medicago truncatula','Ensembl',57581),('Medicago truncatula','GreeNC',9676),('Musa acuminata','Ensembl',36517),('Oryza barthii','CantataDB',7062),('Oryza barthii','Ensembl',41595),('Oryza brachyantha','CantataDB',6004),('Oryza brachyantha','Ensembl',32017),('Oryza nivara','CantataDB',8955),('Oryza nivara','Ensembl',48356),('Oryza punctata','Ensembl',41047),('Oryza rufipogon','CantataDB',10261),('Oryza rufipogon','Ensembl',47421),('Oryza sativa Japonica Group','Ensembl',42246),('Oryza sativa Japonica Group','GreeNC',5237),('Ostreococcus lucimarinus','Ensembl',7603),('Phaseolus vulgaris','Ensembl',32718),('Physcomitrella patens','Ensembl',86669),('Physcomitrella patens','GreeNC',9690),('Populus trichocarpa','Ensembl',73012),('Populus trichocarpa','GreeNC',5569),('Prunus persica','Ensembl',47089),('Selaginella moellendorffii','Ensembl',34825),('Setaria italica','CantataDB',4208),('Setaria italica','Ensembl',41023),('Solanum lycopersicum','CantataDB',4716),('Solanum lycopersicum','Ensembl',34414),('Solanum tuberosum','Ensembl',56210),('Solanum tuberosum','GreeNC',6680),('Sorghum bicolor','Ensembl',47095),('Sorghum bicolor','GreeNC',5305),('Theobroma cacao','CantataDB',5256),('Theobroma cacao','Ensembl',44060),('Trifolium pratense','CantataDB',10179),('Trifolium pratense','Ensembl',41269),('Triticum aestivum','Ensembl',133332),('Triticum aestivum','GreeNC',38820),('Vitis vinifera','CantataDB',4542),('Vitis vinifera','Ensembl',29859),('Zea mays','Ensembl',131400);
/*!40000 ALTER TABLE `conteo_lncrna_especie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-14 21:16:06
