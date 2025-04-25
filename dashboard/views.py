from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from authentication.models import UserProfile
from services.user_service import update_user_profile
from community_hub.models import Event
from django.views import View
from django.utils import timezone
import uuid

# Create your views here.

@login_required(login_url='auth:login')
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def account(request):
    user_profile = request.user.userprofile
    membership_program_choices = UserProfile.MEMBERSHIP_PROGRAM_CHOICES
    payment_type_choices = UserProfile.PAYMENT_TYPE_CHOICES

    if request.method == 'POST':
        # Update user profile using the service function
        update_user_profile(request.user, request.POST)
        messages.success(request, 'Profile updated successfully!')

    context = {
        'user_profile': user_profile,
        'membership_program_choices': membership_program_choices,
        'payment_type_choices': payment_type_choices,
    }
    return render(request, 'dashboard/account.html', context)

class EventListView(ListView):
    model = Event
    template_name = 'dashboard/events.html'
    context_object_name = 'events'
    ordering = ['-start_date']
    
    def get_queryset(self):
        # Only show public events to regular users
        return Event.objects.filter(is_public=True).order_by('-start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'dashboard/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        # Only show public events to regular users
        return Event.objects.filter(is_public=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Add registration status to context
            context['is_registered'] = False  # TODO: Implement event registration
        return context

@login_required
def event_register(request, slug):
    event = get_object_or_404(Event, slug=slug, is_public=True)
    # TODO: Implement event registration logic
    messages.success(request, f'You have successfully registered for {event.title}')
    return redirect('dashboard:event_detail', slug=slug)

@login_required
def event_cancel_registration(request, slug):
    event = get_object_or_404(Event, slug=slug, is_public=True)
    # TODO: Implement event registration cancellation logic
    messages.success(request, f'You have cancelled your registration for {event.title}')
    return redirect('dashboard:event_detail', slug=slug)

class TicketPurchaseView(View):
    template_name = 'dashboard/ticket_purchase.html'

    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        user_profile = request.user.userprofile
        context = {
            'event': event,
            'user_profile': user_profile,
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        user_profile = request.user.userprofile
        num_tickets = int(request.POST.get('num_tickets', 1))

        # Calculate paid tickets (after free tickets)
        free_tickets = user_profile.get_free_tickets()
        paid_tickets = max(0, num_tickets - free_tickets)
        total_cost = paid_tickets * event.ticket_price

        # Generate unique ticket ID
        ticket_id = f"{event.slug}-{request.user.id}-{uuid.uuid4().hex[:8]}"

        # Create event registration
        registration = EventRegistration.objects.create(
            user=request.user,
            event=event,
            ticket_id=ticket_id,
            num_tickets=num_tickets
        )

        # Update user's purchased tickets
        purchased_tickets = user_profile.purchased_tickets or {}
        if event.id not in purchased_tickets:
            purchased_tickets[event.id] = []
        purchased_tickets[event.id].append({
            'ticket_id': ticket_id,
            'num_tickets': num_tickets,
            'purchase_date': timezone.now().isoformat(),
            'total_cost': total_cost
        })
        user_profile.purchased_tickets = purchased_tickets
        user_profile.save()

        messages.success(request, f'Successfully purchased {num_tickets} ticket(s) for {event.title}')
        return redirect('community_hub:event_detail', slug=event.slug)
