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

def save_experiment_info(start_date, end_date, result):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Запрос на добавление записи в таблицу experiments_history
        query = """
            INSERT INTO experiments_history (start_date, end_date, result)
            VALUES (%s, %s, %s)
        """
        # Выполнение запроса
        cursor.execute(query, (start_date, end_date, result))

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

# Функция для получения топ 10 последних экспериментов
def get_top_10_experiments():
    conn = get_db_connection()
    query = """
        SELECT experiment_id, start_date, end_date, result
        FROM experiments_history
        ORDER BY start_date DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Функция для поиска эксперимента по ID
def get_experiment_by_id(experiment_id):
    conn = get_db_connection()
    query = """
        SELECT experiment_id, start_date, end_date, result
        FROM experiments_history
        WHERE experiment_id = %s;
    """
    df = pd.read_sql(query, conn, params=(experiment_id,))
    conn.close()
    return df