from django.contrib import admin
from .models import UserProgress, Activity, Roadmap


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "status", "percentage", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "lesson__title")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "title", "created_at")
    list_filter = ("activity_type",)
    search_fields = ("user__email", "title")
    readonly_fields = ("user", "activity_type", "title", "description", "metadata", "created_at")


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "status", "order")
    list_filter = ("status",)
    search_fields = ("user__email", "title")
