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
-- Table structure for table `maestra_especies`
--

DROP TABLE IF EXISTS `maestra_especies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maestra_especies` (
  `id_especie` int(11) NOT NULL AUTO_INCREMENT,
  `especie` varchar(100) NOT NULL,
  PRIMARY KEY (`id_especie`)
) ENGINE=MyISAM AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestra_especies`
--

LOCK TABLES `maestra_especies` WRITE;
/*!40000 ALTER TABLE `maestra_especies` DISABLE KEYS */;
INSERT INTO `maestra_especies` VALUES (1,'Aegilops tauschii'),(2,'Amborella trichopoda'),(3,'Ananas comosus'),(4,'Arabidopsis halleri'),(5,'Arabidopsis lyrata'),(6,'Arabidopsis thaliana'),(7,'Beta vulgaris'),(8,'Brachypodium distachyon'),(9,'Brassica napus'),(10,'Brassica oleracea'),(11,'Brassica rapa'),(12,'C.savignyi'),(13,'Caenorhabditis elegans'),(14,'Capsella grandiflora'),(15,'Capsella rubella'),(16,'Carica papaya'),(17,'Chenopodium quinoa'),(18,'Chlamydomonas reinhardtii'),(19,'Chondrus crispus'),(20,'Citrus clementina'),(21,'Citrus sinensis'),(22,'Coccomyxa subellipsoidea C-169'),(23,'Corchorus capsularis'),(24,'Cucumis sativus'),(25,'Cyanidioschyzon merolae'),(26,'Daucus carota'),(27,'Dioscorea rotundata'),(28,'Eucalyptus grandis'),(29,'Eutrema salsugineum'),(30,'Fragaria vesca'),(31,'Fruitfly'),(32,'Galdieria sulphuraria'),(33,'Glycine max'),(34,'Gossypium raimondii'),(35,'Helianthus annuus'),(36,'Hordeum vulgare'),(37,'Human'),(38,'Leersia perrieri'),(39,'Linum usitatissimum'),(40,'Lupinus angustifolius'),(41,'Malus domestica'),(42,'Manihot esculenta'),(43,'Medicago truncatula'),(44,'Micromonas pusilla CCMP1545'),(45,'Micromonas pusilla RCC299'),(46,'Mimulus guttatus'),(47,'Musa acuminata'),(48,'Nicotiana attenuata'),(49,'Oryza barthii'),(50,'Oryza brachyantha'),(51,'Oryza glaberrima'),(52,'Oryza glumipatula'),(53,'Oryza longistaminata'),(54,'Oryza meridionalis'),(55,'Oryza nivara'),(56,'Oryza punctata'),(57,'Oryza rufipogon'),(58,'Oryza sativa Indica Group'),(59,'Oryza sativa Japonica Group'),(60,'Ostreococcus lucimarinus'),(61,'Phaseolus vulgaris'),(62,'Physcomitrella patens'),(63,'Populus trichocarpa'),(64,'Prunus persica'),(65,'Ricinus communis'),(66,'Saccharomyces cerevisiae'),(67,'Selaginella moellendorffii'),(68,'Setaria italica'),(69,'Solanum lycopersicum'),(70,'Solanum tuberosum'),(71,'Sorghum bicolor'),(72,'Spirodela polyrhiza'),(73,'Theobroma cacao'),(74,'Trifolium pratense'),(75,'Triticum aestivum'),(76,'Triticum dicoccoides\r\n'),(77,'Triticum urartu'),(78,'Vigna angularis'),(79,'Vigna radiata'),(80,'Vitis vinifera'),(81,'Volvox carteri'),(82,'Zea mays'),(83,'Zostera marina');
/*!40000 ALTER TABLE `maestra_especies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-14 21:15:51
