""" Default urlconf for reunition """

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from django.views.generic.base import TemplateView

import reunition.views
import reunition.apps.reunions.views


sitemaps = {
    # Fill me with sitemaps
}

admin.autodiscover()

urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Allauth
    url(r'^accounts/login/$', reunition.views.login_signup_view, name='account_login'),
    url(r'^accounts/', include('allauth.urls')),

    # Alumni
    url(r'^alumni/', include('reunition.apps.alumni.urls', 'alumni', 'alumni')),

    # Reunions
    url(r'^$', reunition.apps.reunions.views.redirect_to_latest),
    url(r'^reunions/', include('reunition.apps.reunions.urls', 'reunions', 'reunions')),

    # Sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # robots.txt
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    # Add debug-toolbar
    try:
        import debug_toolbar
    except ImportError:
        # Temporarily debugging a deployed environment; don't install debug toolbar.
        pass
    else:
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

        # Serve media files through Django.
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        # Show error pages during development
        urlpatterns += [
            url(r'^403/$', 'django.views.defaults.permission_denied'),
            url(r'^404/$', 'django.views.defaults.page_not_found'),
            url(r'^500/$', 'django.views.defaults.server_error')
        ]
