import json

import pytest

from core.models import User
from goals.models.board import Board, BoardParticipant
from goals.models.category import GoalCategory


@pytest.mark.django_db
def test_category_create(client):
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

    category_data = {
        'title': 'Test',
        'board': board.pk
    }

    expected_response = {
        'title': 'Test',
        'board': board.pk,
        'is_deleted': False
    }

    response = client.post(
        '/goals/goal_category/create',
        data=json.dumps(category_data),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['title'] == expected_response['title']
    assert response.data['board'] == expected_response['board']
    assert response.data['is_deleted'] == expected_response['is_deleted']


@pytest.mark.django_db
def test_category_detail(client):

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

    category = GoalCategory.objects.create(
        board=board,
        title='Test',
        user=user,
        is_deleted=False
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = {
        'id': category.pk,
        'title': 'Test',
        'is_deleted': False
    }

    response = client.get(f'/goals/goal_category/{category.pk}')

    assert response.status_code == 200
    assert response.data['id'] == expected_response['id']
    assert response.data['title'] == expected_response['title']
    assert response.data['is_deleted'] == expected_response['is_deleted']


@pytest.mark.django_db
def test_category_delete(client):
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

    category = GoalCategory.objects.create(
        board=board,
        title='Test',
        user=user,
        is_deleted=False
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    response = client.delete(f'/goals/goal_category/{category.pk}')
    assert response.status_code == 204


@pytest.mark.django_db
def test_category_list(client):
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

    GoalCategory.objects.create(
        board=board,
        title='Test_1',
        user=user,
        is_deleted=False
    )

    GoalCategory.objects.create(
        board=board,
        title='Test_2',
        user=user,
        is_deleted=False
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = [{
            'title': 'Test_1',
            'is_deleted': False
        },
        {
            'title': 'Test_2',
            'is_deleted': False
        }
    ]

    response = client.get('/goals/goal_category/list')

    assert response.status_code == 200
    assert response.data[0]['title'] == expected_response[0]['title']
    assert response.data[0]['is_deleted'] == expected_response[0]['is_deleted']

    assert response.data[1]['title'] == expected_response[1]['title']
    assert response.data[1]['is_deleted'] == expected_response[1]['is_deleted']