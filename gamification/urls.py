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
    path(
        "v1/score_user/modify/<int:user_id>/<int:new_score>/",
        views.modify_score_user,
        name="modify-score_user",
    ),
    # Badge
    path("v1/badges/", views.get_all_badges, name="get_all_badges"),
    path("v1/badges/modify/<int:badge_id>/", views.modify_badge, name="modify_badge"),
    path("v1/badges/create/", views.create_badge, name="create_badge"),
    # modify score
    path(
        "v1/modify_score/<int:user_id>/<int:new_score>/",
        views.modify_score,
        name="modify_score",
    ),
    # updatescore
    path(
        "v1/update_score/<int:user_id>/<str:type>/",
        views.update_score,
        name="update_score",
    ),
    # Award
    path("v1/awards/", views.award_list, name="award-list"),
    path("v1/awards/<int:pk>/", views.award_detail, name="award-detail"),
]
