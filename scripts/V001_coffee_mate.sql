-- This table holds users
CREATE TABLE usersTable(
userId varchar(255), 
gender INT(1),
age INT(2),
registrationTimeStamp varchar(255),
postcode varchar(255),
PRIMARY KEY (userId)
);

-- This table holds user's answers to questionare about their coffee preferences 
CREATE TABLE responses(
responseIndex INT AUTO_INCREMENT,
userId varchar(255),
questionId varchar(255),
questionValue int(2),
responseTimeStamp varchar(255),
PRIMARY KEY (responseIndex)
);

-- This table holds user's cafe rankings. Do they like cafe or not for categories.
CREATE TABLE rankings(
rankingIndex INT AUTO_INCREMENT,
userId varchar(255),
cafeId varchar(255),
categoryId varchar(255),
rankingValue int(1),
rankingTimeStamp varchar(255),
PRIMARY KEY (rankingIndex)
);

-- This table holds recomendations for each cafe for each user
CREATE TABLE predictions(
predictionIndex int AUTO_INCREMENT,
userId varchar(255),
cafeId varchar(255),
predicitonValue DECIMAL(3, 2),
predictionTimeStamp varchar(255),
PRIMARY KEY (predictionIndex)
);