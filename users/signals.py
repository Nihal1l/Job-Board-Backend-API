"""
===========================================
apps/users/signals.py
===========================================
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group

from .utils import send_activation_helper


@receiver(pre_save, sender=User)
def set_user_role(sender, instance, **kwargs):
    """Automatically set user role based on is_staff during registration/save"""
    if instance.is_staff:
        instance.role = 'employer'
    else:
        instance.role = 'job_seeker'


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        send_activation_helper(instance)


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Assign user to appropriate Django Group and grant group permissions explicitly"""
    if instance.is_active:
        try:
            if instance.is_staff:
                target_group = Group.objects.get(name='Employer')
                remove_group = Group.objects.get(name='Job_Seeker')
            else:
                target_group = Group.objects.get(name='Job_Seeker')
                remove_group = Group.objects.get(name='Employer')
            
            # Add to the correct group
            if not instance.groups.filter(name=target_group.name).exists():
                instance.groups.add(target_group)
            
            # Remove from the other group to ensure they only have one role
            if instance.groups.filter(name=remove_group.name).exists():
                instance.groups.remove(remove_group)
                
            # Explicitly grant the group's permissions to the user object
            # This makes them visible in the "Chosen permissions" box in the Django Admin
            group_permissions = target_group.permissions.all()
            instance.user_permissions.set(group_permissions)
                
        except Group.DoesNotExist:
            # Silently fail if groups are not created yet, or log it if needed
            print(f"WARNING: Group 'Employer' or 'Job_Seeker' does not exist in the database.")


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

