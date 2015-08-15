from django.contrib import admin

from .models import GraduatingClass, Person, School


class GraduatingClassAdmin(admin.ModelAdmin):
    pass


class PersonAdmin(admin.ModelAdmin):
    ordering = ('graduation_last_name', 'graduation_first_name')
    list_display = [
        'display_name',
        'graduation_last_name',
        'graduation_first_name',
        'verified',
    ]


class SchoolAdmin(admin.ModelAdmin):
    pass


admin.site.register(GraduatingClass, GraduatingClassAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(School, SchoolAdmin)
