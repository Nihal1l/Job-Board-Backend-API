from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

def send_activation_helper(user):
    """
    Helper function to send activation email.
    Used by signals and custom resend endpoint.
    """
    print(f"DEBUG: Sending activation email to {user.email}")
    token = default_token_generator.make_token(user)
    # The URL structure matches the one expected by your frontend based on signals.py
    activation_url = f"{settings.FRONTEND_URL}/users/activate/{user.id}/{token}/"

    subject = 'Activate Your Account'
    message = f'Hi ,\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
    recipient_list = [user.email]

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return True
    except Exception as e:
        print(f"Failed to send email to {user.email}: {str(e)}")
        return False
