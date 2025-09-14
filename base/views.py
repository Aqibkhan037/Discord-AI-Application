from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.db.models import Q
from .models import Rooms,Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id':1,'name':'let learn python!'},

#     {'id':2,'name':'Design with me'},   
#     {'id':3,'name':'Frontend Developer'}
# ]


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')

    else:
        messages.error(request,'An Error Occured during registration')

    return render(request, 'base/login_register.html',{'form':form})

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        
        username = request.POST.get('username').lower()
        password = request.POST.get('password')


        try:
            user = User.objects.get(username = username)
            
        except:
            messages.error(request,'User does not exist!')


        user = authenticate(request,username=username,password=password) # Either it will give us an error or let us login. 
        
        print("This is the User: ",user)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist')

    print(request.method)
        

    context = {'page':page}
    return render(request,'base/login_register.html',context)
    

def home(request,*args,**kwargs):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Rooms.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains = q) | Q(description__icontains=q))
     # it will search for the elements that contains at least the search elements
                                             # This i indicates that is not a case Sensitive.
    ## So by using Q method imported from db.models import Q. we can use use the Or |, and And feature of the python...
    # basically we can check for multiple conditons using Q.

    topic = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms':rooms,'topics':topic,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    rooms = Rooms.objects.get(id = pk)
    
    context = {'rooms':rooms}
    return render(request,'base/room.html',context) 

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room) 

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')

    
            
    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def delete(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')


    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

