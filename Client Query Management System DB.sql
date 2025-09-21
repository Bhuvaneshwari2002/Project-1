create database client_query;
use client_query;
create table client
(query_id INT AUTO_INCREMENT PRIMARY KEY,
 client_email varchar(35),
 client_mobile varchar (20),
 query_heading varchar(50),
 query_description text,
 status varchar(10),
 date_raised datetime,
 date_closed datetime
 );
select * from client;
SELECT * FROM client WHERE status = 'opened';
SELECT * FROM client WHERE status = 'closed';
delete from client where status = "null";

create table users (
   username varchar(35),
   hashed_password varchar(256),
   role ENUM("client","support"));

insert into users(username,hashed_password,role) values 
("testclient1",SHA2("Pooja@25",256),"client"),
("testsupport2",SHA2('Vicky@11',256),"support"),
("testsupport1",SHA2('Jan@0925',256),"support"),
("testsupport3",SHA2('Feb@1103',256),"support"),
("testsupport4",SHA2('March@11',256),"support"),
("testsupport5",SHA2('April@11',256),"support"),
("testsupport6",SHA2('May@1103',256),"support"),
("testsupport7",SHA2('June@0925',256),"support"),
("testsupport8",SHA2('July@0311',256),"support"),
("testsupport9",SHA2('Aug@11',256),"support"),
("testclient2",SHA2("Sun@025",256),"client"),
("testclient3",SHA2("Moon@1125",256),"client"),
("testclient4",SHA2("Star@0911",256),"client"),
("testclient5",SHA2("Ocean@20",256),"client"),
("testclient6",SHA2("Sea@2002",256),"client"),
("testclient7",SHA2("Bhuvi@25",256),"client"),
("testclient8",SHA2("Vignesh@25",256),"client"),
("testclient9",SHA2("Varsh@25",256),"client");

select * from users;






