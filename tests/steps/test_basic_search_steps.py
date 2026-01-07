import re
import sys
from pathlib import Path

# Add project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.sync_api import Page, expect
from pytest_bdd import scenario, given, when, then, parsers
from tests.pages.home_page import HomePage


# Resolve the feature file path relative to this test file to avoid issues with different working directories
FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"


@scenario(str(FEATURES_DIR / "basic_search.feature"), "T1 - One way flight search")
def test_one_way_flight_search():
    pass


@given("As an not logged user navigate to homepage https://www.kiwi.com/en/")
def navigate_to_homepage(page: Page):
    home_page = HomePage(page)
    home_page.navigate()
    expect(page).to_have_url(home_page.url)


@when("I select one-way trip type")
def select_one_way_trip(page: Page):
    home_page = HomePage(page)
    home_page.select_one_way_trip()


@when("Set as departure airport RTM")
def set_departure_airport(page: Page):
    home_page = HomePage(page)
    home_page.set_departure_airport("RTM")


@when("Set the arrival Airport MAD")
def set_arrival_airport(page: Page):
    home_page = HomePage(page)
    home_page.set_arrival_airport("MAD")


@when(
    parsers.parse(
        'Set the departure time "{value:d}" {unit} in the future starting current date'
    )
)
def set_departure_time(page: Page, value, unit):
    home_page = HomePage(page)
    if unit == "week" or unit == "weeks":
        total_days = value * 7
    elif unit == "day" or unit == "days":
        total_days = value
    else:
        raise ValueError(
            f"Unsupported time unit: {unit}. Please use 'week(s)' or 'day(s)'."
        )
    home_page.set_departure_date(total_days)


@when("Uncheck the `Check accommodation with booking.com` option")
def uncheck_accommodation_option(page: Page):
    home_page = HomePage(page)
    home_page.uncheck_accommodation_option()


@when("Click the search button")
def click_search_button(page: Page):
    home_page = HomePage(page)
    home_page.click_search_button()


@then("I am redirected to search results page")
def redirected_to_search_results_page(page: Page):
    home_page = HomePage(page)
    expect(page).to_have_url(
        re.compile(r"^https://www\.kiwi\.com/en/search/results/.*$")
    )
    expect(home_page.search_results_list).to_be_visible()
