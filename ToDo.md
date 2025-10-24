# Plan

## Wstępny plan

Fajnie jest mieć uporządkowany kod oraz dostępy do wszystkiego do czego się potrzebuje, więc w pierwszej kolejności tym bym się zajał. Jedną z rzeczy na poczatek byłoby zebranie wszystkich informacji potrzebnych do działań deweloperskich (może być to robione na równi z wstępną przebudową aplikacji).

1. Przeniesienie wszystkiego na Github'a pod odpowiednią organizacje, wtedy łatwo zadbać żeby wszystko było w jednym miejscu i każdy miał do wszystkiego dostęp czego potrzebuje.
2. Każdy projekt w pythonie powinien być łatwy do rekreacji, z doświadczenia najbardziej polecam wszystkim narzędzie do kontroli projektu `uv`, to jest odpowiednik `pip`'a, `poetry` czy `conda`'y, ale działa setki razy szybciej. Z tym narzędziem uruchomienie projektu to są 2 komendy nie zależnie na jakim komputerze to się robi.

## Aplikacja do obsługi komory

1. Stworzyć klasę w pythonie do obsługi (połączenia z arduino i rpi)
2. Stworzyć klasę do łączenia się z bazą danych
3. Stworzyć graficzny interfejs użytkownika
   1. Strona główna = dashboard
   2. Strona do zarządzania komorą
   3. Strona do administracji użytkownikami (kto ma dostęp do zarządzania komorą)
   4. Strona do przeglądania i tagowania zdjęć
4. Sporządzić prostą dokumentację techniczną (w pliku README.md)
5. Upewnić się że strona poprawnie działa i łączy się z komorą
6. Sieciowy dostęp do aplikacji?

## Model AI

1. Zebrać wszystkie informacje na temat celu projektu, możliwości modeli i obecnym state-of-the-art w tym temacie.
2. Tagowanie wszystkich obecnie posiadanych obrazków **[Nie techniczne]**
3. Wstępny trening modelu na posiadanym zbiorze danych i porównanie go z obecnie posiadanym starym modelem
4. Zautomatyzowanie uczenia się modelu na podstawie zbieranych danych
