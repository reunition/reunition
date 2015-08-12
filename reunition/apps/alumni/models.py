from django.db import models


class GraduatingClass(models.Model):

    school = models.ForeignKey('School')
    year = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Graduating Classes'
        unique_together = [
            ('school', 'year'),
        ]

    def __unicode__(self):
        return u'{0.school.name} class of {0.year}'.format(self)


class Person(models.Model):

    graduating_class = models.ForeignKey('GraduatingClass')
    graduation_first_name = models.CharField(max_length=100)
    graduation_last_name = models.CharField(max_length=100)
    current_first_name = models.CharField(max_length=100, blank=True, null=True)
    current_last_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'People'

    @property
    def display_name(self):
        if not self.current_first_name and not self.current_last_name:
            # No new names
            return u'{0.graduation_first_name} {0.graduation_last_name}'.format(self)
        elif not self.current_first_name and self.current_last_name:
            # New last name
            return u'{0.graduation_first_name} {0.current_last_name} ({0.graduation_last_name})'.format(self)
        elif self.current_first_name and not self.current_last_name:
            # New first name
            return u'{0.current_first_name} ({0.graduation_first_name}) {0.graduation_last_name}'.format(self)
        else:
            # New first and last name
            return u'{0.current_first_name} {0.current_last_name} ({0.graduation_first_name} {0.graduation_last_name})'.format(self)

    def __unicode__(self):
        return self.display_name


class School(models.Model):

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
