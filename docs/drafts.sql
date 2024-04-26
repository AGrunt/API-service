select COUNT(*) from usersTable where userId = "3abe714d-cf2d-49fe-8eaf-e4ef304a22c1";
select * from usersTable ;
select COUNT(*) from usersTable ;
select * from rankings where categoryId = 'Test';










select * from rankings;
select COUNT(*) from rankings;

select tbl.userId, tbl.cafeId, tbl.rankingValue from tbl;

Select tbl.userId, tbl.cafeId, tbl.rankingValue, ud.cluster
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
join usersData ud on tbl.userId = ud.cluster WHERE r = 1 ORDER BY userId;

select userId from responses where questionValue != 0;

select * from usersData;
select count(*) from usersData where cluster =1;
select count(*) from usersData where cluster =2;
select count(*) from usersData where cluster =0;
DELETE FROM usersTable WHERE userId='01061add-1302-4846-bb8e-b8e0ffe7ac84';
DELETE FROM usersTable WHERE userId='25c26f74-d0eb-408b-8f97-26429032c832';
DELETE FROM usersTable WHERE userId='273cf928-a41f-43c6-9dac-c13385b2a29e';


Select tbl.userId, tbl.cafeId, tbl.rankingValue
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
WHERE r = 1 ORDER BY userId;

select COUNT(*) from cafes;



#Собираем датасет cafeId, userCluster, avg(rankingValue)
Select distinct tbl2.cafeId,  ud.cluster, avg(tbl2.rankingValue) over ( partition by cluster, cafeid) 
from (
Select tbl.userId, tbl.cafeId, tbl.rankingValue
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
WHERE r = 1 ORDER BY userId
) tbl2 left join usersData ud on tbl2.userId = ud.userId;


Select tbl2.cafeId,  tbl2.rankingValue, ud.cluster, avg(tbl2.rankingValue) over ( partition by cluster, cafeid) 
from (
Select tbl.userId, tbl.cafeId, tbl.rankingValue
from (SELECT *, row_number() OVER (PARTITION BY userId, cafeId ORDER BY STR_TO_DATE(rankingTimeStamp, '%Y-%m-%d %H:%i:%s.%f') DESC) r FROM rankings WHERE categoryId = 1) tbl 
WHERE r = 1 ORDER BY userId
) tbl2 left join usersData ud on tbl2.userId = ud.userId;



show tables;
  
SELECT COUNT(userId) FROM usersTable WHERE userId = 3abe714d-cf2d-49fe-8eaf-e4ef304a22c1;

select * from usersTable join responses ON usersTable.userId = responses.userId;



DELETE FROM responses WHERE questionId='test';
commit;

select count(*) from usersData;



select distinct questionId from responses where questionId not like "test";

select distinct questionId from responses;


SELECT resp.*, row_number() OVER (PARTITION BY questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses resp;

SELECT resp.*, row_number() OVER (PARTITION BY questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses;


select usersTable.userId, gender, age, postcode, questionId, questionValue from usersTable join responses ON usersTable.userId = responses.userId where questionId not like "test" order by responseTimeStamp and questionId ;



 select count(*) from responses;
 select tbl.* from (SELECT *, row_number() OVER (PARTITION BY questionId and userId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses resp) tbl;
 SELECT count(*) from responses;
 SELECT *, row_number() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses;
 Select tbl.* from (SELECT *, row_number() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses) tbl where r = 1;
 
 SELECT *, row_number() OVER (PARTITION BY userId, questionId ORDER BY STR_TO_DATE(responseTimeStamp, '%Y-%m-%d %H:%i:%s.%f ') DESC) r FROM responses;
 
select *from responses where (select count(*) ) > 0;

select count(*) from responses where questionId = '7' order by responseTimeStamp DESC ;

Select DISTINCT postcode from usersTable order by questionId ASC;

#U.userId, U.age, U.gender, U.postcode, 

SELECT COUNT(userId) FROM usersTable WHERE userId = "3abe714d-cf2d-49fe-8eaf-e4ef304a22c1";

SELECT COUNT(*) FROM usersTable WHERE userId = "3abe714d-cf2d-49fe-8eaf-e4ef304a22c1";

ALTER TABLE cafes ADD delivery varchar(255);

select count(*) from responses;
select count(*) from usersTable;
select count(*) from rankings;
select count(*) from cafes;


SELECT DISTINCT cafeId FROM cafes where servesCoffee = "TRUE";

select count(*) from cafes where servesCoffee = "TRUE"; 

commit;