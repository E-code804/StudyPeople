from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"  # All fields from Room.
        exclude = ["host", "participants"]
