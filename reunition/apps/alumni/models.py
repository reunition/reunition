from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import TimeStampedModel


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


class Note(TimeStampedModel):

    CONTACTED_CHOICES = [
        ('', 'No contact made'),
        ('', '---'),
        ('incoming', 'This person contacted the alumni committee'),
        ('', '---'),
        ('email', 'Sent email'),
        ('facebook', 'Sent Facebook message or request'),
        ('phone', 'Made phone call'),
        ('text', 'Sent text message'),
        ('other', 'Made other contact'),
    ]

    created_by = models.ForeignKey('auth.User')
    person = models.ForeignKey('Person')
    contacted = models.CharField(max_length=10, blank=True, null=True, choices=CONTACTED_CHOICES)
    text = models.TextField()

    class Meta:
        ordering = ('created_by',)


class PersonManager(models.Manager):

    def matching_any_name_in_class(self, graduating_class, first_name, last_name):
        criteria_list = [
            dict(graduation_first_name__iexact=first_name, graduation_last_name__iexact=last_name),
            dict(graduation_first_name__iexact=first_name, current_last_name__iexact=last_name),
            dict(current_first_name__iexact=first_name, graduation_last_name__iexact=last_name),
            dict(current_first_name__iexact=first_name, current_last_name__iexact=last_name),
        ]
        for criteria in criteria_list:
            criteria = dict(criteria, graduating_class=graduating_class)
            match = self.exclude(verified=None).filter(**criteria).first()
            if match:
                return match

    def matching_graduation_name_in_class(self, graduating_class, first_name, last_name):
        criteria = dict(
            graduation_first_name__iexact=first_name,
            graduation_last_name__iexact=last_name,
            graduating_class=graduating_class,
        )
        match = self.exclude(verified=None).filter(**criteria).first()
        return match


class Person(TimeStampedModel):

    objects = PersonManager()

    graduating_class = models.ForeignKey('GraduatingClass')
    graduation_first_name = models.CharField(max_length=100)
    graduation_last_name = models.CharField(max_length=100)
    current_first_name = models.CharField(max_length=100, blank=True, null=True)
    current_last_name = models.CharField(max_length=100, blank=True, null=True)
    verified = models.DateTimeField(blank=True, null=True)
    user = models.OneToOneField('auth.User', blank=True, null=True)

    class Meta:
        ordering = ('graduation_last_name',)
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

    def get_absolute_url(self):
        return reverse('alumni:person_detail', kwargs=dict(pk=self.pk))


class School(models.Model):

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
