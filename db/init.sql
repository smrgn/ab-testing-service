-- -- Создание таблицы "object_metrics"
-- CREATE TABLE object_metrics (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     description TEXT
-- );

-- -- Создание таблицы "users"
-- CREATE TABLE users (
--     id PRIMARY KEY,
--     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     name VARCHAR(255) NOT NULL,
--     surname VARCHAR(255) NOT NULL,
--     age INT,
--     birth_date DATE,
--     birth_place VARCHAR(255)
-- );

-- -- Создание таблицы "experiments"
-- CREATE TABLE experiments (
--     id SERIAL PRIMARY KEY,
--     user_id INT,
--     group_id INT,
--     num INT,
--     denom INT,
--     object_metric_id INT REFERENCES object_metrics(id),
--     entry_date TIMESTAMP
-- );

-- -- Создание таблицы "groups"
-- CREATE TABLE groups (
--     id SERIAL PRIMARY KEY,
--     experiment_id INT REFERENCES experiments(id),
--     amount INT,
--     create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     description TEXT
-- );

-- Создание таблицы "experiments_history"
CREATE TABLE experiments_history (
    experiment_id SERIAL PRIMARY KEY,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    result TEXT,
    your_comment TEXT
);
