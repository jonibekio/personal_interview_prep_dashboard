from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Q, Avg
from datetime import timedelta
from django.utils import timezone

from apps.learning.models import Module, Lesson, QuizAttempt
from apps.coding.models import Challenge, Submission
from .models import UserProgress, Activity, Roadmap


class DashboardView(APIView):
    """GET /api/dashboard — all stats in one response."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # ── Stats ──
        total_lessons = Lesson.objects.filter(is_active=True).count()
        completed_lessons = UserProgress.objects.filter(
            user=user, status="completed"
        ).count()
        quizzes_taken = QuizAttempt.objects.filter(user=user).count()
        avg_quiz_score = QuizAttempt.objects.filter(user=user).aggregate(
            avg=Avg("score")
        )["avg"] or 0
        challenges_solved = Submission.objects.filter(
            user=user, status="accepted"
        ).values("challenge").distinct().count()

        # Study time (from activity — mock calculation)
        today = timezone.now().date()
        today_activities = Activity.objects.filter(
            user=user,
            created_at__date=today,
        ).count()
        study_hours = today_activities * 0.5  # rough estimate

        stats = {
            "study_time_today": f"{int(study_hours)}h {int((study_hours % 1) * 60)}m",
            "lessons_completed": f"{completed_lessons}/{total_lessons}",
            "lessons_percentage": round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0),
            "quizzes_taken": quizzes_taken,
            "avg_quiz_score": round(avg_quiz_score),
            "challenges_solved": challenges_solved,
        }

        # ── Progress by category ──
        from apps.learning.models import Category
        categories = Category.objects.filter(is_active=True).annotate(
            total_lessons=Count("modules__lessons", filter=Q(modules__lessons__is_active=True)),
            completed_lessons_count=Count(
                "modules__lessons__user_progress",
                filter=Q(
                    modules__lessons__user_progress__user=user,
                    modules__lessons__user_progress__status="completed",
                ),
            ),
        )
        progress = []
        for cat in categories:
            total = cat.total_lessons
            completed = cat.completed_lessons_count
            pct = round((completed / total * 100) if total > 0 else 0)
            progress.append({
                "category": cat.name,
                "icon": cat.icon,
                "percentage": pct,
            })

        # ── Recent Activity ──
        activities = Activity.objects.filter(user=user)[:5]
        recent_activity = [
            {
                "type": a.activity_type,
                "title": a.title,
                "description": a.description,
                "metadata": a.metadata,
                "time_ago": _time_ago(a.created_at),
            }
            for a in activities
        ]

        # ── Upcoming Challenges ──
        upcoming = Challenge.objects.filter(is_active=True).order_by("order")[:3]
        upcoming_challenges = [
            {
                "id": str(c.id),
                "title": c.title,
                "difficulty": c.difficulty,
                "description": c.description[:100],
                "points": c.points,
            }
            for c in upcoming
        ]

        # ── Roadmap ──
        roadmap_items = Roadmap.objects.filter(user=user).order_by("order")
        roadmap = [
            {
                "title": r.title,
                "description": r.description,
                "status": r.status,
            }
            for r in roadmap_items
        ]

        return Response({
            "stats": stats,
            "progress": progress,
            "recent_activity": recent_activity,
            "upcoming_challenges": upcoming_challenges,
            "roadmap": roadmap,
        })


def _time_ago(dt):
    """Simple relative time string."""
    diff = timezone.now() - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    else:
        return f"{seconds // 86400}d ago"
