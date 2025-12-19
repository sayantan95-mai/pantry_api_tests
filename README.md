# FakeAPI Testing Framework

A robust API automation testing framework built with **Python** and **Pytest**. This project targets the [PantryCloud API](https://getpantry.cloud/) to demonstrate CRUD (Create, Read, Update, Delete) testing capabilities, dynamic payload generation, and automated HTML reporting.

## 🚀 Key Features

* **API Testing:** Full coverage of HTTP methods (GET, POST, PUT, DELETE) using the `requests` library.
* **Pytest Framework:** Utilizes fixtures for setup/teardown and efficient test management.
* **Dynamic Data:** Generates unique basket names and payloads using `uuid` to prevent data collision during tests.
* **HTML Reporting:** Automatically generates timestamped HTML reports for every test run using `pytest-html`.
* **Dependency Management:** Managed via `pyproject.toml` (compatible with `pip` and `uv`).

## 📂 Project Structure

```text
fakeapi-testing/
├── api_call/
│   └── pantry.py             # API wrapper functions (Endpoints & Logic)
├── tests/
│   ├── conftest.py           # Pytest fixtures and hooks (Reporting config)
│   └── test_pantry_details.py # Actual test cases
├── reports/                  # Generated HTML reports (Created automatically)
├── main.py                   # Entry point script
├── pyproject.toml            # Project dependencies and config
├── uv.lock                   # Lock file (if using uv)
└── README.md                 # Project documentation

Here is a step-by-step guide on how to execute the tests, formatted as a **Markdown** file. You can save this as **`TEST_EXECUTION_GUIDE.md`**.

* * * * *

Markdown

```
# 📖 Step-by-Step Test Execution Guide

This guide provides detailed instructions on how to set up the environment and run both functional and performance tests for the FakeAPI (PantryCloud) Testing Framework.

---

## 🟢 Phase 1: Environment Setup

Before running any tests, ensure your environment is configured correctly.

### 1. Install Python
Ensure you have Python **3.13+** installed.
```bash
python --version

```

### 2\. Create a Virtual Environment

It is best practice to run tests in an isolated environment.

Bash

```
# Windows
.venv\Scripts\activate
uv sync

```

### 3\. Install Dependencies

Install all required libraries defined in `pyproject.toml`.

Bash

```
uv pip install .

```

*Alternatively, install manually:*

Bash

```
pip install pytest pytest-html requests locust pytest-playwright

```

* * * * *

🟡 Phase 2: Running Functional Tests (Pytest)
---------------------------------------------

These tests verify that the API works as expected (Creating, Reading, Updating, and Deleting data).

### 1\. Run All Tests

To execute the entire suite of positive and negative tests:

Bash

```
pytest

```

### 2\. Run with Verbose Output

To see exactly which tests are running and passing in real-time:

Bash

```
pytest -v

```

### 3\. Run Specific Test Files

If you only want to run the **positive** functional tests:

Bash

```
pytest tests/test_pantry_details.py

```

If you only want to run the **negative** error handling tests:

Bash

```
pytest tests/test_negative_pantry.py

```

### 4\. Run Tests by Name (Keyword)

To run only the tests related to "creation":

Bash

```
pytest -k "create"

```

* * * * *

🟠 Phase 3: Viewing Test Reports
--------------------------------

The framework is configured to generate an HTML report automatically after every Pytest run.

1.  Navigate to the `reports/` folder in your project directory.

2.  Locate the latest file (e.g., `report_2025-12-19_10-30-00.html`).

3.  **Right-click** the file and select **Open in Browser** (Chrome, Firefox, Edge, etc.).

4.  Review the **Results Table** to see which tests passed or failed and check the **Duration** column for speed.

* * * * *

🔴 Phase 4: Running Load Tests (Locust)
---------------------------------------

These tests simulate multiple users hitting the API simultaneously to check for performance issues or rate limits.

### 1\. Start the Locust Server

Run the following command in your terminal:

Bash

```
locust

```

### 2\. Access the Dashboard

Open your web browser and go to:

👉 http://localhost:8089

### 3\. Configure the Test

Enter the following settings in the Locust UI:

-   **Number of Users:** `5` (Recommended for free tier)

-   **Spawn Rate:** `1` (Add 1 user per second)

-   **Host:** `https://getpantry.cloud`

### 4\. Start & Monitor

1.  Click **Start Swarming**.

2.  Watch the **Statistics** tab for:

    -   **RPS:** Requests Per Second.

    -   **Failures:** Any 429 (Rate Limit) or 500 errors.

    -   **Average Response Time:** How long the API takes to reply.

3.  Click **Stop** when you are done.

* * * * *
