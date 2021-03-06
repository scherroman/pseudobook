DROP SCHEMA pseudobook;
CREATE SCHEMA pseudobook;
USE pseudobook;
CREATE USER IF NOT EXISTS 'pseudobook'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON pseudobook.* To 'pseudobook'@'localhost';

CREATE TABLE `User` (
    userID INTEGER NOT NULL AUTO_INCREMENT,
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    email VARCHAR(60) NOT NULL UNIQUE,
    passwordHash CHAR(128) NOT NULL,
    address VARCHAR(40),
    city VARCHAR(20),
    state CHAR(2),
    zipCode CHAR(5),
    telephone CHAR(10),
    accountCreationDate DATETIME,
    rating INTEGER,
    INDEX (firstName),
    INDEX (lastName),
    PRIMARY KEY (userID)
);
CREATE TABLE Messages (
    messageID INTEGER NOT NULL AUTO_INCREMENT,
    fromID INTEGER,
    toID INTEGER,
    `subject` CHAR(100),
    content TEXT,
    PRIMARY KEY (messageID),
    FOREIGN KEY (fromID)
        REFERENCES `User` (userID),
    FOREIGN KEY (toID)
        REFERENCES `User` (userID)
);
CREATE TABLE Preferences (
    userID INTEGER NOT NULL,
    preferenceType VARCHAR(10) NOT NULL,
    preferenceVal VARCHAR(20),
    PRIMARY KEY (userID , preferenceType),
    FOREIGN KEY (userID)
        REFERENCES `User` (userID)
);
CREATE TABLE UserAccounts (
    userID INTEGER NOT NULL,
    accountNumber INTEGER NOT NULL,
    creditCardNumber VARCHAR(16),
    PRIMARY KEY (userID , accountNumber),
    FOREIGN KEY (userID)
        REFERENCES `User` (userID)
);
CREATE TABLE `Group` (
    groupID INTEGER NOT NULL AUTO_INCREMENT,
    groupName VARCHAR(60),
    groupType CHAR(2),
    ownerID INTEGER,
    INDEX (groupName),
    PRIMARY KEY (groupID),
    FOREIGN KEY (ownerID)
        REFERENCES `User` (userID)
);
CREATE TABLE GroupUsers (
    groupID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    PRIMARY KEY (groupID , userID),
    FOREIGN KEY (groupID)
        REFERENCES `Group` (groupID)
        ON DELETE CASCADE,
    FOREIGN KEY (userID)
        REFERENCES `User` (userID)
);
CREATE TABLE `Page` (
    pageID INTEGER NOT NULL AUTO_INCREMENT,
    userID INTEGER,
    groupID INTEGER,
    postCount INTEGER,
    pageType CHAR(2),
    PRIMARY KEY (pageID),
    FOREIGN KEY (groupID)
        REFERENCES `Group` (groupID)
        ON DELETE CASCADE,
    FOREIGN KEY (userID)
        REFERENCES `User` (userID)
);
CREATE TABLE Post (
    postID INTEGER NOT NULL AUTO_INCREMENT,
    pageID INTEGER NOT NULL,
    postDate DATETIME,
    postContent VARCHAR(140),
    authorID INTEGER,
    PRIMARY KEY (postID),
    FOREIGN KEY (pageID)
        REFERENCES `Page` (pageID)
        ON DELETE CASCADE,
    FOREIGN KEY (authorID)
        REFERENCES `User` (userID)
);
CREATE TABLE `Comment` (
    commentID INTEGER NOT NULL AUTO_INCREMENT,
    postID INTEGER,
    commentDate DATETIME,
    content VARCHAR(140),
    authorID INTEGER,
    PRIMARY KEY (commentID),
    FOREIGN KEY (postID)
        REFERENCES Post (postID)
        ON DELETE CASCADE,
    FOREIGN KEY (authorID)
        REFERENCES `User` (userID)
);
CREATE TABLE Likes (
    parentID INTEGER NOT NULL,
    authorID INTEGER NOT NULL,
    postID INTEGER,
    commentID INTEGER,
    -- parentID == postID or commentID
    -- contentType: page or comment
    contentType CHAR(2) NOT NULL,
    PRIMARY KEY (parentID , contentType , authorID),
    FOREIGN KEY (postID)
        REFERENCES Post (postID)
        ON DELETE CASCADE,
    FOREIGN KEY (commentID)
        REFERENCES `Comment` (commentID)
        ON DELETE CASCADE,
	FOREIGN KEY (authorID)
        REFERENCES `User` (userID)
);
CREATE TABLE Employee (
    userID INTEGER NOT NULL,
    SSN CHAR(10),
    startDate DATETIME,
    hourlyRate DOUBLE,
    PRIMARY KEY (userID),
    FOREIGN KEY (userID)
        REFERENCES `User` (userID)
);
CREATE TABLE Manager (
    userID INTEGER NOT NULL,
    PRIMARY KEY (userID),
    FOREIGN KEY (userID)
        REFERENCES Employee (userID)
);
CREATE TABLE Manages (
    managerID INTEGER NOT NULL,
    employeeID INTEGER NOT NULL,
    PRIMARY KEY (managerID , employeeID),
    FOREIGN KEY (managerID)
        REFERENCES Manager (userID),
    FOREIGN KEY (employeeID)
        REFERENCES Employee (userID)
);
CREATE TABLE Advertisement (
    adID INTEGER NOT NULL AUTO_INCREMENT,
    employeeID INTEGER,
    adType CHAR(2),
    datePosted DATETIME,
    company VARCHAR(60),
    itemName VARCHAR(60),
    content TEXT,
    unitPrice DOUBLE,
    numberAvailableUnits INTEGER,
    PRIMARY KEY (adID),
    FOREIGN KEY (employeeID)
        REFERENCES Employee (userID)
);
CREATE TABLE Sales (
    transactionID INTEGER NOT NULL AUTO_INCREMENT,
    adID INTEGER NOT NULL,
    buyerId INTEGER,
    buyerAccount INTEGER,
    transactionDateTime DATETIME,
    numberOfUnits INTEGER,
    approved TINYINT(1),
    PRIMARY KEY (transactionID),
    FOREIGN KEY (adID)
        REFERENCES Advertisement (adID),
    FOREIGN KEY (buyerID , buyerAccount)
        REFERENCES UserAccounts (userID , accountNumber)
);