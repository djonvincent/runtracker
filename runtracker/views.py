from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Run
from django.core import serializers
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import datetime

def index(request):
   #Serve the login page is user is not logged in
   if not request.user.is_authenticated():
      return render(request, 'runtracker/index.html')
   #Otherwise serve the dashboard
   else:
      return render(request, 'runtracker/dashboard.html')

def logIn(request):
   username = request.POST['username']
   password = request.POST['password']
   #Try to authenticate user with given credentials
   user = authenticate(username=username, password=password)
   #If credentials are invalid, return login page with error message
   if user is None:
      c = {'loginError': "True"}
      return render(request, 'runtracker/index.html', c)
   #Log user in if credentials are correct, return to dashboard page
   else:
      login(request, user)
      return redirect('/')

#Logs the user out
def logOut(request):
   logout(request)
   return redirect('/')

def signUp(request):
   #If user is already logged in, redirect them to home page
   if request.user.is_authenticated():
      return redirect('/')
   #If user is requesting page, serve an empty form
   if request.method == 'GET':
      form = SignUpForm()
   #If user is submitting the form, process data
   elif request.method == 'POST':
      #Bind form to the data
      form = SignUpForm(request.POST)
      #Create user if form is valid, otherwise return form with error messages
      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
         mass = form.cleaned_data['mass']
         #Create new user object with given credentials
         user = User.objects.create_user(username=username, password=password)
         #If a mass is specified, use that. Otherwise use default value (70)
         if mass is not None:
            user.userinfo.mass = mass
         #Save the user and log them in
         user.save()
         login(request, user)
         return redirect('/')
   #Serve sign up page with form
   return render(request, 'runtracker/signup.html', {'form': form})


#Function to add run to the database
@login_required
def addRun(request):
   if request.method == "POST":
      #Bind form to data
      form = AddRunForm(request.POST)
      if form.is_valid():
         distance = form.cleaned_data['distance']
         duration = form.cleaned_data['duration']
         #Save the run if the duration and distance are greater than 0
         if duration > 0 and distance > 0:
            datetime = form.cleaned_data['datetime']
            #Calculate calories burnt using formula
            calories = 0.005*request.user.userinfo.mass*(200*distance + 3.5*duration)
            #Create new run object and save to database
            run = Run(distance=distance, duration=duration, date=datetime, user=request.user, calories=calories)
            run.save()
            #Return code 204, successfuly fulfilled request and no content to send
            return HttpResponse(status=204)
   #Return 400 bad request if form is invalid
   return HttpResponse(status=400)

#Function to delete runs from database      
@login_required
def deleteRun(request):
   if request.method == "POST":
      #Get list of primary keys of runs to be deleted
      runIds = request.POST.getlist('delete-run[]')
      #Convert ids to integers
      runIds = map(lambda x: int(x), runIds)
      #Delete the selected runs
      for i in runIds:
         Run.objects.get(pk=i).delete()
      #Return code 204, successfuly fulfilled request and no content to send
      return HttpResponse(status=204)

#Function to return all runs within a specified time frame
@login_required
def getRunsSince(request):
   if request.method == "POST":
      timeFrame = request.POST['timeFrame']
      #Dictionary of how many days are in each time frame
      timeFrames = {
         'last-week': 7,
         'last-month': 30,
         'last-year': 365,
      }
      if timeFrame in timeFrames:
         #Get the number of days in time frame
         days = timeFrames[timeFrame]
         timeDelta = datetime.timedelta(days=days)
         #Find minimum date by subtracting days from today
         date = datetime.date.today() - timeDelta
         #Get list of all run objects since minimum date
         runs = Run.objects.filter(user=request.user, date__gte=date).order_by('date')
         #Serialise list of runs as JSON and send
         runJSON = serializers.serialize('json', runs, fields=('distance', 'duration', 'date', 'calories'))
         return HttpResponse(runJSON, content_type="text/json")

#Function to return all runs between two specified dates
@login_required
def getRunsBetween(request):
   if request.method == "POST":
      #Bind form to data
      form = GetRunsBetweenForm(request.POST)
      if form.is_valid():
         lowerDate = form.cleaned_data['lowerdate']
         upperDate = form.cleaned_data['upperdate']
         #Get initial list of runs belonging to the user
         runs = Run.objects.filter(user=request.user)
         #Filter out runs with date lower than lowerDate, if specified
         if lowerDate is not None:
            runs = runs.filter(date__gte = lowerDate)
         #Filter out runs with date higher than upperDate, if specified
         if upperDate is not None:
            runs = runs.filter(date__lte = upperDate)
         #Order runs by date
         runs = runs.order_by('date')
         #Serialise list of runs as JSON and send
         runJSON = serializers.serialize('json', runs, fields=('distance', 'duration', 'date', 'calories'))
         return HttpResponse(runJSON, content_type="text/json")
   
