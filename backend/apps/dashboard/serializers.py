from rest_framework import serializers
from .models import UserProgress, Activity, Roadmap


class UserProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)

    class Meta:
        model = UserProgress
        fields = ("id", "lesson", "lesson_title", "status", "percentage")


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "activity_type", "title", "description", "metadata", "created_at")


class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ("id", "title", "description", "status", "order")


class DashboardSerializer(serializers.Serializer):
    """Single endpoint returning all dashboard data."""
    stats = serializers.DictField()
    progress = serializers.ListField()
    recent_activity = serializers.ListField()
    upcoming_challenges = serializers.ListField()
    roadmap = serializers.ListField()
