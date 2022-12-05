from rest_framework import serializers
from applications.book.models import Book
from django.contrib.auth import get_user_model

user = get_user_model

class BookSerializer(serializers.ModelSerializer):
    # Класс сериализатор для создание книг
    
    owner = serializers.EmailField(required=False)
    
    class Meta:
        model = Book
        fields = '__all__'
    
    
    def create(self, validated_date):
        # Сохранение поста в бд
        
        request = self.context.get('request')
        user = request.user
        
        book = Book.objects.create(owner=user, **validated_date)
        
        return book