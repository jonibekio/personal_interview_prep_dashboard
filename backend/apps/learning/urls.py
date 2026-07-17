from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", views.CategoryDetailView.as_view(), name="category-detail"),
    # Modules
    path("modules/", views.ModuleListView.as_view(), name="module-list"),
    path("modules/<uuid:pk>/", views.ModuleDetailView.as_view(), name="module-detail"),
    # Lessons
    path("lessons/<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),
    path("lessons/<uuid:pk>/complete/", views.LessonCompleteView.as_view(), name="lesson-complete"),
    # Interview Questions
    path("questions/", views.InterviewQuestionListView.as_view(), name="question-list"),
    path("questions/<uuid:pk>/", views.InterviewQuestionDetailView.as_view(), name="question-detail"),
    # Quiz
    path("quiz/<uuid:pk>/", views.QuizDetailView.as_view(), name="quiz-detail"),
    path("quiz/<uuid:pk>/submit/", views.QuizSubmitView.as_view(), name="quiz-submit"),
]
