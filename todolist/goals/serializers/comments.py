from rest_framework import serializers

from core.serializers import UserRetrieveSerializer
from goals.models.comments import GoalComment


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
