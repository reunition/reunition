from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', view=views.ReunionDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/rsvp/$', view=views.ReunionRsvpView.as_view(), name='rsvp'),
]
