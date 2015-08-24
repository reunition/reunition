from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        view=views.detail_view,
        name='person_detail',
    ),
    url(
        r'^(?P<pk>\d+)/add_note/$',
        view=views.note_add_view,
        name='note_add',
    ),
]
