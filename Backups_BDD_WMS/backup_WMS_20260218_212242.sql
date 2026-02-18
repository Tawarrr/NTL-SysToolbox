-- ===========================================
-- SAUVEGARDE DE LA BASE : WMS
-- DATE : 2026-02-18 21:22:42
-- ===========================================

SET FOREIGN_KEY_CHECKS = 0;


-- Table : camions
DROP TABLE IF EXISTS `camions`;
CREATE TABLE `camions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricule` varchar(50) NOT NULL,
  `transporteur_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transporteur_id` (`transporteur_id`),
  CONSTRAINT `camions_ibfk_1` FOREIGN KEY (`transporteur_id`) REFERENCES `transporteurs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `camions` (`id`, `matricule`, `transporteur_id`) VALUES
(17, 'AA-123-AA', 6),
(18, 'BB-456-BB', 6),
(19, 'CC-789-CC', 7),
(20, 'DD-321-DD', 8),
(21, 'EE-654-EE', 8),
(22, 'FF-987-FF', 9),
(23, 'GG-147-GG', 6),
(24, 'HH-258-HH', 7);

-- Table : transporteurs
DROP TABLE IF EXISTS `transporteurs`;
CREATE TABLE `transporteurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `transporteurs` (`id`, `nom`) VALUES
(7, 'Aline'),
(6, 'Antoine'),
(8, 'Jean'),
(9, 'Mary');

SET FOREIGN_KEY_CHECKS = 1;
-- ===========================================
-- FIN DE LA SAUVEGARDE
-- ===========================================
