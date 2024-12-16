import streamlit as st

# Tytuł aplikacji
st.set_page_config(page_title="Moja aplikacja Streamlit", page_icon=":guardsman:", layout="wide")

# Tytuł strony głównej
st.title("Witaj w mojej aplikacji Streamlit!")

# Dodaj możliwość nawigacji do innych stron
#st.sidebar.title("Nawigacja")
pages = {
    "Strona 2": "pages/analiza_userstory.py",
}

#selection = st.sidebar.radio("Wybierz stronę:", list(pages.keys()))

# Ładuj i uruchom wybrany plik z katalogu 'pages'
#with open(pages[selection]) as page_file:
#    exec(page_file.read())
