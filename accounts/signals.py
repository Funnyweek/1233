from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from .utils import send_welcome_email

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)
        send_welcome_email(instance.email)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль когда сохраняется пользователь"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
