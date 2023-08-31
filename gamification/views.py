from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gamification, UserGamification
from .models import Badge, UserBadge
from .serializers import GamificationSerializerGet, GamificationSerializerPut
from .serializers import UserGamificationSerializerGet, UserGamificationSerializerPut
from .serializers import BadgeSerializer, UserBadgeSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
# get, create, modify, delete


@api_view(["GET"])
def get_gamification_parameters(request):
    gamification_parameters = Gamification.objects.all()
    serializer = GamificationSerializerGet(gamification_parameters, many=True)
    return Response(serializer.data[0])


@api_view(["PUT"])
def modify_gamification_parameters(request):
    try:
        gamification_parameters = Gamification.objects.first()
    except Gamification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = GamificationSerializerPut(
            gamification_parameters, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UserGamification score
@api_view(["GET"])
def get_score_all(request):
    score_users = UserGamification.objects.all()
    serializer = UserGamificationSerializerGet(score_users, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_score_user(request, user_id):
    try:
        score = UserGamification.objects.get(user_id=user_id)
    except UserGamification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserGamificationSerializerGet(score, many=False)
    print(serializer.data)
    return Response(serializer.data)

@api_view(["PUT"])
def modify_score_user(request, user_id):
    try: 
        score_user = UserGamification.objects.get(user_id=user_id)
    except UserGamification.DoesNotExist:
        # create an object of UserGamification with the points recieved
        score_user_object = {
            "score" : request.data["points"],
            "user_id": user_id,
        }
        serializer = UserGamificationSerializerPut(data=score_user_object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    score_user.score = score_user.score + int(request.data["points"])
    score_user.save()
    return Response(status=status.HTTP_200_OK)



@api_view(["GET"])
def get_badge(request, badge_id):
    badge = Badge.objects.get(id=badge_id)
    serializer = BadgeSerializer(badge)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_badges(request):
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_badge(request):
    serializer = BadgeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["PUT"])
def modify_badge(request, badge_id):
    try:
        badge = Badge.objects.get(id=badge_id)
    except Badge.DoesNotExist:
        return Response({"message": "Badge not found."}, status=404)

    serializer = BadgeSerializer(badge, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Badge updated successfully."})

    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def delete_badge(request, badge_id):
    try:
        badge = Badge.objects.get(id=badge_id)
    except Badge.DoesNotExist:
        return Response({"message": "Badge not found."}, status=404)

    badge.delete()
    return Response({"message": "Badge deleted successfully."})


# Userbadge
@api_view(["GET"])
def get_user_badges(request, user_id):
    user_badges = UserBadge.objects.filter(user_id=user_id)
    serializer = UserBadgeSerializer(user_badges, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_user_badge(request):
    serializer = UserBadgeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def delete_user_badge(request, user_badge_id):
    user_badge = get_object_or_404(UserBadge, pk=user_badge_id)
    user_badge.delete()
    return Response({"message": "User badge deleted successfully."})
