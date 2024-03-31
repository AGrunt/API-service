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

-- This table holds cafes's params
CREATE TABLE cafes(
cafeIndex INT AUTO_INCREMENT,
cafeId varchar(255),
displayName varchar(255),
formattedAddress varchar(255),
latitude varchar(255),
longitude varchar(255),
servesCoffee varchar(255),
takeout varchar(255),
goodForChildren varchar(255),
goodForGroups varchar(255),
PRIMARY KEY (cafeIndex)
);


-- This table holds reviews
CREATE TABLE reviews(
reviewIndex INT AUTO_INCREMENT,
cafeId varchar(255),
userFirstName varchar(255),
userSecondName varchar(255),
ranking  int(1),
PRIMARY KEY (cafeIndex)
);

