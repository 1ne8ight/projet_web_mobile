from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def index(request):
    return render(request, 'index.html')


def compare(request):
    return render(request, 'compare.html')


def scan(request):
    return render(request, 'scan.html')


def visual(request):
    return render(request, 'visual.html')



@csrf_exempt
def autocomplete(request):
    query = request.GET.get("q", "").strip()
    suggestions = []

    if query:
        try:
            url = f"https://www.jumia.ci/catalog/api/autocomplete/?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/114.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                suggestions = [item['value'] for item in data.get('suggestions', [])]

        except Exception as e:
            print("Erreur autocomplete:", e)

    return JsonResponse({"suggestions": suggestions})





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

    produits_trouves = [] 

    # Sélectionner la div principale contenant tous les articles
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

            # Réduction (div avec classe "bdg _dsct _sm")
            reduction_tag = item.select_one('.bdg._dsct._sm')
            reduction = reduction_tag.get_text(strip=True) if reduction_tag else '0%'

            prix_sans_reduction_tag = item.select_one('.old')
            # prix_sans_reduction = prix_sans_reduction_tag.get_text(strip=True) if reduction_tag else '0 FCFA'
            prix_sans_reduction = prix_sans_reduction_tag.get_text(strip=True) if prix_sans_reduction_tag else '0 FCFA'


            # Image (balise <img>)
            img_tag = item.select_one('.img-c img')
            if img_tag:
                image = img_tag.get('data-src', img_tag.get('src', ''))
            else:
                image = 'N/A'

            # Marque (data-ga4-item_brand)
            brand_tag = item.select_one('a[data-ga4-item_brand]')
            brand = brand_tag['data-ga4-item_brand'] if brand_tag else 'N/A'

            # Avis (note et nombre d’avis)
            avis_tag = item.select_one('.rev')
            if avis_tag:
                # Note (ex: "4.2 out of 5")
                note_tag = avis_tag.select_one('.stars._s')
                note = note_tag.get_text(strip=True) if note_tag else 'N/A'

                # Nombre d’avis (le texte après les étoiles, ex "(249)")
                nb_avis = avis_tag.get_text(strip=True).replace(note, '').strip()
            else:
                note = 'N/A'
                nb_avis = '0'
            
            produits_trouves.append({
                'nom': nom,
                'lien': lien,
                'prix': prix,
                'reduction': reduction,
                'prix_sans_reduction': prix_sans_reduction,
                'image': image,
                'note': note,
                'nb_avis': nb_avis,
                'boutique' : brand
            })
    return JsonResponse({'produits': produits_trouves})


def chercher_produit_oraimo(request):
    # On récupère le nom du produit passé en paramètre GET
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

    # Sélectionner tous les produits
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

def chercher_produit_global(request):
    """
    Route principale qui redirige vers le bon scraper
    selon la catégorie (Jumia, Oraimo, Adjovan).
    """
    categorie = request.GET.get('categorie', '').lower()  # récupère la catégorie envoyée
    produit = request.GET.get('nom')
    nbreproduits = int(request.GET.get('nbreproduits', 10))

    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    # Dispatch vers le bon scraper
    if categorie == "electronique":
        return chercher_produit_oraimo(request)
    elif categorie == "vivrier":
        return chercher_produit_adjovan(request)
    else:  # par défaut => Global (Jumia)
        return chercher_produit(request)



def chercher_produit_global_2(request):
    """
    - Global (Jumia)
    - Electronique (Oraimo)
    - Vivrier (Adjovan)
    """

    categorie = request.GET.get('categorie', 'global').lower()
    produit = request.GET.get('nom')
    nbreproduits = int(request.GET.get('nbreproduits', 10))

    if not produit:
        return JsonResponse({'error': 'Veuillez fournir le nom du produit'}, status=400)

    produits = []

    try:
        if categorie == "electronique":  # Scraper Oraimo
            url = f"https://www.oraimo.com/catalogsearch/result/?q={produit}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                items = soup.select(".product-item-info")[:nbreproduits]
                for item in items:
                    nom = item.select_one(".product-item-link")
                    prix = item.select_one(".price")
                    image = item.select_one(".product-image-photo")
                    lien = item.select_one("a")

                    produits.append({
                        "nom": nom.text.strip() if nom else "Inconnu",
                        "prix": prix.text.strip() if prix else "Non disponible",
                        "image": image["src"] if image else "",
                        "lien": lien["href"] if lien else "",
                        "site": "Oraimo"
                    })

        elif categorie == "vivrier":  # Scraper Adjovan
            url = f"https://www.adjovan.com/recherche?controller=search&s={produit}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                items = soup.select(".js-product-miniature")[:nbreproduits]
                for item in items:
                    nom = item.select_one(".product-title a")
                    prix = item.select_one(".price")
                    image = item.select_one("img")
                    lien = item.select_one(".product-title a")

                    produits.append({
                        "nom": nom.text.strip() if nom else "Inconnu",
                        "prix": prix.text.strip() if prix else "Non disponible",
                        "image": image["data-src"] if image and "data-src" in image.attrs else "",
                        "lien": lien["href"] if lien else "",
                        "site": "Adjovan"
                    })

        else:  # Scraper Jumia (par défaut Global)
            url = f"https://www.jumia.ci/catalog/?q={produit}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                items = soup.select(".info")[:nbreproduits]
                for item in items:
                    nom = item.select_one(".name")
                    prix = item.select_one(".prc")
                    image = item.find_previous("img")
                    lien = item.find_parent("a")

                    produits.append({
                        "nom": nom.text.strip() if nom else "Inconnu",
                        "prix": prix.text.strip() if prix else "Non disponible",
                        "image": image["data-src"] if image and "data-src" in image.attrs else "",
                        "lien": "https://www.jumia.ci" + lien["href"] if lien else "",
                        "site": "Jumia"
                    })

        return JsonResponse({"produits": produits})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)