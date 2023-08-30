from django.conf import settings
from django.urls import path, re_path
# from .views import PostList, PostDetail 
from . import views



urlpatterns = [
    path('v1/gamification_parameters/', views.get_gamification_parameters, name='get-gamification_parameters'),
    path('v1/gamification_parameters/modify/', views.modify_gamification_parameters , name='modify-gamification_parameters'),
]