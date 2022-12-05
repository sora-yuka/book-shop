from django.urls import path
from applications.book.views import *

urlpatterns = [
    path('', BookListApiView.as_view()),
    path('post/', BookCreateApiView.as_view()),
    path('<int:pk>/', BookRetrieve.as_view()),
    path('update/<int:pk>/', BookUpdateApiView.as_view()),
    path('delete/<int:pk>/', BookDestroyApiView.as_view())
]
