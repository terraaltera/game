# Wersja angielska (en.html)

`en.html` jest generowany z `index.html` – nie edytuj go ręcznie.

    python3 tools/i18n/build_en.py   # tworzy en.html
    python3 tools/i18n/scan_en.py    # pokazuje literały, które mogły zostać po polsku

Tłumaczenia: `cand.json` + `tr/b*.json` (indeks → tekst), `tr2.json` (tekst → tekst),
wyrażenia regularne i poprawki kodu w `build_en.py` (REG, POST), pomoc w `help_en.html`.
Nowy polski tekst w `index.html` trzeba dopisać do `tr2.json` (albo do słownika w `build_en.py`).
