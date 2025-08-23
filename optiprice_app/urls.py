from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("compare", views.compare, name="compare"),
    path('compare/chercher_produit/', views.chercher_produit, name='chercher_produit'),
    path('compare/chercher_produit_oraimo/', views.chercher_produit_oraimo, name='chercher_produit_oraimo'),
    path('compare/chercher_produit_adjovan/', views.chercher_produit_adjovan, name='chercher_produit_adjovan'),
    path('compare/chercher_produit_global/', views.chercher_produit_global, name='chercher_produit_global'),


    path("scan", views.scan, name="scan"),
    path("visual", views.visual, name="visual")
]