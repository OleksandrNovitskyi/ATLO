# Generated by Django 4.1.4 on 2023-02-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True, default="default-user-icon-21.jpg", null=True, upload_to=""
            ),
        ),
    ]
