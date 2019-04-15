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
-- Table structure for table `especies_seleccionadas`
--

DROP TABLE IF EXISTS `especies_seleccionadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `especies_seleccionadas` (
  `especie` varchar(100) NOT NULL,
  `PTC` int(11) NOT NULL,
  `lncRNA` int(11) NOT NULL,
  `fuente` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especies_seleccionadas`
--

LOCK TABLES `especies_seleccionadas` WRITE;
/*!40000 ALTER TABLE `especies_seleccionadas` DISABLE KEYS */;
INSERT INTO `especies_seleccionadas` VALUES ('Triticum aestivum',107545,38820,'GreeNC'),('Brassica napus',101040,12010,'CantataDB'),('Oryza rufipogon',37071,10261,'CantataDB'),('Trifolium pratense',39917,10179,'CantataDB'),('Physcomitrella patens',32447,9690,'GreeNC'),('Medicago truncatula',50444,9676,'GreeNC'),('Manihot esculenta',33044,9504,'CantataDB'),('Oryza nivara',36313,8955,'CantataDB'),('Brassica rapa',41018,8501,'CantataDB'),('Hordeum vulgare',37705,7970,'CantataDB'),('Arabidopsis lyrata',32667,7593,'CantataDB'),('Cucumis sativus',23780,7348,'CantataDB'),('Brassica oleracea',59220,7338,'CantataDB'),('Oryza barthii',34575,7062,'CantataDB'),('Glycine max',55897,6689,'GreeNC'),('Solanum tuberosum',39021,6680,'GreeNC'),('Corchorus capsularis',29356,6459,'CantataDB'),('Leersia perrieri',29078,6402,'CantataDB'),('Oryza brachyantha',32037,6004,'CantataDB'),('Amborella trichopoda',27313,5698,'GreeNC'),('Brachypodium distachyon',34310,5584,'GreeNC'),('Populus trichocarpa',41335,5569,'GreeNC'),('Sorghum bicolor',34118,5305,'GreeNC'),('Theobroma cacao',29188,5256,'CantataDB'),('Oryza sativa Japonica Group',35821,5237,'GreeNC'),('Solanum lycopersicum',33697,4716,'CantataDB'),('Vitis vinifera',29927,4542,'CantataDB'),('Arabidopsis thaliana',27628,4373,'CantataDB'),('Gossypium raimondii',38208,4216,'GreeNC'),('Setaria italica',35831,4208,'CantataDB');
/*!40000 ALTER TABLE `especies_seleccionadas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-14 21:16:05
