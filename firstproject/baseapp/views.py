from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.

rooms = [
       {"id":1, "name": "learn data-science"},
       {"id":2, "name": "learn python"},
       {"id":3, "name": "learn full stack"}
]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #rooms = Room.objects.all()
    rooms = Room.objects.filter(topic__name__icontains = q)
    topics = Topic.objects.all()
    return render(request, 'baseapp/home.html', {"rums": rooms, "topics": topics})

def room(request, pk):
    room = Room.objects.get(id=int(pk))
    context = {"rumm": room}
    return render(request, 'baseapp/room.html', context)

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

def updateRoom(request, pk):
    room = Room.objects.get(id = int(pk))
    form = RoomForm(instance=room)
    if request.method == 'POST':
       form = RoomForm(request.POST, instance=room)
       if form.is_valid():
          form.save()
          return redirect('home')


    context = {'form': form}
    return render(request, 'baseapp/create_room.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id = int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'baseapp/delete.html', context)





