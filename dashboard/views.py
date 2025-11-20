from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages
from user.models import Client
from shop.models import Article, Catalogue

# ✅ Décorateur de connexion
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_email' not in request.session:
            messages.warning(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('user:login')

        return view_func(request, *args, **kwargs)
    return wrapper


# ✅ Vue du dashboard admin
@login_required
def dash(request):
    user_email = request.session.get('user_email')
    is_admin = request.session.get('is_admin', False)

    # Vérifie le rôle d'administrateur
    if not is_admin:
        messages.error(request, "Accès refusé. Vous devez être administrateur pour voir cette page.")
        return redirect('user:login')

    # Récupère les infos de l'utilisateur connecté
    try:
        admin_user = Client.objects.get(email=user_email)
    except Client.DoesNotExist:
        messages.error(request, "Utilisateur introuvable. Veuillez vous reconnecter.")
        request.session.flush()
        return redirect('user:login')

    # Empêche le cache du navigateur (protection retour arrière)
    response = render(request, 'dash/dash_admin.html', {'user': admin_user})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

@login_required
def tous_articles(request):
    articles = Article.objects.select_related('catalogue').all()
    return render(request, 'dash/articles.html', {
        'articles': articles,
        'user': request.user  # <-- important
    })

def ajouter_article(request):
    """
    Ajouter un nouvel article sans forms.py
    """
    catalogues = Catalogue.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        stock = request.POST.get('stock')
        catalogue_id = request.POST.get('catalogue')
        image = request.FILES.get('image')

        if nom and description and prix and stock and catalogue_id:
            try:
                catalogue = Catalogue.objects.get(id=catalogue_id)
                Article.objects.create(
                    nom=nom,
                    description=description,
                    prix=prix,
                    stock=stock,
                    catalogue=catalogue,
                    image=image
                )
                messages.success(request, "Article ajouté avec succès !")
                return redirect('dash:catalogue_articles')
            except Catalogue.DoesNotExist:
                messages.error(request, "Catalogue invalide.")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'dash/ajouter_article.html', {'catalogues': catalogues})

