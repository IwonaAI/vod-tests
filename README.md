# vod-tests

## Test API:
Url: https://vod.film/search-route  

Status code: 200 OK  

Metoda: Post   

Uruchomienie: Aby uruchomić test należy znajdując się w docelowej ścieżce do pliku wpisać w terminalu komendę pytest test_api_vod.py  

Opis testu: Test odpytuje endpoint z frazą „the pickup”, sprawdza status code odpowiedzi i wyszukuje w ciele JSON dane filmu  

Problemy na które się natknęłam: Serwer wymagał nagłówka User-Agent, bez tego zwracany był błąd 403  


