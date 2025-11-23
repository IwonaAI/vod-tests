# vod-tests

## Test API
Url: https://vod.film/search-route  

Status code: 200 OK  

Metoda: Post   

Uruchomienie: Aby uruchomić test należy znajdując się w docelowej ścieżce do pliku wpisać w terminalu komendę pytest test_api_vod.py  

Opis testu: Test odpytuje endpoint z frazą „the pickup”, sprawdza status code odpowiedzi i wyszukuje w ciele JSON dane filmu  

Problemy na które się natknęłam: Serwer wymagał nagłówka User-Agent, bez tego zwracany był błąd 403  

## Test E2E  

Projekt testów automatycznych E2E dla serwisu https://www.vod.film z wykorzystaniem Python + Selenium w konwencji Page Object Model (POM)  
Wybieram Selenium ze względu na większą prostotę i jego dłuższą obecność na rynku. Choć Playwright zyskuje coraz większą popularność na co również zwracam szczególną uwagę.

Uruchomienie:  

powershell  

python -m venv .venv  

.venv\Scripts\Activate.ps1  

pip install -r requirements.txt  

pytest -vv  


## Testowanie manualne – Raport błędu nr 1 

ID: jira-01-427  

Tytuł: Nie działa przycisk „Wyczyść”  

Opis: Po wejściu w zakładkę „Filmy” w miejscu sortowania filmów według wybranych kryteriów nie działa przycisk „Wyczyść” mający na celu resetowanie wyborów.  

Środowisko: Windows 10 Przeglądarka Chrome 142,  iOS Przeglądarka Safari 18  

Priorytet: Niski  

Kroki do reprodukcji:  

1.	Wejdź na stronę: https://vod.film/
   
2.	Kliknij w zakładkę „Filmy” na górze ekranu
   
3.	Kliknij poniżej w zakładkę „Sortuj wg.”
   
4.	Zaznacz losowy parametr, np. „Popularność rosnąco”
   
5.	Kliknij przycisk „Wyczyść”
    
Oczekiwany rezultat: Ptaszek oznaczający sortowanie według popularności rosnącej odznacza się i układ filmów wraca do początkowych pozycji.  

Rzeczywisty rezultat: Przycisk nie reaguje. Ptaszek zaznaczenia nie znika i układ filmów wyświetla się nadal według tego zaznaczenia.  

Osoba zgłaszająca: Iwona Gotowała  

Przypisane do: Frontend Developer  

Załącznik: Sortowanie.jpg  

	

## Testowanie manualne – Raport błędu nr 2  


ID: jira-01-428  

Tytuł: Zła kolejność wyświetlania filmów według kryteriów daty produkcji  

Opis: Po ustawieniu sortowania wyświetlania filmów według „Produkcji najnowszych” wyświetlają się filmy najstarsze z początków XX wieku. Analogicznie dzieje się w przypadku wyboru kryterium „Produkcje najstarsze”  

Środowisko: Windows 10 Przeglądarka Chrome 142,  iOS Przeglądarka Safari 18  

Priorytet: Niski  

Kroki do reprodukcji:  

1.	Wejdź na stronę: https://vod.film/
   
2.	Kliknij w zakładkę „Filmy” na górze ekranu
    
3.	Kliknij poniżej w zakładkę „Sortuj wg.”
   
4.	Wybierz opcję „Produkcje najnowsze”
   
Oczekiwany rezultat: Wyświetlają się najnowsze produkcje, czyli dodane w pobliżu bieżącego roku  

Rzeczywisty rezultat: Wyświetlają się najstarsze dostępne filmy na stronie  

Osoba zgłaszająca: Iwona Gotowała  

Przypisane do: Frontend/Backend Developer  

Załącznik: Produkcje.jpg  

## SQL  

Zapytanie SQL zależy od struktury bazy danych, czyli od tego jakie baza danych zawiera tabele i kolumny. Zakładając pewien typowy model:  

- film (film.id, film.title…)
  
- category (category.id, category.name…)
  
Zapytanie SQL będzie wyglądało następująco:  


SELECT  

  f.id AS film_id,  
  
  f.title AS film_title,  
  
  c.id AS category_id,  
  
  c.name AS category_name  
  
FROM film f  

JOIN film_category fc  

  ON f.id = fc.film_id  
  
JOIN category c  

  ON fc.category_id = c.id  
  
WHERE f.title = 'The Pickup';  

Opis kroków w zapytaniu  

•	Kroki to połączenie tabel film i film_category aby dostać powiązania między filmem a kategoriami.  

•	Następnie łączenie z tabelą kategorii żeby poznać nazwy kategorii.  

•	Na koniec filtrowanie po tytule filmu żeby sprawdzić tylko ten konkretny film  






