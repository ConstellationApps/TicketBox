import json

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
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
from .forms import ReplyForm

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
    ticketForm = TicketForm()
    box = Box.objects.get(pk=box_id)

    return render(request, 'constellation_ticketbox/box.html', {
        'form': ticketForm,
        'id': box_id,
        'template_settings': template_settings,
        'box': box,
        'user_id' : request.user.id
    })


@login_required
# add permissions
def view_ticket(request, ticket_id):
    '''Return the base template that will call the API to display the
    ticket with all replies'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    ticket = Ticket.objects.get(pk=ticket_id)
    replyForm = ReplyForm()

    return render(request, 'constellation_ticketbox/ticket.html', {
        'form' : replyForm,
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
@permission_required('constellation_ticketbox.action_read_box',
                     (Box, 'id', 'box_id'))
def api_v1_box_open_tickets(request, box_id):
    '''Retrieve all unarchived tickets for box'''
    ticketObjects = Ticket.objects.filter(box=Box.objects.get(pk=box_id),
                                      archived=False)
    if ticketObjects:
        tickets = serializers.serialize('json', ticketObjects)
        return HttpResponse(tickets)
    else:
        return HttpResponseNotFound("There are no open tickets in this box.")


@login_required
# add permissions
def api_v1_box_closed_tickets(request, box_id):
    '''Retrieve all unarchived tickets for the box'''
    ticketObjects = Ticket.objects.filter(box=Box.objects.get(pk=box_id),
                                      archived=True)
    if ticketObjects:
        tickets = serializers.serialize('json', ticketObjects)
        return HttpResponse(tickets)
    else:
        return HttpResponseNotFound("There are no closed tickets in this box.")

# -----------------------------------------------------------------------------
# API Functions related to Ticket Operations
# -----------------------------------------------------------------------------

@login_required
# add permissions
# this is extremely broken.
def api_v1_ticket_create(request, box_id):
    '''Create a ticket'''
    ticketForm = TicketForm(request.POST or None)
    if request.POST and ticketForm.is_valid():
        newTicket = Ticket()
        newTicket.title = ticketForm.cleaned_data['title']
        newTicket.body = ticketForm.cleaned_data['body']
        newTicket.box = get_object_or_404(Box, pk=box_id)
        newTicket.owner = request.user
        newTicket.anonymous = ticketForm.cleaned_data['anonymous']
        if (newTicket.anonymous == False):
            newTicket.author = request.user.username
        newTicket.status = 'Open'
        try:
            newTicket.save()
            return HttpResponse(serializers.serialize('json', [newTicket,]))
        except:
            return HttpResponseServerError("Could not save ticket at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")


@login_required
# add permissions
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
# add permissions
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
# add permissions
def api_v1_ticket_replies(request, ticket_id):
    ''''Retrieve all replies for a ticket'''
    replyObjects = Reply.objects.filter(ticket=Ticket.objects.get(pk=ticket_id))
    if replyObjects:
        replies = serializers.serialize('json', replyObjects)
        return HttpResponse(replies)
    else:
        return HttpResponseNotFound("There are no replies to this ticket.")

# -----------------------------------------------------------------------------
# API Functions related to Reply Operations
# -----------------------------------------------------------------------------

@login_required
# add permissions
def api_v1_reply_create(request, ticket_id):
    '''Create a reply for a ticket'''
    replyForm = ReplyForm(request.POST or None)
    if request.POST and replyForm.is_valid():
        newReply = Reply()
        newReply.body = replyForm.cleaned_data['body']
        newReply.owner = request.user
        newReply.author = request.user.username
        newReply.ticket = get_object_or_404(Ticket, pk=ticket_id)
        try:
            newReply.save()
            return HttpResponse(serializers.serialize('json', [newReply,]))
        except:
            return HttpResponseServerError("Could not save reply at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")
    

# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------

@login_required
def view_dashboard(request):
    '''Return a card that will appear on the main dashboard'''
    return render(request, 'constellation_ticketbox/dashboard.html')