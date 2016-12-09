USE pseudobook;

delimiter $
DROP PROCEDURE IF EXISTS registerUser;
CREATE PROCEDURE registerUser (
	OUT userID INTEGER,
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    email VARCHAR(60),
    passwordHash CHAR(128),
    address VARCHAR(40),
    city VARCHAR(20),
    state CHAR(2),
    zipCode CHAR(5),
    telephone CHAR(10),
    accountCreationDate DATETIME,
    rating INTEGER
)
BEGIN
	INSERT INTO `User` (firstName, lastName, email, passwordHash, address, city, state, zipCode, telephone, accountCreationDate, rating)
    VALUES (firstName, lastName, email, passwordHash, address, city, state, zipCode, telephone, accountCreationDate, rating);
    SET userID = last_insert_id();
    INSERT INTO `Page` (userID, postCount, pageType)
    VALUES (userID, 0, "pr");
END$

DROP PROCEDURE IF EXISTS sendMessage;
CREATE PROCEDURE sendMessage(
    fromID INTEGER,
    toID INTEGER,
    `subject` CHAR(100),
    content TEXT
)
BEGIN
	INSERT INTO Messages (fromID, toID, `subject`, content)
	VALUES (fromID, toID, `subject`, content);
END$

DROP PROCEDURE IF EXISTS deleteMessage;
CREATE PROCEDURE deleteMessage(
	selfID INTEGER,
	messageID INTEGER
)
BEGIN
	DECLARE frID INTEGER;
    DECLARE tID INTEGER;
	SELECT fromID into frID FROM Messages WHERE (messageID = Messages.messageID);
    SELECT toID into tID FROM Messages WHERE (messageID = Messages.messageID);
    IF(selfID = frID OR tID = selfID) THEN
		DELETE FROM Messages
		WHERE messageID = Messages.messageID;
	END IF;
END$

DROP PROCEDURE IF EXISTS createGroup;
CREATE PROCEDURE createGroup(
    OUT groupID INTEGER,
	groupName VARCHAR(60),
    groupType CHAR(2),
    ownerID INTEGER
)
BEGIN
	DECLARE lastID INTEGER;
	INSERT INTO `Group` (groupName, groupType, ownerID)
    VALUES (groupName, groupType, ownerID);
    SET groupID = last_insert_id();
    INSERT INTO `Page` (groupID, postCount, pageType)
    VALUES (groupID, 0, "gr");
    INSERT INTO GroupUsers (groupID, userID)
    VALUES (groupID, ownerID);
END$

DROP PROCEDURE IF EXISTS searchForUser;
CREATE PROCEDURE searchForUser(
	userID INTEGER,
	firstName VARCHAR(20),
    lastName VARCHAR(20)
)
BEGIN
	SELECT * 
    FROM `User` 
    WHERE ((firstName = `User`.firstName AND lastName = `User`.lastName) OR userID = `User`.userID);
END$

DROP PROCEDURE IF EXISTS addUserToOwnGroup;
CREATE PROCEDURE addUserToOwnGroup(
	selfID INTEGER,
    groupID INTEGER,
    userID INTEGER
)
BEGIN
	IF (SELECT EXISTS(SELECT 1 FROM `Group` WHERE (selfID = `Group`.ownerID AND groupID = `Group`.groupID))) THEN
		INSERT INTO GroupUsers (groupID, userID)
		VALUES (groupID, userID);
	END IF;
END$

DROP PROCEDURE IF EXISTS makePost;
CREATE PROCEDURE makePost(
	OUT postID INTEGER,
	selfID INTEGER,
	pageID INTEGER,
    pageType CHAR(2),
    postDate DATETIME,
    postContent VARCHAR(140)
) -- makePost(1, 1, 'gr', now(), 'test content');
BEGIN
    DECLARE pgType CHAR(2);
    DECLARE ownID INTEGER;
    -- SELECT pageType into pgType FROM `Page` WHERE (pageID = `Page`.pageID);
    
    IF (pageType = 'gr') THEN
		SELECT groupID into ownID FROM `Page` WHERE (pageID = `Page`.pageID);
	ELSE SELECT userID into ownID FROM `Page` WHERE (pageID = `Page`.pageID);
	END IF;
    IF (pageType = 'gr') THEN
		INSERT INTO Post (pageID, postDate, postContent, authorID)
		VALUES (pageID, postDate, postContent, selfID);
	ELSEIF (pageType = 'pr') THEN
		INSERT INTO Post (pageID, postDate, postContent, authorID)
		VALUES (pageID, postDate, postContent, selfID);
    END IF;

    SET postID = last_insert_id();
END$

