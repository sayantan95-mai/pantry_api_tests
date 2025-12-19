from locust import HttpUser, task, between, SequentialTaskSet
import uuid
import random

# We use the same ID from your project
PANTRY_ID = "53748d1f-f12a-44f0-bc4b-7cc65a5fa7b9"


class BasketLifecycle(SequentialTaskSet):
    """
    Simulates a full CRUD lifecycle for a single basket.
    Running tasks sequentially ensures we don't try to delete 
    a basket before creating it.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.payload = None
        self.basket_name = None

    def on_start(self):
        """
        Runs once when a User starts this task set.
        We generate a unique basket name for this user to avoid collisions.
        """
        self.basket_name = f"locust_basket_{uuid.uuid4().hex[:8]}"
        self.payload = {"product": "Locust Load Item", "qty": 100}

    @task
    def create_basket(self):
        """Step 1: Create"""
        self.client.post(
            f"/apiv1/pantry/{PANTRY_ID}/basket/{self.basket_name}",
            json=self.payload,
            name="/basket/[name] - CREATE"  # Groups stats in UI
        )

    @task
    def get_basket(self):
        """Step 2: Read"""
        self.client.get(
            f"/apiv1/pantry/{PANTRY_ID}/basket/{self.basket_name}",
            name="/basket/[name] - READ"
        )

    @task
    def update_basket(self):
        """Step 3: Update"""
        update_data = {"qty": 200, "status": "updated_by_locust"}
        self.client.put(
            f"/apiv1/pantry/{PANTRY_ID}/basket/{self.basket_name}",
            json=update_data,
            name="/basket/[name] - UPDATE"
        )

    @task
    def delete_basket(self):
        """Step 4: Delete"""
        self.client.delete(
            f"/apiv1/pantry/{PANTRY_ID}/basket/{self.basket_name}",
            name="/basket/[name] - DELETE"
        )


class PantryUser(HttpUser):
    # Wait between 2 and 5 seconds between tasks to be polite to the free API
    wait_time = between(2, 5)

    # Base host URL
    host = "https://getpantry.cloud"

    # Register the sequence of tasks
    tasks = {BasketLifecycle: 1}

    @task(1)
    def get_pantry_details(self):
        """
        Occasional task: Get general pantry details.
        (Running alongside the CRUD sequence with lower weight if needed)
        """
        self.client.get(
            f"/apiv1/pantry/{PANTRY_ID}",
            name="/pantry - DETAILS"
        )