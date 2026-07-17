from django.contrib import admin
from .models import (
    Category, Module, Lesson, InterviewQuestion,
    Quiz, QuizQuestion, QuizAttempt,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ("order",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("category", "order")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "difficulty", "read_time_minutes", "order", "is_active")
    list_filter = ("difficulty", "module__category", "is_active")
    search_fields = ("title",)
    ordering = ("module", "order")


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "difficulty", "order", "created_at")
    list_filter = ("difficulty", "category")
    search_fields = ("title",)
    ordering = ("category", "order")


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    ordering = ("order",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "time_limit_minutes", "passing_score", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title",)
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "question_text", "correct_option_index", "order")
    list_filter = ("quiz",)
    ordering = ("quiz", "order")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "completed_at")
    list_filter = ("quiz",)
    search_fields = ("user__email",)
    readonly_fields = ("user", "quiz", "score", "answers", "completed_at")
