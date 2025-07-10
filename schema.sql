CREATE DATABASE notes_app;

USE notes_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


-- freesqldatabase.com

-- 1. Drop existing foreign key constraint
ALTER TABLE notes DROP FOREIGN KEY notes_ibfk_1;

-- 2. Add new foreign key constraint with ON DELETE CASCADE
ALTER TABLE notes
ADD CONSTRAINT fk_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
