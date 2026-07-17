from django.contrib import admin
from .models import Challenge, TestCase, Submission


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    ordering = ("order",)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "difficulty", "points", "language", "is_active", "order")
    list_filter = ("difficulty", "category", "is_active", "language")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("category", "order")
    inlines = [TestCaseInline]


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("challenge", "order", "is_hidden")
    list_filter = ("challenge", "is_hidden")
    ordering = ("challenge", "order")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "challenge", "status", "test_cases_passed", "test_cases_total", "runtime_ms", "created_at")
    list_filter = ("status", "language")
    search_fields = ("user__email", "challenge__title")
    readonly_fields = ("user", "challenge", "code", "language", "status", "runtime_ms", "memory_mb", "test_cases_passed", "test_cases_total", "output", "created_at")
