use pseudobook;

-- basic users
INSERT INTO `User` (`passwordHash`,`firstName`,`lastName`,`address`,`city`,`state`,`zipCode`,`telephone`,`email`,`accountCreationDate`,`rating`) VALUES 
("pwd","Josiah","Gates","248-6520 Magnis St.","Orlando","FL","28336","8327315523","ac.libero.nec@loremsit.edu","2016-12-14 12:12:41",5),
("pwd","Zephania","Gray","Ap #990-9718 Vel Rd.","Augusta","GA","33283","6107022041","et.netus.et@egestasDuis.co.uk","2016-02-29 12:20:08",4),
("pwd","Ashton","Lindsay","P.O. Box 637, 6381 A Street","Reno","NV","19345","1728795170","est.Nunc@eget.edu","2017-10-23 03:25:22",6),
("pwd","Moses","Kramer","P.O. Box 401, 8296 Sed Av.","Broken Arrow","OK","87908","3383163057","Vestibulum.ante.ipsum@CrasinterdumNunc.net","2016-11-14 19:41:49",3),
("pwd","Marvin","Maxwell","3728 Morbi St.","Anchorage","AK","99814","6219386969","eu.placerat@eudui.net","2016-04-18 15:41:34",6),
("pwd","Herman","Travis","753-1179 Velit. St.","Kansas City","KS","44248","6426316904","Donec@In.org","2016-04-26 15:53:13",7),
("pwd","Keaton","Gonzales","Ap #251-2398 Mi Road","Covington","KY","53329","3851212078","ullamcorper@Quisquetincidunt.ca","2017-03-09 07:31:52",9),
("pwd","Declan","Mason","7456 Faucibus. Rd.","Helena","MT","62434","5991876157","Sed.neque@laciniaSedcongue.net","2017-07-04 00:37:58",5),
("pwd","Ronan","Price","9856 Semper Rd.","Tallahassee","FL","53485","2722917145","orci.sem@nequeNullamnisl.co.uk","2017-03-09 07:31:52",8),
("pwd","Cadman","Pickett","P.O. Box 827, 1764 Mi, Rd.","Annapolis","MD","75550","7862533351","mi.lorem.vehicula@Quisquenonummyipsum.net","2016-08-18 01:46:59",10);

-- employees
INSERT INTO `User` (`passwordHash`,`firstName`,`lastName`,`address`,`city`,`state`,`zipCode`,`telephone`,`email`,`accountCreationDate`,`rating`) VALUES 
("pwd","Eagan","Gonzales","Ap #832-124 Congue. Av.","Newark","DE","65262","4891622153","blandit@tinciduntnunc.org","2016-02-02 15:32:08",6),
("pwd","Isaiah","Davenport","P.O. Box 940, 9262 Vivamus St.","Akron","OH","59377","1419120980","et.commodo@molestiedapibusligula.co.uk","2017-09-16 15:06:17",1),
("pwd","Allen","Downs","P.O. Box 783, 257 Dolor Av.","Allentown","PA","70853","2085231126","bibendum.ullamcorper.Duis@Fusce.org","2016-08-15 09:53:52",7),
("pwd","Nasim","Clements","Ap #172-9187 Fermentum Street","San Antonio","TX","94962","6118249796","Duis@morbi.com","2017-03-25 03:48:39",5),
("pwd","Judah","Huber","643-5477 Erat Rd.","Milwaukee","WI","48599","7276568237","Suspendisse.sagittis@Fusce.edu","2016-11-04 11:03:18",7),
("pwd","Fuller","Alvarado","P.O. Box 663, 961 Massa. Street","Lincoln","NE","89159","5967529391","felis@sed.com","2017-05-05 12:18:25",9),
("pwd","Steel","Preston","3481 Ac Avenue","Casper","WY","25780","2112086271","pharetra.felis@sodales.edu","2017-08-16 06:05:53",9),
("pwd","Ashton","Howard","Ap #608-3479 Ipsum St.","Joliet","IL","71690","3501380905","aliquet.magna@Donecporttitortellus.edu","2017-03-04 04:43:21",9),
("pwd","Basil","Pratt","377-3384 Augue Rd.","Sacramento","CA","95572","2506102243","venenatis@etrutrumeu.edu","2017-03-10 02:42:14",1),
("pwd","Baker","Acosta","312-6667 Ut Rd.","Memphis","TN","20964","5493645759","posuere.cubilia@auctor.org","2016-08-22 08:41:56",4);

