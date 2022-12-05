from django.contrib.auth.models import (
    BaseUserManager, AbstractUser, PermissionsMixin
)
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.db import models
from django.apps import apps



class UserManager(BaseUserManager):

    #* Настройка встроенного пользователя.
    
    use_in_migrations = True
    
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self._create_user(username, email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    
    #* Кастомный пользователь, принимающий имя, почту, пароль.
    
    username = models.CharField(db_index=True, max_length=80)
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    #* функция генерации кода
    
    def create_activation_code(self):
        import uuid 
        code = str(uuid.uuid4())
        self.activation_code = code 