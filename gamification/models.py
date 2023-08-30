from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


# Gamification parametres
class Gamification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    course_completed = models.IntegerField(
        default=0, null=True, blank=True
    )  # blankTrue means it is nor required
    program_completed = models.IntegerField(
        default=0, null=True, blank=True
    )  # blankTrue means it is nor required
    learning_section_completed = models.IntegerField(
        default=0, null=True, blank=True
    )  # blankTrue means it is nor required
    learning_unit_completed = models.IntegerField(
        default=0, null=True, blank=True
    )  # blankTrue means it is nor required

    def __str__(self):
        return "Gamification parameters"


# UserGamification table to store the scores of users
class UserGamification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        default=0, null=True, blank=True
    )  # blankTrue means it is nor required
    last_time_played_spinningwheel = models.DateTimeField(null=True, blank=True)

# Badge Model


class Badge(models.Model):
    badge_image = models.ImageField(upload_to="badge_images/")
    name = models.CharField(max_length=255)
    rule = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name
