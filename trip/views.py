from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Trip, Note

# Create your views here.


class HomeView(TemplateView):
    template_name = "trip/index.html"


def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        "trips": trips
    }
    return render(request, "trip/trip_list.html", context)


class TripCreateView(CreateView):
    model = Trip
    fields = ['city', 'country', 'start_date', 'end_date']
    template_name = "trip/trip_form.html"
    success_url = reverse_lazy('trips-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TripDetailView(DetailView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context
    
class NoteDetailView(DetailView):
    model = Note

class NoteListView(ListView):
    model = Note
    
    def get_queryset(self):
        return Note.objects.filter(trip__owner=self.request.user)
    
class NoteCreateView(CreateView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('note-list')

    def get_form(self, form_class=None):
        form = super(NoteCreateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form

class NoteUpdateView(UpdateView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('note-list')

    def get_form(self, form_class=None):
        form = super(NoteUpdateView, self).get_form()
        trips = Trip.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form
    
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')

class TripUpdateView(UpdateView):
    model = Trip
    fields = ['city', 'country', 'start_date', 'end_date']
    success_url = reverse_lazy('trips-list')
    #template names mode_form trip_form 
    
class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trips-list')