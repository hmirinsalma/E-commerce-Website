from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
import json

from .models import Produit, Categorie, Marque, Panier, ArticlePanier, Commande, CommandeProduit
from .forms import CommandeForm, ProfileForm, PasswordChangeCustomForm, RegisterForm, ConnexionForm

# Vue pour la page d'accueil
def home_view(request):
    nouveautes = Produit.objects.order_by('-date_ajout')[:8]
    bestsellers = Produit.objects.filter(est_meilleure_vente=True)[:8]
    categories = Categorie.objects.all()[:4]
    marques = Marque.objects.all()  # Add this line to define marques
    
    return render(request, 'CosmoLux/home.html', {
        'nouveautes': nouveautes,
        'bestsellers': bestsellers,
        'categories': categories,
        'marques': marques,
    })
# Vue pour la page Produits
def produits_view(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    marques = Marque.objects.all()

    # Filtres dynamiques
    categorie_filter = request.GET.get('categorie')
    if categorie_filter:
        produits = produits.filter(categorie__nom=categorie_filter)

    prix_min = request.GET.get('prix_min')
    prix_max = request.GET.get('prix_max')
    if prix_min and prix_max:
        produits = produits.filter(prix__gte=prix_min, prix__lte=prix_max)

    marque_filter = request.GET.get('marque')
    if marque_filter:
        produits = produits.filter(marque__nom=marque_filter)

    # Filtre bestseller
    bestseller = request.GET.get('bestseller')
    if bestseller == 'true':
        produits = produits.filter(est_meilleure_vente=True)

    # Recherche par mot-clé
    recherche = request.GET.get('recherche')
    if recherche:
        produits = produits.filter(nom__icontains=recherche)

    # Tri des produits
    sort = request.GET.get('sort', 'nouveautes')
    if sort == 'prix_asc':
        produits = produits.order_by('prix')
    elif sort == 'prix_desc':
        produits = produits.order_by('-prix')
    else:  # Par défaut: nouveautés
        produits = produits.order_by('-date_ajout')

    # Pagination : 9 produits par page
    paginator = Paginator(produits, 9)
    page_number = request.GET.get('page')
    produits_page = paginator.get_page(page_number)

    context = {
        'produits': produits_page,
        'paginator': paginator,
        'categories': categories,
        'marques': marques,
        'categorie_filter': categorie_filter,
        'marque_filter': marque_filter,
        'recherche': recherche,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'sort': sort
    }
    return render(request, 'CosmoLux/produits.html', context)

# Vue pour ajouter un produit au panier
# Vue pour ajouter un produit au panier
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    # Vérifier si le produit est en stock
    if produit.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Ce produit est en rupture de stock.'
            })
        messages.error(request, "Ce produit est en rupture de stock.")
        return redirect('produits')
    
    # Vérifier si l'utilisateur est connecté
    if request.user.is_authenticated:
        panier, created = Panier.objects.get_or_create(user=request.user)
    else:
        # Pour les utilisateurs non connectés, on utilise la session
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        panier, created = Panier.objects.get_or_create(user=None)
        request.session['panier_id'] = panier.id
    
    # Vérifier si le produit est déjà dans le panier
    article, created = ArticlePanier.objects.get_or_create(panier=panier, produit=produit)
    
    # Vérifier si la quantité demandée est disponible en stock
    if not created and article.quantite + 1 > produit.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Stock insuffisant. Quantité disponible: {produit.stock}'
            })
        messages.error(request, f"Stock insuffisant. Quantité disponible: {produit.stock}")
        return redirect('produits')
    
    if not created:
        # Si le produit est déjà dans le panier, on met à jour la quantité
        article.quantite += 1
        article.save()
    
    # Si la requête est AJAX, renvoyer une réponse JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Produit ajouté au panier',
            'panier_count': panier.articles.count(),
            'panier_total': float(panier.total())
        })
    
    # Sinon, rediriger vers la page produits
    return redirect('produits')

# Vue pour mettre à jour la quantité d'un produit dans le panier
# Vue pour mettre à jour la quantité d'un produit dans le panier
def mise_a_jour_quantite(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    if request.user.is_authenticated:
        panier = get_object_or_404(Panier, user=request.user)
    else:
        panier_id = request.session.get('panier_id')
        panier = get_object_or_404(Panier, id=panier_id, user=None)
    
    article = get_object_or_404(ArticlePanier, panier=panier, produit=produit)
    
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        
        # Vérifier si la quantité demandée est disponible en stock
        if quantite > produit.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Stock insuffisant. Quantité disponible: {produit.stock}'
                })
            messages.error(request, f"Stock insuffisant. Quantité disponible: {produit.stock}")
            return redirect('panier')
        
        if quantite > 0:
            article.quantite = quantite
            article.save()
        else:
            article.delete()
    
    # Si la requête est AJAX, renvoyer une réponse JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Quantité mise à jour',
            'article_total': float(article.total_article()),
            'panier_total': float(panier.total())
        })
    
    return redirect('panier')
# Vue pour supprimer un produit du panier
def supprimer_article(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    if request.user.is_authenticated:
        panier = get_object_or_404(Panier, user=request.user)
    else:
        panier_id = request.session.get('panier_id')
        panier = get_object_or_404(Panier, id=panier_id, user=None)
    
    article = get_object_or_404(ArticlePanier, panier=panier, produit=produit)
    article.delete()
    
    # Si la requête est AJAX, renvoyer une réponse JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Produit supprimé du panier',
            'panier_count': panier.articles.count(),
            'panier_total': float(panier.total())
        })
    
    return redirect('panier')

