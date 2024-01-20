from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {"id": 1, "name": "Let us learn python!"},
#     {"id": 2, "name": "Design w/ me!"},
#     {"id": 3, "name": "Full-stack devs."},
# ]


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        # Make sure user exists, import User model.
        try:
            user = User.objects.get(username=username)
        except:
            # import messages
            messages.error(request, "User does not exist.")
        # Import authenticate, login, logout
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Adds session in db and browser
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist.")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


# Import UserCreationForm
def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Want to access user
            user = form.save(commit=False)
            # Clean data
            user.username = user.username.lower()
            user.save()
            # Login newly registered user.
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration.")
    return render(request, "base/login_register.html", {"form": form})


# Create your views here. NEED urls file for this app folder
def home(request):
    # Request is an http object, what user is sending to backend
    # return HttpResponse("Home Page")

    # Rendering your template. Be sure to add to TEMPLATES in setting.py
    # Passing rooms variable into the home.html file through context.
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    # Seeing if the query parameter exists then get topics whose name matches it
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )  # icontains for some match

    topics = Topic.objects.all()
    room_count = rooms.count()
    # For activity feed, shows activity for specified q topic, if any.
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    # return HttpResponse("ROOM")
    # Need to create templates folder in app directory and create a folder w/ same name in that templates folder.
    # Be sure to add path.
    # room = None

    # for i in rooms:
    #     if i["id"] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    # Query child objects of a room - for many to one.
    room_messages = room.message_set.all().order_by("-created")
    # For many to many
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        # Add user when they add a message to a room
        room.participants.add(request.user)
        # Reload page w/ get req.
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # Get user's rooms
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


# Import login_required
@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)  # Save model to DB
        #     # Auto set the host
        #     room.host = request.user
        #     room.save()
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # Prefill form w/ these values
    topics = Topic.objects.all()

    if request.user != room.host:
        # Need httpresponse
        return HttpResponse("You are not allowed here.")
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        # Need httpresponse
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        # Need httpresponse
        return HttpResponse("You are not allowed here.")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})
