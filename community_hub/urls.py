from django.urls import path
from . import views

app_name = 'community_hub'

urlpatterns = [
    path('', views.admin_home, name='home'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<slug:slug>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]
