import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<Map<String, dynamic>>> getProduits({
  String? nom,
  int? nbre,
  int? min,
  int? max,
  String? trier,
}) async {
  try {
    // Construction de l'URL avec seulement nom et nbre
    final Uri url = Uri.parse(
      'http://10.0.2.2:8000/optiprice_app/compare/chercher_produit/?nom=$nom&nbreproduits=$nbre',
    );

    final response = await http.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      List<Map<String, dynamic>> produits =
          List<Map<String, dynamic>>.from(data['produits']);

      // Filtrage par min et max
      if (min != null || max != null) {
        produits = produits.where((produit) {
          // Nettoyer le prix pour récupérer seulement le nombre
          String prixStr = produit['prix']
              .toString()
              .replaceAll(RegExp(r'[^0-9]'), ''); // enlève tout sauf chiffres
          int prixInt = int.tryParse(prixStr) ?? 0;

          if (min != null && prixInt < min) return false;
          if (max != null && prixInt > max) return false;
          return true;
        }).toList();
      }

      // Tri selon l'option
      if (trier != null) {
        if (trier.trim() == 'Prix croissant') {
          produits.sort((a, b) {
            int prixA = int.tryParse(a['prix'].toString().replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
            int prixB = int.tryParse(b['prix'].toString().replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
            return prixA.compareTo(prixB);
          });
        } else if (trier.trim() == 'Prix décroissant') {
          produits.sort((a, b) {
            int prixA = int.tryParse(a['prix'].toString().replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
            int prixB = int.tryParse(b['prix'].toString().replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
            return prixB.compareTo(prixA);
          });
        }
        // '-- Trier par --' => aucun tri
      }

      return produits;
    } else if (response.statusCode == 404) {
      print("Aucun produit trouvé.");
      return [];
    } else {
      print("Erreur API: ${response.body}");
      return [];
    }
  } catch (e) {
    print("Erreur: $e");
    return [];
  }
}


