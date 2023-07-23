# Generated by Django 4.2.3 on 2023-07-23 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0002_remove_memory_internal_memory_ram_memory_rom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='modules',
        ),
        migrations.AddField(
            model_name='camera',
            name='module',
            field=models.IntegerField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='RAM',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='ROM',
            field=models.IntegerField(null=True),
        ),
    ]