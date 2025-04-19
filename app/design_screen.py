import streamlit as st
from app.analysis import calculate_sample_size_mean, calculate_sample_size_proportion

# 🎯 Основной интерфейс страницы
def render_design_screen():
    st.title("📐 Дизайн A/B-теста")

    st.markdown("Задайте параметры эксперимента, чтобы рассчитать нужный объем выборки для каждой группы")

    # === Шаг 1: Уровень значимости и мощность ===
    st.markdown("### Общие параметры эксперимента")

    col1, col2 = st.columns(2)
    with col1:
        alpha = st.slider("Уровень значимости (α)", 0.01, 0.2, 0.05, step=0.01)
    with col2:
        power = st.slider("Мощность теста (1 - β)", 0.5, 0.99, 0.8, step=0.01)

    # st.divider()

    # === Шаг 2: Выбор типа метрики ===
    st.markdown("### Выбор типа метрики")
    col1, col2 = st.columns(2)
    with col1:
        metric_type = st.radio("Тип метрики", ["Конверсия", "Среднее", "Отношения (ratio)"])
    with col2:
        compare_count = st.selectbox("Выберите количество сравнений", [1, 2, 3, 4, 5, 6])
        if compare_count >= 3:
            st.warning("🚨 Будет достаточно сложно отловить эффект, \
                       убедитесь, что такое количество сравнений необходимо!")

    if compare_count >= 2:
        alpha /= compare_count

    # === Шаг 4: Динамический ввод параметров и расчёт ===
    if metric_type == "Среднее":
        # st.subheader("Параметры метрики типа 'Среднее'")
        mean = st.number_input("Базовое значение метрики", value=100.0)
        std_dev = st.number_input("Стандартное отклонение", value=20.0, min_value=0.01)
        mde = st.number_input("Абсолютный mde", value=5.0, min_value=0.01)

        if st.button("Рассчитать размер выборки"):
            size = calculate_sample_size_mean(std_dev, mde, alpha, power)
            st.success(f"🔹 Рекомендуемый размер выборки на группу: **{size} пользователей**")

    elif metric_type == "Конверсия":
        # st.subheader("Параметры метрики типа 'Конверсия'")
        baseline = st.number_input("Базовая конверсия (%)", value=15.0, max_value=100.0)
        mde = st.number_input("Абсолютный MDE (разница в %-пунктах)", value=1.0, min_value=0.01)

        p1 = baseline / 100
        p2 = (baseline + mde) / 100

        if st.button("Рассчитать размер выборки"):
            size = calculate_sample_size_proportion(p1, p2, alpha, power)
            st.success(f"🔹 Рекомендуемый размер выборки на группу: **{size} пользователей**")

    elif metric_type == "Отношения (ratio)":
        # st.subheader("Параметры метрики типа 'Ratio'")
        st.error(f"🚨 Перед расчетом объема выборки, метрику необходимо линеаризовать, и считать стандартное отклонение после преобразования")
        mean_ratio = st.number_input("Базовое значение метрики (ratio)", value=25.0, min_value=0.01)
        std_ratio = st.number_input("Стандартное отклонение (после линеаризации)", value=0.5, min_value=0.01)
        mde = st.number_input("Абсолютный mde", value=1.0, min_value=0.01)

        if st.button("Рассчитать размер выборки"):
            size = calculate_sample_size_mean(std_ratio, mde, alpha, power)
            st.success(f"🔹 Рекомендуемый размер выборки на группу: **{size} пользователей**")