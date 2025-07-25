from django.contrib import admin
from django.utils.html import format_html
from .models import Produit, Categorie, Marque, Commande, CommandeProduit, User, ArticlePanier, Panier

# Administration des Marques
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web', 'afficher_logo')
    search_fields = ('nom',)
    
    def afficher_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "Aucun logo"
    afficher_logo.short_description = 'Logo'

# Administration des Produits
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'get_marque', 'get_categorie', 'date_ajout', 'afficher_image')
    list_filter = ('categorie', 'marque', 'est_meilleure_vente')
    search_fields = ('nom', 'description', 'marque__nom')
    ordering = ('-date_ajout',)
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'description', 'prix', 'stock')
        }),
        ('Catégorisation', {
            'fields': ('categorie', 'marque')
        }),
        ('Média', {
            'fields': ('image',)
        }),
        ('Options', {
            'fields': ('est_meilleure_vente',)
        }),
    )
    
    def get_marque(self, obj):
        return obj.marque.nom if obj.marque else "-"
    get_marque.short_description = 'Marque'
    get_marque.admin_order_field = 'marque__nom'
    
    def get_categorie(self, obj):
        return obj.categorie.nom if obj.categorie else "-"
    get_categorie.short_description = 'Catégorie'
    get_categorie.admin_order_field = 'categorie__nom'
    
    def afficher_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Aucune image"
    afficher_image.short_description = 'Aperçu'

# Administration des Commandes
class CommandeProduitInline(admin.TabularInline):
    model = CommandeProduit
    extra = 0
    readonly_fields = ('produit', 'quantite')

# Mise à jour de la classe CommandeAdmin
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_commande', 'statut', 'mode_paiement', 'adresse', 'telephone', 'email', 'livraison', 'total_commande')
    list_filter = ('statut', 'date_commande', 'livraison', 'mode_paiement')
    search_fields = ('user__username', 'user__email', 'adresse', 'telephone')
    readonly_fields = ('date_commande',)
    inlines = [CommandeProduitInline]
    
    def total_commande(self, obj):
        total = sum(item.produit.prix * item.quantite for item in obj.commandeproduit_set.all())
        return f"{total} DH"
    total_commande.short_description = 'Total'
    
    fieldsets = (
        ('Client', {
            'fields': ('user', 'adresse', 'telephone', 'email')
        }),
        ('Livraison et Paiement', {
            'fields': ('livraison', 'mode_paiement', 'statut')
        }),
        ('Informations', {
            'fields': ('date_commande',)
        }),
    )

# Administration des Utilisateurs
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telephone', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'newsletter')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telephone')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'telephone')
        }),
        ('Profil', {
            'fields': ('photo_profil', 'langue', 'newsletter')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# Administration des Catégories
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

# Administration du Panier
class ArticlePanierInline(admin.TabularInline):
    model = ArticlePanier
    extra = 0

class PanierAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_creation', 'nombre_articles', 'total_panier')
    inlines = [ArticlePanierInline]
    
    def nombre_articles(self, obj):
        return obj.articles.count()
    nombre_articles.short_description = 'Nombre d\'articles'
    
    def total_panier(self, obj):
        total = sum(article.total_article() for article in obj.articles.all())
        return f"{total} €"
    total_panier.short_description = 'Total'


# Enregistrement des modèles dans l'admin
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Marque, MarqueAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Panier, PanierAdmin)
