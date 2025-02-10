
import os
import pytest
from datetime import datetime

from iwa.models.Product import Product
from iwa.models.User import User
from iwa import create_app, get_db

# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def new_user():
    user = User(10, "user5@localhost.com", "password", datetime.now(), "Steve", "Shopper",
                "user5@localhost.com", "+44808123456", "London", "State", "Greater London",
                "United Kingdom", "ROLE_USER", True, False, "")
    return user


@pytest.fixture(scope='module')
def new_product():
    product = Product(50, "SWA543-A343-00462", "Pilex One",
                      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                      "generic-product-50.jpg", 9.95, False, 9.95, True, 0, 4, True)
    return product


@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!