-- managers
INSERT INTO `User` (`passwordHash`,`firstName`,`lastName`,`address`,`city`,`state`,`zipCode`,`telephone`,`email`,`accountCreationDate`,`rating`) VALUES 
("pwd","Castor","Strong","P.O. Box 638, 6301 Fusce Rd.","Metairie","LA","20439","2922388657","Cras.convallis@adipiscing.org","2016-01-06 08:30:29",9),
("pwd","Cade","Trujillo","P.O. Box 226, 5580 Tellus. Road","Cambridge","MA","10314","3584156207","aliquam.eros@Namconsequatdolor.ca","2017-04-14 13:53:56",1),
("pwd","Quamar","Calderon","Ap #990-3883 Fringilla St.","Kapolei","HI","65485","5648060076","orci.consectetuer.euismod@sagittisNullamvitae.com","2015-12-06 06:56:59",2),
("pwd","Lars","Calderon","673-6222 Ac Av.","Little Rock","AR","71935","3466122632","parturient.montes.nascetur@sitamet.ca","2017-03-29 15:00:26",8),
("pwd","Anthony","Clarke","P.O. Box 584, 9061 Et Rd.","Wichita","KS","41366","3187504830","placerat.augue.Sed@laoreetipsum.co.uk","2015-12-02 19:36:09",3),
("pwd","Fletcher","Small","P.O. Box 986, 4303 Eu Ave","West Jordan","UT","52371","5859441394","id.erat.Etiam@ipsumnonarcu.ca","2016-12-09 21:07:22",5),
("pwd","Felix","Hendrix","467-838 Eu, Ave","Tacoma","WA","23613","3871428435","rutrum@temporlorem.com","2017-07-12 01:47:42",5),
("pwd","Kermit","Lindsey","9039 Quisque Street","San Jose","CA","91770","8602088130","euismod.ac@felis.co.uk","2017-05-30 04:15:50",9),
("pwd","Joshua","Harrison","Ap #896-7302 Nonummy Avenue","Chattanooga","TN","84295","3719453840","libero@a.co.uk","2017-10-01 22:17:03",3),
("pwd","Carlos","Mack","Ap #753-5282 Amet, St.","Annapolis","MD","60247","5498361463","laoreet.libero@arcuAliquamultrices.co.uk","2016-11-05 08:15:01",5);

INSERT INTO `Messages` (`fromID`,`toID`,`subject`,`content`) VALUES 
(2,1,"Nulla interdum. Curabitur","lobortis quam a felis ullamcorper viverra. Maecenas iaculis aliquet diam."),
(2,4,"faucibus ut, nulla.","imperdiet dictum magna. Ut tincidunt orci quis lectus. Nullam suscipit, est ac facilisis facilisis, magna tellus faucibus leo,"),
(2,6,"gravida sagittis. Duis","tempus non, lacinia at, iaculis quis, pede. Praesent eu dui."),
(10,7,"Sed molestie. Sed","tellus id nunc interdum feugiat. Sed nec metus facilisis lorem tristique aliquet."),
(8,6,"diam dictum sapien.","risus odio, auctor vitae, aliquet nec, imperdiet nec, leo. Morbi"),
(10,1,"Curabitur dictum. Phasellus","gravida molestie arcu. Sed eu nibh vulputate mauris sagittis placerat. Cras dictum ultricies ligula. Nullam enim."),
(2,2,"ornare, libero at","non nisi. Aenean eget metus. In nec orci. Donec nibh. Quisque nonummy ipsum non arcu. Vivamus"),
(10,4,"id, mollis nec,","Suspendisse dui. Fusce diam nunc, ullamcorper eu, euismod ac, fermentum vel, mauris."),
(5,4,"mi pede, nonummy","dapibus gravida. Aliquam tincidunt, nunc ac mattis ornare, lectus ante dictum mi, ac mattis velit"),
(1,10,"amet, consectetuer adipiscing","Nulla interdum. Curabitur dictum. Phasellus in felis. Nulla tempor augue ac ipsum. Phasellus");

