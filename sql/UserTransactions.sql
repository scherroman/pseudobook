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
	INSERT INTO Post (pageID, postDate, postContent, authorID, authorType)
    VALUES (pageID, postDate, postContent, authorID, authorType);
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
	messageID INTEGER
)
BEGIN
	DELETE FROM Messages
    WHERE messageID = Messages.messageID;
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

CREATE PROCEDURE addUserToGroup(
	groupID INTEGER,
    userID INTEGER
)
BEGIN
	INSERT INTO GroupUsers (groupID, userID)
    VALUES (groupID, userID);
END$

CREATE PROCEDURE makeComment(
	postID INTEGER,
    commentDate DATETIME,
    content VARCHAR(140),
    authorID INTEGER,
    authorType CHAR(2)
)
BEGIN
	INSERT INTO makeComment(postID, commentDate, content, authorID, authorType)
    VALUES (postID, commentDate, content, authorID, authorType);
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
	DELETE FROM GroupUsers
    WHERE (groupID = GroupUsers.groupID AND userID = GroupUsers.userID);
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
	commentID INTEGER
)
BEGIN
	DELETE FROM `Comment`
    WHERE commentID = `Comment`.commentID;
END$

CREATE PROCEDURE removePost(
	postID INTEGER
)
BEGIN
	DELETE FROM Post
    WHERE postID = Post.postID;
END$

CREATE PROCEDURE modifyPost(
	postID INTEGER,
    postContent VARCHAR(140)
)
BEGIN
	UPDATE Post
    SET Post.postContent = postContent
    WHERE postID = Post.postID;
END$

CREATE PROCEDURE modifyComment(
	commentID INTEGER,
    content VARCHAR(140)
)
BEGIN
	UPDATE `Comment`
    SET `Comment`.content = content
    WHERE commentID = `Comment`.commentID;
END$

CREATE PROCEDURE deleteGroup(
	groupID INTEGER
)
BEGIN
	DELETE FROM `Group`
    WHERE groupID = `Group`.groupID;
END$

CREATE PROCEDURE renameGroup(
	groupID INTEGER,
    groupName VARCHAR(60)
)
BEGIN
	UPDATE `Group`
    SET `Group`.groupName = groupName
    WHERE groupID = `Group`.groupID;
END$