from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gamification, UserGamification
from .models import Badge, UserBadge
from .models import Award
from .models import UserGamification
from .serializers import GamificationSerializerGet, GamificationSerializerPut
from .serializers import UserGamificationSerializerGet, UserGamificationSerializerPut
from .serializers import BadgeSerializer, UserBadgeSerializer
from .serializers import AwardSerializer
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


# this is a function called by update score api_view to handle userGamification to be created when non-existant
def modify_score_user(user_id, new_score):
    try:
        user = UserGamification.objects.get(user_id=user_id)
        current_score = user.score
        badges = Badge.objects.all()

        # checking if user has any badges
        for badge in badges:
            if new_score >= badge.rule and current_score < badge.rule:
                UserBadge.objects.create(user_id=user.user_id, badge_id=badge)

        # checking if user should lose badges
        for badge in badges:
            if new_score < badge.rule and current_score >= badge.rule:
                UserBadge.objects.filter(user_id=user.user_id, badge_id=badge).delete()
    except UserGamification.DoesNotExist:
        return Response({"message": "UserGamification not found"}, status=404)

    # simpler code  here for userGamification modification/creation  without serializers
    # try:
    # score_user = UserGamification.objects.get(user_id=user_id)
    # score_user.score = new_score
    # score_user.save()
    # except UserGamification.DoesNotExist:
    # # create an object of UserGamification with the points received
    # UserGamification.objects.create(user_id=user_id, score=new_score)
    try:
        score_user = UserGamification.objects.get(user_id=user_id)

    except UserGamification.DoesNotExist:
        # create an object of UserGamification with the points recieved
        score_user = {
            "score": new_score,
            "user_id": user_id,
        }
        serializer = UserGamificationSerializerPut(data=score_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    print("score_user", score_user)

    score_user.score = new_score
    score_user.save()

    serializer = UserGamificationSerializerPut(data=score_user)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


# api view that handles modification score for api calls it is different from modifi_user_score


@api_view(["PUT"])
def modify_score(request, user_id, new_score):
    modify_score_user(user_id, new_score)
    # if api_response.status_code == 200:
    #     response_data = api_response.data
    #     return Response(f"API Response: {response_data['message']}")
    # else:
    #     # Handle errors or other responses
    return Response("user score and badge modified")


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


def create_user_badge(user_id, badge_id):
    user_badge = {
        "user_id": user_id,
        "badge_id": badge_id,
    }
    serializer = UserBadgeSerializer(data=user_badge)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def delete_user_badge(request, user_badge_id):
    user_badge = get_object_or_404(UserBadge, pk=user_badge_id)
    user_badge.delete()
    return Response({"message": "User badge deleted successfully."})


@api_view(["POST"])
def update_score(request, user_id, type):
    try:
        user_gamification = UserGamification.objects.get(user_id=user_id)
        total_score = (
            user_gamification.score
        )  # if no condition met in if elif statements, score is made to old score
        gamification = Gamification.objects.get(id=1)

        if type == "unit":
            new_score = gamification.learning_unit_completed + total_score
            print(new_score)

        elif type == "section":
            new_score = gamification.learning_section_completed + total_score
        elif type == "course":
            new_score = gamification.course_completed + total_score
        elif type == "program":
            new_score = gamification.program_completed + total_score

        modify_score_user(user_id, new_score)  # this function also handles badges

        return Response(
            {"message": "Score updated successfully."}
        )  # Return the response
    except UserGamification.DoesNotExist:
        return Response({"message": "UserGamification not found for user "}, status=404)
    except Gamification.DoesNotExist:
        return Response({"message": "Gamification not found"}, status=404)

    return Response({"message": "Type 'unit' not found"}, status=400)


# Awards
@api_view(["GET", "POST"])
def award_list(request):
    if request.method == "GET":
        awards = Award.objects.all()
        serializer = AwardSerializer(awards, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def award_detail(request, pk):
    try:
        award = Award.objects.get(pk=pk)
    except Award.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AwardSerializer(award)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = AwardSerializer(award, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        award.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
