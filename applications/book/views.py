from django.shortcuts import render
from rest_framework.generics import *
from applications.book.models import Book
from applications.book.serializer import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .permissions import IsOwner

user = get_user_model()
    
    
##** CRUD для книг
    
class BookListApiView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
class BookRetrieve(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    
class BookCreateApiView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]    
    
    
class BookUpdateApiView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner]
    

class BookDestroyApiView(DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsOwner, IsAdminUser]