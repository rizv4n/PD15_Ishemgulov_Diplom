import json

import pytest
from django.utils import timezone

from core.models import User
from goals.models.board import Board, BoardParticipant
from goals.models.category import GoalCategory
from goals.models.goal import Goal, Status, Priority


@pytest.mark.django_db
def test_goal_create(client):
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

    goal_data = {
        'title': 'Test',
        'category': category.pk,
        'description': 'Test Description',
    }

    expected_response = {
        'title': 'Test',
        'description': 'Test Description',
        'status': Status.to_do,
        'priority': Priority.medium,
        'category': category.pk
    }

    response = client.post(
        '/goals/goal/create',
        data=json.dumps(goal_data),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['title'] == expected_response['title']
    assert response.data['description'] == expected_response['description']
    assert response.data['status'] == expected_response['status']
    assert response.data['priority'] == expected_response['priority']
    assert response.data['category'] == expected_response['category']


@pytest.mark.django_db
def test_goal_detail(client):

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

    goal = Goal.objects.create(
        title='Test',
        user=user,
        category=category,
        description='Test Description',
        due_date=timezone.make_aware(timezone.datetime(2023, 7, 20, 15, 30, 0))
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = {
        'id': goal.pk,
        'title': 'Test',
        'description': 'Test Description',
        'status': Status.to_do,
        'priority': Priority.medium,
        'due_date': '2023-07-20T15:30:00Z'
    }

    response = client.get(f'/goals/goal/{goal.pk}')

    assert response.status_code == 200
    assert response.data['id'] == expected_response['id']
    assert response.data['title'] == expected_response['title']
    assert response.data['description'] == expected_response['description']
    assert response.data['status'] == expected_response['status']
    assert response.data['priority'] == expected_response['priority']
    assert response.data['due_date'] == expected_response['due_date']


@pytest.mark.django_db
def test_goal_delete(client):
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

    goal = Goal.objects.create(
        title='Test',
        user=user,
        category=category,
        description='Test Description',
        due_date=timezone.make_aware(timezone.datetime(2023, 7, 20, 15, 30, 0))
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    response = client.delete(f'/goals/goal/{goal.pk}')
    assert response.status_code == 204


@pytest.mark.django_db
def test_goal_list(client):
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

    Goal.objects.create(
        title='Test_1',
        user=user,
        category=category,
        description='Test Description',
        due_date=timezone.make_aware(timezone.datetime(2023, 7, 20, 15, 30, 0))
    )

    Goal.objects.create(
        title='Test_2',
        user=user,
        category=category,
        description='Test Description',
        due_date=timezone.make_aware(timezone.datetime(2023, 7, 20, 15, 30, 0))
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = [{
            'title': 'Test_1',
            'description': 'Test Description',
            'status': Status.to_do,
            'priority': Priority.medium,
            'due_date': '2023-07-20T15:30:00Z'
        },
        {
            'title': 'Test_2',
            'description': 'Test Description',
            'status': Status.to_do,
            'priority': Priority.medium,
            'due_date': '2023-07-20T15:30:00Z'
        }
    ]

    response = client.get('/goals/goal/list')

    assert response.status_code == 200
    assert response.data[0]['title'] == expected_response[0]['title']
    assert response.data[0]['description'] == expected_response[0]['description']
    assert response.data[0]['status'] == expected_response[0]['status']
    assert response.data[0]['priority'] == expected_response[0]['priority']
    assert response.data[0]['due_date'] == expected_response[0]['due_date']

    assert response.data[1]['title'] == expected_response[1]['title']
    assert response.data[1]['description'] == expected_response[1]['description']
    assert response.data[1]['status'] == expected_response[1]['status']
    assert response.data[1]['priority'] == expected_response[1]['priority']
    assert response.data[1]['due_date'] == expected_response[1]['due_date']