INSERT INTO `Preferences` (`userID`,`preferenceType`,`preferenceVal`) VALUES 
(7,"vel","condimentum"),
(1,"sit","nisi"),
(7,"orci","Sed"),
(8,"rhoncus","Quisque"),
(4,"molestie","senectus"),
(8,"tincidunt","ridiculus"),
(6,"Nullam","dictum"),
(8,"erat","Cum"),
(6,"sem","Nam"),
(2,"convallis","pellentesque");

INSERT INTO `UserAccounts` (`userID`,`accountNumber`,`creditCardNumber`) VALUES
(1,1,"4716405529576"),
(1,2,"4716954302679"),
(2,1,"4716149412642"),
(3,1,"4556057662108794"),
(4,1,"4024007154800857"),
(5,1,"4556912579437"),
(6,1,"4871863128922"),
(7,1,"4716800514798065"),
(8,1,"4485111876719"),
(9,1,"4556885598512857"),
(10,1,"4602244800941"),

-- employees
(11,1,"4716021683398690"),
(12,1,"4087485848565470"),
(13,1,"4556160229651"),
(14,1,"4916648275052802"),
(15,1,"4024007112911"),
(16,1,"4024007176204823"),
(17,1,"4556349311730635"),
(18,1,"4485094998688"),
(19,1,"4916848837467"),
(20,1,"4024007138619522"),

-- managers
(21,1,"4539026290273"),
(22,1,"4539997641485981"),
(23,1,"4916488814040"),
(24,1,"4485737446630983"),
(25,1,"4916076180598"),
(26,1,"4532407733011"),
(27,1,"4539515385287"),
(28,1,"4485798139498"),
(29,1,"4716009434033"),
(30,1,"4485938380762");


INSERT INTO `Group` (`groupName`,`groupType`,`ownerID`) VALUES 
("Mi Enim Condimentum Associates",6,9),
("Aenean Company",1,6),
("Arcu Corp.",10,5),
("Nisi A Odio Inc.",3,10),
("A Corp.",6,7),
("Pharetra Incorporated",5,1),
("Facilisi Sed Institute",5,6),
("Est Industries",7,4),
("Et Netus Et Incorporated",2,5),
("Morbi Tristique Inc.",9,9);

INSERT INTO `GroupUsers` (`groupID`,`userID`) VALUES 
(10,8),
(6,7),
(2,3),
(8,6),
(7,10),
(3,10),
(3,8),
(6,9),
(1,6),
(5,10);

INSERT INTO `Page` (`userID`,`pageType`) VALUES 
(1,1),
(2,1),
(3,1),
(4,1),
(5,1),
(6,1),
(7,1),
(8,1),
(9,1),
(10,1),
(11,1),
(12,1),
(13,1),
(14,1),
(15,1),
(16,1),
(17,1),
(18,1),
(19,1),
(20,1),
(21,1),
(22,1),
(23,1),
(24,1),
(25,1),
(26,1),
(27,1),
(28,1),
(29,1),
(30,1);

INSERT INTO `Page` (`groupID`,`pageType`) VALUES 
(1,2),
(2,2),
(3,2),
(4,2),
(5,2),
(6,2),
(7,2),
(8,2),
(9,2),
(10,2);

INSERT INTO `Post` (`pageID`,`postDate`,`postContent`,`authorID`) VALUES 
(3,"2017-07-16 23:33:09","Duis volutpat nunc sit amet metus. Aliquam erat volutpat. Nulla facilisis. Suspendisse commodo tincidunt nibh. Phasellus nulla.",4),
(5,"2017-06-04 03:45:56","Nam consequat dolor vitae dolor. Donec fringilla. Donec feugiat metus sit amet ante. Vivamus non lorem vitae",3),
(8,"2016-03-09 18:16:29","sed, sapien. Nunc pulvinar arcu et pede. Nunc sed orci lobortis",8),
(3,"2016-02-28 19:06:01","non massa non ante bibendum ullamcorper. Duis cursus, diam at pretium aliquet, metus urna convallis erat, eget tincidunt",9),
(6,"2016-01-29 04:07:33","sed, est. Nunc laoreet lectus quis massa. Mauris vestibulum, neque sed dictum eleifend, nunc risus varius orci, in consequat enim",5),
(1,"2016-01-14 16:18:46","amet luctus vulputate, nisi sem semper erat, in consectetuer ipsum nunc",6),
(8,"2016-07-23 15:10:14","velit egestas lacinia. Sed congue, elit sed consequat auctor, nunc nulla vulputate dui, nec tempus mauris",1),
(1,"2016-08-27 12:06:56","ac nulla. In tincidunt congue turpis. In condimentum. Donec at arcu. Vestibulum ante ipsum",1),
(7,"2017-03-18 02:34:00","ut, pellentesque eget, dictum placerat, augue. Sed molestie. Sed id risus quis",6),
(2,"2017-10-03 00:48:25","Nulla tempor augue ac ipsum. Phasellus vitae mauris sit amet lorem semper auctor. Mauris vel turpis. Aliquam adipiscing",4);

