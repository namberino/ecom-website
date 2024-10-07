create database ecomdb;
use ecomdb;

create table Users (
    id int auto_increment not null,
    name varchar(100) not null,
    email varchar(100) unique not null,
    password varchar(255) not null,
    role varchar(10) not null,
    primary key (id)
);
