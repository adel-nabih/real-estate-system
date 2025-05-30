-- Create the database
CREATE DATABASE IF NOT EXISTS real_estate_db;
USE real_estate_db;

-- Properties table
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    size INT NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    status ENUM('available', 'sold') DEFAULT 'available'
);

-- Clients table
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(100),
    preferences TEXT,
    broker_id INT,
    FOREIGN KEY (broker_id) REFERENCES brokers(id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Brokers table
CREATE TABLE IF NOT EXISTS brokers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    years_experience INT DEFAULT 0
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    client_id INT NOT NULL,
    broker_id INT NOT NULL,
    date DATE NOT NULL,
    final_price DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (broker_id) REFERENCES brokers(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(100) NOT NULL UNIQUE,
--     password_hash VARCHAR(255) NOT NULL,
--     role ENUM('admin', 'broker', 'client') NOT NULL
-- );

-- ALTER TABLE brokers
-- ADD COLUMN user_id INT UNIQUE,
-- ADD CONSTRAINT fk_broker_user FOREIGN KEY (user_id) REFERENCES users(id)
--     ON DELETE SET NULL ON UPDATE CASCADE;

-- ALTER TABLE clients
-- ADD COLUMN user_id INT UNIQUE,
-- ADD CONSTRAINT fk_client_user FOREIGN KEY (user_id) REFERENCES users(id)
--     ON DELETE SET NULL ON UPDATE CASCADE;

-- show tables;

-- ALTER TABLE users
-- ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- INSERT INTO users (username, password_hash, role) 
-- VALUES ('admin1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I6y', 'admin');