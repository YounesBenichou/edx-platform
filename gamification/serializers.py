from rest_framework import serializers
from .models import Gamification, UserGamification
# from .models import Badge


class GamificationSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Gamification
        fields = "__all__"


class GamificationSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Gamification
        fields = "__all__"


class UserGamificationSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = "__all__"


class UserGamificationSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = UserGamification
        fields = "__all__"


# class BadgeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Badge
#         fields = "__all__"
