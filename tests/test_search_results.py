from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils import config


def test_search_returns_results(driver):
    home = HomePage(driver)
    home.go_to()

    home.search(config.SEARCH_PHRASE)

    results_page = SearchResultsPage(driver)
    items = results_page.wait_for_results(minimum=1, timeout=35)

    assert items, "Expected at least one search result for configured SEARCH_PHRASE"

