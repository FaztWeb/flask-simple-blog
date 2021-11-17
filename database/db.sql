CREATE DATABASE blogdb;

USE blogdb;

CREATE TABLE users(
	id INT(11) AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100),
	username VARCHAR(30),
	password VARCHAR(100),
	email VARCHAR(100),
	register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts(
	id INT(11) AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(225),
	author VARCHAR(100),
	content TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
