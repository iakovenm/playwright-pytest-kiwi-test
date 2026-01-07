# Kiwi.com Flight Search Automation

An automated test framework for Kiwi.com search functionality, built with Python, Playwright, and Pytest using Behavior-Driven Development (BDD) principles.

## Project Structure

```
tests/
├── features/             # Gherkin feature files
│   └── basic_search.feature
├── pages/                # Page Object Model definitions
│   └── home_page.py
└── steps/                # Step definitions for Gherkin scenarios
    └── test_basic_search_steps.py
test_data/                # Test data and mappings
├── airports.py
env/                      # Environment-specific configuration
config.py                 # Configuration loader
conftest.py               # Pytest configuration and fixtures
pytest.ini                # Pytest settings
.github/
└── workflows/
    └── playwright.yml    # GitHub Actions CI/CD workflow
Dockerfile                # Dockerfile for containerization
requirements.txt          # Python dependencies
README.md                 # Project README
```

## Getting Started

### Prerequisites

- Python 3.8+ (tested with Python 3.14.2)
- pip (Python package installer)
- (Optional) Docker for containerized execution
- (Optional) Allure commandline for test reporting (requires Java 8+)

### Installation

1.  **Install Python (if needed):**

    Check if Python is installed:

    ```powershell
    python --version
    ```

    If Python is not installed or the version is below 3.8, download and install it:

    **Option 1: Using Scoop (recommended for Windows)**

    ```powershell
    # Install Scoop if not already installed
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    iex "& {$(irm get.scoop.sh)} -RunAsAdmin"

    # Install Python
    scoop install python

    # Verify installation
    python --version
    pip --version
    ```

    **Option 2: Official Installer**

    - Visit [python.org/downloads](https://www.python.org/downloads/)
    - Download Python 3.8 or higher
    - Run the installer and **check "Add Python to PATH"**
    - Verify installation by running `python --version` in a new terminal

2.  **Clone the repository:**

    ```powershell
    git clone <copy ssh or https link to the repo from github >
    cd <location where repo was cloned>
    ```

3.  **Install Python dependencies:**

    ```powershell
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**

    ```powershell
    python -m playwright install
    ```

5.  **Configure environment variables:**

    The framework uses environment variables for configuration. You can set them via:

    - System environment variables
    - `.env` files (placed in project root or `env/` directory)

    **Environment File Search Order:**

    1. `env/<TEST_ENV>.env` (if TEST_ENV is set, e.g., `env/staging.env`)
    2. `<TEST_ENV>.env` (if TEST_ENV is set, e.g., `staging.env`)
    3. `env/test.env`
    4. `test.env`
    5. `.env`

    **Switch Environments:**

    ```powershell
    # If there were multiple environments switch env is possible via setting env variables from terminal
    $env:TEST_ENV="staging"
    python -m pytest
    ```

    **Available Configuration Variables:**

    - `BASE_URL` - Application URL (default: `https://www.kiwi.com/en/`)
    - `HEADLESS` - Run browser in headless mode (default: `false`)
    - `DEFAULT_TIMEOUT` - Timeout in milliseconds (default: `15000`)
    - `DEFAULT_BROWSER` - Browser to use: chromium, firefox, webkit (default: `chromium`)
    - `TEST_DATA_PATH` - Test data directory (default: `test_data`)

## How to Run Tests

### Run All Tests

To run all tests in the suite:

```powershell
python -m pytest
```

### Run Specific Test Cases

#### By Marker

If a test scenario in the feature file is tagged (e.g., `@smoke`, `@one_way`), you can run it using the `-m` flag:

```powershell
python -m pytest -m smoke
python -m pytest -m one_way
```

Available markers:

- `smoke` - Critical path smoke tests
- `one_way` - One-way flight search tests
- `basic_search` - Basic search functionality tests

**Note:** Markers are defined in `pytest.ini` and can be applied to scenarios using tags in `.feature` files (e.g., `@smoke`, `@one_way`).

#### By File and Scenario Name

You can also specify the test file and the scenario function directly:

```powershell
python -m pytest tests/steps/test_basic_search_steps.py::test_one_way_flight_search
```

#### By Keyword

Run tests matching a keyword in the test name:

```powershell
python -m pytest -k "one_way"
```

### Run Tests in Headless/Headed Mode

Set the `HEADLESS` environment variable or configure it in your `.env` file:

```powershell
# Set for current session
$env:HEADLESS="true"
python -m pytest

# Or in one line
$env:HEADLESS="true"; python -m pytest
```

**Note:** By default, tests run in headless mode. The `HEADLESS` environment variable overrides the browser launch configuration for more control over test runs on specific environments.

## Docker Integration

The project includes Docker support for running tests in an isolated, reproducible environment with all dependencies pre-configured.

### Prerequisites

**Install Docker (if needed):**

Check if Docker is installed:

```powershell
docker --version
```

If Docker is not installed, choose one of the following options:

**Option 1: Docker Engine with WSL 2 (Lightweight, No GUI)**

This option doesn't require Docker Desktop and uses fewer resources:

```powershell
# Step 1: Install WSL 2 (if not already installed)
wsl --install

# Step 2: Restart your computer

# Step 3: Install a Linux distribution (e.g., Ubuntu)
wsl --install -d Ubuntu

# Step 4: Launch Ubuntu from Start Menu and set up username/password

# Step 5: Inside Ubuntu terminal, install Docker Engine
sudo apt-get update
sudo apt-get install -y docker.io

# Step 6: Start Docker service
sudo service docker start

# Step 7: Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Step 8: Exit and reopen Ubuntu terminal

# Step 9: Verify Docker works
docker --version
docker run hello-world
```

**To use Docker from PowerShell with WSL:**

```powershell
# Run Docker commands via WSL
wsl docker --version
wsl docker build -t tests .
wsl docker run tests
```

**Option 2: Using Scoop (recommended for Windows)**

```powershell
# Install Docker Desktop via Scoop
scoop bucket add extras
scoop install docker-desktop

# Start Docker Desktop from Start Menu or:
start-process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

**Option 3: Official Installer (Docker Desktop)**

1. Visit [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download Docker Desktop for Windows
3. Run the installer
4. Restart your computer when prompted
5. Launch Docker Desktop from Start Menu
6. Wait for Docker Engine to start (check system tray icon)

**Verify Installation:**

```powershell
# Check Docker version
docker --version

# Test Docker is running
docker run hello-world
```

**Note:**

- Docker Desktop requires Windows 10/11 Pro, Enterprise, or Education with Hyper-V enabled, or Windows Home with WSL 2
- Docker Engine with WSL 2 (Option 1) works on all Windows versions and uses fewer resources

### Build the Docker Image

**If using Docker Desktop or direct Docker access:**

```powershell
docker build -t tests .
```

**If using Docker Engine with WSL:**

```powershell
wsl docker build -t tests .
```

### Run Tests in a Docker Container

**If using Docker Desktop or direct Docker access:**

To run all tests in the Docker container:

```powershell
docker run tests
```

To run a specific test (e.g., by marker) in the Docker container:

```powershell
docker run tests pytest -m basic_search
```

**If using Docker Engine with WSL:**

```powershell
# Run all tests
wsl docker run tests

# Run specific marker
wsl docker run tests pytest -m basic_search
```

## Test Reporting with Allure

This project uses Allure Framework for beautiful, interactive test reports with BDD step visualization, screenshots, and execution history.

### Prerequisites

Allure requires Java Runtime Environment (JRE) 8 or higher. We'll install both Java and Allure using Scoop (Windows package manager).

### Installation on Windows

#### Step 1: Install Scoop (if not already installed)

Open PowerShell and run:

```powershell
# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Install Scoop
iex "& {$(irm get.scoop.sh)} -RunAsAdmin"

# Verify installation
scoop --version
```

#### Step 2: Install Java (required for Allure)

```powershell
# Add Java bucket
scoop bucket add java

# Install OpenJDK
scoop install openjdk

# Set JAVA_HOME permanently
[Environment]::SetEnvironmentVariable("JAVA_HOME", "$HOME\scoop\apps\openjdk\current", "User")

# Verify Java installation
java -version
```

#### Step 3: Install Allure

```powershell
# Install Allure
scoop install allure

# Verify Allure installation (restart terminal first)
allure --version
```

**Important:** After installation, **restart your PowerShell terminal** or open a new one for the PATH changes to take effect.

### Generate and View Reports

#### Option 1: Run Tests and View Report Immediately

```powershell
# Run tests and generate report data
python -m pytest --alluredir=allure-results

# Generate and open report in browser (starts local server)
allure serve allure-results
```

This will:

- Generate the HTML report
- Start a local web server
- Automatically open the report in your default browser

Press `Ctrl+C` in the terminal to stop the server.

#### Option 2: Generate Static HTML Report

```powershell
# Run tests
python -m pytest --alluredir=allure-results

# Generate static HTML report
allure generate allure-results -o allure-report --clean

# Open in browser
start allure-report/index.html
```

The static report can be shared by uploading the `allure-report` folder to a web server.

### Run Tests with Specific Markers

```powershell
# Smoke tests with report
python -m pytest -m smoke --alluredir=allure-results
allure serve allure-results

# Regression tests with report
python -m pytest -m regression --alluredir=allure-results
allure serve allure-results
```

## CI/CD with GitHub Actions

This project is configured with GitHub Actions for continuous integration. The workflow defined in `.github/workflows/playwright.yml` automatically runs tests on `push` and `pull_request` events to the `main` branch.

### Workflow Details

The `playwright.yml` workflow performs the following steps:

1.  **Checkout Code:** Retrieves the project code from the repository.
2.  **Setup Python:** Configures Python 3.14.2 environment.
3.  **Install Dependencies:** Installs Python packages from `requirements.txt` and Playwright browsers.
4.  **Run Playwright Tests:** Executes all tests with Allure reporting (`--alluredir=allure-results`).
5.  **Upload Allure Results:** Uploads test results as artifacts (30-day retention).
6.  **Get Allure History:** Retrieves previous report history from `gh-pages` branch for trend analysis.
7.  **Generate Allure Report:** Creates HTML report with historical data.
8.  **Deploy to GitHub Pages:** Publishes report to GitHub Pages for public access.

### View Reports

After the workflow completes, you can:

- **Download artifacts:** Go to Actions → Workflow run → Artifacts → `allure-results`
- **View online report:** Visit `https://<username>.github.io/<repo-name>/` (requires GitHub Pages to be enabled)

### Enable GitHub Pages

To view reports online:

1. Go to repository **Settings** → **Pages**
2. Set **Source** to "Deploy from a branch"
3. Select **Branch**: `gh-pages` and `/` (root)
4. Click **Save**

The report will be available at `https://<username>.github.io/<repo-name>/` after the next workflow run.

## Configuration Details

### Environment Variables

All configuration is managed through the `config.py` module, which loads values from environment variables or `.env` files:

| Variable          | Default                    | Description                                      |
| ----------------- | -------------------------- | ------------------------------------------------ |
| `TEST_ENV`        | (not set)                  | Environment identifier (e.g., `staging`, `prod`) |
| `BASE_URL`        | `https://www.kiwi.com/en/` | Application URL to test                          |
| `HEADLESS`        | `false`                    | Run browser in headless mode                     |
| `DEFAULT_TIMEOUT` | `15000`                    | Timeout in milliseconds                          |
| `DEFAULT_BROWSER` | `chromium`                 | Browser: chromium, firefox, or webkit            |
| `TEST_DATA_PATH`  | `test_data`                | Directory for test data files                    |

### Debug Configuration

To verify your current configuration:

```powershell
python -c "from config import config; config.print_config()"
```

Output example:

```
=== Test Configuration ===
TEST_ENV: staging
BASE_URL: https://staging.kiwi.com/en/
DEFAULT_TIMEOUT: 15000
HEADLESS: True
DEFAULT_BROWSER: chromium
TEST_DATA_PATH: test_data
===========================
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/<feature name>`)
3. Commit changes (`git commit -m 'Add <feature description>'`)
4. Push to the branch (`git push origin feature/<feature name>`)
5. Open a Pull Request
