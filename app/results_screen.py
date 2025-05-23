import streamlit as st
import pandas as pd
from app.analysis import run_ab_test
from app.data_loader import load_data, save_experiment_info

def render_results_screen():
    st.title("📊 Результаты A/B-теста")
    st.markdown("""
    **Формат данных для корректного расчета**
    - Метрика расчитана по кажому пользователю (или единице рандомизации)
    - Отсутсвие пропусков
    - Обязательные поля - **group (значения 0 и 1)**, **metric**
    - Если ratio метрика, то дополнительно обязательны поля **num**, **denom**
    - Разделитель для csv - ';'
    """)

    uploaded_file_result = st.file_uploader("Загрузите CSV или Excel с метриками", type=["csv", "xlsx"])

    if uploaded_file_result:
        try:
            df = load_data(uploaded_file_result)

            st.subheader("Предпросмотр данных")
            st.dataframe(df.head(3))

            test_type = st.radio("Выберите критерий", ["t-test", "z-test", "t-test с линеаризацией (для ratio)"])

            if 'group' in df.columns and 'metric' in df.columns:
                st.subheader("📈 Анализ различий между группами")
                if st.button('Рассчитать результаты'):
                    p_value = 0
                    stats, p_value, a, b = run_ab_test(df, test_type)
                    if p_value <= 0.05 and b - a > 0:
                        st.success(f'Различия статистически значимы')
                    elif p_value <= 0.05 and b - a < 0:
                        st.error(f'Различия статистически значимы')
                    else:
                        st.info(f'Статистически значимых различий нет')
                    # Подготовка данных
                    results = {
                        "Показатель": [
                            "p-value",
                            "Значение статистики",
                            "Значение метрики в контроле",
                            "Значение метрики в эксперименте",
                            "Абсолютная разница",
                            "Относительная разница"
                        ],
                        "Значение": [
                            round(p_value, 2),
                            round(stats, 2),
                            a,
                            b,
                            b - a,
                            100.00 - (b * 100.00 / a)
                        ]
                    }

                    # Преобразование в DataFrame
                    df_results = pd.DataFrame(results)

                    # Отображение данных в интерактивной таблице
                    st.dataframe(df_results)

                if st.button('Сохранить полученные результаты'):
                    start_date = st.date_input('Введите дату начала эксперимента')
                    end_date = st.date_input('Введите дату окончания эксперимента')
                    if st.button('Сохранить'):
                        save_experiment_info(start_date, end_date, df_results)
                        st.success('Результат сохранен!')
                    
            else:
                st.error("Файл должен содержать столбцы 'group' и 'metric'")

        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")
