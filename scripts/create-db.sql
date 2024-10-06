create database ecomdb;
use ecomdb;

create table Users (
    id int auto_increment not null,
    name varchar(100) not null,
    email varchar(100) unique not null,
    password varchar(255) not null,
    primary key (id)
);

insert into Users (name, email, password) values
("John Doe", "john@example.com", "password123"),
("Jane Smith", "jane@example.com", "password123"),
("Alice Johnson", "alice@example.com", "password123"),
("Bob Williams", "bob@example.com", "password123"),
("Charlie Brown", "charlie@example.com", "password123"),
("David Harris", "david@example.com", "password123"),
("Ella Davis", "ella@example.com", "password123"),
("Frank Wilson", "frank@example.com", "password123"),
("Grace Lee", "grace@example.com", "password123"),
("Henry Adams", "henry@example.com", "password123");
