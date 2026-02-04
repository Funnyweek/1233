from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

@shared_task
def send_login_email(user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    send_mail(
        subject="Login notification",
        message="You have successfully logged in.",
        from_email=None,  # возьмётся DEFAULT_FROM_EMAIL
        recipient_list=[user.email],
        fail_silently=True,  # ошибка не ломает логин
    )
