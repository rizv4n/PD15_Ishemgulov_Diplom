from django.contrib import admin

from goals.models.category import GoalCategory
from goals.models.comments import GoalComment
from goals.models.goal import Goal
from goals.models.board import Board


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user", "category", "status", "priority", "created", "updated")
    search_fields = ("title", "description", "user", "category")


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "user", "text", "created", "updated")
    search_fields = ("title", "user")


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_field = "title"


admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
