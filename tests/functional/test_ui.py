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

import pytest


def test_home_page(test_client):
    """
    Test the home page of InsecureWebApp
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome To <br/>IWA Pharmacy Direct" in response.data
    assert b"Register" in response.data
    assert b"Shop Now" in response.data


def test_products_page(test_client):
    """
    Test the product page of InsecureWebApp
    """
    response = test_client.get('/products/')
    assert response.status_code == 200
    assert b"Enter search keywords" in response.data
    assert b"Alphadex Lite" in response.data

