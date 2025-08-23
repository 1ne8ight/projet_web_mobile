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



def chercher_produit_adjovan(request):
    # On récupère le nom du produit passé en paramètre GET
    produit = request.GET.get('nom')
    nbreproduits = int(request.GET.get('nbreproduits', 10))
    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    url = f'https://www.adjovan.com/?s={produit}&post_type=product&dgwt_wcas=1'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({'error': 'Impossible de récupérer les données'}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')
    produits_trouves = []

    container = soup.select('.product-block-inner')[:nbreproduits]

    for item in container:
        # Nom
        nom_tag = item.select_one('.product-name')
        nom = nom_tag.get_text(strip=True) if nom_tag else 'N/A'

        # Lien
        lien_tag = item.select_one('a')
        lien = lien_tag['href'] if lien_tag and 'href' in lien_tag.attrs else 'N/A'

        # Prix
        prix_tag = item.select_one('.price .woocommerce-Price-amount')
        prix = prix_tag.get_text(strip=True) if prix_tag else 'N/A'

        # Image
        img_tag = item.select_one('.image-block img')
        image = img_tag.get('src', '') if img_tag else 'N/A'

        # Description courte
        desc_tag = item.select_one('.woocommerce-product-details__short-description p')
        description = desc_tag.get_text(strip=True) if desc_tag else 'N/A'

        produits_trouves.append({
            'nom': nom,
            'lien': lien,
            'prix': prix,
            'image': image,
            'description': description,
            'marchand' : "Adjovan"
        })

    return JsonResponse({'produits': produits_trouves})
