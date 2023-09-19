from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

rooms = [
       {"id":1, "name": "learn data-science"},
       {"id":2, "name": "learn python"},
       {"id":3, "name": "learn full stack"}
]

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
       return redirect('home')

    if request.method == 'POST':
       print("post request:", request.POST)
       username = request.POST.get('usernamee').lower()
       password = request.POST.get('passwordd')
       print("username:", username, "password:", password)

       try:
           user = User.objects.get(username = username)
       except:
            messages.error(request, "User Doesn't exist")

       user = authenticate(request, username=username, password=password)

       if user is not None:
          login(request, user)
          return redirect('home')
       else:
           messages.error(request, "Username or Password are does not exists")
           
           
    context = {"page": page}
    return render(request, 'baseapp/login_register.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = "register"   # not used 
    form =  UserCreationForm()
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          user = form.save(commit = False)
          user.username = user.username.lower()
          user.save()
          login(request, user)
          return redirect("home")
       else:
           messages.error(request, "An error occured during the registration")

    return render(request, 'baseapp/login_register.html', {"form": form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #rooms = Room.objects.all()
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    return render(request, 'baseapp/home.html', {"rums": rooms, "topics": topics, "room_count": room_count})

def room(request, pk):
    room = Room.objects.get(id=int(pk))
    room_messages = room.message_set.all().order_by("-created")
    context = {"rumm": room, "room_messages":room_messages}
    return render(request, 'baseapp/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
       #print(request.POST)
       form = RoomForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect('home')

    context = {"form": form}
    return render(request, 'baseapp/create_room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = int(pk))
    form = RoomForm(instance=room)

    if request.user != room.host:
       return HttpResponse("You are not allowed")

    if request.method == 'POST':
       form = RoomForm(request.POST, instance=room)
       if form.is_valid():
          form.save()
          return redirect('home')


    context = {'form': form}
    return render(request, 'baseapp/create_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = int(pk))
    if request.user != room.host:
       return HttpResponse("You are not allowed")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'baseapp/delete.html', context)





