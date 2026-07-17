from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import (
    Category, Module, Lesson, InterviewQuestion,
    Quiz, QuizQuestion, QuizAttempt,
)
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    ModuleDetailSerializer,
    LessonDetailSerializer,
    InterviewQuestionListSerializer, InterviewQuestionDetailSerializer,
    QuizDetailSerializer, QuizSubmitSerializer, QuizAttemptSerializer,
)


# ─── Categories ───────────────────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """GET /api/categories"""
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["order", "name"]

    def get_queryset(self):
        return Category.objects.filter(is_active=True).annotate(
            module_count=Count("modules", filter=Q(modules__is_active=True))
        )


class CategoryDetailView(generics.RetrieveAPIView):
    """GET /api/categories/{slug}"""
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related("modules")


# ─── Modules ──────────────────────────────────────────────────────────────

class ModuleListView(generics.ListAPIView):
    """GET /api/modules"""
    serializer_class = ModuleDetailSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name"]
    ordering_fields = ["order", "name"]

    def get_queryset(self):
        return Module.objects.filter(is_active=True).select_related("category").prefetch_related("lessons")


class ModuleDetailView(generics.RetrieveAPIView):
    """GET /api/modules/{id}"""
    serializer_class = ModuleDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Module.objects.filter(is_active=True).select_related("category").prefetch_related("lessons")


# ─── Lessons ──────────────────────────────────────────────────────────────

class LessonDetailView(generics.RetrieveAPIView):
    """GET /api/lessons/{id}"""
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Lesson.objects.filter(is_active=True).select_related("module__category")


class LessonCompleteView(generics.UpdateAPIView):
    """PATCH /api/lessons/{id}/complete"""
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(is_active=True)

    def partial_update(self, request, *args, **kwargs):
        from apps.dashboard.models import UserProgress
        lesson = self.get_object()
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
        )
        progress.status = "completed"
        progress.save()
        return Response({"detail": "Lesson marked as completed."}, status=status.HTTP_200_OK)


# ─── Interview Questions ──────────────────────────────────────────────────

class InterviewQuestionListView(generics.ListAPIView):
    """GET /api/questions"""
    serializer_class = InterviewQuestionListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["category", "difficulty"]
    search_fields = ["title", "description"]
    ordering_fields = ["order", "difficulty"]

    def get_queryset(self):
        return InterviewQuestion.objects.all()


class InterviewQuestionDetailView(generics.RetrieveAPIView):
    """GET /api/questions/{id}"""
    serializer_class = InterviewQuestionDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = InterviewQuestion.objects.all()


# ─── Quiz ─────────────────────────────────────────────────────────────────

class QuizDetailView(generics.RetrieveAPIView):
    """GET /api/quiz/{id}"""
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Quiz.objects.filter(is_active=True).prefetch_related("questions")


class QuizSubmitView(generics.GenericAPIView):
    """POST /api/quiz/{id}/submit"""
    serializer_class = QuizSubmitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quiz_id = self.kwargs["pk"]
        try:
            quiz = Quiz.objects.get(pk=quiz_id, is_active=True)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers_data = serializer.validated_data["answers"]
        questions = {str(q.id): q for q in quiz.questions.all()}

        correct = 0
        total = len(answers_data)
        results = []

        for answer in answers_data:
            q_id = answer["question_id"]
            selected = answer["selected_index"]
            question = questions.get(q_id)
            if question:
                is_correct = selected == question.correct_option_index
                if is_correct:
                    correct += 1
                results.append({
                    "question_id": q_id,
                    "selected_index": selected,
                    "is_correct": is_correct,
                })
            else:
                results.append({
                    "question_id": q_id,
                    "selected_index": selected,
                    "is_correct": False,
                })

        score = round((correct / total) * 100) if total > 0 else 0

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            answers=results,
        )

        return Response({
            "attempt_id": str(attempt.id),
            "score": score,
            "correct": correct,
            "total": total,
            "passed": score >= quiz.passing_score,
            "results": results,
        }, status=status.HTTP_201_CREATED)
