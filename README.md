# Saucedemo Playwright Automation Testing Project

A web automation testing framework based on Playwright and pytest for testing the Swag Labs e-commerce website.

## Project Features

- Browser automation using Playwright
- Page Object Model (POM) design pattern
- Multi-browser parallel testing support
- Automatic retry mechanism for improved test stability
- Integrated Allure test reporting
- Data-driven testing support

## Tech Stack

- **Playwright** 1.48.0 - Browser automation framework
- **pytest** 8.3.4 - Testing framework
- **pytest-xdist** 3.6.1 - Parallel testing
- **allure-pytest** 2.15.3 - Test reporting
- **pytest-rerunfailures** 16.1 - Test retry mechanism
- **pytest-ordering** 0.6 - Test order control
- **PyYAML** 6.0.2 - Configuration file parsing

## Project Structure

```
saucedemo_playwright/
├── base/                  # Base classes
│   └── base.py            # BasePage and BaseHandle base classes
├── page/                  # Page Object Model
│   ├── login_page.py      # Login page
│   ├── home_page.py       # Home page
│   ├── cart_page.py       # Shopping cart page
│   └── swag_labs.py       # Swag Labs common page
├── scripts/               # Test scripts
│   ├── test_login.py      # Login tests
│   └── test_shopping.py   # Shopping flow tests
├── utility/               # Utility classes
│   ├── driver_factory.py  # Browser driver factory
│   └── data_reader.py     # Data reading utilities
├── data/                  # Test data
│   ├── test_login.json
│   ├── test_login_failed.json
│   └── test_add_to_cart.json
├── conftest.py            # pytest configuration
├── environment.yaml       # Environment configuration
├── pytest.ini             # pytest configuration file
└── requirements.txt       # Python dependencies
```

## Requirements

- Python 3.8+
- Chrome / Edge / Firefox browsers

## Installation Steps

### 1. Clone the Project

```bash
git clone <repository-url>
cd saucedemo_playwright
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

## Configuration

### Environment Configuration (environment.yaml)

```yaml
web:
  url: "https://www.saucedemo.com/"

browser:
  enabled:
    - chrome
    - edge
    - firefox
  parallel:
    enabled: true
    workers: auto
```

**Configuration Options:**
- `web.url`: Target website URL for testing
- `browser.enabled`: List of enabled browsers
- `browser.parallel.enabled`: Whether to enable parallel testing
- `browser.parallel.workers`: Number of parallel worker processes (auto or specific number)

### Pytest Configuration (pytest.ini)

```ini
[pytest]
addopts = -s -v --reruns 2 --reruns-delay 3 --alluredir=allure-results --tb=short --color=no
testpaths = ./scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Configuration Options:**
- `--reruns 2`: Retry tests 2 times on failure
- `--reruns-delay 3`: Wait 3 seconds between each retry
- `--alluredir=allure-results`: Allure report output directory

## Running Tests

### Basic Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest scripts/test_login.py

# Run specific test class
pytest scripts/test_shopping.py::TestShopping

# Run specific test method
pytest scripts/test_shopping.py::TestShopping::test_login
```

### Headless Mode

```bash
pytest --headless
```

### Parallel Testing

```bash
# Use 3 parallel processes
pytest -n 3

# Use auto-detected CPU cores
pytest -n auto
```

### Combined Usage

```bash
# Headless mode + parallel testing + clean reports + generate report + open report
Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue; pytest -n 3 --headless; allure generate ./allure-results -o ./report --clean; allure open ./report
```

## Test Reports

### Generate Allure Report

```bash
# Generate HTML report
allure generate ./allure-results -o ./report --clean

# Open report
allure open ./report
```

### View Historical Reports

```bash
allure serve ./allure-results
```

## Page Object Model Design

The project adopts a three-layer POM architecture:

### 1. Page Layer (BasePage)
Defines page element locators

```python
class LoginPage(BasePage):
    def find_username_input(self) -> Locator:
        return self.get_element("#user-name")
```

### 2. Handle Layer (BaseHandle)
Encapsulates page operations

```python
class LoginHandle(BaseHandle):
    def input_username(self, username: str):
        self.input_text(self.login_page.find_username_input(), username)
```

### 3. Proxy Layer
Encapsulates business logic

```python
class LoginProxy:
    def login(self, username: str, password: str):
        self.login_handle.input_username(username)
        self.login_handle.input_password(password)
        self.login_handle.click_login_button()
```

## Data-Driven Testing

Use JSON files to store test data:

```json
{
  "test_case_1": {
    "username": "standard_user",
    "password": "secret_sauce"
  }
}
```

Usage in tests:

```python
@pytest.mark.parametrize("username, password", get_json_data("data/test_login.json"))
def test_login(self, username, password):
    self.login_proxy.login(username, password)
```

## FAQ

### 1. Network Connection Error (net::ERR_CONNECTION_RESET)

The project is configured with an automatic retry mechanism that retries 2 times with a 3-second interval by default. If the issue persists, please check your network connection or increase the retry count.

### 2. Test Execution Order Issues

Use the `pytest-ordering` plugin to control test execution order:

```python
@pytest.mark.run(order=1)
def test_login(self):
    pass

@pytest.mark.run(order=2)
def test_add_goods_to_cart(self):
    pass
```