DROP PROCEDURE IF EXISTS makeComment;
CREATE PROCEDURE makeComment(
    OUT commentID INTEGER,
	postID INTEGER,
    commentDate DATETIME,
    content VARCHAR(140),
    authorID INTEGER
) -- (1, now(), "blah", 6, "us");
BEGIN
	-- DECLARE pgID INTEGER;
    -- DECLARE grID INTEGER;
    -- DECLARE userExistsInGroup TINYINT;
    -- SELECT pageID into pgID FROM Post WHERE (postID = Post.postID) LIMIT 1;
    -- IF (authorType = "gr") THEN
	-- 	SELECT groupID into ownID FROM `Page` WHERE (pageID = `Page`.pageID) LIMIT 1;
	-- ELSE SELECT userID into ownID FROM `Page` WHERE (pageID = `Page`.pageID) LIMIT 1;
    -- END IF;
    -- SELECT 1 into userExistsInGroup FROM GroupUsers WHERE (authorID = GroupUsers.userID AND ownID = GroupUsers.groupID) LIMIT 1;
	-- IF (userExistsInGroup != 0) THEN
	INSERT INTO `Comment`(postID, commentDate, content, authorID)
	VALUES (postID, commentDate, content, authorID);
    SET commentID = last_insert_id();
    -- END IF;
END$

DROP PROCEDURE IF EXISTS `like`;
CREATE PROCEDURE `like`(
	parentID INTEGER,
    authorID INTEGER,
    contentType CHAR(2)
)
BEGIN 
	IF (contentType = 'cm') THEN
		INSERT INTO `Likes` (parentID, authorID, commentID, contentType)
		VALUES (parentID, authorID, parentID, contentType);
	ELSE 
		INSERT INTO `Likes` (parentID, authorID, postID, contentType)
		VALUES (parentID, authorID, parentID, contentType);
	END IF;
END$

DROP PROCEDURE IF EXISTS removeUserFromGroup;
CREATE PROCEDURE removeUserFromGroup(
	selfID INTEGER,
	groupID INTEGER,
    userID INTEGER
)
BEGIN
	IF (SELECT EXISTS(SELECT 1 FROM `Group` WHERE (selfID = `Group`.ownerID AND groupID = `Group`.groupID))) THEN
		DELETE FROM GroupUsers
		WHERE (groupID = GroupUsers.groupID AND userID = GroupUsers.userID);
	END IF;
END$

DROP PROCEDURE IF EXISTS unlike;
CREATE PROCEDURE unlike(
	parentID INTEGER,
    authorID INTEGER,
    contentType CHAR(2)
)
BEGIN
	DELETE FROM `Likes`
    WHERE (
    parentID = `Likes`.parentID 
    AND authorID = `Likes`.authorID
    AND contentType = `Likes`.contentType
    );
END$

DROP PROCEDURE IF EXISTS removeComment;
CREATE PROCEDURE removeComment(
	commentID INTEGER
)
BEGIN
	DELETE FROM `Comment`
	WHERE (commentID = `Comment`.commentID);
END$

DROP PROCEDURE IF EXISTS removePost;
CREATE PROCEDURE removePost(
	postID INTEGER
)
BEGIN
	DELETE FROM Post
	WHERE postID = Post.postID;
END$

DROP PROCEDURE IF EXISTS modifyPost;
CREATE PROCEDURE modifyPost(
	postID INTEGER,
    postContent VARCHAR(140)
)
BEGIN
	UPDATE Post
    SET Post.postContent = postContent
    WHERE postID = Post.postID;
END$

DROP PROCEDURE IF EXISTS modifyComment;
CREATE PROCEDURE modifyComment(
	commentID INTEGER,
    content VARCHAR(140)
)
BEGIN
	UPDATE `Comment`
    SET `Comment`.content = content
    WHERE commentID = `Comment`.commentID;
END$

DROP PROCEDURE IF EXISTS deleteGroup;
CREATE PROCEDURE deleteGroup(
	selfID INTEGER,
	groupID INTEGER
)
BEGIN
	DELETE FROM `Group`
    WHERE (groupID = `Group`.groupID AND selfID = `Group`.ownerID);
END$

DROP PROCEDURE IF EXISTS renameGroup;
CREATE PROCEDURE renameGroup(
	selfID INTEGER,
	groupID INTEGER,
    groupName VARCHAR(60)
)
BEGIN
	UPDATE `Group`
    SET `Group`.groupName = groupName
    WHERE (groupID = `Group`.groupID AND selfID = `Group`.ownerID);
END$

DROP PROCEDURE IF EXISTS joinGroup;
CREATE PROCEDURE joinGroup(
	selfID INTEGER,
	groupID INTEGER
)
BEGIN
	DECLARE userExists INTEGER;
    SELECT 1 into userExists FROM GroupUsers WHERE(GroupUsers.groupID = groupID AND GroupUsers.userID = selfID);
    IF (userExists IS NULL) THEN
		INSERT INTO GroupUsers(userID , groupID)
		VALUES(selfID, groupID);
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'User is already a member of this group.';
	END IF;
END$

DROP PROCEDURE IF EXISTS unjoinGroup;
CREATE PROCEDURE unjoinGroup(
	selfID INTEGER,
	groupID INTEGER
)
BEGIN
	DECLARE userExists INTEGER;
    SELECT 1 into userExists FROM GroupUsers WHERE(GroupUsers.groupID = groupID AND GroupUsers.userID = selfID);
    IF (userExists IS NOT NULL) THEN
		DELETE FROM GroupUsers WHERE(selfID = GroupUsers.userID AND groupID = GroupUsers.groupID);
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'User is not a member of this group.';
	END IF;
END$
