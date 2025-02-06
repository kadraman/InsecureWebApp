def test_new_user(new_user):
    """
    Test the User model of InsecureWebApp
    """
    assert new_user.username == 'user5@localhost.com'
    assert new_user.email == 'user5@localhost.com'


def test_new_product(new_product):
    """
    Test the Product model of InsecureWebApp
    """
    assert new_product.code == 'SWA543-A343-00462'
    assert new_product.name == 'Pilex One'
