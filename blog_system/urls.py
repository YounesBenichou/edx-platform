from django.conf import settings
from django.urls import path, re_path

# from .views import PostList, PostDetail
from . import views

urlpatterns = [
    # Posts
    path("v1/posts/", views.post_list, name="post-list"),
    path("v1/posts/<int:pk>/", views.post_detail, name="post-detail"),
    # Post Comments
    path(
        "v1/posts/<int:post_id>/comments/",
        views.post_comment_list,
        name="post-comment-list",
    ),
    path(
        "v1/posts/<int:user_id>/<int:post_id>/create_comment/",
        views.post_comment_create,
        name="post-comment-create",
    ),
    path(
        "v1/posts/comments/<int:pk>/",
        views.post_comment_detail,
        name="post-comment-detail",
    ),
    # Like Post
    path("v1/likepost/<int:post_id>/", views.like_post_list, name="like-post-list"),
    path(
        "v1/likepost/",
        views.like_post_create,
        name="like-post-create",
    ),
    path(
        "v1/likepost/<int:user_id>/<int:post_id>/",
        views.like_post_delete,
        name="like-post-delete",
    ),
]
