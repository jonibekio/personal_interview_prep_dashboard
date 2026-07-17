from rest_framework import serializers
from .models import Challenge, TestCase, Submission


class ChallengeListSerializer(serializers.ModelSerializer):
    test_case_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Challenge
        fields = (
            "id", "title", "slug", "difficulty", "tags", "points",
            "language", "is_active", "order", "test_case_count",
        )


class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = (
            "id", "title", "slug", "description", "difficulty", "tags",
            "starter_code", "language", "constraints", "examples",
            "time_limit_seconds", "memory_limit_mb", "points",
        )


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ("id", "input_data", "expected_output", "is_hidden", "order")


class SubmissionCreateSerializer(serializers.Serializer):
    code = serializers.CharField()
    language = serializers.CharField(default="python3")


class SubmissionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            "id", "status", "runtime_ms", "memory_mb",
            "test_cases_passed", "test_cases_total", "output", "created_at",
        )
        read_only_fields = fields
