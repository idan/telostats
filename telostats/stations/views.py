from django.views.generic import ListView, DetailView, TemplateView
from .models import Station


class StationMap(TemplateView):
    template_name = "map.html"


class StationList(ListView):
    context_object_name = 'stations'
    model = Station


class StationDetail(DetailView):
    model = Station
    context_object_name = 'station'
