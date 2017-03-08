from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# this doesn't support multiple threaded replies yet
class Reply(models.Model):
    ticket = models.ForeignKey('Ticket', blank=True, null=True)
    owner = models.ForeignKey(User)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Ticket(models.Model):
    owner = models.ForeignKey(User)
    anonymous = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=128)
    inbox = models.ForeignKey('Inbox', blank=True, null=True)

class Inbox(models.Model):
    name = models.CharField(max_length=128, unique=True)
    desc = models.TextField()
    archived = models.BooleanField(default=False)
    readGroup = models.ForeignKey(Group, null=True, blank=True,
                                  related_name='+')
    addGroup = models.ForeignKey(Group, null=True, blank=True,
                                 related_name='+')
    manageGroup = models.ForeignKey(Group, null=True, blank=True,
                                    related_name='+')

    class Meta:
        permissions = (
            ("create_inbox", "Can create an inbox"),
        )


