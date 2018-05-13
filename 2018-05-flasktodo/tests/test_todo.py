import pytest
from flasktd.db import get_db

def test_index(client, auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response data
    assert b'test\nnbody' in response.data
    assert b'Deadline: 2018-05-12' in response.data
    assert b'href="/1/update"' in response.data
