from django.db import models
from apps.common.models import TimeStampedModel


class UserProgress(TimeStampedModel):
    """Track user's progress on lessons."""
    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey("learning.Lesson", on_delete=models.CASCADE, related_name="user_progress")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_started")
    percentage = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "lesson")
        verbose_name = "User Progress"
        verbose_name_plural = "User Progress"
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.lesson.title} — {self.status}"


class Activity(TimeStampedModel):
    """User's recent activity feed."""
    TYPE_CHOICES = [
        ("lesson_completed", "Lesson Completed"),
        ("quiz_attempted", "Quiz Attempted"),
        ("challenge_solved", "Challenge Solved"),
        ("challenge_attempted", "Challenge Attempted"),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        indexes = [
            models.Index(fields=["user", "activity_type"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.activity_type} — {self.title}"


class Roadmap(TimeStampedModel):
    """User's roadmap progress."""
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("active", "Active"),
        ("pending", "Pending"),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="roadmap_items")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Roadmap"
        verbose_name_plural = "Roadmaps"
        indexes = [
            models.Index(fields=["user", "order"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.title}"
