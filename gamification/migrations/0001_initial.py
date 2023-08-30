# Generated by Django 3.2.19 on 2023-08-30 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gamification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course_completed', models.IntegerField(blank=True, default=0, null=True)),
                ('program_completed', models.IntegerField(blank=True, default=0, null=True)),
                ('learning_section_completed', models.IntegerField(blank=True, default=0, null=True)),
                ('learning_unit_completed', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGamification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, default=0, null=True)),
                ('last_time_played_spinningwheel', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
