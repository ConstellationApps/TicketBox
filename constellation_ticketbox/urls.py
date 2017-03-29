from django.conf.urls import url

from . import views

urlpatterns = [

# =============================================================================
# View Routes
# =============================================================================

    url(r'^view/boxes$', 
        views.view_boxes,
        name="view_boxes"),
    url(r'^view/box/(?P<box_id>\d+)$', 
        views.view_box,
        name="view_box"),
    url(r'^view/ticket/(?P<ticket_id>\d+)$', 
        views.view_ticket,
        name="view_ticket"),

# =============================================================================
# Management Routes
# =============================================================================

    url(r'^manage/boxes$', 
        views.manage_boxes,
        name="manage_boxes"),
    url(r'^manage/box/(?P<box_id>\d+)/edit$', 
        views.manage_box_edit,
        name="manage_box_edit"),


# =============================================================================
# API Routes for the v1 API
# =============================================================================

# -----------------------------------------------------------------------------
# API Routes related to Box Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/box/list$', 
        views.api_v1_box_list,
        name="api_v1_box_list"),
    url(r'^api/v1/box/create$', 
        views.api_v1_box_create, 
        name="api_v1_box_create"),
    url(r'^api/v1/box/(?P<box_id>\d+)/archive$', 
        views.api_v1_box_archive,
        name="api_v1_box_archive"),
    url(r'^api/v1/box/(?P<box_id>\d+)/unarchive$', 
        views.api_v1_box_unarchive,
        name="api_v1_box_unarchive"),
    url(r'^api/v1/box/(?P<box_id>\d+)/update$', 
        views.api_v1_box_update,
        name="api_v1_box_update"),
    url(r'^api/v1/box/(?P<box_id>\d+)/info$', 
        views.api_v1_box_info,
        name="api_v1_box_info"),

# -----------------------------------------------------------------------------
# API Routes related to Ticket Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/ticket/(?P<ticket_id>\d+)/info$', 
        views.api_v1_ticket_info,
        name="api_v1_ticket_info"),
    url(r'^api/v1/ticket/list$', 
        views.api_v1_ticket_list,
        name="api_v1_ticket_list"),
    url(r'^api/v1/ticket/create$', 
        views.api_v1_ticket_create, 
        name="api_v1_ticket_create"),
    url(r'^api/v1/ticket/(?P<ticket_id>\d+)/archive$', 
        views.api_v1_ticket_archive,
        name="api_v1_ticket_archive"),
    url(r'^api/v1/ticket/(?P<ticket_id>\d+)/unarchive$', 
        views.api_v1_ticket_unarchive,
        name="api_v1_ticket_unarchive"),


# -----------------------------------------------------------------------------
# Dashboard routes
# -----------------------------------------------------------------------------

    url(r'^view/dashboard$', 
        views.view_dashboard,
        name="view_dashboard"),


]