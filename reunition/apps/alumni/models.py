from django.db import models


class School(models.Model):

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class GraduatingClass(models.Model):

    school = models.ForeignKey('School')
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = [
            ('school', 'year'),
        ]

    def __unicode__(self):
        return u'{0.school.name} class of {0.year}'.format(self)
