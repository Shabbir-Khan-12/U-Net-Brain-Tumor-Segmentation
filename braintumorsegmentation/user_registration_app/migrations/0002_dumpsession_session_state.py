# Generated by Django 4.2.4 on 2023-08-20 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dumpsession',
            name='session_state',
            field=models.CharField(choices=[('S', 'S'), ('E', 'E')], default='E', max_length=5),
            preserve_default=False,
        ),
    ]