from django.urls import path
from . import views

urlpatterns = [
    path("challenges/", views.ChallengeListView.as_view(), name="challenge-list"),
    path("challenges/<uuid:pk>/", views.ChallengeDetailView.as_view(), name="challenge-detail"),
    path("challenges/<uuid:pk>/run/", views.ChallengeRunView.as_view(), name="challenge-run"),
    path("challenges/<uuid:pk>/submit/", views.ChallengeSubmitView.as_view(), name="challenge-submit"),
    path("submissions/", views.SubmissionListView.as_view(), name="submission-list"),
]
