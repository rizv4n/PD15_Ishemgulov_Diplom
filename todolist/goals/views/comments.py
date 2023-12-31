from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models.comments import GoalComment
from goals.permissions import CommentPermissions
from goals.serializers.comments import GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["goal", "created"]
    ordering = ["created"]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
