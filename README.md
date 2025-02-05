# Discord Bot - Prosty Turniej Typerski

## Opis projektu
To jest prosty bot Discord do turnieju typerskiego. Użytkownicy posiadający rolę **"Zweryfikowany"** mogą zgłaszać swoje kupony raz dziennie, podając liczbę punktów i link. Bot sumuje punkty, umożliwia sprawdzenie rankingu oraz oferuje kalkulator punktów. Dodatkowo, właściciel bota ma dostęp do zaawansowanych poleceń kontroli.

## Komendy użytkowników
- **!kupon [punkty] [link]** – dodaje zgłoszenie kuponu (tylko raz dziennie)
- **!ranking** – wyświetla aktualny ranking punktowy
- **!kalkulator [typ] [odds] [kwota]** – oblicza punkty wg zasad:
  - Zakład SOLO: mnożnik 1 (lub 2, jeśli odds > 10.0)
  - Zakład AKO: mnożnik 2.5 (lub 5, jeśli odds > 10.0)
  - Przykład: !kalkulator AKO 11.0 50 → 250 punktów
- **!help** – wyświetla listę dostępnych komend

## Komendy właściciela (zaawansowana kontrola)
- **!shutdown** – wyłącza bota
- **!reload [nazwa_modulu]** – przeładowuje wskazany moduł
- **!status** – pokazuje status bota

## Jak uruchomić bota
1. Sklonuj repozytorium.
2. Utwórz plik **.env** z zawartością:
