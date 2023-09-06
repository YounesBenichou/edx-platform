from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.images import ImageFile


from .models import User
from .models import Gamification, UserGamification
from .models import Badge, UserBadge
from .models import Award, UserAward
from .models import UserGamification
from .serializers import (
    GamificationSerializerGet,
    GamificationSerializerPut,
    LeaderboardSerializer,
    UserGamificationLastTimePlayedSerializer,
    UserGamificationSerializer,
    UserSerializer,
)
from .serializers import UserGamificationSerializerGet, UserGamificationSerializerPut
from .serializers import BadgeSerializer, UserBadgeSerializer
from .serializers import AwardSerializer, UserAwardSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
# get, create, modify, delete


# Users for usernames
@api_view(["GET"])
def user_list(request):
    """
    List all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def user_detail(request, pk):
    """
    Retrieve a single user by primary key (id).
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


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


# Get avalaible badges
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


# Userbadges
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


# Score
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
    # return Response({"message": "Type 'unit' not found"}, status=400)


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


# UserAward views


@api_view(["GET"])
def user_award_list(request):
    user_awards = UserAward.objects.all()
    serializer = UserAwardSerializer(user_awards, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_user_award(request, user_id):
    user_awards = UserAward.objects.filter(user_id=user_id).values_list(
        "award_id", flat=True
    )
    return Response(list(user_awards))


@api_view(["POST"])
def user_award_create(request):
    serializer = UserAwardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def user_award_update(request, pk):
    try:
        user_award = UserAward.objects.get(pk=pk)
    except UserAward.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserAwardSerializer(user_award, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# handling awards


@api_view(["POST"])
def handle_award(request, user_id, award_id):
    # Get the user and award objects
    user = get_object_or_404(User, pk=user_id)
    award = get_object_or_404(Award, pk=award_id)

    # Check if the user's score is sufficient for the award rule
    user_gamification = get_object_or_404(UserGamification, user_id=user_id)
    if user_gamification.score >= award.rule:
        # Deduct points from the user's score based on the award rule
        user_gamification.score -= award.rule
        user_gamification.save()

        # Create a UserAward record for the user
        user_award = UserAward.objects.create(user_id=user, award_id=award)

        # Return a success response
        return Response(
            {
                "message": f"Award '{award.name}' has been granted to user '{user.username}'."
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        # Return a response indicating insufficient score
        return Response(
            {"message": "Insufficient score to receive this award."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# spinning wheel
@api_view(["GET"])
def get_last_time_played_spinningwheel(request, user_id):
    try:
        user_gamification = UserGamification.objects.get(user_id=user_id)
    except UserGamification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserGamificationLastTimePlayedSerializer(user_gamification)
    return Response(serializer.data)


@api_view(["PUT"])
def update_last_time_played_spinningwheel(request, user_id):
    try:
        user_gamification = UserGamification.objects.get(user_id=user_id)
    except UserGamification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserGamificationLastTimePlayedSerializer(
        user_gamification, data=request.data
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Leaderboard


def get_user_badges_leaderboard(user_id):
    user_badges = UserBadge.objects.filter(user_id=user_id).order_by(
        "-created"
    )  # Sort badges by creation date in descending order
    latest_badge = (
        user_badges.first()
    )  # Get the first badge (the latest one) in the sorted list

    if latest_badge:
        print("baadge image", latest_badge.badge_id.badge_image)
        # image_object = (ImageFile(open(latest_badge.badge_id.badge_image, "rb")),)
        badge_data = {
            "badge_id": latest_badge.badge_id.id,
            "name": latest_badge.badge_id.name,
            "badge_image": latest_badge.badge_id.badge_image.url,
            "rule": latest_badge.badge_id.rule,
            # Add other badge fields as needed
        }
    else:
        badge_data = None  # No badges found for the user

    return badge_data


@api_view(["GET"])
def get_leaderboard(request):
    users = UserGamification.objects.all()
    leaderboard_data = []

    for user in users:
        user_id = user.user_id.id
        badges = get_user_badges_leaderboard(user_id)
        print("----bajes", badges)
        user_data = {
            "user_id": user.user_id.id,
            "username": user.user_id.username,  # Fetch the username from the User model
            "score": user.score,
            "badge": badges,
        }
        leaderboard_data.append(user_data)

    leaderboard_data = sorted(leaderboard_data, key=lambda x: x["score"], reverse=True)
    # serializer = LeaderboardSerializer(leaderboard_data, many=True)
    return Response(leaderboard_data)


# userpage


@api_view(["GET"])
def get_user_page_data(request, user_id):
    try:
        # Get user's gamification data
        score = UserGamification.objects.get(user_id=user_id)
        serializer_score = UserGamificationSerializerGet(score, many=False).data
    except UserGamification.DoesNotExist:
        serializer_score = None

    # Get the last created badge for the user
    last_created_badge = (
        UserBadge.objects.filter(user_id=user_id).order_by("-created").first()
    )
    if last_created_badge:
        last_created_badge_data = {
            "name": last_created_badge.badge_id.name,
            "badge_image": last_created_badge.badge_id.badge_image.url,
        }
    else:
        last_created_badge_data = None

    try:
        # Get user's last time played spinning wheel
        user_gamification = UserGamification.objects.get(user_id=user_id)
        serializer_last_time_played = UserGamificationLastTimePlayedSerializer(
            user_gamification
        ).data
    except UserGamification.DoesNotExist:
        serializer_last_time_played = None

    # Get user's awards with their id and name
    user_awards = UserAward.objects.filter(user_id=user_id)
    award_ids = user_awards.values_list("award_id", flat=True)  # Get the award IDs

    # Get the Award objects with id and name
    awards = Award.objects.filter(id__in=award_ids).values("id", "name")

    user_awards_list = list(awards)

    user_data = {
        "user_score": serializer_score,
        "last_created_badge": last_created_badge_data,
        "last_time_played_spinningwheel": serializer_last_time_played,
        "user_awards": user_awards_list,
    }

    return Response(user_data)
