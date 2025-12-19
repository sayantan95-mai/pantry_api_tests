import pytest
import uuid
import os
import json
from datetime import datetime
from api_call import pantry


# --- Data Fixtures ---
@pytest.fixture
def update_payload():
    return json.dumps({
        "name": "Pytest Pantry",
        "description": "Pytest pantry accn"
    })


@pytest.fixture
def reset_payload():
    return json.dumps({
        "name": "Sayantan Pantry",
        "description": "pantry accn"
    })


@pytest.fixture
def sample_payload():
    return {
        "product": "Test Item",
        "quantity": 50,
        "active": True
    }


@pytest.fixture
def basket_name() -> str:
    """Generates a unique basket name for every test to avoid collisions."""
    return f"test_basket_{uuid.uuid4().hex[:8]}"


# --- Logic Fixtures ---

@pytest.fixture
def managed_basket(basket_name, sample_payload):
    """
    Creates a basket, yields the name, and safely deletes it after.
    """
    # Setup
    pantry.post_create_update(basket_name, json.dumps(sample_payload))

    yield basket_name

    # Teardown (Safely delete)
    pantry.delete_basket(basket_name)


@pytest.fixture
def restore_pantry(reset_payload):
    """
    Ensures the pantry details are reset to default AFTER the test runs.
    This fixes the issue where tests fail because the name wasn't reset.
    """
    yield
    pantry.put_update_details(reset_payload)


# --- Reporting Hook ---
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{now}.html"

    if not os.path.exists("reports"):
        os.makedirs("reports")

    config.option.htmlpath = os.path.join("reports", report_name)
    config.option.self_contained_html = True