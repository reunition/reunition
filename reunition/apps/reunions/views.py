from datetime import date

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView

from reunition.apps.alumni import models as alumni_m

from . import forms as f
from . import models as m


def redirect_to_latest(request):
    # TODO: don't assume only a single graduating class
    today = date.today()
    reunion = m.Reunion.objects.filter(starts_on__gte=today).order_by('starts_on')[0]
    return redirect(
        'reunions:detail',
        pk=reunion.pk,
    )


# ------------------------------------------


class ReunionDetailView(DetailView):

    model = m.Reunion
    context_object_name = 'reunion'


detail_view = ReunionDetailView.as_view()


# ------------------------------------------


class ReunionReportsView(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):

    model = m.Reunion
    context_object_name = 'reunion'
    template_name_suffix = '_reports'

    raise_exception = True


reports_view =  ReunionReportsView.as_view()


# ------------------------------------------


class GetRsvpMixin(object):

    def get_reunion(self):
        return m.Reunion.objects.get(pk=self.kwargs['pk'])

    def get_rsvp(self):
        reunion = self.get_reunion()
        return reunion.rsvp_set.get(created_by=self.request.user)


class GetAttendeeMixin(object):

    attendee_class = None

    def get_attendee(self):
        attendee = self.attendee_class.objects.get(
            pk=self.kwargs['attendee_pk'],
            rsvp=self.get_rsvp(),
        )
        return attendee


class RedirectToRsvpOnSuccessMixin(object):

    def get_success_url(self):
        return reverse('reunions:rsvp', kwargs=dict(pk=self.kwargs['pk']))


class RsvpView(LoginRequiredMixin, DetailView):

    model = m.Reunion
    context_object_name = 'reunion'
    template_name_suffix = '_rsvp'

    def get_context_data(self, **kwargs):
        context = super(RsvpView, self).get_context_data(**kwargs)
        rsvp = self.request.user.rsvp_set.filter(reunion=self.object).first()
        if rsvp:
            context.update(
                rsvp=rsvp,
                update_form=f.UpdateForm(initial=dict(
                    attending=rsvp.attending,
                    current_city=rsvp.current_city,
                    contact_method=rsvp.contact_method,
                    phone=rsvp.phone,
                ))
            )
        else:
            context.update(self._initial_form_context_data())
        return context

    def _initial_form_context_data(self):
        form_data = {}
        fb_account = self.request.user.socialaccount_set.filter(provider='facebook').first()
        if fb_account:
            fb_data = fb_account.extra_data
            first_name = fb_data.get('first_name')
            last_name = fb_data.get('last_name')
            alumnus = alumni_m.Person.objects.matching_any_name_in_class(
                self.object.graduating_class, first_name, last_name)
            if alumnus:
                message = """
                    We matched your Facebook contact information with our alumni roster.
                    Please complete the following and change your current name if necessary.
                """
                messages.add_message(self.request, messages.INFO, message)
                form_data.update(
                    graduation_first_name=alumnus.graduation_first_name,
                    graduation_last_name=alumnus.graduation_last_name,
                    current_first_name=alumnus.current_first_name,
                    current_last_name=alumnus.current_last_name,
                )
            else:
                message = 'Is this information correct? Please change your current or graduation names as needed.'
                messages.add_message(self.request, messages.INFO, message)
                form_data.update(
                    graduation_first_name=first_name,
                    graduation_last_name=last_name,
                )
        initial_form = f.InitialForm(initial=form_data)
        return dict(
            initial_form=initial_form,
        )


