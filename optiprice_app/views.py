from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.


def index(request):
    return render(request, 'index.html')


def compare(request):
    return render(request, 'compare.html')


def scan(request):
    return render(request, 'scan.html')


def visual(request):
    return render(request, 'visual.html')



def chercher_produit_oraimo(request):
    produit = request.GET.get('nom')
    nbreproduits = int(request.GET.get('nbreproduits', 10))
    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    url = f'https://ci.oraimo.com/search?keyword={produit}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({'error': 'Impossible de récupérer les données'}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')
    produits_trouves = []

    # Sélectionner tous les produits
    container = soup.select('.js_product.site-product')[:nbreproduits]

    for item in container:
        # Nom
        nom_tag = item.select_one('h3 a span')
        nom = nom_tag.get_text(strip=True) if nom_tag else 'N/A'

        # Lien
        lien_tag = item.select_one('a.js_select_item')
        lien = 'https://ci.oraimo.com' + lien_tag['href'] if lien_tag and 'href' in lien_tag.attrs else 'N/A'

        # Prix actuel
        prix_tag = item.select_one('.product-price span')
        prix = prix_tag.get_text(strip=True) if prix_tag else 'N/A'

        # Ancien prix / prix barré
        old_price_tag = item.select_one('.product-price del')
        prix_sans_reduction = old_price_tag.get_text(strip=True) if old_price_tag else prix

        # Image
        img_tag = item.select_one('.product-picture-wrap img')
        image = img_tag.get('data-src', img_tag.get('src', '')) if img_tag else 'N/A'

        # Note et nombre d'avis
        note_tag = item.select_one('.review-score')
        note = note_tag.get_text(strip=True) if note_tag else 'N/A'

        nb_avis_tag = item.select_one('.review-count')
        nb_avis = nb_avis_tag.get_text(strip=True).replace('(', '').replace(')', '') if nb_avis_tag else '0'

        # Catégorie
        categorie = item.get('data-category', 'N/A')

        produits_trouves.append({
            'nom': nom,
            'lien': lien,
            'prix': prix,
            'prix_sans_reduction': prix_sans_reduction,
            'image': image,
            'note': note,
            'nb_avis': nb_avis,
            'categorie': categorie,
            "marchand" : "Oraimo"
        })

    return JsonResponse({'produits': produits_trouves})


