from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView

from .models import Reunion


def redirect_to_latest(request):
    # TODO: don't assume only a single graduating class
    today = date.today()
    reunion = Reunion.objects.filter(starts_on__gte=today).order_by('starts_on')[0]
    return redirect(
        'reunions:detail',
        pk=reunion.pk,
    )


class ReunionDetailView(DetailView):

    model = Reunion
    context_object_name = 'reunion'


class ReunionRsvpView(DetailView):

    model = Reunion
    context_object_name = 'reunion'
    template_name_suffix = '_rsvp'
