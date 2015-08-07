from django.db import models


class Reunion(models.Model):

    graduating_class = models.ForeignKey('alumni.GraduatingClass')
    year = models.PositiveIntegerField()
    starts_on = models.DateField()
    ends_on = models.DateField()

    def __unicode__(self):
        return u'{0.year}-year reunion of the {0.graduating_class}'.format(self)
