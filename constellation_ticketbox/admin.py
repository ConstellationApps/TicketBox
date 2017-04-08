from django.contrib import admin

from .models import Box
from .models import Ticket
from .models import Reply

admin.site.register(Box)
admin.site.register(Ticket)
admin.site.register(Reply)
