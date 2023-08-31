from django.contrib import admin

# Register your models here.
from . import models

# Register your models here.
admin.site.register(models.Gamification)
admin.site.register(models.UserGamification)
admin.site.register(models.Badge)


# badge register
# admin.register(models.Badge)
# class BadgeAdmin(admin.ModelAdmin):
#     list_display = ("name", "rule", "created", "modified")
#     search_fields = ("name",)
#     list_filter = ("created", "modified")
