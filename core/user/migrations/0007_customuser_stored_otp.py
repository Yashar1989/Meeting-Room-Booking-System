# Generated by Django 4.2.7 on 2024-03-13 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stored_otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
