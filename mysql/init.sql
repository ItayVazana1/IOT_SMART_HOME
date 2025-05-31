-- ==========================================
-- 🗄️ Database & User Setup for IoT Project
-- ==========================================

-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS iot_data;

-- Switch to the newly created (or existing) database
USE iot_data;

-- ==========================================
-- 👤 User Configuration
-- ==========================================

-- Drop existing user if it exists (helps reset plugin/auth if needed)
DROP USER IF EXISTS 'iotuser'@'%';

-- Recreate the user with mysql_native_password (required for compatibility)
CREATE USER 'iotuser'@'%' IDENTIFIED WITH mysql_native_password BY 'iotpass';

-- Grant full permissions to the user on the iot_data database
GRANT ALL PRIVILEGES ON iot_data.* TO 'iotuser'@'%';

-- Apply changes immediately
FLUSH PRIVILEGES;

-- ==========================================
-- 📋 Table Definition
-- ==========================================

-- Create the device_data table if it doesn't exist
CREATE TABLE IF NOT EXISTS device_data (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique ID for each record
    device_type VARCHAR(50),                 -- Type of device (e.g., dht, light)
    value TEXT,                              -- Sensor reading or value
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- Auto-filled timestamp
);
