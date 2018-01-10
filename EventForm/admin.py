from django.contrib import admin
from .models import NewEvents

admin.site.register([
    NewEvents,
])
