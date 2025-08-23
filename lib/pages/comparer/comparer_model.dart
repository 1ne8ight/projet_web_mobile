import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/form_field_controller.dart';
import '/index.dart';
import 'comparer_widget.dart' show ComparerWidget;
import 'package:flutter/material.dart';
import 'package:mask_text_input_formatter/mask_text_input_formatter.dart';

class ComparerModel extends FlutterFlowModel<ComparerWidget> {
  ///  State fields for stateful widgets in this page.

  final formKey = GlobalKey<FormState>();
  // State field(s) for nom_produits widget.
  FocusNode? nomProduitsFocusNode;
  TextEditingController? nomProduitsTextController;
  String? Function(BuildContext, String?)? nomProduitsTextControllerValidator;
  String? _nomProduitsTextControllerValidator(
      BuildContext context, String? val) {
    if (val == null || val.isEmpty) {
      return 'Please enter the patients full name.';
    }

    return null;
  }

  // State field(s) for min widget.
  FocusNode? minFocusNode;
  TextEditingController? minTextController;
  String? Function(BuildContext, String?)? minTextControllerValidator;
  String? _minTextControllerValidator(BuildContext context, String? val) {
    if (val == null || val.isEmpty) {
      return 'Please enter an age for the patient.';
    }

    return null;
  }

  // State field(s) for max widget.
  FocusNode? maxFocusNode;
  TextEditingController? maxTextController;
  String? Function(BuildContext, String?)? maxTextControllerValidator;
  // State field(s) for nbre_produits widget.
  FocusNode? nbreProduitsFocusNode;
  TextEditingController? nbreProduitsTextController;
  late MaskTextInputFormatter nbreProduitsMask;
  String? Function(BuildContext, String?)? nbreProduitsTextControllerValidator;
  String? _nbreProduitsTextControllerValidator(
      BuildContext context, String? val) {
    if (val == null || val.isEmpty) {
      return 'Please enter the date of birth of the patient.';
    }

    return null;
  }

  // State field(s) for trier widget.
  String? trierValue;
  FormFieldController<String>? trierValueController;

  @override
  void initState(BuildContext context) {
    nomProduitsTextControllerValidator = _nomProduitsTextControllerValidator;
    minTextControllerValidator = _minTextControllerValidator;
    nbreProduitsTextControllerValidator = _nbreProduitsTextControllerValidator;
  }

  @override
  void dispose() {
    nomProduitsFocusNode?.dispose();
    nomProduitsTextController?.dispose();

    minFocusNode?.dispose();
    minTextController?.dispose();

    maxFocusNode?.dispose();
    maxTextController?.dispose();

    nbreProduitsFocusNode?.dispose();
    nbreProduitsTextController?.dispose();
  }
}
