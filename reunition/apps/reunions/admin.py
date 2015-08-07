from django.contrib import admin

from .models import Reunion


class ReunionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reunion, ReunionAdmin)
