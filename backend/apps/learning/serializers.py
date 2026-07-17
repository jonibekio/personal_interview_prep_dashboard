from rest_framework import serializers
from .models import (
    Category, Module, Lesson, InterviewQuestion,
    Quiz, QuizQuestion, QuizAttempt,
)


class LessonBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "difficulty", "read_time_minutes", "order")


class ModuleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ("id", "name", "description", "icon", "order")


class CategoryListSerializer(serializers.ModelSerializer):
    module_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "icon", "image", "order", "module_count")


class CategoryDetailSerializer(serializers.ModelSerializer):
    modules = ModuleBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "icon", "image", "order", "modules")


class ModuleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    lessons = LessonBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ("id", "name", "description", "icon", "order", "category", "category_name", "lessons")


class LessonDetailSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source="module.name", read_only=True)
    category_slug = serializers.CharField(source="module.category.slug", read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id", "title", "slug", "difficulty", "read_time_minutes",
            "content", "code_blocks", "order", "module", "module_name", "category_slug",
        )


class InterviewQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ("id", "title", "difficulty", "tags", "order")


class InterviewQuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = (
            "id", "title", "description", "difficulty", "tags",
            "sample_answer", "hints", "order", "category",
        )


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ("id", "question_text", "options", "correct_option_index", "explanation", "order")


class QuizListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Quiz
        fields = ("id", "title", "description", "time_limit_minutes", "passing_score", "question_count")


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = (
            "id", "title", "description", "time_limit_minutes",
            "passing_score", "questions",
        )


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.DictField(),
        help_text='List of {"question_id": uuid, "selected_index": int}',
    )

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError("Answers cannot be empty.")
        for item in value:
            if "question_id" not in item or "selected_index" not in item:
                raise serializers.ValidationError("Each answer must have question_id and selected_index.")
        return value


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ("id", "quiz", "score", "answers", "completed_at")
        read_only_fields = ("id", "score", "answers", "completed_at")
