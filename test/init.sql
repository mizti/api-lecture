CREATE TABLE student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    interest JSON,
    description TEXT
);

CREATE TABLE lecture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    professor VARCHAR(255) NOT NULL,
    credits INT NOT NULL,
    description TEXT
);
