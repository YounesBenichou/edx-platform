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
    path("v1/score_user/<int:user_id>/", views.get_score_user, name="get-score_user"),
    # Badge
    path("v1/badges/", views.get_all_badges, name="get_all_badges"),
    path("v1/badges/create/", views.create_badge, name="create_badge"),
    path("v1/badge/<int:badge_id>/", views.modify_badge, name="modify_badge"),
    path("v1/badges/<int:badge_id>/delete/", views.delete_badge, name="delete_badge"),
]
