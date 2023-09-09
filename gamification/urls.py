from django.conf import settings
from django.urls import path, re_path
from . import views


urlpatterns = [
    # users
    path("v1/users/", views.user_list, name="user-list"),
    path("v1/users/<int:pk>/", views.user_detail, name="user-detail"),
    # gamification parameters (how much  points we get for completing a unit  - sectiom - course)
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
    # Score of user
    path("v1/score_user/", views.get_score_all, name="get-score_user_all"),
    path("v1/score_user/<int:user_id>/", views.get_score_user, name="get-score_user"),
    path(
        "v1/score_user/modify/<int:user_id>/<int:new_score>/",
        views.modify_score_user,
        name="modify-score_user",
    ),
    # Badges
    path("v1/badges/", views.get_all_badges, name="get_all_badges"),
    path("v1/badges/modify/<int:badge_id>/", views.modify_badge, name="modify_badge"),
    path("v1/badges/create/", views.create_badge, name="create_badge"),
    # modify score (this overrides the user's score)
    path(
        "v1/modify_score/<int:user_id>/<int:new_score>/",
        views.modify_score,
        name="modify_score",
    ),
    # updatescore when unit - section - course completed, it adds the parameter to the old  score
    path(
        "v1/update_score/<int:user_id>/<str:type>/",
        views.update_score,
        name="update_score",
    ),
    # Award
    path("v1/awards/", views.award_list, name="award-list"),
    path("v1/awards/<int:pk>/", views.award_detail, name="award-detail"),
    # UserAwards
    path("v1/user_awards/", views.user_award_list, name="user_award_list"),
    path("v1/user_awards/<int:user_id>/", views.get_user_award, name="get_user_award"),
    path("v1/user_awards/create/", views.user_award_create, name="user_award_create"),
    path(
        "v1/user_awards/update/<int:pk>/",
        views.user_award_update,
        name="user_award_update",
    ),
    # this one should be called when a user(user_id) clicks convert on a certain award(award_id) and it handles how awards are given it return
    # it return award granted for user or points isnufficient
    path(
        "v1/handle_award/<int:user_id>/<int:award_id>/",
        views.handle_award,
        name="handle_award",
    ),
    # last_time_played_spinning_wheel
    path(
        "v1/user_gamifications/wheel_time/<int:user_id>/",
        views.get_last_time_played_spinningwheel,
        name="get-last-time-played-spinningwheel",
    ),
    path(
        "v1/user_gamifications/wheel_time_update/<int:user_id>/",
        views.update_last_time_played_spinningwheel,
        name="update-last-time-played-spinningwheel",
    ),
    # leaderboard data
    path("v1/leaderboard/", views.get_leaderboard, name="leaderboard"),
    path("v1/leaderboard/<int:user_id>/", views.get_leaderboard_user, name="leaderboard of user"),

    # user_page_data
    path(
        "v1/user_page/<int:user_id>/", views.get_user_page_data, name="user-page-data"
    ),
]
