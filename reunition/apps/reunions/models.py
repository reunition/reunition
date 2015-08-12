from django.core.urlresolvers import reverse
from django.db import models


class Reunion(models.Model):

    graduating_class = models.ForeignKey('alumni.GraduatingClass')
    year = models.PositiveIntegerField()
    starts_on = models.DateField()
    ends_on = models.DateField()
    city = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'{0.year}-year reunion of the {0.graduating_class}'.format(self)

    def get_absolute_url(self):
        return reverse('reunions:detail', kwargs=dict(pk=self.pk))
