from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Pages principales
    path('', views.home_view, name='home'),
    path('produits/', views.produits_view, name='produits'),
    
    # Gestion du panier
    path('panier/', views.panier_view, name='panier'),
    path('ajouter_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('mise_a_jour_quantite/<int:produit_id>/', views.mise_a_jour_quantite, name='mise_a_jour_quantite'),
    path('supprimer_article/<int:produit_id>/', views.supprimer_article, name='supprimer_article'),
    
    # Processus de commande
    path('checkout/', views.checkout, name='checkout'),
    path('commande/', views.checkout, name='passer_commande'),  # Alias pour la compatibilité
    path('commande/confirmation/', views.confirmation_commande, name='confirmation_commande'),
    path('commande/historique/', views.historique_commandes, name='historique_commandes'),
    path('commande/<int:commande_id>/', views.details_commande, name='details_commande'),
    
    # Gestion du profil utilisateur
    path('profil/', views.profil_view, name='profil'),
    path('profil/mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
    # Authentification
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    
    # Réinitialisation de mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), 
        name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'),
    
    # API
    path('api/produits-panier/', views.produits_panier_api, name='produits_panier_api'),
    path('api/panier-info/', views.panier_info_api, name='panier_info_api'),
    path('about/', views.about_view, name='about'),
]
