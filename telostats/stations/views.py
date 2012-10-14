from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from .models import Station


class StationMap(TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super(StationMap, self).get_context_data(**kwargs)
        context['tileserver_url'] = settings.TILESERVER_URL
        return context


class StationList(ListView):
    context_object_name = 'stations'
    model = Station


class StationDetail(DetailView):
    model = Station
    context_object_name = 'station'
