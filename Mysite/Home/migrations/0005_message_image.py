# Generated by Django 4.2.6 on 2024-01-02 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0004_room_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
