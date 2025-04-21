-- Create Database
CREATE DATABASE IF NOT EXISTS criminal_record_db;
USE criminal_record_db;

-- User Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, 
    role ENUM('Admin', 'Director', 'Officer', 'Guest') NOT NULL DEFAULT 'Officer',
    status ENUM('Active', 'Inactive') NOT NULL DEFAULT 'Active', 
    description TEXT,
    delete_at TIMESTAMP DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Address Table of charged person
CREATE TABLE IF NOT EXISTS addresses ( -- ---------------------------------------------------------who data is this
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    district VARCHAR(100),
    commune VARCHAR(100),
    village VARCHAR(100),
    street_address VARCHAR(255),
    postal_code VARCHAR(50),
    country VARCHAR(100)
);

-- Charged Person Table
CREATE TABLE IF NOT EXISTS charged_persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    dob DATE NOT NULL,
    nationality VARCHAR(100),
    occupation VARCHAR(100),
    MaritalStatus VARCHAR(100),
    workplace VARCHAR(100),
    contact_info VARCHAR(100),
    birth_place INT,
    current_location INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    modified_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (birth_place) REFERENCES addresses(id) ON DELETE CASCADE,
    FOREIGN KEY (current_location) REFERENCES addresses(id) ON DELETE CASCADE,
    FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Case Information Table
CREATE TABLE IF NOT EXISTS cases (
    case_number INT NOT NULL PRIMARY KEY,
    category ENUM('Felony', 'Misdemeanor', 'Infraction') NOT NULL,
    status ENUM('Guilty', 'Innocent', 'Under Investigation') NOT NULL,
    arrest_date DATE NOT NULL,
    arrest_agency VARCHAR(100) NOT NULL,
    arrest_location int NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    arrest_time TIME NOT NULL
);
-- Relation Table: Cases and Charged Persons (Many-to-Many)
CREATE TABLE IF NOT EXISTS case_charged_persons (
    case_number INT NOT NULL,
    charged_person_id INT,
    description TEXT,
    PRIMARY KEY (case_number, charged_person_id),
    FOREIGN KEY (case_number) REFERENCES cases(case_number) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (charged_person_id) REFERENCES charged_persons(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Court Table (One-to-Many with Cases)
CREATE TABLE IF NOT EXISTS courts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_number INT,
    court_category ENUM('Trial', 'Supreme', 'Appeal') NOT NULL,
    court_decision ENUM('Guilty', 'Innocent', 'Pending') NOT NULL,
    court_date DATE NOT NULL,
    court_location INT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    modified_by INT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (modified_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (court_location) REFERENCES addresses(id) ON DELETE CASCADE,
    FOREIGN KEY (case_number) REFERENCES cases(case_number) ON DELETE CASCADE
);

-- Log Table to store user activities (One-to-Many with Users)
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action ENUM('Create', 'Update', 'Delete', 'Login', 'Logout') NOT NULL,
    detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for frequently queried fields
-- CREATE INDEX idx_card_number ON charged_persons(card_number);
-- CREATE INDEX idx_username ON users(username);
-- CREATE INDEX idx_case_status ON cases(status);
-- CREATE INDEX idx_court_decision ON courts(court_decision);
-- CREATE INDEX idx_action_user ON logs(action, user_id);  -- Log table index
