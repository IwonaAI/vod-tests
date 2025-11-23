import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.movie_page import MoviePage
from utils import config


def test_playback_requires_login_modal(driver):
    home = HomePage(driver)
    home.go_to()

    home.search(config.SEARCH_PHRASE)

    results = SearchResultsPage(driver)
    results.open_first_result()

    movie = MoviePage(driver)
    player = movie.get_player()
    player.play()

    appeared = movie.wait_for_login_modal(timeout=config.LOGIN_MODAL_TIMEOUT)

    assert appeared, f"Expected login modal (restriction) to appear after starting playback for unauthenticated user within {config.LOGIN_MODAL_TIMEOUT}s"
