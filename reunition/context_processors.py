from django.contrib.sites.models import Site


def site(request):
    return dict(site=Site.objects.get_current())
