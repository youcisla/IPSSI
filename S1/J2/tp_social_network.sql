-- 1. Creation of Tables
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_inscription DATE NOT NULL,
    bio TEXT
);

CREATE TABLE Friendships (
    user_id1 INT,
    user_id2 INT,
    date_friendship DATE NOT NULL,
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content TEXT NOT NULL,
    date_post DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE PostTags (
    post_id INT,
    tag_id INT,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
);

CREATE TABLE Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    content TEXT NOT NULL,
    date_comment DATETIME NOT NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 2. Insertion of Data
INSERT INTO Users (username, email, date_inscription, bio) VALUES
('Alice', 'alice@example.com', '2024-01-01', 'Loves coding.'),
('Bob', 'bob@example.com', '2024-01-02', 'Enjoys hiking.'),
('Charlie', 'charlie@example.com', '2024-01-03', 'Movie buff.');

INSERT INTO Friendships (user_id1, user_id2, date_friendship) VALUES
(1, 2, '2024-01-05'),
(2, 3, '2024-01-06');

INSERT INTO Posts (user_id, content, date_post) VALUES
(1, 'Hello world!', '2024-01-10 10:00:00'),
(2, 'Good morning!', '2024-01-11 09:30:00');

INSERT INTO Tags (tag_name) VALUES ('Tech'), ('Movies'), ('Travel');

INSERT INTO PostTags (post_id, tag_id) VALUES
(1, 1), (2, 3);

INSERT INTO Comments (post_id, user_id, content, date_comment) VALUES
(1, 2, 'Nice post!', '2024-01-10 11:00:00'),
(2, 1, 'Enjoy your trip!', '2024-01-11 10:00:00');

-- 3. Queries and Joins
SELECT post_id, username, date_post FROM Posts JOIN Users ON Posts.user_id = Users.user_id ORDER BY date_post DESC;

SELECT Comments.comment_id, Comments.content, Users.username, Comments.date_comment, Posts.content FROM Comments JOIN Users ON Comments.user_id = Users.user_id JOIN Posts ON Comments.post_id = Posts.post_id;

SELECT u1.username AS Friend1, u2.username AS Friend2, Friendships.date_friendship FROM Friendships JOIN Users u1 ON Friendships.user_id1 = u1.user_id JOIN Users u2 ON Friendships.user_id2 = u2.user_id;

-- 4. Aggregation Queries
SELECT username, COUNT(post_id) AS post_count FROM Users LEFT JOIN Posts ON Users.user_id = Posts.user_id GROUP BY username ORDER BY post_count DESC;

SELECT tag_name, COUNT(PostTags.tag_id) AS usage_count FROM Tags LEFT JOIN PostTags ON Tags.tag_id = PostTags.tag_id GROUP BY tag_name ORDER BY usage_count DESC;

SELECT AVG(comment_count) AS avg_comments_per_post FROM (
    SELECT Posts.post_id, COUNT(Comments.comment_id) AS comment_count FROM Posts LEFT JOIN Comments ON Posts.post_id = Comments.post_id GROUP BY Posts.post_id
) AS temp;

-- 5. Views and Procedures
CREATE VIEW v_AllPosts AS SELECT Posts.post_id, Users.username, Posts.content, Posts.date_post, GROUP_CONCAT(Tags.tag_name SEPARATOR ', ') AS tags FROM Posts LEFT JOIN PostTags ON Posts.post_id = PostTags.post_id LEFT JOIN Tags ON PostTags.tag_id = Tags.tag_id JOIN Users ON Posts.user_id = Users.user_id GROUP BY Posts.post_id;

DELIMITER //
CREATE PROCEDURE sp_GetPostsByUser(IN userPseudo VARCHAR(255))
BEGIN
    SELECT Posts.post_id, Posts.content, Posts.date_post FROM Posts JOIN Users ON Posts.user_id = Users.user_id WHERE Users.username = userPseudo;
END //
DELIMITER ;

-- 6. Triggers
DELIMITER //
CREATE TRIGGER after_friendship_insert AFTER INSERT ON Friendships FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Friendships WHERE user_id1 = NEW.user_id2 AND user_id2 = NEW.user_id1) THEN
        INSERT INTO Friendships (user_id1, user_id2, date_friendship) VALUES (NEW.user_id2, NEW.user_id1, NEW.date_friendship);
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER after_comment_insert
AFTER INSERT ON Comments
FOR EACH ROW
BEGIN
    UPDATE Posts SET nb_comments = (SELECT COUNT(*) FROM Comments WHERE Comments.post_id = Posts.post_id)
    WHERE Posts.post_id = NEW.post_id;
END //
DELIMITER ;

-- 7. Updates and Deletions
UPDATE Tags SET tag_name = 'Film' WHERE tag_name = 'Cinéma';

DELETE FROM Users WHERE username = 'Charlie';
