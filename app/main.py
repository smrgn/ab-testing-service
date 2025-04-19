import streamlit as st

from app.home_screen import render_home_screen
from app.design_screen import render_design_screen
from app.validation_screen import render_validation_screen
from app.results_screen import render_results_screen
from app.faq_screen import render_faq_screen
from app.history_screen import render_history_screen
from app.experiment_create_screen import render_experiment_create_screen

st.set_page_config(page_title="Сервис автоматизации A/B-тестирования", layout="wide")

# Инициализация состояния
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Главная"

# Отображение меню
menu = st.sidebar.radio("Меню", [
    "🏠 Главная",
    "🪄 Создать эксперимент",
    "📐 Дизайн эксперимента",
    "✅ Валидация метрик",
    "📊 Анализ результатов",
    "📚 История экспериментов",
    "ℹ️ FAQ"
], index=["🏠 Главная", "🪄 Создать эксперимент", "📐 Дизайн эксперимента", "✅ Валидация метрик", "📊 Анализ результатов", "📚 История экспериментов", "ℹ️ FAQ"].index(st.session_state.menu))

# Обновляем активную вкладку
st.session_state.menu = menu

# Отображение нужного экрана
if menu == "🏠 Главная":
    render_home_screen()
elif menu == "🪄 Создать эксперимент":
    render_experiment_create_screen()
elif menu == "📐 Дизайн эксперимента":
    render_design_screen()
elif menu == "✅ Валидация метрик":
    render_validation_screen()
elif menu == "📊 Анализ результатов":
    render_results_screen()
elif menu == "📚 История экспериментов":
    render_history_screen()
elif menu == "ℹ️ FAQ":
    render_faq_screen()