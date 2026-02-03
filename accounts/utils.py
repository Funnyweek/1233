from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(email):
    """Отправить приветственное письмо. Не прерывает создание пользователя при ошибке."""
    try:
        subject = "Welcome to our platform"
        message = "Thank you for signing up. We're glad to have you on board!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        # Логируем ошибку, но не прерываем создание пользователя
        logger.error(f"Failed to send welcome email to {email}: {str(e)}", exc_info=True)