from django.db import migrations

def seed_categories(apps, schema_editor):
    JobCategory = apps.get_model('employer', 'JobCategory')
    categories = ['IT', 'Marketing', 'Sales', 'Finance', 'Human Resources', 'Education', 'Healthcare', 'Engineering', 'Customer Service', 'General']
    for category_name in categories:
        JobCategory.objects.get_or_create(name=category_name)

def reverse_seed_categories(apps, schema_editor):
    JobCategory = apps.get_model('employer', 'JobCategory')
    JobCategory.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0013_alter_job_category'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed_categories),
    ]
