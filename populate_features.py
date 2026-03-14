import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')
django.setup()

from payments.models import PremiumFeature, FeatureItem

def populate():
    # Clear existing data to avoid duplicates if run multiple times
    # PremiumFeature.objects.all().delete() 
    
    features = [
        {
            "name": "Basic Plan",
            "price": 0.00,
            "description": "Get started with basic features for job hunting.",
            "is_recommended": False,
            "icon_type": "basic",
            "items": [
                "Up to 5 job applications per day",
                "Basic profile visibility",
                "Email notifications for new jobs"
            ]
        },
        {
            "name": "Pro Plan",
            "price": 19.99,
            "description": "Enhance your job search with advanced tools and priority visibility.",
            "is_recommended": True,
            "icon_type": "pro",
            "items": [
                "Unlimited job applications",
                "Featured profile in search results",
                "Direct messaging to employers",
                "Advanced job filters",
                "Priority customer support"
            ]
        },
        {
            "name": "Ultimate Plan",
            "price": 49.99,
            "description": "The ultimate package for serious professionals seeking top-tier opportunities.",
            "is_recommended": False,
            "icon_type": "premium",
            "items": [
                "All Pro features included",
                "AI-powered resume optimization",
                "One-on-one career coaching session",
                "Exclusive access to 'unlisted' jobs",
                "Verified professional badge"
            ]
        }
    ]

    for feature_data in features:
        items_data = feature_data.pop('items')
        feature, created = PremiumFeature.objects.get_or_create(
            name=feature_data['name'],
            defaults=feature_data
        )
        if created:
            print(f"Created feature: {feature.name}")
            for item_text in items_data:
                FeatureItem.objects.create(premium_feature=feature, text=item_text)
                print(f"  Added item: {item_text}")
        else:
            print(f"Feature already exists: {feature.name}")

if __name__ == "__main__":
    populate()
