import pandas as pd
import psycopg2
import os
import streamlit as st

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "abtest"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file, sep=';')
    else:
        return pd.read_excel(file, engine='openpyxl')

# Проверка существования эксперимента с таким id
def check_experiment_exists(experiment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM experiments_history WHERE id = %s", (experiment_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Получить доступный experiment_id из базы данных
def get_next_experiment_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM experiments_history")
    result = cursor.fetchone()
    conn.close()
    return result[0] + 1 if result[0] else 1

def insert_experiment_to_db(experiment_id, start_date, end_date, result, your_comment):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO experiments_history (id, start_date, end_date, result, your_comment) VALUES (%s, %s, %s, %s, %s)",
        (experiment_id, start_date, end_date, result, your_comment)
    )
    conn.commit()
    conn.close()

# Функция для удаления эксперимента по ID
def delete_experiment_from_db(experiment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM experiments_history WHERE id = %s", (experiment_id,))
    conn.commit()
    conn.close()

def save_experiment_info(id, start_date, end_date, result, your_comment):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Запрос на добавление записи в таблицу experiments_history
        query = """
            INSERT INTO experiments_history (id, start_date, end_date, result, your_comment)
            VALUES (%s, %s, %s)
        """
        # Выполнение запроса
        cursor.execute(query, (id, start_date, end_date, result, your_comment))
        # Фиксируем изменения в базе данных
        conn.commit()
        print("Результат эксперимента успешно сохранен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()

# Функция для получения топ 5 последних экспериментов
def get_top_5_experiments():
    conn = get_db_connection()
    try:
        # Основной запрос
        query = """
            SELECT id, start_date, end_date, result, your_comment
            FROM experiments_history
            ORDER BY start_date DESC
            LIMIT 5;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Ошибка при выполнении запроса:", e)
        return pd.DataFrame()  # Вернуть пустой DataFrame, чтобы не упасть на .empty
    finally:
        conn.close()

# Функция для поиска эксперимента по ID
def get_experiment_by_id(experiment_id):
    conn = get_db_connection()
    try:
        query = """
            SELECT id, start_date, end_date, result, your_comment
            FROM experiments_history
            WHERE id = %s;
        """
        df = pd.read_sql(query, conn, params=(experiment_id,))
        return df
    except Exception as e:
        print("Ошибка при выполнении запроса:", e)
        return pd.DataFrame()  # Вернуть пустой DataFrame, чтобы не упасть на .empty
    finally:
        conn.close()