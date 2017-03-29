import json

from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from guardian.decorators import (
    permission_required,
)
from guardian.shortcuts import get_objects_for_user

from constellation_base.models import GlobalTemplateSettings

from .models import Box
from .models import Ticket
from .models import Reply

from .forms import BoxForm
from .forms import TicketForm

# =============================================================================
# View Functions
# =============================================================================

@login_required
def view_boxes(request):
    '''Return the base template that will call the API to display
    a list of boxes'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()

    return render(request, 'constellation_ticketbox/view-list.html', {
        'template_settings': template_settings,
    })


@login_required
@permission_required('constellation_ticketbox.action_add_tickets',
                     (Box, 'id', 'box_id'))
def view_box(request, box_id):
    '''Return the base template that will call the API to display the
    box with all visible tickets'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    newForm = TicketForm()
    editForm = TicketForm(prefix="edit")
    box = Box.objects.get(pk=box_id)

    return render(request, 'constellation_ticketbox/box.html', {
        'form': newForm,
        'editForm': editForm,
        'id': box_id,
        'template_settings': template_settings,
        'box': box,
    })


@login_required
def view_ticket(request, ticket_id):
    '''Return the base template that will call the API to display the
    ticket with all replies'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    ticket = Ticket.objects.get(pk=ticket_id)

    return render(request, 'constellation_ticketbox/ticket.html', {
        'id': ticket_id,
        'template_settings': template_settings,
        'ticket': ticket,
    })


# =============================================================================
# Management Routes
# =============================================================================


@login_required
@permission_required('constellation_ticketbox.create_box')
def manage_boxes(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    boxForm = BoxForm()
    groups = [(g.name, g.pk) for g in Group.objects.all()]
    return render(request, 'constellation_ticketbox/manage-boxes.html', {
        'form': boxForm,
        'template_settings': template_settings,
        'groups': groups,
    })


@login_required
@permission_required('constellation_ticketbox.action_manage_box', 
                     (Box, 'id', 'box_id'))
def manage_box_edit(request, box_id):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    box = Box.objects.get(pk=box_id)
    boxForm = BoxForm(instance=box)
    groups = box.get_box_permissions()
    return render(request, 'constellation_ticketbox/edit-box.html', {
        'form': boxForm,
        'box_id': box_id,
        'template_settings': template_settings,
        'groups': groups,
    })
    


# =============================================================================
# API Functions for the v1 API
# =============================================================================

# -----------------------------------------------------------------------------
# API Functions related to Box Operations
# -----------------------------------------------------------------------------

@login_required
def api_v1_box_list(request):
    '''List all boxes that a user is allowed to view'''
    boxObjects = get_objects_for_user(
        request.user,
        'constellation_ticketbox.action_add_tickets',
        Box)
    if boxObjects:
        boxes = serializers.serialize('json', boxObjects)
        return HttpResponse(boxes)
    else:
        return HttpResponseNotFound("You have no boxes at this time")


@login_required
@permission_required('constellation_ticketbox.add_box')
def api_v1_box_create(request):
    '''Create a box'''
    boxForm = BoxForm(request.POST or None)
    if request.POST and boxForm.is_valid():
        newBox = Box()
        newBox.name = boxForm.cleaned_data['name']
        newBox.desc = boxForm.cleaned_data['desc']
        try:
            newBox.save()
            newBox.set_box_permissions(request.POST.items())
            return HttpResponse(serializers.serialize('json', [newBox,]))
        except:
            return HttpResponseServerError("Could not save box at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
@permission_required('constellation_ticketbox.action_manage_box',
                     (Box, 'id', 'box_id'))
def api_v1_box_update(request, box_id):
    '''Update a box'''
    boxForm = BoxForm(request.POST or None)
    if request.POST and boxForm.is_valid():
        try: 
            box = Box.objects.get(pk=box_id)
            box.set_box_permissions(request.POST.items())
            box.name = boxForm.cleaned_data['name']
            box.desc = boxForm.cleaned_data['desc']
            box.save()
            return HttpResponse(json.dumps({"box" : reverse("view_box", args=[box_id,])}))
        except AttributeError:
            return HttpResponseServerError("Invalid Box ID!")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
@permission_required('constellation_ticketbox.action_manage_box',
                     (Box, 'id', 'box_id'))
def api_v1_box_archive(request, box_id):
    '''Archive a box'''
    box = Box.objects.get(pk=box_id)
    box.archived = True
    try:
        box.save()
        return HttpResponse("Box Archived")
    except:
        return HttpResponseServerError("Box could not be archived at this time")


@login_required
@permission_required('constellation_ticketbox.action_manage_box',
                     (Box, 'id', 'box_id'))
def api_v1_box_unarchive(request, box_id):
    '''Unarchive a box'''
    box = Box.objects.get(pk=box_id)
    box.archived = False
    try:
        box.save()
        return HttpResponse("Box Un-Archived")
    except:
        return HttpResponseServerError("Box could not be un-archived at this time")


@login_required
@permission_required('constellation_ticketbox.action_add_tickets',
                     (Box, 'id', 'box_id'))
def api_v1_box_info(request, box_id):
    '''Retrieve box title and description'''
    try:
        box = Box.objects.get(pk=box_id)
        response = json.dumps({"title" : box.name, "desc" : box.desc})
        return HttpResponse(response)
    except:
        return HttpResponseNotFound("No box with given ID found")

# -----------------------------------------------------------------------------
# API Functions related to Ticket Operations
# -----------------------------------------------------------------------------

@login_required
def api_v1_ticket_list(request):
    '''List all tickets that a user is allowed to view'''


@login_required
def api_v1_ticket_create(request):
    '''Create a ticket'''
    ticketForm = TicketForm(request.POST or None)
    if request.POST and ticketForm.is_valid():
        newTicket = Ticket()
        newTicket.title = ticketForm.cleaned_data['title']
        newTicket.body = ticketForm.cleaned_data['body']
        try:
            newTicket.save()
            return HttpResponse(serializers.serialize('json', [newTicket,]))
        except:
            return HttpResponseServerError("Could not save ticket at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
def api_v1_ticket_archive(request, ticket_id):
    '''Archive a ticket'''
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.archived = True
    try:
        ticket.save()
        return HttpResponse("Ticket Archived")
    except:
        return HttpResponseServerError("Ticket could not be archived at this time")


@login_required
def api_v1_ticket_unarchive(request, ticket_id):
    '''Archive a ticket'''
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.archived = False
    try:
        ticket.save()
        return HttpResponse("Ticket Unarchived")
    except:
        return HttpResponseServerError("Ticket could not be unarchived at this time")


@login_required
def api_v1_ticket_info(request, ticket_id):
    '''Retrieve ticket title, timestamp, and status'''
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        response = json.dumps({
            "title" : ticket.title,
            "timestamp" : ticket.timestamp, 
            "status" : ticket.status,
        })
        return HttpResponse(response)
    except:
        return HttpResponseNotFound("No ticket with given ID found")



# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------

@login_required
def view_dashboard(request):
    '''Return a card that will appear on the main dashboard'''
    return render(request, 'constellation_ticketbox/dashboard.html')