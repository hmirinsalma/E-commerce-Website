# Generated by Django 5.2 on 2025-04-23 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CosmoLux', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='categorie',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='date_ajout',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='description',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='est_meilleure_vente',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='image',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='prix',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='stock',
        ),
    ]
