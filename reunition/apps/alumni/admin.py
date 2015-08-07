from django.contrib import admin

from .models import GraduatingClass, School


class GraduatingClassAdmin(admin.ModelAdmin):
    pass


class SchoolAdmin(admin.ModelAdmin):
    pass


admin.site.register(GraduatingClass, GraduatingClassAdmin)
admin.site.register(School, SchoolAdmin)
