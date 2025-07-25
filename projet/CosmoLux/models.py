from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Modèle utilisateur personnalisé
class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='photos/', blank=True, null=True)
    langue = models.CharField(max_length=20, blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username

# Modèle pour les catégories de produits
class Categorie(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.nom

# Modèle pour les marques
class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='marques/', blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

# Modèle pour les produits
class Produit(models.Model):
    nom = models.CharField(max_length=100, default='')
    description = models.TextField(null=True, blank=True)
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Prix (DH)"
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    marque = models.ForeignKey(Marque, on_delete=models.SET_NULL, null=True, related_name='produits')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='produits')
    date_ajout = models.DateTimeField(default=timezone.now)
    est_meilleure_vente = models.BooleanField(default=False)  # Pour les bestsellers

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-date_ajout']

    def __str__(self):
        return self.nom
    
    def est_disponible(self):
        return self.stock > 0

# Modèle pour le panier d'achat
class Panier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'

    def __str__(self):
        return f"Panier - {self.user.username if self.user else 'Non connecté'}"
    
    def total(self):
        return sum(article.total_article() for article in self.articles.all())

# Modèle pour les articles dans le panier
class ArticlePanier(models.Model):
    panier = models.ForeignKey(Panier, related_name="articles", on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Article du panier'
        verbose_name_plural = 'Articles du panier'

    def total_article(self):
        return self.produit.prix * self.quantite

    def __str__(self):
        return f"{self.produit.nom} (x{self.quantite})"

# Modèle pour les commandes
class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée')
    ]
    
    LIVRAISON_CHOICES = [
        ('standard', 'Standard (3-5 jours)'),
        ('express', 'Express (1-2 jours)')
    ]
    
    PAIEMENT_CHOICES = [
        ('en_ligne', 'Paiement en ligne'),
        ('livraison', 'Paiement à la livraison')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    livraison = models.CharField(max_length=100, choices=LIVRAISON_CHOICES, default='standard')
    mode_paiement = models.CharField(max_length=100, choices=PAIEMENT_CHOICES, default='livraison')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"
    
    def total(self):
        """Calcule le total de la commande"""
        return sum(item.produit.prix * item.quantite for item in self.commandeproduit_set.all())
    
    def nombre_articles(self):
        """Retourne le nombre total d'articles dans la commande"""
        return sum(item.quantite for item in self.commandeproduit_set.all())

# Modèle pour les produits dans une commande
class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Produit commandé'
        verbose_name_plural = 'Produits commandés'

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"
    
    def save(self, *args, **kwargs):
        # Enregistre le prix au moment de la commande pour historique
        if not self.prix_unitaire:
            self.prix_unitaire = self.produit.prix
        super().save(*args, **kwargs)
    
    def total_ligne(self):
        """Calcule le total pour cette ligne de commande"""
        if self.prix_unitaire:
            return self.prix_unitaire * self.quantite
        return self.produit.prix * self.quantite
