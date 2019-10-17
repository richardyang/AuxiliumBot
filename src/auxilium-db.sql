CREATE TABLE `users` (
  `id` INT NOT NULL DEFAULT 0,
  `level` INT NULL DEFAULT 0,
  `exp` INT NULL DEFAULT 0,
  `points` INT NULL DEFAULT 0,
  PRIMARY KEY (`id` ASC)
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `transactions` (
  `src_id` INT NULL DEFAULT 0,
  `dest_id` INT NULL DEFAULT 0,
  `src_pts` INT NULL DEFAULT 0,
  `dest_pts` INT NULL DEFAULT 0,
  `amount` INT NULL DEFAULT 0,
  `ts` TIMESTAMP NULL DEFAULT '00-00-00 00:00:00'
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `gametime` (
  `user_id` INT NULL DEFAULT 0,
  `app_id` VARCHAR(5000) NULL DEFAULT NULL,
  `played` INT NULL DEFAULT 0
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `users_awards` (
  `user_id` INT NULL DEFAULT 0,
  `award_id` VARCHAR(5000) NULL DEFAULT NULL
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `awards` (
  `award_id` VARCHAR(1000) NOT NULL,
  `award_img` VARCHAR(5000) NULL DEFAULT NULL,
  PRIMARY KEY (`award_id` ASC)
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `users_awards_primary` (
  `user_id` INT NOT NULL DEFAULT 0,
  `award_id` VARCHAR(5000) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id` ASC)
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `October_2019` (
  `id` INT NOT NULL DEFAULT 0,
  `exp_this_month` INT NULL DEFAULT 0,
  `points_this_month` INT NULL DEFAULT 0,
  PRIMARY KEY (`id` ASC)
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
CREATE TABLE `battle` (
  `user_id` INT NOT NULL DEFAULT 0,
  `class` VARCHAR(5000) NULL DEFAULT NULL,
  `wins` INT NULL DEFAULT 0,
  `losses` INT NULL DEFAULT 0,
  `pvp` INT NULL DEFAULT '',
  PRIMARY KEY (`user_id` ASC)
) DEFAULT CHARSET=utf8 ENGINE=InnoDB;
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (83607236668030976,15,31771,8315);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (113457284708843520,3,1276,3932);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (117819770778157056,7,7520,2990);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (137812388614373376,4,2032,40);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (138491187370786816,1,86,24);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (177571103110070282,6,4829,5288);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (197056064636715009,13,25121,2389);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (198269517007159296,6,4860,125);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (198314980355866624,3,1239,709);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (199390635017502720,1,296,112);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (249721325600505858,1,193,71);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (261954705339449344,7,6813,46078);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (271427590927941634,1,45,20);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (288097695711625216,1,0,10);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (295416063552651266,7,8240,7301);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (364930858198499328,1,219,9719);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (365742362158301186,1,16,19);
INSERT INTO `users` (`id`,`level`,`exp`,`points`) VALUES (377012775404306445,1,0,5);
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,261954705339449344,21226,3229,69,'2019-10-06 18:49:46.885264');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (197056064636715009,117819770778157056,20348,4638,69,'2019-10-08 19:26:07.304677');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (117819770778157056,364930858198499328,4807,7,4707,'2019-10-08 19:30:31.964030');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (117819770778157056,364930858198499328,100,4714,100,'2019-10-08 19:30:44.617040');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,137812388614373376,35567,46,10000,'2019-10-08 19:57:43.917715');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,137812388614373376,25762,78,10000,'2019-10-08 19:58:32.677725');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,137812388614373376,11633,154,10000,'2019-10-08 19:59:48.025009');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (197056064636715009,198269517007159296,22641,165,1000,'2019-10-08 23:24:46.626276');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (197056064636715009,177571103110070282,24438,814,5000,'2019-10-11 00:31:28.597091');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (117819770778157056,364930858198499328,347,4824,100,'2019-10-11 19:00:54.561951');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (117819770778157056,364930858198499328,247,4924,247,'2019-10-11 19:01:06.141059');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (197056064636715009,117819770778157056,21166,0,5000,'2019-10-11 19:02:30.008179');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (117819770778157056,364930858198499328,4500,5171,4500,'2019-10-11 19:04:05.652953');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (295416063552651266,198269517007159296,9090,200,100,'2019-10-13 06:07:18.200463');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,261954705339449344,25493,10092,10023,'2019-10-14 18:47:58.130498');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,197056064636715009,11548,6554,11479,'2019-10-14 19:19:39.527410');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (197056064636715009,261954705339449344,18033,20645,18033,'2019-10-14 19:19:55.536952');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (198269517007159296,261954705339449344,3825,38855,3825,'2019-10-14 21:17:14.993159');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,113457284708843520,3442,70,3000,'2019-10-15 06:07:36.537864');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,295416063552651266,7784,7632,1,'2019-10-16 21:30:22.212601');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (83607236668030976,261954705339449344,7783,43844,1000,'2019-10-16 21:30:44.388895');
INSERT INTO `transactions` (`src_id`,`dest_id`,`src_pts`,`dest_pts`,`amount`,`ts`) VALUES (198269517007159296,261954705339449344,910,44936,910,'2019-10-16 21:48:40.656236');
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'VmlzdWFsIFN0dWRpbyBDb2Rl',2733);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'U2xheSB0aGUgU3BpcmU=',21);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'VGhlIEVsZGVyIFNjcm9sbHMgT25saW5l',2126);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199369399923113984,'QXBleCBMZWdlbmRz',2439);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (194529228446760960,'V29ybGQgb2YgV2FyY3JhZnQgQ2xhc3NpYw==',6150);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'U3BvdGlmeQ==',314);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (141333417311600640,'U3BvdGlmeQ==',353);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'U3RhckNyYWZ0IElJ',325);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'U3BvdGlmeQ==',638);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'QXBleCBMZWdlbmRz',290);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'U1RBUiBXQVJTIEJhdHRsZWZyb250IElJ',44);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'TGVhZ3VlIG9mIExlZ2VuZHM=',2533);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'Q2xvbmUgSGVybw==',183);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (364930858198499328,'R3VpbGQgV2FycyAy',3198);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'RklOQUwgRkFOVEFTWSBYSVY=',764);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (107702794168832000,'R3VpbGQgV2FycyAy',1580);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (113457284708843520,'TGVhZ3VlIG9mIExlZ2VuZHM=',2405);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (222401312753451008,'V29ybGQgb2YgV2FyY3JhZnQgQ2xhc3NpYw==',3982);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (233039835374288896,'Rm9ydG5pdGU=',2481);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'R29vZ2xlIENocm9tZQ==',850);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (118852276642250752,'U01JVEU=',927);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (216690878671093762,'U3BvdGlmeQ==',2846);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (326776364516507649,'QXBleCBMZWdlbmRz',1640);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'TGVhZ3VlIG9mIExlZ2VuZHM=',1596);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (194529228446760960,'SGVyb2VzIG9mIHRoZSBTdG9ybQ==',160);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (177571103110070282,'TGVhZ3VlIG9mIExlZ2VuZHM=',3733);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'R0YgU2ltdWxhdG9y',6951);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'TGVhZ3VlIG9mIExlZ2VuZHM=',1419);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122401478311804930,'U3BvdGlmeQ==',550);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (177571103110070282,'U01JVEU=',416);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (249721325600505858,'TGVmdCA0IERlYWQgMg==',134);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'U3BvdGlmeQ==',1851);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (203551703524573185,'U3BvdGlmeQ==',945);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (315250339773415424,'R3VpbGQgV2FycyAy',785);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'V29ybGQgb2YgV2FyY3JhZnQgQ2xhc3NpYw==',238);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'U3BvdGlmeQ==',159);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'RklGQSAxNw==',73);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'SGVyb2VzIG9mIHRoZSBTdG9ybQ==',2470);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'QXBleCBMZWdlbmRz',84);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (307563693351370752,'TmV2ZXIgU3BsaXQgdGhlIFBhcnR5',276);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'Rm9yemEgSG9yaXpvbiA0',140);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'RGF1bnRsZXNz',650);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (115682216952070151,'Rm9ydG5pdGU=',1295);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (107702794168832000,'RGVhZCBieSBEYXlsaWdodA==',241);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'QVNUUk9ORUVS',1142);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (164125035156602881,'R3VpbGQgV2FycyAy',1066);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (222401312753451008,'V29ybGQgb2YgV2FyY3JhZnQ=',6);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'Rm9vdGJhbGwgTWFuYWdlciAyMDE5IERlbW8=',451);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'TWluZWNyYWZ0',715);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (307563693351370752,'Um9ja2V0IExlYWd1ZQ==',328);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'Q291bnRlci1TdHJpa2U6IEdsb2JhbCBPZmZlbnNpdmU=',640);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (177571103110070282,'TUlORE5JR0hU 167',53);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (314380659865157642,'R3VpbGQgV2FycyAy 100',81);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (233039835374288896,'VG90YWwgV2FyOiBUSFJFRSBLSU5HRE9NUw== 124',1550);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'VG90YWwgV2FyOiBUSFJFRSBLSU5HRE9NUw== 258',16);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'U3BvdGlmeQ== 164',241);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'V2FyY3JhZnQgSUlJ 245',1522);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (213408803125854208,'R2hvc3QgUmVjb24gQnJlYWtwb2ludA== 27',3385);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (205472713228288001,'R3VpbGQgV2FycyAy 191',55);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'TWluZWNyYWZ0 242',51);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'U3RlbGxhcmlz 36',293);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199369399923113984,'TGVhZ3VlIG9mIExlZ2VuZHM= 204',272);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'TVRHQXJlbmE= 153',56);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'TVRHOiBBcmVuYQ== 82',28);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (255054748175040513,'R3JhbmQgVGhlZnQgQXV0byBW 116',212);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (113457284708843520,'RmFjdG9yaW8= 95',2897);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'Q09ERSBWRUlO 126',529);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'VG9tIENsYW5jeSdzIFJhaW5ib3cgU2l4IFNpZWdl 138',213);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (237345248664092672,'RGVzdGlueSAy 112',918);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (107702794168832000,'T3V0bGFzdA== 199',38);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'U3BvdGlmeQ== 294',231);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 111',175);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 33',421);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'RGVzdGlueSAy 164',2283);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 211',148);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 268',454);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (115682216952070151,'VG90YWwgV2FyOiBUSFJFRSBLSU5HRE9NUw== 44',812);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (118852276642250752,'Q291bnRlci1TdHJpa2U6IEdsb2JhbCBPZmZlbnNpdmU= 57',158);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'RGVzdGlueSAy 259',1539);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'SGVhcnRoc3RvbmU= 141',581);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'RGVzdGlueSAy 178',333);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'UHVtbWVsIFBhcnR5 35',305);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'UHVtbWVsIFBhcnR5 42',159);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'SEVMTEZJUkU= 106',246);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (307019137622736896,'RGVzdGlueSAy 242',606);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'T0xEVFY= 148',6);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (307019137622736896,'Uk9CTE9Y 105',1516);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'SSBMb3ZlIFlvdSwgQ29sb25lbCBTYW5kZXJzISBBIEZpbmdlciBMaWNraW7igJkgR29vZCBEYXRpbmcgU2ltdWxhdG9y 129',11698);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'QVNUUk9ORUVS 50',312);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (314380659865157642,'TVRHQXJlbmE= 201',10);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (314380659865157642,'TVRHOiBBcmVuYQ== 248',514);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'UmFpbmJvdyBTaXggU2llZ2U= 23',19);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'Q291bnRlci1TdHJpa2U6IEdsb2JhbCBPZmZlbnNpdmU= 154',69);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'U3RhdGUgb2YgRGVjYXkgMg== 140',2);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (198314980355866624,'REFSSyBTT1VMUyBJSUk= 176',501);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'U3RhciBDaXRpemVu 208',1);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (83607236668030976,'U3RhckNyYWZ0IElJ 39',22);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'RGVzdGlueSAy 223',2264);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199390635017502720,'VGVhbSBGb3J0cmVzcyAy 238',223);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'RGVzdGlueSAy 282',836);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'Q3ViZSBXb3JsZA== 41',3);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'R2hvc3QgUmVjb24gQnJlYWtwb2ludA== 215',514);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'R2hvc3QgUmVjb27CriBCcmVha3BvaW50 258',574);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (408780025022906369,'RGVhZCBieSBEYXlsaWdodA== 30',80);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'R3VpbGQgV2FycyAy 206',40);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (377012775404306445,'U3BvdGlmeQ== 186',633);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (377012775404306445,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 245',255);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (249721325600505858,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 172',77);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'TGVmdCA0IERlYWQgMg== 129',55);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (377012775404306445,'b3N1IQ== 273',20);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (281166591515820032,'TGVhZ3VlIG9mIExlZ2VuZHM= 12',45);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (118852276642250752,'TWluZWNyYWZ0IDEuMTIuMg== 90',118);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (288097695711625216,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 36',94);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (150261891699179520,'UE9TVEFMIFJlZHV4 167',122);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (271427590927941634,'U3BvdGlmeQ== 274',59);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (315250339773415424,'QW5hcmNoeSBPbmxpbmU= 52',1053);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (288097695711625216,'Um9ja2V0IExlYWd1ZQ== 250',895);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'Qm9yZGVybGFuZHMgMw== 124',42);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'QXBleCBMZWdlbmRz 130',81);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (174278530056716298,'U3BvdGlmeQ== 191',25);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'RGVzdGlueSAy 237',584);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (115682216952070151,'TGVhZ3VlIG9mIExlZ2VuZHM= 287',239);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (377012775404306445,'T3ZlcndhdGNo 183',144);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (198314980355866624,'SGFsbyBXYXJzOiBEZWZpbml0aXZlIEVkaXRpb24= 209',58);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (377012775404306445,'Um9ja2V0IExlYWd1ZQ== 158',156);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (295416063552651266,'R3VpbGQgV2Fycw== 288',5);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'Qmx1ZVN0YWNrcw== 46',5);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'U2thdGVyIFhM 130',5);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (354101490245173248,'TWFwbGVTdG9yeQ== 68',1463);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199369399923113984,'Q3Jvc3NGaXJl 191',43);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'b3N1IQ== 155',1);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (314380659865157642,'VG90YWwgV2FyOiBXQVJIQU1NRVIgSUk= 59',437);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (122613995638095872,'QWltIExhYg== 137',15);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (198314980355866624,'Q291bnRlci1TdHJpa2U6IEdsb2JhbCBPZmZlbnNpdmU= 183',83);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (213408803125854208,'RGVzdGlueSAy 141',471);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (197056064636715009,'UHVtbWVsIFBhcnR5 50',72);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'UHVtbWVsIFBhcnR5 236',70);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 220',100);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (198314980355866624,'R29sZiBXaXRoIFlvdXIgRnJpZW5kcw== 21',73);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'V2FsbHBhcGVyIEVuZ2luZQ== 99',137);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'R3VpbGQgV2FycyAz 184',379);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (113457284708843520,'Tm9SZWxvYWQgSGVyb2Vz 234',6);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (261954705339449344,'RGlhYmxv 199',7);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (249721325600505858,'Q291bnRlci1TdHJpa2U6IEdsb2JhbCBPZmZlbnNpdmU= 38',97);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (249721325600505858,'UHVtbWVsIFBhcnR5 188',69);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (249721325600505858,'TGVhZ3VlIG9mIExlZ2VuZHM= 167',81);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (213408803125854208,'R2FycnkncyBNb2Q= 193',545);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'VmluZGljdHVz 283',317);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199369399923113984,'VEVSQQ== 21',5);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (199369399923113984,'U291bFdvcmtlcg== 17',102);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'TGVhZ3VlIG9mIExlZ2VuZHM= 214',233);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (307563693351370752,'R3VpbGQgV2FycyAy 116',1);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (354101490245173248,'RGlhYmxvIElJSQ== 51',4);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (117819770778157056,'S292YWFLJ3MgRlBTIEFpbSBUcmFpbmVy 149',2);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'Rm9ydG5pdGU= 56',37);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (90543954625323008,'TGVnZW5kcyBvZiBSdW5ldGVycmE= 3',69);
INSERT INTO `gametime` (`user_id`,`app_id`,`played`) VALUES (239348329975250944,'T3ZlcndhdGNo 208',10);
INSERT INTO `users_awards` (`user_id`,`award_id`) VALUES (197056064636715009,'U2VwdGVtYmVyIDIwMTkgQ2hhbXBpb24=');
INSERT INTO `awards` (`award_id`,`award_img`) VALUES ('U2VwdGVtYmVyIDIwMTkgQ2hhbXBpb24=','aHR0cHM6Ly93d3cucG9sbHV4LmZ1bi9tZWRhbHMvZXZlbnRtdnAucG5n');
INSERT INTO `users_awards_primary` (`user_id`,`award_id`) VALUES (197056064636715009,'U2VwdGVtYmVyIDIwMTkgQ2hhbXBpb24=');
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (83607236668030976,31973,61011);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (113457284708843520,1362,742);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (117819770778157056,7527,8187);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (137812388614373376,2032,1910);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (138491187370786816,86,24);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (177571103110070282,4850,5572);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (197056064636715009,25283,40990);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (198269517007159296,4955,4115);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (198314980355866624,1239,709);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (199390635017502720,296,68);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (249721325600505858,193,74);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (261954705339449344,6813,12157);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (271427590927941634,45,20);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (288097695711625216,0,10);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (295416063552651266,8240,5766);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (364930858198499328,219,65);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (365742362158301186,16,19);
INSERT INTO `October_2019` (`id`,`exp_this_month`,`points_this_month`) VALUES (377012775404306445,0,5);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (83607236668030976,'wow_paladin',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (113457284708843520,'gw2_elementalist',0,0,0);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (117819770778157056,'gw2_necromancer',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (137812388614373376,'gw2_spellbreaker',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (177571103110070282,'gw2_necromancer',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (197056064636715009,'gw2_dragonhunter',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (198269517007159296,'wow_paladin',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (199390635017502720,'gw2_dragonhunter',0,0,1);
INSERT INTO `battle` (`user_id`,`class`,`wins`,`losses`,`pvp`) VALUES (295416063552651266,'gw2_necromancer',0,0,1);
