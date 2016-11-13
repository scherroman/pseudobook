delimiter $

CREATE PROCEDURE registerUser (
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    address VARCHAR(40),
    city VARCHAR(20),
    state CHAR(2),
    zipCode CHAR(5),
    telephone CHAR(10),
    email VARCHAR(60),
    accountCreationDate DATETIME,
    rating INTEGER
)
BEGIN
	DECLARE lastID INTEGER;
	INSERT INTO `User` (firstName, lastName, address, city, state, zipCode, telephone, email, accountCreationDate, rating)
    VALUES (firstName, lastName, address, city, state, zipCode, telephone, email, accountCreationDate, rating);
    SELECT last_insert_id() into lastID;
    INSERT INTO `Page` (ownerID, postCount, pageType)
    VALUES (lastID, 0, "pr");
END$

CREATE PROCEDURE postToPage(
	pageID INTEGER, 
    postDate DATETIME,
    postContent VARCHAR(140),
    authorID INTEGER,
    authorType CHAR(2)
)
BEGIN
	DECLARE ownID INTEGER;
	SELECT ownerID into ownID FROM `Page` WHERE (pageID = `Page`.pageID);
    IF(ownID = authorID) THEN
		INSERT INTO Post (pageID, postDate, postContent, authorID, authorType)
		VALUES (pageID, postDate, postContent, authorID, authorType);
    END IF;
END$

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

CREATE PROCEDURE createGroup(
	groupName VARCHAR(60),
    groupType CHAR(2),
    ownerID INTEGER
)
BEGIN
	DECLARE lastID INTEGER;
	INSERT INTO `Group` (groupName, groupType, ownerID)
    VALUES (groupName, groupType, ownerID);
    SELECT last_insert_id() into lastID;
    INSERT INTO `Page` (ownerID, postCount, pageType)
    VALUES (lastID, 0, "gr");
    INSERT INTO GroupUsers (groupID, userID)
    VALUES (lastID, ownerID);
END$

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

CREATE PROCEDURE addUserToOwnGroup(
	selfID INTEGER,
    groupID INTEGER,
    userID INTEGER
)
BEGIN
	IF (SELECT 1 FROM `Group` WHERE (selfID = `Group`.ownerID AND groupID = `Group`.groupID)) THEN
		INSERT INTO GroupUsers (groupID, userID)
		VALUES (groupID, userID);
	END IF;
END$

CREATE PROCEDURE makePost(
	selfID INTEGER,
	pageID INTEGER,
    postDate DATETIME,
    postContent VARCHAR(140),
    authorID INTEGER,
    authorType CHAR(2)
)
BEGIN
    DECLARE ownID INTEGER;
    SELECT ownerID into ownID FROM `Page` WHERE (pageID = `Page`.pageID) LIMIT 1;
	IF (SELECT 1 FROM GroupUsers WHERE (selfID = GroupUsers.userID AND ownID = GroupUsers.groupID)) THEN
		INSERT INTO Post (pageID, postDate, postContent, authorID, authorType)
		VALUES (pageID, postDate, postContent, authorID, authorType);
	END IF;
END$

CREATE PROCEDURE makeComment(
	postID INTEGER,
    commentDate DATETIME,
    content VARCHAR(140),
    authorID INTEGER,
    authorType CHAR(2)
) -- (1, now(), "blah", 6, "us");
BEGIN
	DECLARE pgID INTEGER;
    DECLARE ownID INTEGER;
    DECLARE userExistsInGroup TINYINT;
    SELECT pageID into pgID FROM Post WHERE (postID = Post.postID) LIMIT 1;
    SELECT ownerID into ownID FROM `Page` WHERE (pageID = `Page`.pageID) LIMIT 1;
    SELECT 1 into userExistsInGroup FROM GroupUsers WHERE (authorID = GroupUsers.userID AND ownID = GroupUsers.groupID) LIMIT 1;
	IF (userExistsInGroup != 0) THEN
		INSERT INTO `Comment`(postID, commentDate, content, authorID, authorType)
		VALUES (postID, commentDate, content, authorID, authorType);
    END IF;
END$

CREATE PROCEDURE `like`(
	parentID INTEGER,
    authorID INTEGER,
    authorType CHAR(2),
    contentType CHAR(2)
)
BEGIN 
	INSERT INTO `Likes` (parentID, authorID, authorType, contentType)
    VALUES (parentID, authorID, authorType, contentType);
END$

CREATE PROCEDURE removeUserFromGroup(
	groupID INTEGER,
    userID INTEGER
)
BEGIN
	IF (SELECT 1 FROM `Group` WHERE (selfID = `Group`.ownerID AND groupID = `Group`.groupID)) THEN
		DELETE FROM GroupUsers
		WHERE (groupID = GroupUsers.groupID AND userID = GroupUsers.userID);
	END IF;
END$

CREATE PROCEDURE unlike(
	parentID INTEGER,
    authorID INTEGER
)
BEGIN
	DELETE FROM `Likes`
    WHERE (parentID = `Likes`.parentID AND authorID = `Likes`.authorID);
END$

CREATE PROCEDURE removeComment(
	authorID INTEGER,
	commentID INTEGER
)
BEGIN
	DELETE FROM `Comment`
    WHERE (commentID = `Comment`.commentID AND authorID = `Comment`.authorID);
END$

CREATE PROCEDURE removePost(
	authorID INTEGER,
	postID INTEGER
)
BEGIN
	DELETE FROM Post
    WHERE (postID = Post.postID AND authorID = Post.authorID);
END$

CREATE PROCEDURE modifyPost(
	selfID INTEGER,
	postID INTEGER,
    postContent VARCHAR(140)
)
BEGIN
	UPDATE Post
    SET Post.postContent = postContent
    WHERE (postID = Post.postID AND selfID = Post.authorID);
END$

CREATE PROCEDURE modifyComment(
	selfID INTEGER,
	commentID INTEGER,
    content VARCHAR(140)
)
BEGIN
	UPDATE `Comment`
    SET `Comment`.content = content
    WHERE (commentID = `Comment`.commentID AND selfID = `Comment`.authorID);
END$

CREATE PROCEDURE deleteGroup(
	selfID INTEGER,
	groupID INTEGER
)
BEGIN
	DELETE FROM `Group`
    WHERE (groupID = `Group`.groupID AND selfID = `Group`.ownerID);
END$

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
-- join/unjoin group, CHECK contraints on like, word document, check ON DELETE cascades