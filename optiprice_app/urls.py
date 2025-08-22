from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("compare", views.compare, name="compare"),
    path('compare/chercher_produit/', views.chercher_produit, name='chercher_produit'),


    path("scan", views.scan, name="scan"),
    path("visual", views.visual, name="visual")
]