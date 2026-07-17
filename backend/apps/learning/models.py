from django.db import models
from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
    """Top-level curriculum category (Python Core, OOP, Django, etc.)."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Material icon name")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Module(TimeStampedModel):
    """Module within a category (Variables, Control Flow, Functions, etc.)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="modules")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        indexes = [
            models.Index(fields=["category", "order"]),
        ]

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class Lesson(TimeStampedModel):
    """Lesson within a module (Understanding Decorators, Context Managers, etc.)."""
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=300)
    slug = models.SlugField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="intermediate")
    read_time_minutes = models.PositiveIntegerField(default=10)
    content = models.TextField(help_text="Lesson content in Markdown")
    code_blocks = models.JSONField(default=list, blank=True, help_text="List of {filename, code, language}")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        indexes = [
            models.Index(fields=["module", "order"]),
        ]

    def __str__(self):
        return self.title


class InterviewQuestion(TimeStampedModel):
    """Interview question for a category."""
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    tags = models.JSONField(default=list, blank=True)
    sample_answer = models.TextField(blank=True)
    hints = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Interview Question"
        verbose_name_plural = "Interview Questions"
        indexes = [
            models.Index(fields=["category", "difficulty"]),
        ]

    def __str__(self):
        return self.title


class Quiz(TimeStampedModel):
    """Quiz for a category."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(default=30)
    passing_score = models.PositiveIntegerField(default=70, help_text="Percentage to pass")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title


class QuizQuestion(TimeStampedModel):
    """Question within a quiz."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    options = models.JSONField(help_text="List of option strings")
    correct_option_index = models.PositiveIntegerField(help_text="0-based index of correct option")
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"

    def __str__(self):
        return f"{self.quiz.title} — Q{self.order + 1}"


class QuizAttempt(TimeStampedModel):
    """User's quiz attempt with score."""
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(help_text="Percentage score")
    answers = models.JSONField(default=list, blank=True, help_text="List of {question_id, selected_index, is_correct}")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
        ordering = ["-completed_at"]
        indexes = [
            models.Index(fields=["user", "quiz"]),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.quiz.title} — {self.score}%"
