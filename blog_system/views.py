# from rest_framework import generics 

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#### 
from .models import Post
from .serializers import PostSerializer
# Create your views here.

# def homeblog(request):
#     return HttpResponse("<h1> HELLO </h1>")

        
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print("test2")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)