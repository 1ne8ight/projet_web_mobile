import '/backend/api_requests/api_calls.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'liste_produits_model.dart';
export 'liste_produits_model.dart';

class ListeProduitsWidget extends StatefulWidget {
  const ListeProduitsWidget({
    super.key,
    this.produits,
  });

  final List<dynamic>? produits;

  static String routeName = 'liste_produits';
  static String routePath = '/listeProduits';

  @override
  State<ListeProduitsWidget> createState() => _ListeProduitsWidgetState();
}

class _ListeProduitsWidgetState extends State<ListeProduitsWidget> {
  late ListeProduitsModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => ListeProduitsModel());
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {

    final produits = widget.produits ?? [];


    return Scaffold(
      key: scaffoldKey,
      backgroundColor: const Color(0xFFF1F4F8),
      appBar: AppBar(
        backgroundColor: const Color(0xFFEB7D26),
        automaticallyImplyLeading: false,
        leading: FlutterFlowIconButton(
          borderColor: Colors.transparent,
          borderRadius: 30.0,
          borderWidth: 1.0,
          buttonSize: 60.0,
          icon: const Icon(
            Icons.arrow_back_rounded,
            color: Colors.white,
            size: 30.0,
          ),
          onPressed: () async {
            context.pop();
          },
        ),
        title: Text(
          'OptiPrix',
          textAlign: TextAlign.center,
          style: FlutterFlowTheme.of(context).bodyMedium.override(
                font: GoogleFonts.inter(
                  fontWeight: FontWeight.bold,
                  fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
                ),
                color: FlutterFlowTheme.of(context).primaryBackground,
                fontSize: 25.0,
                letterSpacing: 0.0,
                fontWeight: FontWeight.bold,
                fontStyle: FlutterFlowTheme.of(context).bodyMedium.fontStyle,
              ),
        ),
        actions: const [],
        centerTitle: true,
        elevation: 2.0,
      ),
      body: produits.isEmpty
        ? const Center(
            child: Text(
              "Aucun produit trouvé",
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
          )
        : ListView.builder(
            padding: const EdgeInsets.all(16.0),
            itemCount: produits.length,
            itemBuilder: (context, index) {
              final produit = produits[index] as Map<String, dynamic>;

              return Container(
                margin: const EdgeInsets.only(bottom: 16.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  boxShadow: const [
                    BoxShadow(
                      blurRadius: 4.0,
                      color: Color(0x33000000),
                      offset: Offset(0.0, 2.0),
                    )
                  ],
                  borderRadius: BorderRadius.circular(12.0),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Image + prix
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          ClipRRect(
                            borderRadius: BorderRadius.circular(12.0),
                            child: Image.network(
                              produit['image'] ?? '',
                              width: 100.0,
                              height: 80.0,
                              fit: BoxFit.cover,
                              errorBuilder: (_, __, ___) =>
                                  const Icon(Icons.image),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                if (produit['reduction'] != null &&
                                    produit['reduction'].toString().isNotEmpty)
                                  Container(
                                    decoration: BoxDecoration(
                                      gradient: const LinearGradient(
                                        colors: [
                                          Color(0xFFF8F8F8),
                                          Color(0xFFE7DCD7)
                                        ],
                                        stops: [0.0, 1.0],
                                        begin: Alignment.topCenter,
                                        end: Alignment.bottomCenter,
                                      ),
                                      borderRadius: BorderRadius.circular(8.0),
                                    ),
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: 6, vertical: 2),
                                    child: Text(
                                      produit['reduction'],
                                      style: const TextStyle(
                                        color: Color(0xFFFF5963),
                                        fontSize: 16.0,
                                      ),
                                    ),
                                  ),
                                if (produit['prix_sans_reduction'] != null)
                                  Padding(
                                    padding: const EdgeInsets.only(top: 4.0),
                                    child: Text(
                                      produit['prix_sans_reduction'],
                                      style: const TextStyle(
                                        fontSize: 12.0,
                                        color: Color(0xFF57636C),
                                        decoration:
                                            TextDecoration.lineThrough,
                                      ),
                                    ),
                                  ),
                              ],
                            ),
                          ),
                          Text(
                            produit['prix'] ?? '',
                            style: const TextStyle(
                              fontSize: 18.0,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF14181B),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 8),

                      // Nom
                      Text(
                        produit['nom'] ?? '',
                        style: const TextStyle(
                          fontSize: 14.0,
                          color: Color(0xFF57636C),
                        ),
                      ),

                      const SizedBox(height: 8),

                      // Avis et notes
                      Row(
                        children: [
                          const Icon(Icons.star,
                              color: Color(0xFFEC8C09), size: 20),
                          const SizedBox(width: 4),
                          Text(
                            "${produit['note']} ⭐  (${produit['nb_avis']} avis)",
                            style: const TextStyle(
                              fontSize: 14.0,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF14181B),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
    );
  }
}
