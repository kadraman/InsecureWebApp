"""
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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