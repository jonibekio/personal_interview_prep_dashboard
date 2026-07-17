from django.db import models
from apps.common.models import TimeStampedModel


class Challenge(TimeStampedModel):
    """Coding challenge (Two Sum, LRU Cache, etc.)."""
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    category = models.ForeignKey("learning.Category", on_delete=models.CASCADE, related_name="challenges")
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    tags = models.JSONField(default=list, blank=True, help_text='e.g. ["ARRAY", "HASH TABLE"]')
    starter_code = models.TextField(blank=True, help_text="Default code template")
    language = models.CharField(max_length=50, default="python3")
    constraints = models.TextField(blank=True)
    examples = models.JSONField(default=list, blank=True, help_text="List of {input, output, explanation}")
    time_limit_seconds = models.PositiveIntegerField(default=2)
    memory_limit_mb = models.PositiveIntegerField(default=256)
    points = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        indexes = [
            models.Index(fields=["difficulty"]),
            models.Index(fields=["category", "order"]),
        ]

    def __str__(self):
        return self.title


class TestCase(TimeStampedModel):
    """Test case for a coding challenge."""
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.TextField(help_text="Input for the function")
    expected_output = models.TextField(help_text="Expected output")
    is_hidden = models.BooleanField(default=False, help_text="Hidden from user in examples")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Test Case"
        verbose_name_plural = "Test Cases"

    def __str__(self):
        return f"{self.challenge.title} — Test {self.order + 1}"


class Submission(TimeStampedModel):
    """User's code submission for a challenge."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("accepted", "Accepted"),
        ("wrong_answer", "Wrong Answer"),
        ("time_limit", "Time Limit Exceeded"),
        ("runtime_error", "Runtime Error"),
        ("compilation_error", "Compilation Error"),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    language = models.CharField(max_length=50, default="python3")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    runtime_ms = models.PositiveIntegerField(null=True, blank=True)
    memory_mb = models.FloatField(null=True, blank=True)
    test_cases_passed = models.PositiveIntegerField(default=0)
    test_cases_total = models.PositiveIntegerField(default=0)
    output = models.TextField(blank=True, help_text="Execution output or error message")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        indexes = [
            models.Index(fields=["user", "challenge"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.challenge.title} — {self.status}"
