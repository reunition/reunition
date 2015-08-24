from django.core.management.base import NoArgsCommand
from django.db.models.fields import related

from reunition.apps.alumni import models as alumni_m
from reunition.apps.reunions import models as reunions_m


class Command(NoArgsCommand):

    help = 'Associate reunions.Rsvp.created_by to alumni.Person.user when not yet set'

    def handle_noargs(self, **options):
        for rsvp in reunions_m.Rsvp.objects.all():
            user = rsvp.created_by
            try:
                user.person
            except alumni_m.Person.DoesNotExist, e:
                first_alumni_added = rsvp.rsvpalumniattendee_set.order_by('created').first()
                if first_alumni_added:
                    person = first_alumni_added.person
                    print 'Associating user', user, 'with person', person
                    person.user = user
                    person.save()
