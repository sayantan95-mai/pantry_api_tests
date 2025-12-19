import json
import pytest
from api_call import pantry


def test_pantry_details():
    """
    Tests getting details.
    """
    response = pantry.get_pantry_details()
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Sayantan Pantry"
    assert data["description"] == "pantry accn"


def test_update_details(update_payload, restore_pantry):
    """
    Tests updating details.
    Uses 'restore_pantry' fixture to automatically reset the name after this test.
    """
    # 1. Update
    response = pantry.put_update_details(update_payload)
    assert response.status_code == 200

    # 2. Verify
    data = response.json()
    assert data["name"] == "Pytest Pantry"
    assert data["description"] == "Pytest pantry accn"

    # No manual reset needed here; the fixture handles it!


def test_create_basket(basket_name, sample_payload):
    """
    Tests manual creation and deletion.
    """
    payload_str = json.dumps(sample_payload)
    response = pantry.post_create_update(basket_name, payload_str)

    assert response.status_code == 200
    assert response.text == f"Your Pantry was updated with basket: {basket_name}!"
    pantry.delete_basket(basket_name)


def test_get_basket_content(managed_basket, sample_payload):
    """
    Uses 'managed_basket' fixture (already created).
    """
    response = pantry.get_content(managed_basket)
    assert response.status_code == 200

    data = response.json()
    assert data['product'] == sample_payload['product']


def test_update_basket_content(managed_basket, sample_payload):
    """
    Uses 'managed_basket' fixture.
    """
    # Update data
    update_data = json.dumps({"extra_info": "updated", "quantity": 99})
    pantry.put_update_contents(managed_basket, update_data)

    # Verify
    response = pantry.get_content(managed_basket)
    data = response.json()

    assert data['quantity'] == 99
    assert data['extra_info'] == "updated"
    assert data['product'] == sample_payload['product'] # Original data remains


def test_delete_basket(basket_name, sample_payload):
    # Setup
    pantry.post_create_update(basket_name, json.dumps(sample_payload))

    # Test Delete
    response = pantry.delete_basket(basket_name)
    assert response.status_code == 200

    # Verify it's gone
    details = pantry.get_pantry_details().json()
    baskets = [b['name'] for b in details['baskets']]
    assert basket_name not in baskets