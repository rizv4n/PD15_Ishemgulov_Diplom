from django.urls import path

from goals.views.goal import GoalCreateView, GoalListView, GoalView
from goals.views.category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.comments import GoalCommentView, GoalCommentListView, GoalCommentCreateView

urlpatterns = [
    path('goal/create', GoalCreateView.as_view()),
    path('goal/list', GoalListView.as_view()),
    path('goal/<pk>', GoalView.as_view()),
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path('goal_category/<pk>', GoalCategoryView.as_view()),
    path('goal_comment/create', GoalCommentCreateView.as_view()),
    path('goal_comment/list', GoalCommentListView.as_view()),
    path('goal_comment/<pk>', GoalCommentView.as_view()),
]
