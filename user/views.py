from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from .models import Client


def signup(request):
    return render(request, 'user/signup')

def profile(request):
    if 'user_email' not in request.session:
        messages.warning(request, "Vous devez etre connecté pour accéder a cette page ")
        return redirect('user:login')
    #recuperation de client connecté
    email = request.session['user_email']
    try:
        client = Client.objects.get(email=email)
        
    except Client.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('user:login')
    return render(request, 'user/profile.html', {'client': client})



def logout_view(request):
    # Supprime toutes les données de session
    request.session.flush()

    # Empêche le cache du navigateur de garder la page
    response = redirect('user:login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    messages.success(request, "Vous êtes déconnecté avec succès.")
    return response

# ---- REGISTER ----
@csrf_protect
def register_user(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        adresse = request.POST['adresse']
        ville = request.POST['ville']
        password = request.POST['password']
        photo = request.FILES.get("photo")

        if Client.objects.filter(email=email).exists():
            messages.error(request, "Cet e-mail est déjà utilisé.")
            return render(request, 'user/signup.html')

        hashed_password = make_password(password)

        Client.objects.create(
            nom=nom,
            prenom=prenom,
            tel=tel,
            email=email,
            adresse=adresse,
            ville=ville,
            password=hashed_password,
            photo=photo,
        )

        messages.success(request, f"Bienvenue {prenom} ! Votre compte a été créé avec succès.")
        return redirect('user:login')

    return render(request, 'user/signup.html')


# ---- LOGIN ----
@csrf_protect
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Client.objects.get(email=email)
        except Client.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'user/login.html')

        # Vérifie le mot de passe haché
        if check_password(password, user.password):
            # Stocke les infos dans la session
            request.session['user_email'] = user.email
            request.session['user_name'] = user.prenom
            request.session['is_admin'] = user.is_admin  # 👈 important

            if user.photo:
                request.session['user_photo'] = user.photo.url
            else:
                request.session['user_photo'] = None

            # 🔥 redirection selon le rôle
            if user.is_admin:
                return redirect('dashboard:dash')  # ta page admin
            else:
                return redirect('accueil:accueil')  # page normale
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')

def confidentialite(request):
    return render(request, 'user/conf.html')



def update_profile(request):

    if 'user_email' not in request.session:
        messages.warning(request, "Veuillez vous connecter pour modifier votre profil")
        return redirect('user:login')
    
    email = request.session['user_email']
    client = Client.objects.get(email=email)

    if request.method == 'POST':
        #mise a jour des champs
        client.nom = request.POST['nom']
        client.prenom = request.POST['prenom']
        client.email = request.POST['email']
        client.ville = request.POST['ville']
        client.adresse = request.POST['adresse']
        client.tel = request.POST['tel']

        #si une nouvelle photo est ajoutée
        if 'photo' in request.FILES:
            client.photo = request.FILES['photo']

        client.save()
        request.session['user_photo'] = client.photo.url if client.photo else None
        messages.success(request, "Votre profil a été mis à jour avec succès")
        return redirect('user:profile')
    return render(request, 'user/profile.html',{'client':client})

@csrf_protect
def setting_profile(request):
   if 'user_email' not in request.session:
        messages.warning(request, "Veuillez vous connecter pour modifier vos paramètres.")
        return redirect('user:login')
   client = Client.objects.get(email=request.session['user_email'])
   if request.method == "POST":
        client.langue = request.POST.get("langue", "fr")
        client.notif_active = bool(request.POST.get("notifSwitch"))
        client.theme_sombre = bool(request.POST.get("themeSwitch"))
        client.alertes_email = bool(request.POST.get("alertes_email"))
        client.maj_auto = bool(request.POST.get("maj_auto"))
        client.newsletter = bool(request.POST.get("newsletter"))
        client.partage_donnees = bool(request.POST.get("partage_donnees"))
        client.localisation = bool(request.POST.get("localisation"))
        client.save()

        messages.success(request, "Vos paramètres ont été mis à jour avec succès")
        return redirect('user:setting_profile')
   context = {"client": client}
   return render(request, "user/setting.html", context)


   

def settings(request):
    if 'user_email' not in request.session:
        messages.warning(request, "Veuillez vous connecter.")
        return redirect('user:login')

    email = request.session['user_email']
    try:
        client = Client.objects.get(email=email)
    except Client.DoesNotExist:
        messages.error(request, "Compte introuvable.")
        return redirect('user:login')

    return render(request, 'user/setting.html', {'client': client})

@csrf_protect
def change_password(request):
    # Vérifier si l’utilisateur est connecté
    if 'user_email' not in request.session:
        messages.warning(request, "Veuillez vous connecter pour changer votre mot de passe.")
        return redirect('user:login')

    # Récupérer l'utilisateur connecté
    try:
        client = Client.objects.get(email=request.session['user_email'])
    except Client.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('user:login')

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Vérification du mot de passe actuel
        if not check_password(old_password, client.password):
            messages.error(request, "L’ancien mot de passe est incorrect.")
            return redirect('user:settings')

        # Vérification de correspondance du nouveau mot de passe
        if new_password != confirm_password:
            messages.warning(request, "Les nouveaux mots de passe ne correspondent pas.")
            return redirect('user:settings')

        # Sécurité : vérifier que le nouveau mot de passe est différent
        if check_password(new_password, client.password):
            messages.warning(request, "Le nouveau mot de passe doit être différent de l’ancien.")
            return redirect('user:settings')

        # Mise à jour du mot de passe
        client.password = make_password(new_password)
        client.save()

        # Message et redirection
        messages.success(request, "Mot de passe modifié avec succès ✅. Veuillez vous reconnecter.")
        # Optionnel : déconnexion automatique après changement
        request.session.flush()
        return redirect('user:login')

    return redirect('user:settings')

