import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.decorators import (
    login_required,
    permission_required
)

from constellation_base.models import GlobalTemplateSettings

from .models import Inbox
from .models import Ticket
from .models import Reply

from .forms import InboxForm

# =============================================================================
# View Functions
# =============================================================================

@login_required
def view_inboxes(request):
    '''Return the base template that will call the API to display
    a list of inboxes'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()

    return render(request, 'constellation_ticketbox/view-list.html', {
        'template_settings': template_settings,
    })


@login_required
def view_inbox(request, inbox_id):
    '''Return the base template that will call the API to display the
    entire inbox with all tickets'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    newForm = TicketForm()
    editForm = TicketForm(prefix="edit")

    can_add = inbox_perms(request.user, 'add', inbox_id)

    return render(request, 'constellation_ticketbox/inbox.html', {
        'form': newForm,
        'editForm': editForm,
        'id': inbox_id,
        'template_settings': template_settings,
        'can_add': can_add,
    })

# =============================================================================
# Management Routes
# =============================================================================


@login_required
@permission_required('constellation_ticketbox.create_inbox')
def manage_inboxes(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    inboxForm = InboxForm()

    return render(request, 'constellation_ticketbox/manage-inboxes.html', {
        'form': inboxForm,
        'template_settings': template_settings,
    })


@login_required
def manage_inbox_edit(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    inbox = Inbox.objects.get(pk=inbox_id)
    inboxForm = InboxForm(instance=inbox)
    return render(request, 'constellation_ticketbox/edit-inbox.html', {
        'form': inboxForm,
        'inbox_id': inbox_id,
        'template_settings': template_settings,
    })
    


# =============================================================================
# API Functions for the v1 API
# =============================================================================

# -----------------------------------------------------------------------------
# API Functions related to Inbox Operations
# -----------------------------------------------------------------------------

@login_required
def api_v1_inbox_list(request):
    '''List all inboxes that a user is allowed to view'''
    if not request.user.is_superuser:
        inboxObjects = Inbox.objects.filter(pk__in=request.user.groups.all())
    else:
        inboxObjects = Inbox.objects.all()
    if inboxObjects:
        inboxes = serializers.serialize('json', inboxObjects)
        return HttpResponse(inboxes)
    else:
        return HttpResponseNotFound("You have no inboxes at this time")


@login_required
@permission_required('constellation_ticketbox.create_inbox')
def api_v1_inbox_create(request):
    '''Create an inbox'''
    inboxForm = InboxForm(request.POST or None)
    if request.POST and inboxForm.is_valid():
        newInbox = Inbox()
        newInbox.name = inboxForm.cleaned_data['name']
        newInbox.desc = inboxForm.cleaned_data['desc']
        newInbox.readGroup = inboxForm.cleaned_data['readGroup']
        newInbox.addGroup = inboxForm.cleaned_data['addGroup']
        newInbox.manageGroup = inboxForm.cleaned_data['manageGroup']
        try:
            newInbox.save()
            return HttpResponse(serializers.serialize('json', [newInbox,]))
        except:
            return HttpResponseServerError("Could not save inbox at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
def api_v1_inbox_update(request):
    '''Update an inbox'''
    inboxForm = InboxForm(request.POST or None)
    if request.POST and inboxForm.is_valid():
        inbox = Inbox.objects.get(pk=inboxID)
        inbox.name = inboxForm.cleaned_data['name']
        inbox.desc = inboxForm.cleaned_data['desc']
        inbox.readGroup = inboxForm.cleaned_data['readGroup']
        inbox.addGroup = inboxForm.cleaned_data['addGroup']
        inbox.manageGroup = inboxForm.cleaned_data['manageGroup']
        try:
            inbox.save()
            return HttpResponse(json.dumps({"inbox" : reverse("view_inbox", args=[inboxID,])}))
        except:
            return HttpResponseServerError("Invalid Inbox ID!")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
def api_v1_inbox_archive(request):
    '''Archive an inbox'''
    inbox = Inbox.objects.get(pk=inboxID)
    inbox.archived = True
    try:
        inbox.save()
        return HttpResponse("Inbox Archived")
    except:
        return HttpResponseServerError("Inbox could not be archived at this time")


@login_required
def api_v1_inbox_unarchive(request):
    '''Unarchive an inbox'''
    inbox = Inbox.objects.get(pk=inboxID)
    inbox.archived = False
    try:
        inbox.save()
        return HttpResponse("Inbox Un-Archived")
    except:
        return HttpResponseServerError("Inbox could not be un-archived at this time")


@login_required
def api_v1_inbox_info(request):
    '''Retrieve inbox title and description'''
    try:
        inbox = Inbox.objects.get(pk=inboxID)
        response = json.dumps({"title" : inbox.name, "desc" : inbox.desc})
        return HttpResponse(response)
    except:
        return HttpResponseNotFound("No inbox with given ID found")


# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------

@login_required
def view_dashboard(request):
    '''Return a card that will appear on the main dashboard'''

    return render(request, 'constellation_ticketbox/dashboard.html')