from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from employer.models import Job, JobCategory, Review
from job_seeker.models import appliedJobs
from payments.models import PremiumFeature, FeatureItem, Order, SelectedFeature
from users.models import User, Profile, EmailVerificationToken

class Command(BaseCommand):
    help = 'Initialize groups and permissions for the job board'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing groups...")

        # Create Groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        employer_group, _ = Group.objects.get_or_create(name='Employer')
        job_seeker_group, _ = Group.objects.get_or_create(name='Job_Seeker')

        # Define Permissions for Employer
        employer_models = [Job, JobCategory, Review]
        employer_perms = []
        for model in employer_models:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            employer_perms.extend(perms)
        
        employer_group.permissions.set(employer_perms)
        self.stdout.write(self.style.SUCCESS('Successfully initialized Employer group permissions'))

        # Define Permissions for Job Seeker
        seeker_models = [appliedJobs, PremiumFeature, FeatureItem, Order, SelectedFeature, Profile, EmailVerificationToken]
        seeker_perms = []
        for model in seeker_models:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            seeker_perms.extend(perms)
        
        job_seeker_group.permissions.set(seeker_perms)
        self.stdout.write(self.style.SUCCESS('Successfully initialized Job_Seeker group permissions'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions initialized successfully!'))
