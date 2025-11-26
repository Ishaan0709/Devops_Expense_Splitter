# tests/test_app.py

from app import app  # import Flask app

def test_home_route():
    # create a test client
    test_client = app.test_client()

    # send a GET request to "/"
    response = test_client.get('/')

    # check if status code is correct (200 OK)
    assert response.status_code == 200
