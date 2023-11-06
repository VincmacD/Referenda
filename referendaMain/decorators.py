from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

from referendaMain.models import Vote, Referendum

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Insufficient permission to view this page.')
        return wrapper_func
    return decorator

def voter_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admins':
            return redirect('dashboard')
        
        if group == 'voters':
            return view_func(request, *args, **kwargs)
    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'voters':
            return redirect('dashboard')
        
        if group == 'admins':
            return view_func(request, *args, **kwargs)
    return wrapper_function

def prevent_duplicate_vote(view_func):
    def _wrapped_view(request, id, *args, **kwargs):
        voter = request.user.voter 
        referendum = Referendum.objects.get(id=id)

        existing_vote = Vote.objects.filter(voter=voter, referendum=referendum).first()

        if existing_vote:
            return redirect('dashboard')

        return view_func(request, id, *args, **kwargs)
    return _wrapped_view

def unavailable_referendum(view_func):
    def wrapper_func(request, id, *args, **kwargs):
        referendum = Referendum.objects.get(id=id)
        current_date = datetime.now().date()
        start_date = referendum.date_available
        expiry_date = referendum.date_expired
        
        if start_date <= current_date <= expiry_date:
            return view_func(request, id, *args, **kwargs) 
        else:
            return redirect('dashboard')
      
    return wrapper_func
