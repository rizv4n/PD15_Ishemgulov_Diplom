import json
from collections import OrderedDict

import pytest

from core.models import User
from goals.models.board import Board, BoardParticipant


@pytest.mark.django_db
def test_board_create(client):
    User.objects.create_user(
        username='testuser',
        password='testpassword2023'
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    board_data = {
        'title': 'Test',
    }

    expected_response = {
        'title': 'Test',
        'is_deleted': False
    }

    response = client.post('/goals/board/create', data=json.dumps(board_data), content_type='application/json')

    assert response.status_code == 201
    assert response.data['title'] == expected_response['title']
    assert response.data['is_deleted'] == expected_response['is_deleted']


@pytest.mark.django_db
def test_board_detail(client):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword2023'
    )

    board = Board.objects.create(
        title='Test'
    )

    BoardParticipant.objects.create(
        user=user,
        board=board,
        role=BoardParticipant.Role.owner
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = {
        'id': board.pk,
        'title': 'Test',
        'is_deleted': False
    }

    response = client.get(f'/goals/board/{board.pk}')

    assert response.status_code == 200
    assert response.data['id'] == expected_response['id']
    assert response.data['title'] == expected_response['title']
    assert response.data['is_deleted'] == expected_response['is_deleted']


@pytest.mark.django_db
def test_board_delete(client):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword2023'
    )

    board = Board.objects.create(
        title='Test'
    )

    BoardParticipant.objects.create(
        user=user,
        board=board,
        role=BoardParticipant.Role.owner
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    response = client.delete(f'/goals/board/{board.pk}')
    assert response.status_code == 204


@pytest.mark.django_db
def test_board_list(client):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword2023'
    )

    board_1 = Board.objects.create(
        title='Test_1'
    )

    board_2 = Board.objects.create(
        title='Test_2'
    )

    BoardParticipant.objects.create(
        user=user,
        board=board_1,
        role=BoardParticipant.Role.owner
    )

    BoardParticipant.objects.create(
        user=user,
        board=board_2,
        role=BoardParticipant.Role.owner
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = [{
            'id': board_1.pk,
            'title': 'Test_1',
            'is_deleted': False
        },
        {
            'id': board_2.pk,
            'title': 'Test_2',
            'is_deleted': False
        }
    ]

    response = client.get('/goals/board/list')

    assert response.status_code == 200
    assert response.data[0]['id'] == expected_response[0]['id']
    assert response.data[0]['title'] == expected_response[0]['title']
    assert response.data[0]['is_deleted'] == expected_response[0]['is_deleted']

    assert response.data[1]['id'] == expected_response[1]['id']
    assert response.data[1]['title'] == expected_response[1]['title']
    assert response.data[1]['is_deleted'] == expected_response[1]['is_deleted']