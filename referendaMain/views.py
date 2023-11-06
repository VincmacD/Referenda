from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from .forms import ReferendumForm, VoterUpdateForm
from .models import *
from django.contrib.auth.decorators import login_required
from referendaMain.decorators import unauthenticated_user,allowed_users, admin_only, prevent_duplicate_vote, voter_only, unavailable_referendum

# Create your views here.
from .forms import CreateUserForm

#Registering
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created for' + ' ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'referendaPages/register.html', context)

#Logging in/out
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'referendaPages/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#Dashboard
@login_required(login_url='login')
def dashboard(request):
    current_date = datetime.now().date()
    referendums = Referendum.objects.all()
    
    return render(request, 'referendaPages/dashboard.html',
                  context = {'referendums' : referendums,
                             'current_date' : current_date})

# Editing account information
@voter_only
@login_required(login_url='login')
def accountUpdate(request):
    voter = Voter.objects.get(user=request.user)
    if request.method == 'POST':
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        voter.first_name = new_first_name
        voter.last_name = new_last_name
        voter.email = new_email
        voter.phone = request.POST.get('phone')
        voter.save()

        user=voter.user
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email=new_email
        user.save()
        return redirect('account')

    context = {'voter': voter}
    return render(request, 'referendaPages/account.html', context)

#Create Referendum
@login_required(login_url='login')
@admin_only
def createReferendumPage(request):
    if request.method == 'POST':
        form = ReferendumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ReferendumForm()

    context = {'form':form}
    return render(request, 'referendaPages/create.html', context)

#Voting
@voter_only
@prevent_duplicate_vote
@unavailable_referendum
def votePage(request, id):
    referendum = Referendum.objects.get(id=id)

    if request.method == 'POST':
        referendum_id = request.POST.get('referendum_id')
        voter_id = request.POST.get('voter_id')
        choice_id = request.POST.get('choice_id')

        try:
            referendum = Referendum.objects.get(id=referendum_id)
            voter = Voter.objects.get(id=voter_id)
            choice = Choice.objects.get(id=choice_id)
            Vote.objects.create(voter=voter, referendum=referendum, choice=choice)
            messages.success(request, 'Vote submitted successfully')
            return redirect('dashboard')
        except (Referendum.DoesNotExist, Voter.DoesNotExist, Choice.DoesNotExist):
            messages.error(request, 'Invalid referendum, voter, or choice ID')
    
    return render(request, 'referendaPages/vote.html', context={'referendum': referendum})

#Results
@login_required(login_url='login')
def resultsPage(request, id):
   referendum = Referendum.objects.get(id=id)
   total_voters = Voter.objects.count()
   total_votes = Vote.objects.filter(referendum=referendum).count()
   unvoted = (total_voters - total_votes)
   yes_votes = Vote.objects.filter(referendum=referendum, choice_id=1).count()
   no_votes = Vote.objects.filter(referendum=referendum, choice_id=2).count()
   vote_results = []
   for choice in referendum.choices.all():
     voteCount = Vote.objects.filter(referendum=referendum, choice=choice).count()
     vote_results.append([choice.name, voteCount])
  
   return render(request, 'referendaPages/results.html',
                 context={'referendum' : referendum,
                          'unvoted' : unvoted,
                          'yes_votes' : yes_votes,
                          'no_votes' : no_votes,
                          'vote_results' : vote_results,
                          'total_votes': total_votes})
