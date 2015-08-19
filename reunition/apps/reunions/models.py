from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.models import TimeStampedModel

from reunition.apps.alumni import models as alumni_m


class Reunion(models.Model):

    graduating_class = models.ForeignKey('alumni.GraduatingClass')
    year = models.PositiveIntegerField()
    starts_on = models.DateField()
    ends_on = models.DateField()
    city = models.CharField(max_length=200, blank=True, null=True)
    intro_text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{0.year}-year reunion of the {0.graduating_class}'.format(self)

    def get_absolute_url(self):
        return reverse('reunions:detail', kwargs=dict(pk=self.pk))

    def _counts(self, qs):
        all = qs
        yes = all.filter(rsvp__attending='Y')
        maybe = all.filter(rsvp__attending='M')
        no = all.filter(rsvp__attending='N')
        return dict(
            all=all.count(),
            yes=yes.count(),
            maybe=maybe.count(),
            no=no.count(),
        )

    def alumni_counts(self):
        return self._counts(RsvpAlumniAttendee.objects.filter(rsvp__reunion=self))

    def guest_counts(self):
        return self._counts(RsvpGuestAttendee.objects.filter(rsvp__reunion=self))


class RsvpManager(models.Manager):

    def yes(self):
        return self.filter(attending='Y')

    def maybe(self):
        return self.filter(attending='M')

    def no(self):
        return self.filter(attending='N')


class Rsvp(TimeStampedModel):

    objects = RsvpManager()

    ATTENDING_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('M', 'Maybe'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('text', 'Text'),
        ('phone', 'Phone Call'),
        ('none', 'Please do not send me updates'),
    ]

    created_by = models.ForeignKey('auth.User')
    reunion = models.ForeignKey('reunions.Reunion')
    attending = models.CharField(max_length=1, blank=True, null=True, choices=ATTENDING_CHOICES)
    current_city = models.CharField(max_length=200, blank=True, null=True)
    contact_method = models.CharField(max_length=5, choices=CONTACT_METHOD_CHOICES)
    phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = [
            ('created_by', 'reunion'),
        ]

    def add_alumni_attendee_by_name(self, graduation_first_name, graduation_last_name,
                                    current_first_name, current_last_name, request=None,
                                    always_update_current_name=True):
        # Look for existing person that has not yet RSVPd; add to rsvp if found.
        person = alumni_m.Person.objects.matching_graduation_name_in_class(
            self.reunion.graduating_class,
            first_name=graduation_first_name,
            last_name=graduation_last_name
        )
        if person:
            already_registered = RsvpAlumniAttendee.objects.filter(rsvp=self, person=person).exists()
            if already_registered:
                if request:
                    message = '{} has already RSVPd. Please contact us if you think this is in error.'.format(person)
                    messages.add_message(request, messages.WARNING, message)
                person = None
            else:
                changed = False
                L = locals()
                for field in ['current_first_name', 'current_last_name']:
                    value = L[field]
                    if always_update_current_name or value:
                        setattr(person, field, value)
                        changed = True
                if changed:
                    person.save()
        else:
            person = alumni_m.Person.objects.create(
                graduating_class=self.reunion.graduating_class,
                graduation_first_name=graduation_first_name,
                graduation_last_name=graduation_last_name,
                current_first_name=current_first_name,
                current_last_name=current_last_name,
                verified=None,
            )
        if person:
            self.rsvpalumniattendee_set.create(person=person)


class AbstractRsvpAttendee(TimeStampedModel):

    rsvp = models.ForeignKey('reunions.Rsvp')

    class Meta:
        abstract = True


class RsvpAlumniAttendee(AbstractRsvpAttendee):

    person = models.ForeignKey('alumni.Person')

    class Meta:
        ordering = ('person__graduation_first_name',)
        unique_together = [
            ('rsvp', 'person'),
        ]

    def __unicode__(self):
        return unicode(self.person)


class RsvpGuestAttendee(AbstractRsvpAttendee):

    RELATIONSHIP_CHOICES = [
        ('P', 'Partner/Spouse'),
        ('C', 'Child'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    relationship = models.CharField(max_length=1, blank=True, null=True, choices=RELATIONSHIP_CHOICES)

    class Meta:
        ordering = ('first_name',)

    def __unicode__(self):
        if self.last_name:
            name = u'{0.first_name} {0.last_name}'.format(self)
        else:
            name = self.first_name
        if self.relationship:
            rel_text = dict(self.RELATIONSHIP_CHOICES)[self.relationship]
            return u'{} ({})'.format(name, rel_text)
        else:
            return name
