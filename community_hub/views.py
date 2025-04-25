from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event, EventImage, TicketType, FreeTicketAllocation
from .forms import EventForm, TicketTypeFormSet, FreeTicketAllocationFormSet
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
    template_name = 'community_hub/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'community_hub/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'community_hub/event_form.html'
    success_url = reverse_lazy('community_hub:events')
    
    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'community_hub/event_form.html'
    success_url = reverse_lazy('community_hub:events')
    
    def test_func(self):
        # Allow staff users to edit any event
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'community_hub/event_confirm_delete.html'
    success_url = reverse_lazy('community_hub:events')
    
    def test_func(self):
        # Allow staff users to delete any event
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)