INSERT INTO `Comment` (`postID`,`commentDate`,`content`,`authorID`) VALUES 
(9,"2015-11-20 04:36:03","viverra. Maecenas iaculis aliquet diam. Sed diam lorem, auctor quis, tristique ac, eleifend vitae, erat. Vivamus nisi.",1),
(9,"2016-04-14 17:13:31","tincidunt aliquam arcu. Aliquam ultrices iaculis odio. Nam interdum enim non nisi. Aenean eget metus. In",3),
(2,"2016-02-05 20:31:53","ac mattis ornare, lectus ante dictum mi, ac mattis velit justo nec ante. Maecenas mi felis, adipiscing fringilla,",5),
(1,"2017-01-20 20:09:39","auctor, nunc nulla vulputate dui, nec tempus mauris erat eget ipsum. Suspendisse sagittis. Nullam",7),
(6,"2016-08-21 15:05:19","Cras lorem lorem, luctus ut, pellentesque eget, dictum placerat, augue. Sed molestie.",3),
(4,"2016-06-11 07:41:17","Nulla facilisi. Sed neque. Sed eget lacus. Mauris non dui nec urna suscipit",3),
(10,"2017-03-13 09:07:25","pede blandit congue. In scelerisque scelerisque dui. Suspendisse ac metus vitae velit",2),
(4,"2017-05-29 07:21:58","dolor dapibus gravida. Aliquam tincidunt, nunc ac mattis ornare, lectus ante dictum mi, ac mattis velit justo nec",4),
(8,"2016-02-18 14:06:00","Proin sed turpis nec mauris blandit mattis. Cras eget nisi dictum augue malesuada malesuada. Integer id magna et",4),
(2,"2017-10-29 23:42:01","dui, nec tempus mauris erat eget ipsum. Suspendisse sagittis. Nullam vitae diam. Proin dolor. Nulla semper",1);

INSERT INTO `Likes` (`parentID`,`authorID`,`postID`,`contentType`) VALUES 
(3,8,3,1),
(5,2,5,1),
(4,2,4,1),
(7,4,7,1),
(8,1,8,1);

INSERT INTO `Likes` (`parentID`,`authorID`,`commentID`,`contentType`) VALUES 
(10,6,10,2),
(4,10,4,2),
(1,6,1,2),
(1,9,1,2),
(8,4,8,2);

INSERT INTO `Employee` (`userID`,`SSN`,`startDate`,`hourlyRate`) VALUES 
(11,"3149460718","2016-12-24 13:55:07","73207.05"),
(12,"7878536614","2017-01-22 13:53:42","85545.77"),
(13,"2038432116","2015-12-15 06:27:36","65202.32"),
(14,"6989681367","2016-05-25 00:42:24","83968.09"),
(15,"7805975682","2017-01-07 03:43:20","88608.79"),
(16,"5386772195","2016-02-11 03:06:17","86304.06"),
(17,"1218866464","2017-09-16 12:13:05","81460.97"),
(18,"6597817764","2017-06-02 03:11:41","79844.31"),
(19,"6792873334","2017-07-28 17:44:45","67669.42"),
(20,"4643179309","2016-11-17 00:44:52","95759.61"),
(21,"4349547845","2017-03-27 21:43:00","68805.38"),
(22,"5615149720","2017-10-08 18:45:32","94137.47"),
(23,"2256250229","2016-08-27 03:56:01","62817.62"),
(24,"3308070335","2016-06-22 14:06:57","84817.90"),
(25,"2315648374","2017-07-24 08:41:44","95704.21"),
(26,"5737007912","2017-03-28 15:46:43","90292.01"),
(27,"9762563912","2016-12-23 16:00:07","64450.56"),
(28,"2945130705","2016-01-06 11:41:28","69031.90"),
(29,"2704582201","2016-07-18 22:25:51","71612.95"),
(30,"3216455044","2017-02-13 20:07:26","70397.06");

