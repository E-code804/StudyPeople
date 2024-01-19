from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # This value can be blank.
    # Need related_name bc already have a User model connected.
    participants = models.ManyToManyField(
        User, related_name="participants", blank=True
    )  # Store users active in a room
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)  # Initial timestamp

    # Ordering the values in DB, first by updated then by created
    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relationship - one-to-many, connect to parent Table
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()  # Force user to write message
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)  # Initial timestamp

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]
