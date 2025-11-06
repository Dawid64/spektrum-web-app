# Plant Chamber Web App

## Uruchamianie

1. Na komputerze docelowym "terminalu" (tak się nazywa komputer) jeśli nie ma repozytorium to je pobrać: `git clone <link do repo>`.
2. Wejść do repozytorium i pobrać wszystkie zależności (jeśli narzędzie uv nie jest zainstalowane to należy pobrać wpierw je): 
    ```sh
    cd spektrum-web-app
    uv sync
    ```
3. Następnie należy wejść do katalogu `src` i z uprawnieniami administratora uruchomić plik `streamlit_app.py` przy użyciu streamlit'a
    ```sh
    sudo ../.venv/bin/python -m streamlit run streamlit_app.py
    ```
4. Następnie w terminalu powinny wyświetlić się linki do strony na local host'cie (najpewniej na porcie 8501), należy w nie wejść - streamlit jest nie raz dość kapryśny i potrafi nie uruchomić ChamberManager'a przed pierwszym wejściem na stronę.
5. Ostatnim krokiem będzie wejście na stronie w `settings` i zmienić porty do arduino dla każdej z komor na wybrane docelowe porty dla arduino (nie powinny się pokrywać, każda komora, powinna mieć wybrany inny port)



TODO: opisać proces uruchamiania

## Info

### Co działa?

- Baza danych przechowująca informacje na temat ustawień parametrów (bez portu do arduino) oraz wyników pomiarów
- Zmiana parametrów komory - Użytkownik może dowolnie zmieniać parametry komory - są one zapisywane w bazie danych i od następnej komendy arduino czasy np.: światła zostaną zmienione
- Połączenie z arduino (po wybraniu odpowiedniego portu w ustawieniach komory)

### Co nie działa?

- pyarrow - błąd z binarkami blokuje dużą część funkcjonalności streamlit'a
  - autoryzacja
  - labelling
  - wyświetlanie wykresów
- brak połączenia z Raspberry PI - brak wybranych sterowników
