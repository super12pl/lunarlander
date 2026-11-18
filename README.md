Aplikacja konsolowa w C znajduje się w folderze ```sim```. \ 
W ```ui``` znajduje się aplikacja desktopowa obsługująca ```sim```, uruchamiana przez ```app.py```.\ 
W ```przykladowyWynik``` znajdują się wygenerowane w ```ui``` wykresy oraz plik csv.
# Syntax
```sim [m] [H_0] [v_0] [F_c] [nazwapliku] [timeflow]``` \
\
m, H_0, v_0, F_c: dane wejściowe dla symulacji, domyślnie: 2000, 500, 10, 4500 \
\
nazwapliku: nazwa docelowego pliku csv, domyślnie: ksiezycOutput.csv \
\
timeflow: opóźnienie w sekundach między wyświetleniami stanu lądownika, domyślnie: 0.2

# Wymagania aplikacji desktopowej
Python: Pyside6, Matplotlib

Używa pre-kompilowanej ```sim.exe```. Przed użyciem na systemie innym niż Windows trzeba skompilować ```sim.c``` jeszcze raz i zmienić path w linijce 86 w ```app.py```.
