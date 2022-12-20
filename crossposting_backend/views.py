from django.http import HttpResponseRedirect
from django.urls import reverse


def handle_root_path(request):
    return HttpResponseRedirect(reverse('authenticate'))


