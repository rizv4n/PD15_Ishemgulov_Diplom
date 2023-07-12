from rest_framework import permissions

from goals.models.board import BoardParticipant
from goals.models.category import GoalCategory
from goals.models.comments import GoalComment
from goals.models.goal import Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(
                board__participants__user=request.user
            ).exists()
        return GoalCategory.objects.filter(
            board__participants__user=request.user,
            board__participants__role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return Goal.objects.filter(
                category__board__participants__user=request.user
            ).exists()
        return Goal.objects.filter(
            category__board__participants__user=request.user,
            category__board__participants__role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return GoalComment.objects.filter(
                goal__category__board__participants__user=request.user
            ).exists()
        return GoalComment.objects.filter(
            goal__category__board__participants__user=request.user,
            goal__category__board__participants__role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()
