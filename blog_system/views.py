# from rest_framework import generics

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import User

####
from .models import Post, LikePost, PostComment
from .serializers import PostSerializer, PostCommentSerializer, PutSerializerWithoutImage, PutSerializer, LikePostSerializer


@api_view(["POST"])  # this gets a list of  posts or gets one post
def post_list(request):
    if request.method == "POST":
        paginator = PageNumberPagination()
        paginator.page_size = 9
        filterPost = request.data.get('filterPost')
        if request.data.get('filterPost') is "" :
            page = paginator.paginate_queryset(Post.objects.filter(is_published=True), request)
        else :
            page = paginator.paginate_queryset(Post.objects.filter(title__icontains=filterPost,is_published=True), request)
        serializer = PostSerializer(page, many=True)
        response_data = {
        'num_pages': paginator.page.paginator.num_pages,
        'results': serializer.data,
        }
        result = paginator.get_paginated_response(response_data)
        return result

@api_view(["GET"])
def my_post_list(request,user_id):
    if request.method == "GET":
        my_posts = Post.objects.filter(user_id=user_id)
        serializer = PostSerializer(my_posts, many=True)
        # new_my_posts = []
        # for post in serializer.data:  
        #     likes = LikePost.objects.filter(post_id=post['id'])
        #     post['number_of_likes'] = len(likes)
        #     new_my_posts.append(post)
        return Response(serializer.data,status=200)
        
@api_view(["POST"])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk, user_id):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        if int(user_id) != post.user_id.id:
            post.number_of_views += 1
            post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"})

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"})

@api_view(["PUT", "PATCH"])
def post_modify(request, pk=None):
    if request.method == "PUT":
        post = Post.objects.get(id=pk)
        serializer = PutSerializerWithoutImage(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
        cover_photo = request.data.get('cover_photo')
        if '/media/post_covers/' not in cover_photo:
            post.cover_photo = cover_photo
            post.save()
            return Response(status=200)
            
        print(serializer.is_valid())
        errors = serializer.errors
        for field, field_errors in errors.items():
            print(f"Field '{field}': {', '.join(field_errors)}")
        return Response(status=200)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(["POST"])
def toggle_view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.is_published:
        post.is_published = False
        message = "Post unpublished successfully."
    else:
        post.is_published = True
        message = "Post published successfully."

    post.save()
    return Response({"message": message})
