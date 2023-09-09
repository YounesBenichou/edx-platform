# from rest_framework import generics

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User

####
from .models import Post, LikePost, PostComment
from .serializers import PostSerializer, PostCommentSerializer, LikePostSerializer


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        post.number_of_views += 1
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"})


@api_view(["GET"])
def post_comment_list(request, post_id):
    comments = PostComment.objects.filter(post_id=post_id)
    serializer = PostCommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def post_comment_create(request, user_id, post_id):
    user = get_object_or_404(User, pk=user_id)
    post = get_object_or_404(Post, pk=post_id)

    content = request.data.get("content", "")
    parent_comment_id = request.data.get("parent_comment_id")

    post_comment = PostComment.objects.create(
        user_id=user, post_id=post, content=content, parent_comment_id=parent_comment_id
    )
    serializer = PostCommentSerializer(post_comment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def post_comment_detail(request, pk):
    try:
        comment = PostComment.objects.get(pk=pk)
    except PostComment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostCommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def like_post_list(request, post_id):
    likes = LikePost.objects.filter(post_id=post_id)
    serializer = LikePostSerializer(likes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def like_post_create(request):
    serializer = LikePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def like_post_delete(request, user_id, post_id):
    try:
        like = LikePost.objects.get(user_id=user_id, post_id=post_id)
    except LikePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    like.delete()
    return Response({"message": "like deleted"})
