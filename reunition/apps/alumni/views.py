from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.views.generic import DetailView, FormView

from . import forms as f
from . import models as m


class NoteAddView(LoginRequiredMixin, StaffuserRequiredMixin, FormView):

    form_class = f.NoteAddForm
    template_name = 'alumni/note_add.html'

    def get_person(self):
        return m.Person.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        data = form.cleaned_data
        note = m.Note.objects.create(
            created_by=self.request.user,
            person=self.get_person(),
            contacted=data['contacted'],
            text=data['notes'],
        )
        return super(NoteAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(NoteAddView, self).get_context_data(**kwargs)
        data['person'] = self.get_person()
        return data

    def get_success_url(self):
        return self.get_person().get_absolute_url()

note_add_view = NoteAddView.as_view()


class PersonDetailView(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):

    model = m.Person
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        data = super(PersonDetailView, self).get_context_data(**kwargs)
        person = self.object
        data['note_add_form'] = f.NoteAddForm()
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
        return data

detail_view = PersonDetailView.as_view()
