from django.conf import settings
from django.urls import path, re_path
# from .views import PostList, PostDetail 
from . import views

# urlpatterns = [
#     path('homeblog', views.homeblog, name="homeblog"),
    
# ]

urlpatterns = [
    # path('posts/', ),
    # path('posts/<int:pk>/', PostDetail.as_view(), name='blog-detail'),
    path('v1/posts/', views.get_posts, name='post-list'),
    path('v1/posts/create/', views.create_post , name='post-create'),
]