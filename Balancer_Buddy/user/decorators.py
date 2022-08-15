from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def unauthenticated_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('user:home_page')
    else:
      return view_func(request, *args, **kwargs)
  return wrapper_func

def allowed_user(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      group = None
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name or request.user.groups.all()[1].name
      
      if group in allowed_roles:
        return view_func(request, *args, **kwargs)
      else:
        return HttpResponseForbidden('You are not authorized to view this page')
    return wrapper_func
  return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('user:home_page')
        elif group == 'admin':
            return view_func(request, *args, **kwargs) 
    return wrapper_function