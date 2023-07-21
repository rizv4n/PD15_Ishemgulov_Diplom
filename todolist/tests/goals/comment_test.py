import json

import pytest
from django.utils import timezone

from core.models import User
from goals.models.board import Board, BoardParticipant
from goals.models.category import GoalCategory
from goals.models.comments import GoalComment
from goals.models.goal import Goal, Status, Priority


@pytest.mark.django_db
def test_comment_create(client):
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
        due_date=timezone.make_aware(timezone.datetime(2023, 10, 20, 15, 30, 0))
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    comment_data = {
        'text': 'Test',
        'goal': goal.pk,
    }

    expected_response = {
        'text': 'Test',
        'goal': goal.pk,
    }

    response = client.post(
        '/goals/goal_comment/create',
        data=json.dumps(comment_data),
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.data['text'] == expected_response['text']
    assert response.data['goal'] == expected_response['goal']


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
        due_date=timezone.make_aware(timezone.datetime(2023, 10, 20, 15, 30, 0))
    )

    comment = GoalComment.objects.create(
        goal=goal,
        text='Testing Text',
        user=user
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = {
        'id': comment.pk,
        'text': 'Testing Text'
    }

    response = client.get(f'/goals/goal_comment/{comment.pk}')

    assert response.status_code == 200
    assert response.data['id'] == expected_response['id']
    assert response.data['text'] == expected_response['text']


@pytest.mark.django_db
def test_comment_delete(client):
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

    comment = GoalComment.objects.create(
        goal=goal,
        text='Testing Text',
        user=user
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    response = client.delete(f'/goals/goal_comment/{comment.pk}')
    assert response.status_code == 204


@pytest.mark.django_db
def test_comment_list(client):
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

    GoalComment.objects.create(
        goal=goal,
        text='Testing Text 1',
        user=user
    )

    GoalComment.objects.create(
        goal=goal,
        text='Testing Text 2',
        user=user
    )

    client.login(
        username='testuser',
        password='testpassword2023'
    )

    expected_response = [{
            'text': 'Testing Text 1',
            'goal': goal.pk
        },
        {
            'text': 'Testing Text 2',
            'goal': goal.pk
        }
    ]

    response = client.get('/goals/goal_comment/list')

    assert response.status_code == 200
    assert response.data[0]['text'] == expected_response[0]['text']
    assert response.data[0]['goal'] == expected_response[0]['goal']

    assert response.data[1]['text'] == expected_response[1]['text']
    assert response.data[1]['goal'] == expected_response[1]['goal']
    