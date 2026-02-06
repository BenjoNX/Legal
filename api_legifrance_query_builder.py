#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de requêtes pour l'API Légifrance
Basé sur SearchRequestDTO de la documentation Swagger

Copyright (c) 2025 Jean-Michel Tanguy
Licensed under the MIT License (see LICENSE file)

Remarques :
   Certaines parties de ce code ont été développées avec l'aide de Vibe Coding
   et d'outils d'intelligence artificielle.
"""

import json
from typing import Any, Dict, List, Optional


class LegifranceQueryBuilder:
    """Générateur de requêtes pour l'API Légifrance"""

    # Constantes pour les types de recherche
    TYPE_RECHERCHE = {
        "UN_DES_MOTS": "UN_DES_MOTS",
        "EXACTE": "EXACTE",
        "TOUS_LES_MOTS_DANS_UN_CHAMP": "TOUS_LES_MOTS_DANS_UN_CHAMP",
        "AUCUN_DES_MOTS": "AUCUN_DES_MOTS",
        "AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION": "AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION",
    }

    # Constantes pour les types de champs
    TYPE_CHAMP = {
        "ALL": "ALL",
        "TITLE": "TITLE",
        "TABLE": "TABLE",
        "NOR": "NOR",
        "NUM": "NUM",
        "ADVANCED_TEXTE_ID": "ADVANCED_TEXTE_ID",
        "NUM_DELIB": "NUM_DELIB",
        "NUM_DEC": "NUM_DEC",
        "NUM_ARTICLE": "NUM_ARTICLE",
        "ARTICLE": "ARTICLE",
        "MINISTERE": "MINISTERE",
        "VISA": "VISA",
        "NOTICE": "NOTICE",
        "VISA_NOTICE": "VISA_NOTICE",
        "TRAVAUX_PREP": "TRAVAUX_PREP",
        "SIGNATURE": "SIGNATURE",
        "NOTA": "NOTA",
        "NUM_AFFAIRE": "NUM_AFFAIRE",
        "ABSTRATS": "ABSTRATS",
        "RESUMES": "RESUMES",
        "TEXTE": "TEXTE",
        "ECLI": "ECLI",
        "NUM_LOI_DEF": "NUM_LOI_DEF",
        "TYPE_DECISION": "TYPE_DECISION",
        "NUMERO_INTERNE": "NUMERO_INTERNE",
        "REF_PUBLI": "REF_PUBLI",
        "RESUME_CIRC": "RESUME_CIRC",
        "TEXTE_REF": "TEXTE_REF",
        "TITRE_LOI_DEF": "TITRE_LOI_DEF",
        "RAISON_SOCIALE": "RAISON_SOCIALE",
        "MOTS_CLES": "MOTS_CLES",
        "IDCC": "IDCC",
    }

    # Constantes pour les fonds
    FONDS = {
        "ALL": "ALL",
        "JORF": "JORF",
        "CNIL": "CNIL",
        "CETAT": "CETAT",
        "JURI": "JURI",
        "JUFI": "JUFI",
        "CONSTIT": "CONSTIT",
        "KALI": "KALI",
        "CODE_DATE": "CODE_DATE",
        "CODE_ETAT": "CODE_ETAT",
        "LODA_DATE": "LODA_DATE",
        "LODA_ETAT": "LODA_ETAT",
        "CIRC": "CIRC",
        "ACCO": "ACCO",
    }

    def __init__(self):
        self.query = {
            "fond": "",
            "recherche": {
                "champs": [],
                "filtres": [],
                "pageNumber": 1,
                "pageSize": 50,
                "operateur": "ET",
                "sort": "PERTINENCE",
                "secondSort": "DATE_DESC",
                "typePagination": "DEFAUT",
            },
        }

    def set_fond(self, fond: str) -> "LegifranceQueryBuilder":
        """Définit le fonds de recherche."""
        if fond not in self.FONDS.values():
            raise ValueError(
                f"Fonds invalide. Utilisez une des valeurs: {list(self.FONDS.values())}"
            )
        self.query["fond"] = fond
        return self

    def add_field(
        self, type_champ: str, criteres: List[Dict], operateur: str = "ET"
    ) -> "LegifranceQueryBuilder":
        """Ajoute un champ de recherche."""
        if type_champ not in self.TYPE_CHAMP.values():
            raise ValueError(
                f"Type de champ invalide. Utilisez une des valeurs: {list(self.TYPE_CHAMP.values())}"
            )

        champ = {"typeChamp": type_champ, "criteres": criteres, "operateur": operateur}
        self.query["recherche"]["champs"].append(champ)
        return self

    def create_criteria(
        self,
        valeur: str,
        type_recherche: str = "TOUS_LES_MOTS_DANS_UN_CHAMP",
        operateur: str = "ET",
        proximite: Optional[int] = None,
        criteres: Optional[List[Dict]] = None,
    ) -> Dict:
        """Crée un critère de recherche."""
        if type_recherche not in self.TYPE_RECHERCHE.values():
            raise ValueError(
                f"Type de recherche invalide. Utilisez une des valeurs: {list(self.TYPE_RECHERCHE.values())}"
            )

        critere: Dict[str, Any] = {
            "valeur": valeur,
            "typeRecherche": type_recherche,
            "operateur": operateur,
        }

        if proximite is not None:
            critere["proximite"] = proximite

        if criteres is not None:
            critere["criteres"] = criteres

        return critere

    def add_filtre(self, facette: str, valeurs: List[str]) -> "LegifranceQueryBuilder":
        """Ajoute un filtre par valeurs."""
        filtre = {"facette": facette, "valeurs": valeurs}
        self.query["recherche"]["filtres"].append(filtre)
        return self

    def add_dates(
        self, start_date: str, end_date: Optional[str] = None
    ) -> "LegifranceQueryBuilder":
        """Ajoute un filtre par période de dates."""
        fond = self.query.get("fond", "")
        if fond in ["JORF", "LODA_DATE", "LODA_ETAT"]:
            facette_principale = "DATE_PUBLICATION"
        elif fond in ["CETAT", "JURI", "JUFI", "CONSTIT"]:
            facette_principale = "DATE_DECISION"
        elif fond in ["KALI", "CIRC", "ACCO"]:
            facette_principale = "DATE_SIGNATURE"
        else:
            return self

        if end_date is not None:
            filtre = {"facette": facette_principale, "dates": {"start": start_date, "end": end_date}}
        else:
            filtre = {"facette": facette_principale, "dates": {"start": start_date}}

        self.query["recherche"]["filtres"].append(filtre)
        return self

    def set_pagination(
        self, page_number: int = 0, page_size: int = 10, type_pagination: str = "DEFAUT"
    ) -> "LegifranceQueryBuilder":
        """Configure la pagination des résultats."""
        self.query["recherche"]["pageNumber"] = page_number
        self.query["recherche"]["pageSize"] = min(page_size, 50)
        self.query["recherche"]["typePagination"] = type_pagination
        return self

    def set_operator(self, operator: str) -> "LegifranceQueryBuilder":
        """Définit l'opérateur global entre les champs de recherche."""
        if operator not in ["ET", "OU"]:
            raise ValueError("L'opérateur doit être 'ET' ou 'OU'")
        self.query["recherche"]["operateur"] = operator
        return self

    def set_sort(self, sort: str, second_sort: Optional[str] = None) -> "LegifranceQueryBuilder":
        """Configure le tri des résultats."""
        self.query["recherche"]["sort"] = sort
        if second_sort:
            self.query["recherche"]["secondSort"] = second_sort
        return self

    def set_advanced_search(self, advanced: bool = True) -> "LegifranceQueryBuilder":
        """Active ou désactive le mode de recherche avancée."""
        self.query["recherche"]["fromAdvancedRecherche"] = advanced
        return self

    def build(self) -> Dict:
        """Construit et retourne la requête finale."""
        if not self.query["fond"]:
            raise ValueError("Le fonds doit être défini")
        return self.query.copy()

    def to_json(self, indent: int = 2) -> str:
        """Retourne la requête au format JSON."""
        return json.dumps(self.build(), indent=indent, ensure_ascii=False)

    def reset(self) -> "LegifranceQueryBuilder":
        """Remet à zéro le générateur de requêtes."""
        self.__init__()
        return self
