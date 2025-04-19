import streamlit as st
from app.data_loader import get_experiment_by_id, get_top_10_experiments

def render_history_screen():
    st.title("История экспериментов")

    # Выбор между топ 10 последних экспериментов и поиском по ID
    option = st.radio("Выберите действие", ["Топ 10 последних экспериментов", "Поиск по ID"])

    if option == "Топ 10 последних экспериментов":
        # Получаем топ 10 последних экспериментов и отображаем их
        top_10_experiments = get_top_10_experiments()
        if top_10_experiments.empty:
            st.write("Нет данных о последних экспериментах.")
        else:
            st.write("Топ 10 последних экспериментов:")
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
