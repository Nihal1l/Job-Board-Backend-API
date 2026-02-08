from django.core.management.base import BaseCommand
from payments.models import PremiumFeature, FeatureItem

class Command(BaseCommand):
    help = 'Populate initial pricing plans from image'

    def handle(self, *args, **kwargs):
        # Basic Plan
        basic, _ = PremiumFeature.objects.get_or_create(
            name='Basic',
            defaults={
                'price': 9.00,
                'description': 'Essential features for individuals',
                'is_recommended': False,
                'icon_type': 'basic'
            }
        )
        basic_features = [
            'Up to 25 job applications',
            'Basic resume builder',
            'Email job alerts',
            'Profile visibility',
            'Standard support',
            'Mobile app access'
        ]
        for text in basic_features:
            FeatureItem.objects.get_or_create(premium_feature=basic, text=text)

        # Professional Plan
        pro, _ = PremiumFeature.objects.get_or_create(
            name='Professional',
            defaults={
                'price': 29.00,
                'description': 'Everything you need to succeed',
                'is_recommended': True,
                'icon_type': 'pro'
            }
        )
        pro_features = [
            'Unlimited applications',
            'AI-powered resume builder',
            'Instant job alerts',
            'Featured profile',
            'Priority support',
            'Interview coaching',
            'Salary insights',
            'Career analytics'
        ]
        for text in pro_features:
            FeatureItem.objects.get_or_create(premium_feature=pro, text=text)

        # Premium Plan
        premium, _ = PremiumFeature.objects.get_or_create(
            name='Premium',
            defaults={
                'price': 59.00,
                'description': 'Maximum visibility & results',
                'is_recommended': False,
                'icon_type': 'premium'
            }
        )
        premium_features = [
            'Everything in Professional',
            'VIP profile badge',
            'Dedicated career advisor',
            'Direct recruiter messages',
            'Exclusive job listings',
            'Company insights',
            'Network expansion tools',
            'LinkedIn integration',
            'Custom career roadmap'
        ]
        for text in premium_features:
            FeatureItem.objects.get_or_create(premium_feature=premium, text=text)

        self.stdout.write(self.style.SUCCESS('Successfully populated pricing plans'))
