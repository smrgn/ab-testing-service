import streamlit as st
from app.analysis import aa_test_binary, aa_test_mean
from app.data_loader import load_data
import pandas as pd

def render_validation_screen():
    st.title("✅ Валидация метрик")
    st.markdown("""
    **Формат данных для корректной валидации**
    - Метрика расчитана по кажому пользователю (или единице рандомизации)
    - Отсутсвие пропусков
    - Обязательно название поля с метрикой - **metric** 
    - Разделитель для csv - ';'
    """)

    uploaded_file_validation = st.file_uploader("Загрузите файл", type=["csv", "xlsx"])

    if uploaded_file_validation:
        try:
            df = load_data(uploaded_file_validation)

            st.subheader("Предпросмотр данных")
            st.dataframe(df.head(3))
            if df.isnull().sum().sum() > 0:
                st.info("Предупреждение: В таблице есть пропущенные значения. Для более стабильного результата лучше перезапустить валидацию, исключив пропущенные значения")
            
            n_sim = st.number_input("Введите количество симуляций", value=10000, min_value=1000, max_value=100000)
            metric_type = st.selectbox("Выберите тип метрики", ["Бинарная", "Небинарная"])

            if st.button("Провалидировать метрику"):
                st.subheader("Результат валидации:")
            
                with st.spinner('Может потребоваться немного времени. Пожалуйста, подождите...'):
                    # Имитация длительного процесса (например, загрузка или обработка данных)
                    if metric_type == "Бинарная":
                        p_count, p_value, ci = aa_test_binary(df, n_sim) # Замените на реальный процесс, который должен быть выполнен
                    else:
                        p_count, p_value, ci = aa_test_mean(df, n_sim)

                # После завершения загрузки, выводим сообщение
                if 0.05 >= round(ci[0], 2) and 0.05 <= round(ci[1], 2):
                    st.success('Метрика прошла валидацию 👍🏼')
                else:
                    st.error('Метрика не прошла валидацию 😣')

                    st.markdown("""
                    <div style="background-color: #f0f8ff; padding: 1em; border-radius: 0.5em;">
                    <b>Рекомендуем:</b>
                    <ul>
                    <li>Убедитесь, что размер выборки достаточен для оценки стабильности метрики</li>
                    <li>Проверьте, нет ли смещений при разбиении на группы (например, по дате, платформе и т.п.)</li>
                    <li>Посмотрите на распределение метрики — возможно, она нестабильна или содержит выбросы</li>
                    <li>Рассмотрите альтернативную метрику, лучше отражающую поведение пользователей</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)


                # Подготовка данных
                results = {
                    "Показатель": [
                        "Количество случаев ложного прокраса теста",
                        "Уровень статистической значимости оценки",
                        "99%-процентный доверительный интервал для уровня статистической значимости"
                    ],
                    "Значение": [
                        p_count,
                        p_value,
                        ci
                    ]
                }

                # Преобразование в DataFrame
                df_results = pd.DataFrame(results)

                # Отображение данных в интерактивной таблице
                st.dataframe(df_results)

        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")

