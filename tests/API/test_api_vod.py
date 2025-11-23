import unittest
import requests

class TestApiVod(unittest.TestCase):
    def setUp(self):
        self.url = "https://vod.film/search-route"
        self.headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json, text/plain, */*',
            'User-Agent': 'Chrome/142.0.0.0'
        }
        self.payload = {
            "host": "vod.film",
            "locale": "pl",
            "searchTerm": "the pickup"
        }

    def test_search_route(self):
        response = requests.post(self.url, json=self.payload, headers=self.headers)
    
        self.assertEqual(response.status_code, 200, "Status code is not 200")

        data = response.json().get('data', [])
        self.assertGreater(len(data), 0, "No data returned in response")

        movie = data[0]
        self.assertIn('title', movie, "Missing 'title' field in response")
        self.assertIn('slug', movie, "Missing 'slug' field in response")
        self.assertIn('overview', movie, "Missing 'overview' field in response")
        self.assertIn('release_date', movie, "Missing 'release_date' field in response")

        self.assertEqual(movie['title'], "The Pickup Cały Film", "Movie title is incorrect")
        self.assertEqual(movie['title_with_prefix'], "The Pickup VOD • Online Cały Film", "Movie title with prefix is incorrect")
        self.assertEqual(movie['slug'], "the-pickup-caly-film", "Movie slug is incorrect")
        self.assertEqual(movie['overview'], "Odbiór gotówki zmienia się w wyścig na śmierć i życie. Dwóch nietypowych ochroniarzy, Russell i Travis, wpada w zasadzkę bezwzględnych rabusiów. Przewodzi im przebiegła Zoe. Wszystko wymyka się spod kontroli a ochroniarze muszą się zmierzyć z niebezpieczeństwem, konfliktem osobowości i trudnym do ogarnięcia rozwojem zdarzeń.", "Movie overview is incorrect")
        
        
if __name__ == "__main__":
    unittest.main()