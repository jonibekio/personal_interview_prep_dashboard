from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Challenge, Submission
from .serializers import (
    ChallengeListSerializer, ChallengeDetailSerializer,
    SubmissionCreateSerializer, SubmissionResultSerializer,
)
from .services import execute_submission


class ChallengeListView(generics.ListAPIView):
    """GET /api/challenges"""
    serializer_class = ChallengeListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["difficulty", "category", "language"]
    search_fields = ["title", "description", "tags"]
    ordering_fields = ["order", "difficulty", "points", "created_at"]

    def get_queryset(self):
        from django.db.models import Count
        return Challenge.objects.filter(is_active=True).annotate(
            test_case_count=Count("test_cases")
        )


class ChallengeDetailView(generics.RetrieveAPIView):
    """GET /api/challenges/{id}"""
    serializer_class = ChallengeDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Challenge.objects.filter(is_active=True)


class ChallengeRunView(generics.GenericAPIView):
    """POST /api/challenges/{id}/run"""
    serializer_class = SubmissionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        challenge_id = self.kwargs["pk"]
        try:
            challenge = Challenge.objects.get(pk=challenge_id, is_active=True)
        except Challenge.DoesNotExist:
            return Response({"detail": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = Submission.objects.create(
            user=request.user,
            challenge=challenge,
            code=serializer.validated_data["code"],
            language=serializer.validated_data.get("language", "python3"),
        )

        result = execute_submission(submission)

        return Response({
            "submission_id": str(submission.id),
            **result,
        })


class ChallengeSubmitView(generics.GenericAPIView):
    """POST /api/challenges/{id}/submit"""
    serializer_class = SubmissionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        challenge_id = self.kwargs["pk"]
        try:
            challenge = Challenge.objects.get(pk=challenge_id, is_active=True)
        except Challenge.DoesNotExist:
            return Response({"detail": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = Submission.objects.create(
            user=request.user,
            challenge=challenge,
            code=serializer.validated_data["code"],
            language=serializer.validated_data.get("language", "python3"),
        )

        result = execute_submission(submission)

        return Response({
            "submission_id": str(submission.id),
            **result,
        }, status=status.HTTP_201_CREATED)


class SubmissionListView(generics.ListAPIView):
    """GET /api/submissions — user's submissions"""
    serializer_class = SubmissionResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)
