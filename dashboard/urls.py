from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('account/', views.account, name='account'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<slug:slug>/register/', views.event_register, name='event_register'),
    path('events/<slug:slug>/cancel-registration/', views.event_cancel_registration, name='event_cancel_registration'),
    path('event/<slug:slug>/purchase/', views.TicketPurchaseView.as_view(), name='ticket_purchase'),
] 