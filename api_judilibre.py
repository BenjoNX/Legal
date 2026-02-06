#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client pour l'API JudiLibre via PISTE.
Documentation de l'API JudiLibre : https://piste.gouv.fr/api-judilibre/

Copyright (c) 2025 Jean-Michel Tanguy
Licensed under the MIT License (see LICENSE file)

Remarques :
   Certaines parties de ce code ont été développées avec l'aide de Vibe Coding
   et d'outils d'intelligence artificielle.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv


class JudilibreAPI:
    """Client OAuth pour l'API JudiLibre"""

    def __init__(self, sandbox: bool = True):
        """
        Initialise le client OAuth.

        Args:
            sandbox: Utiliser l'environnement sandbox (True) ou production (False)
        """
        load_dotenv(verbose=False)
        if sandbox:
            self.client_id = os.getenv("PISTE_SANDBOX_CLIENT_ID")
            self.client_secret = os.getenv("PISTE_SANDBOX_CLIENT_SECRET")
            self.token_url = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"
            self.base_url = "https://sandbox-api.piste.gouv.fr"
        else:
            self.client_id = os.getenv("PISTE_CLIENT_ID")
            self.client_secret = os.getenv("PISTE_CLIENT_SECRET")
            self.token_url = "https://oauth.piste.gouv.fr/api/oauth/token"
            self.base_url = "https://api.piste.gouv.fr"

        self.api_url = f"{self.base_url}/cassation/judilibre/v1.0"

        # Stockage du token
        self.access_token = None
        self.token_expires_at = None

    def get_access_token(self) -> str:
        """Obtient un token d'accès via OAuth 2.0 Client Credentials."""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        data = {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": self.token_url.replace("https://", "").split("/")[0],
            "Connection": "Keep-Alive",
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "openid",
        }

        try:
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data["access_token"]

            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)

            return self.access_token

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de l'obtention du token: {e}")

    def _get_api_headers(self) -> Dict[str, str]:
        """Génère les en-têtes pour les appels API."""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
        }

    def search(
        self,
        query: Optional[str] = None,
        field: Optional[List[str]] = None,
        operator: str = "and",
        type: Optional[List[str]] = None,
        theme: Optional[List[str]] = None,
        chamber: Optional[List[str]] = None,
        formation: Optional[List[str]] = None,
        jurisdiction: Optional[List[str]] = ["cc", "ca", "tj", "tcom"],
        location: Optional[List[str]] = None,
        publication: Optional[List[str]] = None,
        solution: Optional[List[str]] = None,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
        sort: str = "scorepub",
        order: str = "desc",
        page_size: int = 50,
        page: int = 0,
        resolve_references: bool = True,
        withFileOfType: Optional[List[str]] = None,
        particularInterest: bool = False,
    ) -> Any:
        """
        Effectue une recherche dans la base JudiLibre.

        Args:
            query: Chaîne de recherche
            field: Liste des champs ciblés
            operator: Opérateur logique (or, and, exact)
            type: Types de décision (arret, qpc, ordonnance, saisie)
            theme: Matières juridiques
            chamber: Chambres (pl, mi, civ1, civ2, civ3, comm, soc, cr, etc.)
            formation: Formations
            jurisdiction: Juridictions (cc, ca, tj, tcom)
            location: Codes de sièges de juridiction
            publication: Niveaux de publication
            solution: Types de solution
            date_start: Date début ISO (ex: 2023-01-15)
            date_end: Date fin ISO (ex: 2023-12-15)
            sort: Tri (scorepub, score, date)
            order: Ordre (desc, asc)
            page_size: Résultats par page (max 50)
            page: Numéro de page
            resolve_references: Résoudre les références
            withFileOfType: Types de documents associés
            particularInterest: Filtrer par intérêt particulier

        Returns:
            Résultats de la recherche paginés
        """
        if page_size > 50:
            page_size = 50

        if operator not in ["or", "and", "exact"]:
            raise ValueError("operator doit être 'or', 'and' ou 'exact'")

        if sort not in ["score", "scorepub", "date"]:
            raise ValueError("sort doit être 'score', 'scorepub' ou 'date'")

        if order not in ["asc", "desc"]:
            raise ValueError("order doit être 'asc' ou 'desc'")

        endpoint = f"{self.api_url}/search"

        params = {
            "operator": operator,
            "sort": sort,
            "order": order,
            "page_size": page_size,
            "page": page,
            "resolve_references": "true" if resolve_references else "false",
            "particularInterest": "true" if particularInterest else "false",
        }

        if query:
            params["query"] = query
        if field:
            params["field"] = field
        if type:
            params["type"] = type
        if theme:
            params["theme"] = theme
        if chamber:
            params["chamber"] = chamber
        if formation:
            params["formation"] = formation
        if jurisdiction:
            params["jurisdiction"] = jurisdiction
        if location:
            params["location"] = location
        if publication:
            params["publication"] = publication
        if solution:
            params["solution"] = solution
        if date_start:
            params["date_start"] = date_start
        if date_end:
            params["date_end"] = date_end
        if withFileOfType:
            params["withFileOfType"] = withFileOfType

        try:
            response = requests.get(endpoint, headers=self._get_api_headers(), params=params)
            response.raise_for_status()
            json_data = response.json()
            return self.clean(json_data)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la recherche JudiLibre")
        except Exception as e:
            raise Exception(f"Erreur inattendue lors de la recherche")

    def consult(
        self,
        decision_id: str,
        resolve_references: bool = False,
        query: Optional[str] = None,
        operator: str = "and",
    ) -> Any:
        """
        Récupère le contenu intégral d'une décision.

        Args:
            decision_id: Identifiant de la décision
            resolve_references: Résoudre les références
            query: Termes à surligner
            operator: Opérateur (or, and, exact)

        Returns:
            Décision complète
        """
        if not decision_id or not decision_id.strip():
            raise ValueError(
                "L'identifiant de la décision est obligatoire et ne peut pas être vide"
            )

        if operator not in ["or", "and", "exact"]:
            raise ValueError("operator doit être 'or', 'and' ou 'exact'")

        endpoint = f"{self.api_url}/decision"
        params = {
            "id": decision_id,
            "resolve_references": "true" if resolve_references else "false",
        }

        if query:
            params["query"] = query
            params["operator"] = operator

        try:
            response = requests.get(endpoint, headers=self._get_api_headers(), params=params)
            response.raise_for_status()
            json_data = response.json()
            return self.clean(json_data)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la récupération de la décision '{decision_id}'")
        except Exception as e:
            raise Exception(f"Erreur inattendue lors de la récupération de la décision")

    def taxonomy(
        self,
        taxonomy_id: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        context_value: Optional[str] = None,
    ) -> Any:
        """
        Récupère les listes des termes employés par le processus de recherche.

        Args:
            taxonomy_id: Type de taxonomie (jurisdiction, chamber, solution, theme, location, etc.)
            key: Clé pour obtenir l'intitulé complet
            value: Intitulé pour obtenir la clé
            context_value: Contexte (cc, ca, tj)

        Returns:
            Données de taxonomie
        """
        endpoint = f"{self.api_url}/taxonomy"
        params = {}

        if key and value:
            raise ValueError("Les paramètres 'key' et 'value' sont mutuellement exclusifs")

        if (key or value) and not taxonomy_id:
            raise ValueError("Le paramètre 'taxonomy_id' est requis avec 'key' ou 'value'")

        if taxonomy_id:
            params["id"] = taxonomy_id

        if key:
            params["key"] = key

        if value:
            params["value"] = value

        if context_value:
            params["context_value"] = context_value

        if not params:
            TAXONOMY_DESCRIPTIONS = {
                "type": "Types de décision (arrêt, ordonnance, QPC, etc.)",
                "jurisdiction": "Juridictions (Cour de cassation, cours d'appel, tribunaux, etc.)",
                "chamber": "Chambres de la Cour de cassation (civile, sociale, criminelle, etc.)",
                "formation": "Formations des juridictions",
                "publication": "Niveaux de publication (bulletin, rapport, lettre, etc.)",
                "theme": "Matières juridiques (nomenclature Cour de cassation)",
                "solution": "Types de solution (cassation, rejet, annulation, etc.)",
                "field": "Champs et zones de contenu (exposé, moyens, motivations, dispositif, etc.)",
                "zones": "Zones de contenu des décisions",
                "location": "Codes des sièges de juridiction (cours d'appel, tribunaux)",
                "filetype": "Types de documents associés (rapports, avis, communiqués, etc.)",
            }
            return TAXONOMY_DESCRIPTIONS

        try:
            response = requests.get(endpoint, headers=self._get_api_headers(), params=params)
            response.raise_for_status()
            json_data = response.json()
            result = json_data.get("result", json_data)
            return result

        except requests.exceptions.RequestException as e:
            if taxonomy_id:
                raise Exception(
                    f"Erreur lors de la récupération de la taxonomie '{taxonomy_id}': {e}"
                )
            else:
                raise Exception(f"Erreur lors de la récupération des taxonomies: {e}")

    def clean(self, x, depth=0, max_depth=5):
        """Nettoie un dictionnaire ou une liste en ne conservant que les clés autorisées."""
        allowed_keys = {
            "text", "id", "jurisdiction", "chamber", "formation", "type", "theme",
            "publication", "decision_date", "solution", "jurisdiction", "score"
        }

        if depth >= max_depth:
            return None

        if isinstance(x, dict):
            cleaned = {}
            for k, v in x.items():
                if v:
                    if k in allowed_keys and not isinstance(v, (dict, list)):
                        cleaned[k] = v
                    elif isinstance(v, (dict, list)):
                        cleaned_value = self.clean(v, depth + 1, max_depth)
                        if cleaned_value:
                            cleaned[k] = cleaned_value
            return cleaned if cleaned else None

        if isinstance(x, list):
            if x and all(isinstance(item, str) for item in x):
                return x
            l = [cleaned_v for v in x if v and (cleaned_v := self.clean(v, depth + 1, max_depth)) is not None]
            return l if l else None

        return x
