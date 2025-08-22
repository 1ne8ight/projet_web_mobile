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


def chercher_produit(request):
    # On récupère le nom du produit passé en paramètre GET
    produit = request.GET.get('nom')
    nbreproduits = int(request.GET.get('nbreproduits'))
    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    # URL de recherche sur un site e-commerce (exemple Amazon ou autre)
    # ATTENTION : certains sites bloquent les scrapers et Amazon interdit le scraping
    # url = f'https://www.jumia.ci/search?q={produit}'
    url = f'https://www.jumia.ci/catalog/?q={produit}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({'error': 'Impossible de récupérer les données'}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemple générique de parsing (à adapter selon le site)
    produits_trouves = [] 

    # Sélectionner la div principale contenant tous les articles
    container = soup.select_one('.-phs.-pvxs.row._no-g._4cl-3cm-shs')

    if container:
        # Sélectionner tous les articles à l'intérieur
        for item in container.select('article.prd._fb.col.c-prd')[:nbreproduits]: 
            # Nom
            nom_tag = item.select_one('.name')
            nom = nom_tag.get_text(strip=True) if nom_tag else 'N/A'

            # Lien (balise <a> avec classe 'core')
            lien_tag = item.select_one('a.core')
            lien = lien_tag['href'] if lien_tag and 'href' in lien_tag.attrs else 'N/A'

            # Prix
            prix_tag = item.select_one('.prc')
            prix = prix_tag.get_text(strip=True) if prix_tag else 'N/A'

            # Image (balise <img>)
            img_tag = item.select_one('.img-c img')
            if img_tag:
                # Priorité au data-src si présent
                image = img_tag.get('data-src', img_tag.get('src', ''))
            else:
                image = 'N/A'

            produits_trouves.append({
                'nom': nom,
                'lien': lien,
                'prix': prix,
                'image': image
            })



    return JsonResponse({'produits': produits_trouves})

def chercher_produit_kevajo(request):
    # On récupère le nom du produit passé en paramètre GET
    produit = request.GET.get('nom')
    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    # URL de recherche sur un site e-commerce (exemple Amazon ou autre)
    # ATTENTION : certains sites bloquent les scrapers et Amazon interdit le scraping
    # url = f'https://www.jumia.ci/search?q={produit}'
    url = f'https://www.jumia.ci/catalog/?q={produit}'
    url = f'https://kevajo.com/?s={produit}&post_type=product&product_cat=0'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({'error': 'Impossible de récupérer les données'}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemple générique de parsing (à adapter selon le site)
    produits_trouves = [] 

    # Sélectionner la div principale contenant tous les articles
    container = soup.select_one('.-phs.-pvxs.row._no-g._4cl-3cm-shs')

    if container:
        # Sélectionner tous les articles à l'intérieur
        for item in container.select('article.prd._fb.col.c-prd')[:10]:  # Limite à 10 résultats
            # Nom
            nom_tag = item.select_one('.name')
            nom = nom_tag.get_text(strip=True) if nom_tag else 'N/A'

            # Lien (balise <a> avec classe 'core')
            lien_tag = item.select_one('a.core')
            lien = lien_tag['href'] if lien_tag and 'href' in lien_tag.attrs else 'N/A'

            # Prix
            prix_tag = item.select_one('.prc')
            prix = prix_tag.get_text(strip=True) if prix_tag else 'N/A'

            # Image (balise <img>)
            img_tag = item.select_one('.img-c img')
            if img_tag:
                # Priorité au data-src si présent
                image = img_tag.get('data-src', img_tag.get('src', ''))
            else:
                image = 'N/A'

            produits_trouves.append({
                'nom': nom,
                'lien': lien,
                'prix': prix,
                'image': image
            })




    return JsonResponse({'produits': produits_trouves})



























# def chercher_produit(request):
#     # On récupère le nom du produit passé en paramètre GET
#     produit = request.GET.get('nom')
#     if not produit:
#         return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

#     # URL de recherche sur un site e-commerce (exemple Amazon ou autre)
#     # ATTENTION : certains sites bloquent les scrapers et Amazon interdit le scraping
#     # url = f'https://www.jumia.ci/search?q={produit}'
#     url = f'https://www.jumia.ci/catalog/?q={produit}'

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                       "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return JsonResponse({'error': 'Impossible de récupérer les données'}, status=500)

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Exemple générique de parsing (à adapter selon le site)
#     produits_trouves = []

#     # Sélectionner la div principale contenant tous les articles
#     container = soup.select_one('.-phs.-pvxs.row._no-g._4cl-3cm-shs')

#     if container:
#         # Sélectionner tous les articles à l'intérieur
#         for item in container.select('article.prd._fb.col.c-prd')[:10]:  # Limite à 10 résultats
#             # Nom
#             nom_tag = item.select_one('.name')
#             nom = nom_tag.get_text(strip=True) if nom_tag else 'N/A'

#             # Lien (balise <a> avec classe 'core')
#             lien_tag = item.select_one('a.core')
#             lien = lien_tag['href'] if lien_tag and 'href' in lien_tag.attrs else 'N/A'

#             # Prix
#             prix_tag = item.select_one('.prc')
#             prix = prix_tag.get_text(strip=True) if prix_tag else 'N/A'

#             produits_trouves.append({
#                 'nom': nom,
#                 'lien': lien,
#                 'prix': prix
#             })



#     return JsonResponse({'produits': produits_trouves})
