from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event, EventImage
from authentication.models import EventRegistration
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import uuid

@login_required
def admin_home(request):
    return render(request, 'community_hub/home.html')

class EventListView(ListView):
    model = Event
    template_name = 'community_hub/events.html'
    context_object_name = 'events'
    ordering = ['-start_date']
    
    def get_queryset(self):
        # Only show public events to non-staff users
        if self.request.user.is_staff:
            return Event.objects.all().order_by('-start_date')
        return Event.objects.filter(is_public=True).order_by('-start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'community_hub/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        # Only show public events to non-staff users
        if self.request.user.is_staff:
            return Event.objects.all()
        return Event.objects.filter(is_public=True)

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    template_name = 'community_hub/event_form.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'location', 
              'category', 'is_public', 'status', 'image']
    success_url = reverse_lazy('community_hub:events')
    
    def test_func(self):
        # Only staff users can create events
        return self.request.user.is_staff
    
    def form_valid(self, form):
        print("DEBUG: Form is valid, processing event creation")
        print(f"DEBUG: Event title: {form.cleaned_data.get('title')}")
        print(f"DEBUG: Event category: {form.cleaned_data.get('category')}")
        print(f"DEBUG: Event start date: {form.cleaned_data.get('start_date')}")
        print(f"DEBUG: Event end date: {form.cleaned_data.get('end_date')}")
        print(f"DEBUG: Event location: {form.cleaned_data.get('location')}")
        print(f"DEBUG: Event is public: {form.cleaned_data.get('is_public')}")
        print(f"DEBUG: Event status: {form.cleaned_data.get('status')}")
        
        # Save the form and get the event instance
        event = form.save()
        print(f"DEBUG: Event saved with ID: {event.id}")
        print(f"DEBUG: Event slug: {event.slug}")
        
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'community_hub/event_form.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'location', 
              'category', 'is_public', 'status', 'image']
    success_url = reverse_lazy('community_hub:events')
    
    def test_func(self):
        # Only staff users can edit events
        return self.request.user.is_staff
    
    def get_object(self, queryset=None):
        # Get the event by slug instead of pk
        slug = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug)
    
    def form_valid(self, form):
        print("DEBUG: Form is valid, processing event update")
        print(f"DEBUG: Event title: {form.cleaned_data.get('title')}")
        print(f"DEBUG: Event category: {form.cleaned_data.get('category')}")
        print(f"DEBUG: Event start date: {form.cleaned_data.get('start_date')}")
        print(f"DEBUG: Event end date: {form.cleaned_data.get('end_date')}")
        print(f"DEBUG: Event location: {form.cleaned_data.get('location')}")
        print(f"DEBUG: Event is public: {form.cleaned_data.get('is_public')}")
        print(f"DEBUG: Event status: {form.cleaned_data.get('status')}")
        
        # Save the form and get the event instance
        event = form.save()
        print(f"DEBUG: Event updated with ID: {event.id}")
        print(f"DEBUG: Event slug: {event.slug}")
        
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('community_hub:events')
    
    def test_func(self):
        # Only staff users can delete events
        return self.request.user.is_staff
    
    def get_object(self, queryset=None):
        # Get the event by slug instead of pk
        slug = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug)
