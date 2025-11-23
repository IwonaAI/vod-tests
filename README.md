# vod-tests

## Test API
Url: https://vod.film/search-route  

Status code: 200 OK  

Metoda: Post   

Uruchomienie: Aby uruchomić test należy znajdując się w docelowej ścieżce do pliku wpisać w terminalu komendę pytest test_api_vod.py  

Opis testu: Test odpytuje endpoint z frazą „the pickup”, sprawdza status code odpowiedzi i wyszukuje w ciele JSON dane filmu  

Problemy na które się natknęłam: Serwer wymagał nagłówka User-Agent, bez tego zwracany był błąd 403  

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




