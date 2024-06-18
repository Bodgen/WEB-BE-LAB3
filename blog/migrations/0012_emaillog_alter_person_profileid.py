# Generated by Django 5.0.6 on 2024-06-18 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_shared_to_alter_person_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='profileId',
            field=models.CharField(default='a905dca4-73a0-481d-9991-b18147b08525', max_length=255),
        ),
    ]
