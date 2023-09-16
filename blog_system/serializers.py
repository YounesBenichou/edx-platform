from rest_framework import serializers
from .models import Post, PostComment, LikePost


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class PutSerializerWithoutImage(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('cover_photo', )

        
class PutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
# PostComment serializer
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


# PostLike serializer


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = "__all__"
