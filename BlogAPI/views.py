from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView    # <- as super to your class
from rest_framework.response import Response  # <- to send data to the frontend
from rest_framework import status # <- to include status codes in your response
from .models import Article
from .serializers import ArticleSerializer # <- to format data to and from the database, enforces schema

from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework import status
from .serializers import LoginSerializer
from .serializers import UserRegisterSerializer
from .serializers import UserSerializer
from rest_framework import generics

#add to top
from .serializers import LoginSerializer, UserSerializer


class ProfileView(APIView): # will be protected by default
    
    def get(self, request):
        user = UserSerializer(request.user).data
        return Response(user)


class Blog(APIView):
  def get(self, request):
    # Index Request
    print(request)
    # Get all books from the book table
    blog = Article.objects.all()
    # Use serializer to format table data to JSON
    data = ArticleSerializer(blog, many=True).data
    return Response(data)



#  POST    /people - create
  def post(self, request):
    # Post Request
    print(request.data)
    # format data for postgres
    blogs = ArticleSerializer(data=request.data)
    if blogs.is_valid():
      blogs.save()
      return Response(blogs.data, status=status.HTTP_201_CREATED)
    else: 
      return Response(blogs.errors, status=status.HTTP_400_BAD_REQUEST)

# class  (PeopleDetail) - use primary key (pk) as argument to access id
#  GET     /people/:id - show

class BlogDetail(APIView):

  def get(self, request, slug):
    # Show Request
    print(request)
    blogs = get_object_or_404(Article, slug=slug)
    data = ArticleSerializer(blogs).data
    return Response(data)

  def put(self, request, slug):
    # Update Request
    print(request)
    blogs = get_object_or_404(Article, slug=slug)
    updated = ArticleSerializer(blogs, data=request.data, partial=True)
    if updated.is_valid():
      updated.save()
      return Response(updated.data)
    else:
      return Response(updated.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, slug):
    # Delete Request
    print(request)
    blogs = get_object_or_404(Article, slug=slug)
    blogs.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data,
            context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class SignUpView(generics.CreateAPIView):
    # This view should be accessible also for unauthenticated users.
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        print(request.data)
        user = UserRegisterSerializer(data=request.data)
        if user.is_valid():
            created_user = UserSerializer(data=user.data)
            if created_user.is_valid():
                created_user.save()
                return Response({ 'user': created_user.data }, status=status.HTTP_201_CREATED)
            else:
                return Response(created_user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)