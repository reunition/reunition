from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        view=views.detail_view,
        name='detail',
    ),
    url(
        r'^(?P<pk>\d+)/reports/$',
        view=views.reports_view,
        name='reports',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/$',
        view=views.rsvp_view,
        name='rsvp',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/initial_form/$',
        view=views.rsvp_initial_form_view,
        name='rsvp_initial_form',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/update/$',
        view=views.rsvp_update_view,
        name='rsvp_update',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/alumni/add/$',
        view=views.rsvp_alumni_add_view,
        name='rsvp_alumni_add',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/alumni/(?P<attendee_pk>\d+)/edit/$',
        view=views.rsvp_alumni_edit_view,
        name='rsvp_alumni_edit',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/alumni/(?P<attendee_pk>\d+)/remove/$',
        view=views.rsvp_alumni_remove_view,
        name='rsvp_alumni_remove',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/guests/add/$',
        view=views.rsvp_guest_add_view,
        name='rsvp_guest_add',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/guests/(?P<attendee_pk>\d+)/edit/$',
        view=views.rsvp_guest_edit_view,
        name='rsvp_guest_edit',
    ),
    url(
        r'^(?P<pk>\d+)/rsvp/guests/(?P<attendee_pk>\d+)/remove/$',
        view=views.rsvp_guest_remove_view,
        name='rsvp_guest_remove',
    ),
]
