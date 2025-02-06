import pytest

def test_home_page(test_client):
    """
    Test the home page of InsecureWebApp
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome To IWA Pharmacy Direct" in response.data
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

