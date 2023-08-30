from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Gamification, UserGamification
from .serializers import GamificationSerializerGet, GamificationSerializerPut
from .serializers import UserGamificationSerializerGet, UserGamificationSerializerPut

# Create your views here.
# get, create, modify, delete

@api_view(['GET'])
def get_gamification_parameters(request):
    gamification_parameters = Gamification.objects.all()
    print(gamification_parameters)
    serializer = GamificationSerializerGet(gamification_parameters, many=True)
    return Response(serializer.data[0])


@api_view(['PUT'])
def modify_gamification_parameters(request):
    try:
        gamification_parameters = Gamification.objects.first()
    except Gamification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GamificationSerializerPut(gamification_parameters, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



