"""
Configuration management for Kiwi test framework.

This module handles loading configuration from environment variables and .env files.
It provides a centralized Config class for accessing test settings with type-safe
defaults and validation.

Environment File Search Order:
    If TEST_ENV is set (e.g., TEST_ENV=staging):
    1. ``env/staging.env``
    2. ``staging.env``

    Then fallback to:
    3. ``env/test.env``
    4. ``test.env``
    5. ``.env``

Usage:
    from config import config

    # Access configuration values
    page.goto(config.BASE_URL)

    # Debug configuration
    config.print_config()
"""

import os
import warnings
from pathlib import Path
from dotenv import load_dotenv


def _load_environment() -> None:
    """
    Load environment variables from .env files based on TEST_ENV.

    Searches for environment files in order of specificity, loading the
    first one found. Uses override=True to ensure environment-specific
    values take precedence over system environment variables.
    """
    test_env = os.getenv("TEST_ENV")

    candidate_paths = []

    if test_env:
        candidate_paths.extend(
            [
                Path("env") / f"{test_env}.env",
                Path(f"{test_env}.env"),
            ]
        )

    candidate_paths.extend(
        [
            Path("env") / "test.env",
            Path("test.env"),
            Path(".env"),
        ]
    )

    for env_path in candidate_paths:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
            return

    # Fallback to default search (respects DOTENV_* env vars)
    load_dotenv()


_load_environment()


def _get_env_bool(name: str, default: bool = False) -> bool:
    """
    Safely parse a boolean environment variable.

    Accepts: '1', 'true', 'yes', 'on' (case-insensitive) as True
             '0', 'false', 'no', 'off' (case-insensitive) as False

    Args:
        name: Environment variable name
        default: Default value if not set or invalid

    Returns:
        bool: Parsed boolean value
    """
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    warnings.warn(
        f"Invalid boolean value for {name}: {raw_value!r}. Using default {default}",
        RuntimeWarning,
        stacklevel=2,
    )
    return default


def _get_env_int(name: str, default: int) -> int:
    """
    Safely parse an integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set or invalid

    Returns:
        int: Parsed integer value
    """
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError:
        warnings.warn(
            f"Invalid integer value for {name}: {raw_value!r}. Using default {default}",
            RuntimeWarning,
            stacklevel=2,
        )
        return default


class Config:
    """
    Configuration class for test environment settings.

    All values are loaded from environment variables with sensible defaults.
    Can be overridden via .env files or system environment variables.
    """

    # Base URL for the application under test
    # Override via BASE_URL env var for different environments
    BASE_URL: str = os.getenv("BASE_URL", "https://www.kiwi.com/en/")

    # Timeouts in milliseconds
    # Default: 15 seconds for most operations
    DEFAULT_TIMEOUT: int = _get_env_int("DEFAULT_TIMEOUT", 15000)

    # Browser configuration
    # Set HEADLESS=true for CI/CD environments
    HEADLESS: bool = _get_env_bool("HEADLESS", False)
    # Supported: chromium, firefox, webkit
    DEFAULT_BROWSER: str = os.getenv("DEFAULT_BROWSER", "chromium")

    # Test data directory path (relative to project root)
    TEST_DATA_PATH: str = os.getenv("TEST_DATA_PATH", "test_data")

    @classmethod
    def print_config(cls) -> None:
        """
        Print current configuration for debugging.

        Useful for troubleshooting environment-specific issues or verifying
        which configuration values are being used during test execution.

        Example:
            python -c "from config import config; config.print_config()"
        """
        print("=== Test Configuration ===")
        print(f"TEST_ENV: {os.getenv('TEST_ENV', '<not-set>')}")
        print(f"BASE_URL: {cls.BASE_URL}")
        print(f"DEFAULT_TIMEOUT: {cls.DEFAULT_TIMEOUT}")
        print(f"HEADLESS: {cls.HEADLESS}")
        print(f"DEFAULT_BROWSER: {cls.DEFAULT_BROWSER}")
        print(f"TEST_DATA_PATH: {cls.TEST_DATA_PATH}")
        print("===========================")


# Create a singleton instance
config = Config()
