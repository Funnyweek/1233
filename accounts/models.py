from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError("Нужен username")
        if not email:
            raise ValueError("Нужен email")
        
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        
        return self.create_user(username=username, email=email, password=password, **kwargs)


class CustomUser(AbstractUser):
    """
    Минимальный Custom User
    Только то что нужно для авторизации
    """
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    Дополнительная информация о пользователе
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
