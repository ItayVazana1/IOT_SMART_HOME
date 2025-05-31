-- Create the database (in case it's not created by environment variable)
CREATE DATABASE IF NOT EXISTS iot_data;

-- Use the correct database
USE iot_data;

-- Create the user with native password authentication
CREATE USER IF NOT EXISTS 'iotuser'@'%' IDENTIFIED WITH mysql_native_password BY 'iotpass';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON iot_data.* TO 'iotuser'@'%';
FLUSH PRIVILEGES;

-- Create the table
CREATE TABLE IF NOT EXISTS device_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_type VARCHAR(50),
    value TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
