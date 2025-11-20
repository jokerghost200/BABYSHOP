from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil/index.html')
def contact(request):
    return render(request, 'accueil/contact.html')