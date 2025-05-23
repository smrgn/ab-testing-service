import streamlit as st
from app.data_loader import get_experiment_by_id, get_top_5_experiments, delete_experiment_from_db, check_experiment_exists

def render_history_screen():
    st.title("История экспериментов")

    # Выбор между топ 10 последних экспериментов и поиском по ID
    option = st.radio("Выберите действие", ["Топ 5 последних экспериментов", "Поиск по ID"])

    if option == "Топ 5 последних экспериментов":
        # Получаем топ 10 последних экспериментов и отображаем их
        top_10_experiments = get_top_5_experiments()
        if top_10_experiments.empty:
            st.write("Нет данных о последних экспериментах.")
        else:
            st.write("Топ 5 последних экспериментов:")
            st.dataframe(top_10_experiments)

    elif option == "Поиск по ID":
        # Ввод ID эксперимента
        experiment_id = st.number_input("Введите ID эксперимента", min_value=1)
        if st.button("Поиск"):
            # Получаем эксперимент по ID
            experiment = get_experiment_by_id(experiment_id)
            if experiment.empty:
                st.write(f"Эксперимент с ID {experiment_id} не найден.")
            else:
                st.write(f"Эксперимент с ID {experiment_id}:")
                st.dataframe(experiment)

    # Кнопка для удаления эксперимента
    st.subheader("Удалить эксперимент")
    experiment_id_delete = st.number_input("Введите ID эксперимента для удаления", min_value=2025, step=1)

    # Проверка, существует ли эксперимент с таким ID
    if check_experiment_exists(experiment_id_delete):
        # Кнопка для удаления
        confirm_deletion = st.button(f"Удалить эксперимент с ID {experiment_id_delete}")
        
        if confirm_deletion:
            # Предупреждение перед удалением
            confirm = st.radio("Вы уверены, что хотите удалить этот эксперимент?", ["Да", "Нет"])
            
            if confirm == "Да":
                delete_experiment_from_db(experiment_id_delete)
                st.success(f"Эксперимент с ID {experiment_id_delete} успешно удален!")
            else:
                st.info("Удаление отменено.")
    else:
        st.error(f"Эксперимент с ID {experiment_id_delete} не найден.")