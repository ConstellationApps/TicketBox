from django.conf.urls import url

from . import views

urlpatterns = [

# =============================================================================
# View Routes
# =============================================================================

    url(r'^view/list$', views.view_list,
        name="view_list"),
    url(r'^view/inbox/([\d]*)$', views.view_inbox,
        name="view_inbox"),

# =============================================================================
# Management Routes
# =============================================================================

    url(r'^manage/inboxes$', views.manage_inboxes,
        name="manage_inboxes"),
    url(r'^manage/inbox/([\d]*)/edit$', views.manage_inbox_edit,
        name="manage_inbox_edit"),


# =============================================================================
# API Routes for the v1 API
# =============================================================================

# -----------------------------------------------------------------------------
# API Routes related to Inbox Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/inbox/list$', views.api_v1_inbox_list,
        name="api_v1_inbox_list"),
    url(r'^api/v1/inbox/create$', views.api_v1_inbox_create, 
        name="api_v1_inbox_create"),
    url(r'^api/v1/inbox/archive$', views.api_v1_inbox_archive,
        name="api_v1_inbox_archive"),
    url(r'^api/v1/inbox/unarchive$', views.api_v1_inbox_unarchive,
        name="api_v1_inbox_unarchive"),
    url(r'^api/v1/inbox/([\d]*)/update$', views.api_v1_inbox_update,
        name="api_v1_inbox_update"),
    url(r'^api/v1/inbox/([\d]*)/info$', views.api_v1_inbox_info,
        name="api_v1_inbox_update")


# -----------------------------------------------------------------------------
# Dashboard routes
# -----------------------------------------------------------------------------

    url(r'^view/dashboard$', views.view_dashboard,
        name="view_dashboard"),


]