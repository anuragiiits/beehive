from django.urls import path
from .views import NewEventsView, EventRegistrationView

app_name = 'events_data'

urlpatterns = [
    path('eventsdata/', NewEventsView.as_view(), name='new_events_view'),
    path('eventsreg/', EventRegistrationView.as_view(), name='events_reg_view'),
]