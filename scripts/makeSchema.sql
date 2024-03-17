CREATE TABLE usersTable(
userId varchar(255),
gender INT(1),
age INT(2),
registrationDate varchar(255),
postcode varchar(255),
PRIMARY KEY (userId)
);

CREATE TABLE responses(
responseIndex INT AUTO_INCREMENT,
userId varchar(255),
questionId varchar(255),
questionValue int(2),
responseTimeStamp varchar(255),
PRIMARY KEY (responseIndex)
);

CREATE TABLE rankings(
rankingIndex INT AUTO_INCREMENT,
userId varchar(255),
cafeId varchar(255),
categoryId varchar(255),
rankingValue int(1),
rankingTimeStamp varchar(255),
PRIMARY KEY (rankingIndex)
);

CREATE TABLE predictions(
predictionIndex int AUTO_INCREMENT,
userId varchar(255),
cafeId varchar(255),
predicitonValue DECIMAL(3, 2),
predictionTimeStamp varchar(255),
PRIMARY KEY (predictionIndex)
);