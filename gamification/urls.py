from django.conf import settings
from django.urls import path, re_path

# from .views import PostList, PostDetail
from . import views


urlpatterns = [
    # gamification parameters
    path('v1/gamification_parameters/', views.get_gamification_parameters, name='get-gamification_parameters'),
    path('v1/gamification_parameters/modify/', views.modify_gamification_parameters , name='modify-gamification_parameters'),

    # Score
    # path('v1/socre_user/<int:user_id>/', views.get_score_user, name='get-score_user'),
   
    # Badge
    # path("/v1/badges/", views.get_all_badges, name="get_all_badges"),
    # path("/v1/badge/<int:badge_id>/", views.get_badge, name="get_badge"),
    # path("/v1/badge/<int:badge_id>/modify/", views.modify_badge, name="modify_badge"),
]
