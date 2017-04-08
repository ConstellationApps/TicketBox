from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm, remove_perm, get_perms


class Reply(models.Model):
    ticket = models.ForeignKey('Ticket', blank=True, null=True)
    owner = models.ForeignKey(User)
    author = models.CharField(max_length=128, default='Anonymous')
    body = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    owner = models.ForeignKey(User)
    author = models.CharField(max_length=128, default='Anonymous')
    anonymous = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default='Open'
    )
    archived = models.BooleanField(default=False)
    box = models.ForeignKey('Box', blank=True, null=True)

    class Meta:
        permissions = (
            ("owner", "Owns the ticket"),
        )


class Box(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    archived = models.BooleanField(default=False)

    def set_box_permissions(self, groups):
        permcodenames = []
        for node in Box._meta.permissions:
            permcodenames.append(node[0])

        for groupname, level in groups:
            if groupname.startswith('group-'):
                group = groupname.replace('group-', '', 1)
                group = Group.objects.get(pk=group)
                level = int(level) - 1

                if level == 0:
                    for perm in permcodenames:
                        remove_perm(perm, group, self)
                else:
                    for perm in permcodenames[:level]:
                        assign_perm(perm, group, self)
                    for perm in permcodenames[level:]:
                        remove_perm(perm, group, self)

    def get_box_permissions(self):
        groups = []
        permcodenames = []
        for node in Box._meta.permissions:
            permcodenames.append(node[0])

        for group in Group.objects.all():
            level = len(set(
                get_perms(group, self)).intersection(set(permcodenames))) + 1

            groups.append({
                'name': group.name,
                'id': group.id,
                'level': level
            })

        return groups

    class Meta:
        permissions = (
            ("action_add_tickets", "Can add tickets"),
            ("action_read_box", "Can read a box"),
            ("action_manage_tickets", "Can manage tickets"),
            ("action_manage_box", "Can manage a box"),
        )
