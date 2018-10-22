CREATE TABLE `history` (
  `Id` int(11) NOT NULL,
  `uid` VARCHAR(255) NOT NULL,
  `name` varchar(255) DEFAULT '',
  `url_token` varchar(255) DEFAULT NULL,
  `follow_count` varchar(255) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `headline` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `answer_count` varchar(255) DEFAULT NULL,
  `article_count` varchar(255) DEFAULT NULL ,
  `user_type` varchar(255) DEFAULT NULL ,

  PRIMARY KEY (`Id`),
  UNIQUE KEY `url_token` (`url_token`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

