CREATE USER 'mp3_app'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE mp3_data;
USE 'mp3_app';

GRANT ALL ON mp3_data.* TO 'mp3_app'@'localhost';
