from django.contrib import admin

from .models import Box
from .models import Ticket

admin.site.register(Box)
admin.site.register(Ticket)