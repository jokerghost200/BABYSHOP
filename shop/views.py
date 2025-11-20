from django.shortcuts import render, redirect
from functools import wraps
from django.contrib import messages
from user.models import Client

def update_session(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_email' in request.session:
            try:
                client = Client.objects.get(email=request.session['user_email'])
                request.session['user_name'] = client.prenom
                request.session['user_photo'] = client.photo.url if client.photo else None
            except Client.DoesNotExist:
                pass
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_email' not in request.session:
            messages.warning(request, "Vous devez être connecté pour acceder a cette page.")
            return redirect('user:login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@update_session
def catalogue(request):
    
    return render(request, 'shop/index.html')

@login_required
@update_session
def panier(request):
    return render(request, 'shop/panier.html')


@login_required
@update_session
def commande(request):
    return render(request, 'shop/commande.html')
