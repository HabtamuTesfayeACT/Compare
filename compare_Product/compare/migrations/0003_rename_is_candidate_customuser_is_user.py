# Generated by Django 4.2.1 on 2023-07-24 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0002_customuser_is_candidate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_candidate',
            new_name='is_user',
        ),
    ]
