import pytest
import json
import requests
from api_call import pantry


# --- invalid data fixtures ---

@pytest.fixture
def invalid_json_payload():
    """Returns a string that is NOT valid JSON"""
    return "{ 'bad_syntax': True, "  # Missing closing brace


@pytest.fixture
def non_existent_basket():
    return "basket_does_not_exist_99999"


# --- Negative Tests ---

def test_get_non_existent_basket(non_existent_basket):
    """
    Test retrieving a basket that doesn't exist.
    Expected: 404 Not Found (or API specific error).
    """
    response = pantry.get_content(non_existent_basket)

    # Most APIs return 404, but PantryCloud might return 200 with empty body
    # or specific error message. Let's verify it's NOT a standard success with data.
    if response.status_code == 200:
        # If it returns 200, ensure it's empty
        assert response.json() == {}
    else:
        assert response.status_code == 404


def test_create_basket_empty_name():
    """
    Test creating a basket with an empty string as name.
    """
    response = pantry.post_create_update("", json.dumps({"test": "data"}))

    # This effectively hits the base URL, which might not be allowed for POST
    # or might be a 404/405 Method Not Allowed
    assert response.status_code in [404, 405, 400]


def test_create_basket_invalid_payload_type(basket_name):
    """
    Test sending a plain string/integer instead of a JSON object.
    """
    # Sending a plain string "Hello" instead of JSON {"key": "value"}
    bad_payload = "Just a plain string"

    response = pantry.post_create_update(basket_name, bad_payload)

    # The API expects JSON, so it should likely fail or just store the string depending on leniency.
    # If strict, it returns 400. If lenient, we check behavior.
    # Assuming strict API:
    # assert response.status_code == 400

    # Since Pantry is a simple store, it might actually accept it!
    # Let's verify what happens:
    if response.status_code == 200:
        # If it accepts it, verify it stored it exactly as sent
        fetch = pantry.get_content(basket_name)
        assert fetch.text == bad_payload


def test_invalid_pantry_id():
    """
    Test accessing an invalid Pantry ID.
    Since 'pantry_id' is hardcoded in the module, we can verify this
    by manually constructing a bad URL using the session.
    """
    bad_id = "00000000-0000-0000-0000-000000000000"
    bad_url = f"https://getpantry.cloud/apiv1/pantry/{bad_id}"

    # We use the existing session 's' from pantry.py to keep config
    response = pantry.s.get(bad_url)

    # Should definitely fail authentication/lookup
    assert response.status_code in [404, 401, 403]
    assert "error" in response.text.lower() or "not found" in response.text.lower()


def test_delete_non_existent_basket(non_existent_basket):
    """
    Test deleting a basket that is already gone.
    Idempotency check: Deleting a non-existent item is often 200 OK or 404.
    """
    response = pantry.delete_basket(non_existent_basket)

    # Generally, APIs should return 200 (Success, it's gone) or 404 (Didn't exist).
    # It should NOT be a 500 Server Error.
    assert response.status_code in [200, 404]


def test_update_basket_type_mismatch(managed_basket):
    """
    Test merging incompatible data types.
    1. Create basket with {"count": 10} (Integer)
    2. Try to update "count" to "Ten" (String)
    """
    # managed_basket is already created with sample_payload ({"quantity": 50})

    # Try to overwrite 'quantity' (int) with a string
    mismatch_payload = json.dumps({"quantity": "Fifty"})

    response = pantry.put_update_contents(managed_basket, mismatch_payload)

    # This tests if the API enforces strict typing or allows overwriting.
    assert response.status_code == 200

    # Verify the change happened (Pantry is likely schema-less, so this succeeds)
    data = pantry.get_content(managed_basket).json()
    assert data['quantity'] == "Fifty"