INSERT INTO `Manager` (`userID`) VALUES 
(21),
(22),
(23),
(24),
(25),
(26),
(27),
(28),
(29),
(30);

INSERT INTO `Manages` (`managerID`,`employeeID`) VALUES 
(28,13),
(28,14),
(23,19),
(22,16),
(24,12),
(21,14),
(21,15),
(23,14),
(24,15),
(29,12);

INSERT INTO `Advertisement` (`employeeID`,`adType`,`datePosted`,`company`,`itemName`,`content`,`unitPrice`,`numberAvailableUnits`) VALUES 
(16,9,"2015-11-17 09:48:14","Et Ipsum Cursus PC","nunc ac mattis","faucibus ut, nulla. Cras eu tellus eu augue porttitor interdum. Sed auctor odio a purus. Duis elementum, dui quis accumsan","0.34",95),
(15,10,"2017-05-14 03:21:29","Ac LLC","quis lectus. Nullam","aliquet odio. Etiam ligula tortor, dictum eu, placerat eget, venenatis a, magna. Lorem ipsum","71.74",76),
(20,8,"2017-06-09 17:10:49","Ante Company","Phasellus libero mauris,","taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Mauris ut quam vel","14.53",19),
(18,6,"2016-12-30 12:10:30","Sed Nec Metus LLP","congue, elit sed","velit. Quisque varius. Nam porttitor scelerisque neque. Nullam nisl. Maecenas malesuada","44.18",75),
(17,4,"2016-06-23 18:12:02","Ac Orci Ut Associates","ac risus. Morbi","mollis vitae, posuere at, velit. Cras lorem lorem, luctus ut, pellentesque eget, dictum","25.81",18),
(12,5,"2015-12-04 19:55:56","Molestie In Tempus Associates","at risus. Nunc","pede. Praesent eu dui. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean eget","70.62",23),
(13,3,"2016-02-20 00:17:21","Nec Cursus Incorporated","Phasellus dapibus quam","urna. Vivamus molestie dapibus ligula. Aliquam erat volutpat. Nulla dignissim. Maecenas ornare egestas ligula. Nullam feugiat placerat velit. Quisque varius.","53.82",10),
(18,3,"2017-09-28 01:17:05","Et Magnis Dis Inc.","habitant morbi tristique","tellus. Suspendisse sed dolor. Fusce mi lorem, vehicula et, rutrum","5.28",54),
(11,5,"2016-10-13 01:49:58","Quam Vel PC","ac tellus. Suspendisse","cursus purus. Nullam scelerisque neque sed sem egestas blandit. Nam nulla magna, malesuada","35.16",66),
(19,7,"2017-02-10 02:47:17","Orci LLP","diam nunc, ullamcorper","laoreet, libero et tristique pellentesque, tellus sem mollis dui, in sodales elit erat vitae risus. Duis a mi fringilla","12.11",57),
(20,4,"2016-03-11 01:48:16","Orci LLP","diam nunc, ullamcorper 2: bigger and better","laoreet, libero et tristique pellentesque, tellus sem mollis dui, in sodales elit erat vitae risus. Duis a mi fringilla","102.11",34);


INSERT INTO `Sales` (`adID`,`buyerId`,`buyerAccount`,`transactionDateTime`,`numberOfUnits`,`approved`) VALUES 
(7,5,1,"2015-12-19 02:39:56",4,0),
(2,4,1,"2016-10-16 12:28:14",5,0),
(10,8,1,"2017-10-13 15:32:56",1,0),
(9,7,1,"2016-02-03 21:06:32",3,0),
(7,1,1,"2016-09-03 00:51:59",5,0),
(7,10,1,"2016-06-11 03:04:05",2,0),
(4,7,1,"2017-09-05 12:14:44",5,0),
(6,8,1,"2017-07-10 07:09:59",3,0),
(10,1,2,"2016-03-04 07:41:37",2,0),
(5,9,1,"2015-12-18 06:12:07",2,0);















