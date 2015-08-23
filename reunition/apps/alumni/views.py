from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views.generic import DetailView

from . import models as m


class PersonDetailView(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):

    model = m.Person
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        data = super(PersonDetailView, self).get_context_data(**kwargs)
        person = self.object
        data['reunions'] = [
            dict(
                reunion=reunion,
                attendee=person.rsvpalumniattendee_set.filter(rsvp__reunion=reunion).first(),
            )
            for reunion
            in person.graduating_class.reunion_set.all()
        ]
        if data['reunions']:
            data['contact'] = {}
            most_recent = person.rsvpalumniattendee_set.select_related('rsvp').first()
            data['contact'] = dict(
                method=most_recent.rsvp.contact_method if most_recent else None,
                phone=most_recent.rsvp.phone if most_recent else None,
                email=most_recent.rsvp.created_by.email if most_recent else None,
            )
        print data

        return data


detail_view = PersonDetailView.as_view()
