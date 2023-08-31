from django.conf import settings
from django.urls import path, re_path
from . import views


urlpatterns = [
    # gamification parameters
    path(
        "v1/gamification_parameters/",
        views.get_gamification_parameters,
        name="get-gamification_parameters",
    ),
    path(
        "v1/gamification_parameters/modify/",
        views.modify_gamification_parameters,
        name="modify-gamification_parameters",
    ),
    # Score
    path("v1/score_user/", views.get_score_all, name="get-score_user_all"),
    path("v1/score_user/<int:user_id>/", views.get_score_user, name="get-score_user"),
    path("v1/score_user/modify/<int:user_id>/", views.modify_score_user, name="get-score_user"),
    # Badge
    path("v1/badges/", views.get_all_badges, name="get_all_badges"),
    path("v1/badge/modify/<int:badge_id>/", views.modify_badge, name="modify_badge"),
]