# Vue pour afficher le panier
def panier_view(request):
    if request.user.is_authenticated:
        panier, created = Panier.objects.get_or_create(user=request.user)
    else:
        panier_id = request.session.get('panier_id')
        if panier_id:
            panier = get_object_or_404(Panier, id=panier_id, user=None)
        else:
            panier = Panier.objects.create(user=None)
            request.session['panier_id'] = panier.id
    
    articles = panier.articles.all().select_related('produit')
    total = panier.total()
    
    context = {
        'panier_items': articles,  # Changé de 'articles' à 'panier_items'
        'total_panier': total      # Changé de 'total' à 'total_panier'
    }
    
    return render(request, 'CosmoLux/panier.html', context)
    

# Mise à jour de la fonction checkout
@login_required
def checkout(request):
    panier = get_object_or_404(Panier, user=request.user)
    articles = panier.articles.all().select_related('produit')
    
    if not articles:
        messages.warning(request, "Votre panier est vide.")
        return redirect('panier')
    
    # Vérifier si tous les produits sont disponibles en stock
    for article in articles:
        if article.produit.stock < article.quantite:
            messages.error(request, f"Le produit '{article.produit.nom}' n'est plus disponible en quantité suffisante (stock: {article.produit.stock}).")
            return redirect('panier')
    
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.user = request.user
            commande.save()
            
            # Créer les lignes de commande et mettre à jour le stock
            for article in articles:
                CommandeProduit.objects.create(
                    commande=commande,
                    produit=article.produit,
                    quantite=article.quantite,
                    prix_unitaire=article.produit.prix
                )
                
                # Mettre à jour le stock du produit
                produit = article.produit
                produit.stock -= article.quantite
                produit.save()
            
            # Vider le panier
            articles.delete()
            
            # Stocker le mode de paiement et le total dans la session pour la page de confirmation
            request.session['mode_paiement'] = commande.mode_paiement
            request.session['total_commande'] = str(commande.total())
            
            messages.success(request, "Votre commande a été enregistrée avec succès.")
            return redirect('confirmation_commande')
    else:
        form = CommandeForm(initial={
            'email': request.user.email,
            'telephone': request.user.telephone
        })
    
    context = {
        'form': form,
        'articles': articles,
        'total': panier.total()
    }
    
    return render(request, 'commande/passer_commande.html', context)

def confirmation_commande(request):
    # Récupérer les informations de la session
    mode_paiement = request.session.get('mode_paiement', 'livraison')
    total = request.session.get('total_commande', '0')
    
    # Nettoyer la session
    if 'mode_paiement' in request.session:
        del request.session['mode_paiement']
    if 'total_commande' in request.session:
        del request.session['total_commande']
    
    return render(request, 'commande/confirmation.html', {
        'mode_paiement': mode_paiement,
        'total': total
    })



@login_required
def historique_commandes(request):
    commandes = Commande.objects.filter(user=request.user).order_by('-date_commande')
    return render(request, 'commande/historique.html', {'commandes': commandes})

@login_required
def details_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, user=request.user)
    produits = CommandeProduit.objects.filter(commande=commande).select_related('produit')
    return render(request, 'commande/details.html', {'commande': commande, 'produits': produits})

@login_required
def profil_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profil.html', {'form': form})

@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['current_password']):
                messages.error(request, "Mot de passe actuel incorrect.")
            elif form.cleaned_data['new_password'] != form.cleaned_data['confirm_password']:
                messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
            else:
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Mot de passe mis à jour.")
                return redirect('profil')
    else:
        form = PasswordChangeCustomForm()
    return render(request, 'changer_mot_de_passe.html', {'form': form})

def inscription_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/inscription.html', {'form': form})

def connexion_view(request):
    if request.method == 'POST':
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = ConnexionForm()
    return render(request, 'registration/connexion.html', {'form': form})

@login_required
def deconnexion_view(request):
    logout(request)
    return redirect('connexion')

# API pour le panier flottant
def produits_panier_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produit_ids = data.get('produits', [])
            
            # Récupérer les informations des produits
            produits = Produit.objects.filter(id__in=produit_ids)
            
            # Formater les données pour le frontend
            produits_data = []
            for produit in produits:
                produits_data.append({
                    'id': produit.id,
                    'nom': produit.nom,
                    'prix': float(produit.prix),
                    'image': produit.image.url if produit.image else None,
                    'marque': produit.marque.nom if produit.marque else 'Générique'
                })
            
            return JsonResponse(produits_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def panier_info_api(request):
    if request.user.is_authenticated:
        panier, created = Panier.objects.get_or_create(user=request.user)
    else:
        panier_id = request.session.get('panier_id')
        if panier_id:
            panier = get_object_or_404(Panier, id=panier_id, user=None)
        else:
            panier = Panier.objects.create(user=None)
            request.session['panier_id'] = panier.id
    
    articles = panier.articles.all().select_related('produit')
    articles_data = [
        {
            'produit_id': article.produit.id,
            'nom': article.produit.nom,
            'prix': float(article.produit.prix),
            'quantite': article.quantite,
            'total': float(article.total_article())
        }
        for article in articles
    ]
    
    return JsonResponse({
        'articles': articles_data,
        'total': float(panier.total())
    })
# Add this new function to your existing views.py file
def about_view(request):
    return render(request, 'about.html')
    