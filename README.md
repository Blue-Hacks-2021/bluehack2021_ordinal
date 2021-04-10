# bluehack2021_ordinal

## Pre-requisites:

- Python 3.9.X
- pip
- XAMPP for MySQL

---

## Testing

1. Clone github repository

2. Install pipenv via pip.

$ pip3 install pipenv

4. Run your virtual environment via pipenv.

$ pipenv shell

7. Run the server.

$ flask run

## Manual Development

### MySQL (MariaDB)

1. Create MySQL database with root user (for testing).

$ mysql -u root
$ CREATE DATABASE ordinaldb;

2. Go in ordinaldb;

$ mysql> USE ordinaldb;

3. Create Tables using these queries

```CREATE TABLE userdata(
userid INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
username VARCHAR(30) NOT NULL,
middlename VARCHAR(30),
pass varchar(30) NOT NULL,
city varchar(255),
province varchar(255),
email varchar(50) NOT NULL,
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
```
$CREATE TABLE Recruitment(
    eventid INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    userid INT(6) UNSIGNED NOT NULL,
    title VARCHAR(30) NOT NULL,
    description VARCHAR(30) NOT NULL,
    volunteerno INT NOT NULL,
    postdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    city VARCHAR(255),
    province VARCHAR(255),
    FOREIGN KEY(userid) REFERENCES userdata(userid),
    start_date DATETIME,
    end_date DATETIME
);
```
```
CREATE TABLE Comments(
commentid INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
eventid INT(6) UNSIGNED NOT NULL,
commenttext Text NOT NULL,
comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY(eventid) REFERENCES Recruitment(eventid)
);
```
```
CREATE TABLE Friends(userid int(6) unsigned not null, friendid int(6) unsigned not null, friendship_date timestamp default current_timestamp on update current_timestamp);
```
```
CREATE TABLE Reply(
replyid INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
commentid INT(6) UNSIGNED NOT NULL,
replytext Text NOT NULL,
replydate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY(commentid) REFERENCES comments(commentid)
);
```
```
CREATE TABLE Volunteers(
    userid INT(6) UNSIGNED NOT NULL,
    eventid INT(6) UNSIGNED NOT NULL,
    FOREIGN KEY(eventid) REFERENCES Recruitment(eventid)
);
```
```
INSERT INTO userdata (firstname, lastname, username, middlename, pass, city, province, email) VALUES ('Stephen', 'Craigg', 'scraigg', 'Raba', 'pass123', 'San Mateo', 'Rizal', 'scr@email.com') , ('Frances', 'Calunod', 'fcalunod', 'Villa', 'pass123', 'Tanza', 'Cavite', 'fcv@email.com') , ('Alyza', 'Taray', 'ataray', 'Cruz', 'pass123', 'Marikina', 'Metro Manila', 'atc@email.com');
```
```
INSERT INTO Friends (userid, friendid) VALUES (1, 2), (1, 3), (2, 1), (3, 1);
```
```
INSERT INTO Recruitment (userid, title, description, volunteerno, city, province, start_date, end_date) VALUES (1, 'Agapay', 'Bagyo sa San Mateo', 5000, 'San Mateo', 'Rizal', '2021-04-30 12:00:00', '2021-04-30 18:00:00'), (1, 'Bangon Marikeno', 'Bagyo
 sa Marikina', 5000, 'Marikina', 'Metro Manila', '2021-04-30 12:00:00', '2021-04-30 18:00:00'), (3, 'Hawak Kamay', 'Bagyo sa Laguna', 10000, 'Sta. Rosa', 'Laguna', '2021-04-30 12:00:00', '2021-04-30 18:00:00');
```
```
INSERT INTO Comments (eventid, commenttext) VALUES (3, 'Saan po meeting place?'),  (1, 'May dress code or motif po ba tayo?'), (2, 'Do you cover transportation?');
```
```
INSERT INTO Reply (commentid, replytext) VALUES (1, 'Sa San Mateo National High School po'), (2, 'meron po, blue and white'), (3, 'unfortunately no po');
```
