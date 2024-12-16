# Projekt Streamlit AI-Action-FrontEnd

## Opis

Jest to aplikacja Streamlit, która umożliwia interakcję z JIRA API. Aplikacja wykorzystuje dane z JIRA i pozwala na ich wizualizację lub manipulację w prosty sposób. Aplikacja jest uruchamiana za pomocą pliku `app.py` i korzysta z zmiennych środowiskowych do bezpiecznego zarządzania tokenami API.

## Struktura Katalogów


## Instalacja

### 1. Zainstaluj wymagane biblioteki

Zanim uruchomisz aplikację, musisz zainstalować wymagane pakiety. Możesz to zrobić, uruchamiając poniższe polecenie:

```bash
pip install -r requirements.txt
```
### 2. Utwórz plik .env
W projekcie znajduje się zmienna środowiskowa JIRA_API_TOKEN, która jest potrzebna do autoryzacji w JIRA API. Utwórz plik .env w głównym katalogu projektu i dodaj swój token API:
JIRA_API_TOKEN=twoj_token_api_jira


### 3. Uruchom aplikację
Aby uruchomić aplikację Streamlit, użyj polecenia:

```bash
streamlit run app.py
```

### Wymagania
Aby uruchomić aplikację, musisz mieć zainstalowane następujące pakiety:

Streamlit – do budowy aplikacji webowej.
python-dotenv – do ładowania zmiennych środowiskowych z pliku .env.
requests – do interakcji z JIRA API.
pandas – do przetwarzania danych.



### Wyjaśnienie:

1. **Instalacja**:
   - Instrukcje, jak zainstalować wymagane biblioteki z pliku `requirements.txt` za pomocą polecenia `pip install -r requirements.txt`.
   - Tworzenie pliku `.env`, który zawiera zmienną środowiskową `JIRA_API_TOKEN` potrzebną do autoryzacji w JIRA API.

2. **Uruchomienie aplikacji**:
   - Użytkownik powinien uruchomić aplikację za pomocą komendy `streamlit run app.py`.

3. **Zmienna środowiskowa**:
   - Plik `.env` zawiera zmienną `JIRA_API_TOKEN`, której aplikacja potrzebuje do działania z JIRA API. Plik `.env` jest ignorowany przez Git, więc dane pozostają bezpieczne.

4. **Struktura aplikacji**:
   - Opisuje strukturę katalogów i plików, w tym katalog `pages` zawierający różne strony aplikacji.

Mam nadzieję, że plik `README.md` jest zgodny z Twoimi oczekiwaniami! Jeśli chcesz dodać jakiekolwiek dodatkowe szczegóły, daj znać.
