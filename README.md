Project documentation with instructions and an overview.

markdown
Kopiuj
# Discord Bot - Turnieje Typerskie

## Opis projektu
Ten projekt to bot Discord służący do obsługi turniejów typerskich. Uczestnicy mogą zgłaszać swoje kupony, zdobywać punkty oraz sprawdzać swój ranking. Bot zawiera również panel administracyjny dla organizatorów, własną komendę pomocy oraz integrację z The Odds API.

## Funkcje
- **Zgłaszanie kuponów:** Walidacja formatu, weryfikacja ról, ograniczenie do jednego zgłoszenia dziennie, obliczanie punktów.
- **Ranking i profil:** Komendy `!topka` oraz `!profil` wyświetlają ranking i profil użytkownika.
- **Statystyki:** Panel administracyjny z podsumowaniem turnieju (`!podsumowanie`).
- **Rozszerzona pomoc:** Komenda `!help` wyświetla czytelną listę komend.
- **Integracja z The Odds API:** Komenda `!odds` umożliwia pobieranie kursów sportowych.
- **Bezpieczeństwo:** System anty-oszukańczy oraz precyzyjna weryfikacja danych z linków.

## Struktura projektu
discord-bot/ ├── cogs/ │ ├── admin.py │ ├── championship.py │ ├── help.py │ └── odds.py ├── .gitignore ├── Procfile ├── README.md ├── bot.py ├── requirements.txt └── utils.py

markdown
Kopiuj

## Jak uruchomić bota
1. Sklonuj repozytorium.
2. Utwórz plik `.env` z zawartością:
DISCORD_TOKEN=twoj_token_bota GUILD_ID=twoje_id_serwera ODDS_API_KEY=twój_klucz_api_odds # Opcjonalnie, jeśli chcesz nadpisać domyślny

go
Kopiuj
3. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
Uruchom bota:
bash
Kopiuj
python bot.py
Wdrożenie na Heroku
Upewnij się, że plik Procfile jest poprawnie skonfigurowany. Heroku uruchomi bota poleceniem:

makefile
Kopiuj
worker: python bot.py
Wymagane biblioteki
discord.py==2.3.2
python-dotenv==1.0.0
PyJWT==2.8.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9 # For PostgreSQL
pytz==2023.3.post1 # For timezone handling
requests==2.31.0 # Dla integracji z The Odds API
Licencja
Projekt dostępny jest na licencji MIT.
