from rest_framework import serializers

from .models import User
from .models import Gamification, UserGamification
from .models import Badge, UserBadge
from .models import Award, UserAward


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class GamificationSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Gamification
        fields = "__all__"


class GamificationSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Gamification
        fields = "__all__"


class UserGamificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = "__all__"


class UserGamificationSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = "__all__"


class UserGamificationSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = "__all__"


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class UserAwardSerializer(serializers.ModelSerializer):
    award_id = AwardSerializer()
    class Meta:
        model = UserAward
        fields = "__all__"


class UserGamificationLastTimePlayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = ["last_time_played_spinningwheel"]


class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    score = serializers.IntegerField()
    badges = BadgeSerializer(many=True)
