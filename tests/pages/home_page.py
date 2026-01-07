from playwright.sync_api import Page, Locator
import datetime
import re
from config import config
from test_data.airports import AIRPORT_MAPPINGS


class HomePage:
    """
    Page Object Model for Kiwi.com homepage.

    This class encapsulates all the interactions with the Kiwi.com homepage,
    including flight search functionality, date selection, and form submissions.
    """

    def __init__(self, page: Page) -> None:
        """
        Initialize HomePage with Playwright page instance.

        Args:
            page: Playwright Page object for browser interaction
        """
        self.page = page
        self.url = config.BASE_URL

    # Property-based locators (lazy loading - created when accessed)
    @property
    def privacy_popup_accept_button(self) -> Locator:
        """Privacy consent popup accept button."""
        return self.page.locator("[data-test='CookiesPopup-Accept']")

    @property
    def trip_type_dropdown(self) -> Locator:
        """Button to open trip type dropdown."""
        return self.page.get_by_role("button", name=re.compile(r"Return|One-way"))

    @property
    def one_way_option_in_dropdown(self) -> Locator:
        """One-way option in the trip type dropdown."""
        return self.page.locator("[data-test='ModePopupOption-oneWay']")

    @property
    def from_airport_input(self) -> Locator:
        """Departure airport input field."""
        return self.page.locator(
            "[data-test='PlacePickerInput-origin'] [data-test='SearchField-input']"
        )

    @property
    def to_airport_input(self) -> Locator:
        """Arrival airport input field."""
        return self.page.locator(
            "[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']"
        )

    @property
    def departure_date_input(self) -> Locator:
        """Departure date input field."""
        return self.page.locator("[data-test='SearchFieldDateInput']")

    @property
    def search_button(self) -> Locator:
        """Main search button."""
        return self.page.locator("[data-test='LandingSearchButton']")

    @property
    def clear_button_on_departure(self) -> Locator:
        """Clear button on departure airport input."""
        return self.page.locator(
            "div[data-test='PlacePickerInput-origin'] div[data-test='PlacePickerInputPlace-close']"
        )

    @property
    def clear_button_on_arrival(self) -> Locator:
        """Clear button on arrival airport input."""
        return self.page.locator(
            "div[data-test='PlacePickerInput-destination'] div[data-test='PlacePickerInputPlace-close']"
        )

    @property
    def search_results_list(self) -> Locator:
        """Search results list."""
        return self.page.locator("div[data-test='ResultList-results']")

    def navigate(self) -> None:
        """
        Navigate to the homepage and handle initial setup.

        Waits for the page to fully load and dismisses privacy consent popup.
        """
        self.page.goto(self.url)
        self.page.wait_for_load_state("load")
        self.accept_privacy_consent()

    def accept_privacy_consent(self) -> bool:
        """
        Dismiss the privacy consent popup if present.

        Returns:
            bool: True if popup was accepted, False if not found
        """
        try:
            # Check if popup is visible before trying to click
            if self.privacy_popup_accept_button.is_visible(timeout=5000):
                self.privacy_popup_accept_button.click(timeout=config.DEFAULT_TIMEOUT)
                return True
            else:
                print("Privacy consent popup not visible")
                return False
        except Exception as e:
            print(f"Error while accepting privacy consent: {e}")
            return False

    def select_one_way_trip(self) -> None:
        """Select one-way trip type from the dropdown."""
        self.trip_type_dropdown.click()
        self.one_way_option_in_dropdown.click()

    def set_departure_airport(self, airport_code: str) -> None:
        """
        Set departure airport using airport code.

        Args:
            airport_code: Three-letter airport code (e.g., 'RTM', 'MAD')

        Raises:
            ValueError: If airport code is not in the mappings
        """
        if airport_code not in AIRPORT_MAPPINGS:
            raise ValueError(f"Airport code '{airport_code}' not found in mappings")

        # Clear existing selection if any
        if self.clear_button_on_departure.is_visible():
            self.clear_button_on_departure.click()

        self.from_airport_input.click()
        self.from_airport_input.fill(airport_code)

        full_airport_name = AIRPORT_MAPPINGS[airport_code]
        airport_button = self.page.get_by_role(
            "button", name=f"{full_airport_name} Add"
        )
        airport_button.click()

    def set_arrival_airport(self, airport_code: str) -> None:
        """
        Set arrival airport using airport code.

        Args:
            airport_code: Three-letter airport code (e.g., 'RTM', 'MAD')

        Raises:
            ValueError: If airport code is not in the mappings
        """
        if airport_code not in AIRPORT_MAPPINGS:
            raise ValueError(f"Airport code '{airport_code}' not found in mappings")

        # Clear existing selection if any
        if self.clear_button_on_arrival.is_visible():
            self.clear_button_on_arrival.click()

        self.to_airport_input.click()
        self.to_airport_input.fill(airport_code)

        full_airport_name = AIRPORT_MAPPINGS[airport_code]
        airport_button = self.page.get_by_role(
            "button", name=f"{full_airport_name} Add"
        )
        airport_button.click()

    def set_departure_date(self, total_days: int) -> None:
        """
        Set departure date by adding days to current date.

        Args:
            total_days: Number of days to add to current date
        """
        self.departure_date_input.click()

        target_date = datetime.date.today() + datetime.timedelta(days=total_days)
        target_date_str = target_date.strftime("%Y-%m-%d")

        date_cell = self.page.locator(
            f"div[data-test='CalendarDay'][data-value='{target_date_str}']"
        )
        date_cell.click()

        set_dates_button = self.page.locator("[data-test='SearchFormDoneButton']")
        set_dates_button.click()

    def uncheck_accommodation_option(self) -> None:
        """Uncheck accommodation booking option if checked."""
        accommodation_checkbox = self.page.get_by_label(
            "Check accommodation with Kiwi.com Hotels"
        )
        if accommodation_checkbox.is_checked():
            checkbox_icon = self.page.locator(
                ".orbit-checkbox-icon-container > .orbit-icon"
            ).first
            checkbox_icon.click()

    def click_search_button(self) -> None:
        """Click the main search button to start flight search."""
        self.search_button.click()
