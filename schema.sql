-- Create database (this will work in Docker's MySQL initialization)
CREATE DATABASE IF NOT EXISTS notes_app;
USE notes_app;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create notes table
CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Optional: Insert sample data for testing
INSERT INTO users (username, password) VALUES 
('testuser', 'testpass'),
('demo', 'demo');

INSERT INTO notes (user_id, content) VALUES 
(1, 'This is my first note!'),
(1, 'Remember to dockerize the app'),
(2, 'Demo user note here');