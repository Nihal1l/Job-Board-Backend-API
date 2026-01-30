"""
===========================================
apps/users/signals.py
===========================================
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group

from .utils import send_activation_helper


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        send_activation_helper(instance)


# @receiver(post_save, sender=User)
# def resend_activation_email(sender, instance, created, **kwargs):
#     if created:
#         print(f"DEBUG: Signal fired for user {instance.email}")
#         token = default_token_generator.make_token(instance)
#         activation_url = f"{settings.FRONTEND_URL}/users/resend_activation/{instance.id}/{token}/"

#         subject = 'Activate Your Account'
#         message = f'Hi ,\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
#         recipient_list = [instance.email]

#         try:
#             send_mail(subject, message,
#                       settings.EMAIL_HOST_USER, recipient_list)
#         except Exception as e:
#             print(f"Failed to send email to {instance.email}: {str(e)}")


# # @receiver(post_save, sender=User)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     """Create profile when user is created"""
# #     if created:
# #         if instance.role == 'job_seeker' and not hasattr(instance, 'job_seeker_profile'):
# #             JobSeekerProfile.objects.create(user=instance)
# #         elif instance.role == 'employer' and not hasattr(instance, 'employer_profile'):
# #             EmployerProfile.objects.create(user=instance, company_name='')