class RsvpInitialFormView(LoginRequiredMixin, FormView):

    form_class = f.InitialForm
    template_name = 'reunions/reunion_rsvp_initial_form.html'

    def get_reunion(self):
        return m.Reunion.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('reunions:rsvp', kwargs=dict(pk=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        data = super(RsvpInitialFormView, self).get_context_data(**kwargs)
        data.update(
            reunion=self.get_reunion(),
        )
        return data

    def form_invalid(self, form):
        message = 'Please fill in the required fields to continue.'
        messages.add_message(self.request, messages.WARNING, message)
        return super(RsvpInitialFormView, self).form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        reunion = self.get_reunion()
        if not m.Rsvp.objects.filter(created_by=self.request.user, reunion=reunion).exists():
            rsvp = m.Rsvp.objects.create(
                created_by=self.request.user,
                reunion=reunion,
                attending=data['attending'],
                current_city=data['current_city'],
                contact_method=data['contact_method'],
                phone=data['phone'],
            )
            rsvp.add_alumni_attendee_by_name(
                graduation_first_name=data['graduation_first_name'],
                graduation_last_name=data['graduation_last_name'],
                current_first_name=data['current_first_name'],
                current_last_name=data['current_last_name'],
                request=self.request,
            )
        return super(RsvpInitialFormView, self).form_valid(form)


class RsvpUpdateView(GetRsvpMixin, LoginRequiredMixin, FormView):

    form_class = f.UpdateForm
    template_name = 'reunions/reunion_rsvp_update.html'

    def form_valid(self, form):
        rsvp = self.get_rsvp()
        for k, v in form.cleaned_data.items():
            setattr(rsvp, k, v)
        rsvp.save()
        return super(RsvpUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        # Don't allow GET for this form.
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        data = super(RsvpUpdateView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        data.update(
            reunion=rsvp.reunion,
            rsvp=rsvp,
        )
        return data

    def get_success_url(self):
        return reverse('reunions:rsvp', kwargs=dict(pk=self.kwargs['pk']))


class RsvpAlumniAddView(GetRsvpMixin,
                        LoginRequiredMixin,
                        RedirectToRsvpOnSuccessMixin,
                        FormView):

    form_class = f.AlumniAddForm
    template_name = 'reunions/reunion_rsvp_alumni_add.html'

    def form_valid(self, form):
        data = form.cleaned_data
        self.get_rsvp().add_alumni_attendee_by_name(
            graduation_first_name=data['graduation_first_name'],
            graduation_last_name=data['graduation_last_name'],
            current_first_name=data['current_first_name'],
            current_last_name=data['current_last_name'],
            request=self.request,
            always_update_current_name=False,
        )
        return super(RsvpAlumniAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpAlumniAddView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
        )
        return data


class RsvpAlumniEditView(GetRsvpMixin,
                         GetAttendeeMixin,
                         LoginRequiredMixin,
                         RedirectToRsvpOnSuccessMixin,
                         FormView):

    attendee_class = m.RsvpAlumniAttendee
    form_class = f.AlumniUpdateForm
    template_name = 'reunions/reunion_rsvp_alumni_edit.html'

    def form_valid(self, form):
        data = form.cleaned_data
        attendee = self.get_attendee()
        person = attendee.person
        person.current_first_name = data['current_first_name']
        person.current_last_name = data['current_last_name']
        person.save()
        return super(RsvpAlumniEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpAlumniEditView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
            attendee=self.get_attendee(),
        )
        return data

    def get_initial(self):
        attendee = self.get_attendee()
        return dict(
            current_first_name=attendee.person.current_first_name,
            current_last_name=attendee.person.current_last_name,
        )


class RsvpAlumniRemoveView(GetRsvpMixin,
                           GetAttendeeMixin,
                           LoginRequiredMixin,
                           RedirectToRsvpOnSuccessMixin,
                           FormView):

    attendee_class = m.RsvpAlumniAttendee
    form_class = Form  # empty form
    template_name = 'reunions/reunion_rsvp_alumni_remove.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_rsvp().rsvpalumniattendee_set.count() == 1:
            return HttpResponseRedirect(self.get_success_url())

        return super(RsvpAlumniRemoveView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        attendee = self.get_attendee()
        attendee.delete()
        message = '{} removed from alumni list.'.format(attendee)
        messages.add_message(self.request, messages.SUCCESS, message)
        return super(RsvpAlumniRemoveView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpAlumniRemoveView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
            attendee=self.get_attendee(),
        )
        return data


class RsvpGuestAddView(GetRsvpMixin,
                       LoginRequiredMixin,
                       RedirectToRsvpOnSuccessMixin,
                       FormView):

    form_class = f.GuestForm
    template_name = 'reunions/reunion_rsvp_guest_add.html'

    def form_valid(self, form):
        data = form.cleaned_data
        self.get_rsvp().rsvpguestattendee_set.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            relationship=data['relationship'],
        )
        return super(RsvpGuestAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpGuestAddView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
        )
        return data


class RsvpGuestEditView(GetRsvpMixin,
                        GetAttendeeMixin,
                        LoginRequiredMixin,
                        RedirectToRsvpOnSuccessMixin,
                        FormView):

    attendee_class = m.RsvpGuestAttendee
    form_class = f.GuestForm
    template_name = 'reunions/reunion_rsvp_guest_edit.html'

    def form_valid(self, form):
        data = form.cleaned_data
        attendee = self.get_attendee()
        attendee.first_name = data['first_name']
        attendee.last_name = data['last_name']
        attendee.relationship = data['relationship']
        attendee.save()
        return super(RsvpGuestEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpGuestEditView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
            attendee=self.get_attendee(),
        )
        return data

    def get_initial(self):
        attendee = self.get_attendee()
        return dict(
            first_name=attendee.first_name,
            last_name=attendee.last_name,
            relationship=attendee.relationship,
        )


class RsvpGuestRemoveView(GetRsvpMixin,
                          GetAttendeeMixin,
                          LoginRequiredMixin,
                          RedirectToRsvpOnSuccessMixin,
                          FormView):

    attendee_class = m.RsvpGuestAttendee
    form_class = Form  # empty form
    template_name = 'reunions/reunion_rsvp_guest_remove.html'

    def form_valid(self, form):
        data = form.cleaned_data
        attendee = self.get_attendee()
        attendee.delete()
        message = '{} removed from guest list.'.format(attendee)
        messages.add_message(self.request, messages.SUCCESS, message)
        return super(RsvpGuestRemoveView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RsvpGuestRemoveView, self).get_context_data(**kwargs)
        rsvp = self.get_rsvp()
        reunion = rsvp.reunion
        data.update(
            rsvp=rsvp,
            reunion=reunion,
            attendee=self.get_attendee(),
        )
        return data


rsvp_view = RsvpView.as_view()
rsvp_initial_form_view = RsvpInitialFormView.as_view()
rsvp_update_view = RsvpUpdateView.as_view()
rsvp_alumni_add_view = RsvpAlumniAddView.as_view()
rsvp_alumni_edit_view = RsvpAlumniEditView.as_view()
rsvp_alumni_remove_view = RsvpAlumniRemoveView.as_view()
rsvp_guest_add_view = RsvpGuestAddView.as_view()
rsvp_guest_edit_view = RsvpGuestEditView.as_view()
rsvp_guest_remove_view = RsvpGuestRemoveView.as_view()
