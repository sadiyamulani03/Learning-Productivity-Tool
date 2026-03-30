CREATE DATABASE LearningProductivityDB;
USE LearningProductivityDB;
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
); 
CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_subject_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE study_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    duration FLOAT NOT NULL,
    focus_level INT NOT NULL CHECK (focus_level BETWEEN 1 AND 10),
    difficulty_level INT NOT NULL CHECK (difficulty_level BETWEEN 1 AND 5),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_session_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE,

    CONSTRAINT fk_session_subject
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    ON DELETE CASCADE
);
CREATE TABLE productivity_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_hours FLOAT DEFAULT 0,
    avg_focus FLOAT DEFAULT 0,
    productivity_score FLOAT DEFAULT 0,
    best_study_hour INT,
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_metric_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE fatigue_analysis (
    fatigue_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    fatigue_score FLOAT NOT NULL,
    fatigue_level VARCHAR(20) NOT NULL,
    analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fatigue_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_hours FLOAT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_goal_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    total_hours FLOAT,
    avg_focus FLOAT,
    productivity_score FLOAT,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_report_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Unread',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_notification_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    theme VARCHAR(20) DEFAULT 'Light',
    reminder_time TIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_setting_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
CREATE TABLE settings_new (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    theme VARCHAR(20) DEFAULT 'Light',
    reminder_time TIME,
    notify_goal TINYINT DEFAULT 1,
    notify_fatigue TINYINT DEFAULT 1,
    notify_study TINYINT DEFAULT 1,
    auto_logout INT DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_setting_user_new
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);
SELECT * FROM users;



create database sppu;
use sppu;
create table Teacher(TNO int primary key,
 Tname varchar(50), 
 sal int, 
 subj varchar(30),
 desg varchar(3));
 alter table Teacher add mblNo int;
 drop table Teacher;


