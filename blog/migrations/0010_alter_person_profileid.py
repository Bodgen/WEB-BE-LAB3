# Generated by Django 5.0.6 on 2024-06-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_person_profileid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profileId',
            field=models.CharField(default='27a75dc8-f547-4c21-8593-cfa5b55e8447', max_length=255),
        ),
    ]
