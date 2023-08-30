from django.db import models

# Create your models here.

# Badge Model


class Badge(models.Model):
    badge_image = models.ImageField(upload_to="badge_images/")
    name = models.CharField(max_length=255)
    rule = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
