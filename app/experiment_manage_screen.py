import streamlit as st
from data_loader import get_next_experiment_id, check_experiment_exists, insert_experiment_to_db, delete_experiment_from_db
from datetime import datetime, timedelta

def render_experiment_management_screen():
    st.title("🪄 Управление экспериментами")

    # Раздел для создания эксперимента
    st.subheader("Создать новый эксперимент")

    # Получаем следующий доступный experiment_id
    default_experiment_id = get_next_experiment_id()
    
    # Запрашиваем experiment_id у пользователя с проверкой
    experiment_id = st.number_input(
        "Введите ID эксперимента",
        min_value=1,
        value=default_experiment_id,
        step=1,
    )
    
    # Проверка, что эксперимент с таким ID еще не существует
    if check_experiment_exists(experiment_id):
        st.error(f"Эксперимент с ID {experiment_id} уже существует!")
    else:
        # Запрос даты начала и окончания
        start_date = st.date_input("Дата начала эксперимента", value=datetime.today().date())
        end_date = st.date_input("Дата окончания эксперимента", value=start_date + timedelta(days=7))
        
        # Проверка, что дата начала раньше даты окончания
        if start_date >= end_date:
            st.error("Дата начала не может быть позже или равной дате окончания.")
        else:
            # Запрос комментария
            your_comment = st.text_area("Комментарий (необязательно)", help="Пример: Ожидаем повышение конверсии после изменения кнопки на главной странице.")
            
            # Выбор статуса эксперимента
            result = "В процессе" if start_date > datetime.today().date() else "Дизайне"
            
            # Сохранение данных в базу данных
            if st.button("Создать эксперимент"):
                insert_experiment_to_db(experiment_id, start_date, end_date, result, your_comment)
                st.success(f"Эксперимент с ID {experiment_id} успешно создан!")

    # Раздел для удаления эксперимента
    st.subheader("Удалить эксперимент")
    experiment_id_delete = st.number_input("Введите ID эксперимента для удаления", min_value=1, step=1)

    # Проверка, существует ли эксперимент с таким ID
    if check_experiment_exists(experiment_id_delete):
        # Кнопка для удаления
        confirm_deletion = st.button(f"Удалить эксперимент с ID {experiment_id_delete}")
        
        if confirm_deletion:
            # Запрос на подтверждение удаления
            confirm = st.radio("Вы уверены, что хотите удалить этот эксперимент?", ["Нет", "Да"], key="confirm_radio")
            
            # Выполнение удаления только при подтверждении
            if confirm == "Да":
                delete_experiment_from_db(experiment_id_delete)
                st.success(f"Эксперимент с ID {experiment_id_delete} успешно удален!")
            elif confirm == "Нет":
                st.info("Удаление отменено.")
    else:
        st.error(f"Эксперимент с ID {experiment_id_delete} не найден.")
