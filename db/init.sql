-- Создание таблицы "metrics"
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Создание таблицы "experiments"
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    experiment_id INT,
    user_id INT,
    group_id INT,
    num INT,
    denom INT,
    metric_id INT REFERENCES metrics(id),
    entry_date TIMESTAMP
);

-- Создание таблицы "users"
CREATE TABLE users (
    id INT PRIMARY KEY,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    age INT,
    birth_date DATE,
    birth_place VARCHAR(255)
);

-- Создание таблицы "experiments_history"
CREATE TABLE experiments_history (
    id BIGINT PRIMARY KEY,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    result TEXT,
    your_comment TEXT
);

INSERT INTO users (id, name, surname, age, birth_date, birth_place)
VALUES
(1, 'Anna', 'Ivanova', 25, '1999-02-10', 'Moscow'),
(2, 'Dmitry', 'Petrov', 32, '1992-07-15', 'Saint Petersburg'),
(3, 'Olga', 'Smirnova', 28, '1996-01-05', 'Novosibirsk'),
(4, 'Sergey', 'Volkov', 35, '1989-09-21', 'Kazan'),
(5, 'Natalia', 'Fedorova', 30, '1994-06-30', 'Yekaterinburg'),
(6, 'Alexey', 'Popov', 27, '1997-08-12', 'Omsk'),
(7, 'Maria', 'Sokolova', 29, '1995-11-03', 'Ufa'),
(8, 'Ivan', 'Kuznetsov', 33, '1991-12-25', 'Chelyabinsk'),
(9, 'Elena', 'Lebedeva', 26, '1998-05-19', 'Rostov-on-Don'),
(10, 'Pavel', 'Morozov', 31, '1993-03-17', 'Perm'),
(11, 'Tatiana', 'Nikolaeva', 24, '2000-07-22', 'Voronezh'),
(12, 'Roman', 'Semenov', 36, '1988-04-04', 'Volgograd'),
(13, 'Irina', 'Alekseeva', 27, '1997-10-14', 'Krasnoyarsk'),
(14, 'Vladimir', 'Makarov', 34, '1990-02-28', 'Tyumen'),
(15, 'Svetlana', 'Egorova', 25, '1999-08-18', 'Barnaul'),
(16, 'Anton', 'Vinogradov', 29, '1995-09-09', 'Sochi'),
(17, 'Yulia', 'Belova', 28, '1996-06-11', 'Khabarovsk'),
(18, 'Nikolay', 'Bogdanov', 30, '1994-12-30', 'Irkutsk'),
(19, 'Victoria', 'Koroleva', 23, '2001-01-20', 'Astrakhan'),
(20, 'Andrey', 'Zaitsev', 32, '1992-10-06', 'Tomsk'),
(21, 'Alina', 'Orlova', 26, '1998-03-02', 'Tula'),
(22, 'Maksim', 'Gusev', 35, '1989-11-11', 'Kaliningrad'),
(23, 'Ksenia', 'Medvedeva', 24, '2000-12-01', 'Vladivostok'),
(24, 'Egor', 'Belyaev', 31, '1993-05-27', 'Kirov'),
(25, 'Anastasia', 'Loginova', 27, '1997-07-08', 'Bryansk'),
(26, 'Ilya', 'Sorokin', 30, '1994-09-16', 'Saratov'),
(27, 'Daria', 'Komarova', 29, '1995-02-06', 'Ivanovo'),
(28, 'Stepan', 'Andreev', 33, '1991-06-13', 'Orenburg'),
(29, 'Polina', 'Ermolova', 28, '1996-08-29', 'Kostroma'),
(30, 'Artem', 'Kiselev', 25, '1999-04-23', 'Lipetsk'),
(31, 'Veronika', 'Zhukova', 26, '1998-10-19', 'Murmansk'),
(32, 'Oleg', 'Grigoriev', 34, '1990-01-15', 'Yakutsk'),
(33, 'Ekaterina', 'Solovieva', 27, '1997-03-31', 'Petrozavodsk'),
(34, 'Timofey', 'Romanov', 30, '1994-11-07', 'Smolensk'),
(35, 'Lyudmila', 'Dmitrieva', 28, '1996-05-03', 'Kurgan'),
(36, 'Viktor', 'Afanasev', 35, '1989-07-12', 'Arkhangelsk'),
(37, 'Valeria', 'Shestakova', 25, '1999-09-25', 'Magnitogorsk'),
(38, 'Yaroslav', 'Borisov', 32, '1992-02-18', 'Chita'),
(39, 'Zoya', 'Kovaleva', 29, '1995-06-06', 'Pskov'),
(40, 'Kirill', 'Tikhonov', 31, '1993-08-16', 'Tambov');

INSERT INTO metrics (name, description)
VALUES
('conversion_rate', 'Доля пользователей, совершивших целевое действие (например, покупку) от общего числа пользователей.'),
('average_value', 'Среднее значение числового показателя, например, среднего чека или средней продолжительности сессии.'),
('ratio_metric', 'Отношение двух показателей, например, выручка на одного пользователя (ARPU) или количество покупок на визит.');

INSERT INTO experiments_history (id, start_date, end_date, result, your_comment)
VALUES
(6042025, '2024-01-10 09:00:00', '2024-01-20 18:00:00', 'Метрика увеличилась', 'Использовали персонализированные пуш-уведомления.'),
(6042026, '2024-02-01 10:00:00', '2024-02-10 17:00:00', 'Метрика не изменилась', 'Контроль и тест имели схожие значения, эффект отсутствует.'),
(6042027, '2024-03-05 08:30:00', '2024-03-15 19:00:00', 'Метрика увеличилась', 'Изменён порядок отображения товаров в каталоге.'),
(6042028, '2024-04-01 12:00:00', '2024-04-11 16:00:00', 'Метрика уменьшилась', 'Добавлены рекламные баннеры — повлияли негативно.'),
(6042029, '2024-05-10 11:00:00', '2024-05-20 18:30:00', 'Метрика не изменилась', 'Тестировали автозапуск видео на главной.'),
(6042030, '2024-06-01 09:00:00', '2024-06-10 18:00:00', 'Метрика увеличилась', 'Обновлена справочная информация на экране оплаты.'),
(6042031, '2024-06-15 10:30:00', '2024-06-25 17:00:00', 'Метрика увеличилась', 'Добавлены платные функции в мобильном приложении.'),
(6042032, '2024-07-01 08:00:00', '2024-07-10 18:00:00', 'Метрика не изменилась', 'Низкий объём выборки, повторный запуск запланирован.'),
(6042033, '2024-08-01 13:00:00', '2024-08-12 15:30:00', 'Метрика увеличилась', 'Обновлён сценарий онбординга новых пользователей.'),
(6042034, '2024-09-05 14:00:00', '2024-09-15 18:30:00', 'Метрика уменьшилась', 'Удалены некоторые подсказки в интерфейсе — негативный эффект.');
