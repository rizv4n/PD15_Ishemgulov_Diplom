import json

import pytest

from django.urls import reverse

from core.models import User
from django.test import Client


@pytest.mark.django_db
def test_user_create(client):

    user_data = {
        'username': 'testuser',
        'first_name': 'testname',
        'last_name': 'testname',
        'password': 'testing2023',
        'password_repeat': 'testing2023',
        'email': 'test@email.com'
    }

    expected_response = {
        'username': 'testuser',
        'first_name': 'testname',
        'last_name': 'testname',
        'email': 'test@email.com'
    }

    response = client.post('/core/signup', data=json.dumps(user_data), content_type='application/json')

    assert response.status_code == 201
    assert response.data['username'] == expected_response['username']
    assert response.data['first_name'] == expected_response['first_name']
    assert response.data['last_name'] == expected_response['last_name']
    assert response.data['email'] == expected_response['email']


@pytest.mark.django_db
def test_user_detail(client):

    user = User.objects.create_user(
        username="testuser",
        password="testpassword2023",
        first_name='testname',
        last_name='testname',
        email='test@email.com'
    )

    client.login(
        username="testuser",
        password="testpassword2023"
    )

    expected_response = {
        'id': user.pk,
        'username': 'testuser',
        'first_name': 'testname',
        'last_name': 'testname',
        'email': 'test@email.com'
    }

    response = client.get(f"/core/profile")

    assert response.status_code == 200
    assert response.data['id'] == expected_response['id']
    assert response.data['username'] == expected_response['username']
    assert response.data['first_name'] == expected_response['first_name']
    assert response.data['last_name'] == expected_response['last_name']
    assert response.data['email'] == expected_response['email']


@pytest.mark.django_db
def test_user_password_update(client):

    User.objects.create_user(
        username="testuser",
        password="testpassword2023",
    )

    client.login(
        username="testuser",
        password="testpassword2023"
    )

    data = {
        'old_password': 'testpassword2023',
        'new_password': 'changedtestpassword2023'
    }

    response = client.put('/core/update_password', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login():
    User.objects.create_user(
        username="testuser",
        password="testpassword2023",
    )

    client = Client()

    login_data = {
        'username': 'testuser',
        'password': 'testpassword2023'
    }

    response = client.post(reverse('login'), data=login_data)

    assert response.status_code in [200, 302]
