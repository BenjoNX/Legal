#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client pour l'API Légifrance via PISTE.
Documentation de l'API Légifrance : https://piste.gouv.fr/api-dila-legifrance/

Copyright (c) 2025 Jean-Michel Tanguy
Licensed under the MIT License (see LICENSE file)

Remarques :
   Certaines parties de ce code ont été développées avec l'aide de Vibe Coding
   et d'outils d'intelligence artificielle.
"""

import os
import requests
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from api_legifrance_query_builder import LegifranceQueryBuilder

# Charger .env depuis le répertoire du script (pas le cwd)
_SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(_SCRIPT_DIR / ".env", verbose=False)


class LegifranceAPI:
    """Client pour l'API Légifrance"""

    def __init__(self, sandbox: bool = True):
        """
        Initialise le client.

        Args:
            sandbox: Utiliser l'environnement sandbox (True) ou production (False)
        """
        if sandbox:
            self.client_id = os.getenv("PISTE_SANDBOX_CLIENT_ID")
            self.client_secret = os.getenv("PISTE_SANDBOX_CLIENT_SECRET")
            self.token_url = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"
            self.base_url = "https://sandbox-api.piste.gouv.fr"
            if not self.client_id or not self.client_secret:
                raise ValueError(
                    "Les identifiants PISTE Sandbox sont manquants. "
                    "Veuillez définir PISTE_SANDBOX_CLIENT_ID et PISTE_SANDBOX_CLIENT_SECRET "
                    "dans votre fichier .env. "
                    "Consultez .env.example pour un exemple de configuration."
                )
        else:
            self.client_id = os.getenv("PISTE_CLIENT_ID")
            self.client_secret = os.getenv("PISTE_CLIENT_SECRET")
            self.token_url = "https://oauth.piste.gouv.fr/api/oauth/token"
            self.base_url = "https://api.piste.gouv.fr"
            if not self.client_id or not self.client_secret:
                raise ValueError(
                    "Les identifiants PISTE Production sont manquants. "
                    "Veuillez définir PISTE_CLIENT_ID et PISTE_CLIENT_SECRET "
                    "dans votre fichier .env. "
                    "Consultez .env.example pour un exemple de configuration."
                )

        self.api_url = f"{self.base_url}/dila/legifrance/lf-engine-app"

        # Stockage du token
        self.access_token = None
        self.token_expires_at = None

    def get_access_token(self) -> str:
        """Obtient un token d'accès via OAuth 2.0 Client Credentials."""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "openid",
        }

        try:
            response = requests.post(self.token_url, headers=headers, data=data)
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
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return headers

    def test_connection(self) -> Dict[str, Any]:
        """Teste la connexion à l'API."""
        try:
            token = self.get_access_token()
            token_preview = f"{token[:10]}...{token[-10:]}" if len(token) > 20 else "***"

            result = {
                "status": "success",
                "base_url": self.base_url,
                "api_url": self.api_url,
                "token_obtained": True,
                "token_preview": token_preview,
                "token_expires_at": (
                    self.token_expires_at.isoformat() if self.token_expires_at else None
                ),
                "message": "Token obtenu avec succès. Vérifiez votre abonnement à l'API Légifrance sur https://piste.gouv.fr/ si vous obtenez des erreurs 403.",
            }
            return result
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Échec de l'obtention du token. Vérifiez vos identifiants dans le fichier .env",
            }

    def ping(self) -> str:
        """Teste la connexion à l'endpoint de recherche avec un simple ping."""
        endpoint = f"{self.api_url}/search/ping"

        try:
            response = requests.get(endpoint, headers=self._get_api_headers())
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.HTTPError as e:
            error_msg = f"Erreur HTTP {e.response.status_code} lors du ping"
            if e.response.status_code == 403:
                error_msg += "\n⚠️ Erreur 403: Votre compte n'est probablement pas abonné à l'API Légifrance sur https://piste.gouv.fr/"
            try:
                error_details = e.response.text[:200]
                error_msg += f"\nRéponse: {error_details}"
            except Exception:
                pass
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors du ping: {e}")

    def search(
        self,
        query: Optional[str] = None,
        fond: Optional[str] = "ALL",
        field_type: str = "ALL",
        search_type: str = "TOUS_LES_MOTS_DANS_UN_CHAMP",
        code: Optional[str] = None,
        filters: Optional[Dict[str, List[str]]] = None,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
        page_number: int = 0,
        page_size: int = 10,
        sort: Optional[str] = None,
        operator: str = "ET",
        advanced_search: bool = False,
        clean: bool = True,
    ) -> Any:
        """
        Effectue une recherche dans l'API Légifrance.

        Args:
            query: Terme(s) de recherche textuelle
            fond: Fonds de recherche (ALL, CODE_ETAT, JORF, JURI, etc.)
            field_type: Type de champ (ALL, TITLE, ARTICLE, etc.)
            search_type: Type de recherche (EXACTE, TOUS_LES_MOTS_DANS_UN_CHAMP, etc.)
            code: Nom du code (ex: "Code civil") pour fonds CODE_DATE/CODE_ETAT
            filters: Filtres par valeurs textuelles
            date_start: Date de début (YYYY-MM-DD)
            date_end: Date de fin (YYYY-MM-DD)
            page_number: Numéro de la page
            page_size: Nombre de résultats par page (max 50)
            sort: Ordre de tri
            operator: Opérateur entre champs (ET, OU)
            advanced_search: Active le mode recherche avancée
            clean: Nettoyer les résultats

        Returns:
            Liste des résultats
        """
        endpoint = f"{self.api_url}/search"

        if query is None:
            raise ValueError("Le paramètre 'recherche' doit être fourni")

        queryBuilder = LegifranceQueryBuilder()

        fond = fond or "ALL"
        if fond not in queryBuilder.FONDS.values():
            raise ValueError(
                f"Fond invalide. Utilisez une des valeurs: {list(queryBuilder.FONDS.values())}"
            )
        queryBuilder.set_fond(fond)

        if search_type not in queryBuilder.TYPE_RECHERCHE.values():
            raise ValueError(
                f"Type de recherche invalide. Utilisez une des valeurs: {list(queryBuilder.TYPE_RECHERCHE.values())}"
            )

        if field_type not in queryBuilder.TYPE_CHAMP.values():
            raise ValueError(
                f"Type de champ invalide. Utilisez une des valeurs: {list(queryBuilder.TYPE_CHAMP.values())}"
            )

        critere = queryBuilder.create_criteria(query, search_type)
        queryBuilder.add_field(field_type, [critere])

        if (fond in ["CODE_ETAT", "CODE_DATE"]) and code:
            queryBuilder.add_filtre("TEXT_NOM_CODE", [code])

        if filters:
            for facette, valeurs in filters.items():
                queryBuilder.add_filtre(facette, valeurs)

        if date_start:
            queryBuilder.add_dates(date_start, date_end)

        if operator not in ["ET", "OU"]:
            raise ValueError("L'opérateur doit être 'ET' ou 'OU'")
        queryBuilder.set_operator(operator)

        if advanced_search:
            queryBuilder.set_advanced_search(True)

        queryBuilder.set_pagination(page_number, page_size)

        if sort:
            queryBuilder.set_sort(sort)

        if fond in ["JORF", "CODE_ETAT", "CODE_DATE", "LODA_DATE", "LODA_ETAT"]:
            queryBuilder.add_filtre("ARTICLE_LEGAL_STATUS", ["VIGUEUR"])

        payload = queryBuilder.build()

        try:
            response = requests.post(endpoint, headers=self._get_api_headers(), json=payload)
            response.raise_for_status()
            json_data = response.json()
            summary = self.clean(json_data) if clean else json_data
            return summary if summary else "Aucun résultat"

        except requests.exceptions.HTTPError as e:
            error_msg = f"Erreur HTTP {e.response.status_code}: {e}"

            if e.response.status_code == 403:
                error_msg += "\n\n⚠️ Erreur 403 Forbidden - Causes possibles:"
                error_msg += "\n1. Votre compte n'est pas abonné à l'API Légifrance"
                error_msg += "\n2. Les permissions nécessaires ne sont pas activées"
                error_msg += "\n3. Vérifiez votre abonnement sur https://piste.gouv.fr/"

            try:
                error_details = e.response.json()
                if isinstance(error_details, dict):
                    error_msg += f"\n\nDétails de la réponse API: {error_details}"
                    if "message" in error_details:
                        error_msg += f"\nMessage: {error_details['message']}"
                    if "error" in error_details:
                        error_msg += f"\nErreur: {error_details['error']}"
            except Exception:
                error_msg += f"\n\nRéponse brute: {e.response.text[:500]}"

            error_msg += f"\n\nEn-têtes de réponse: {dict(e.response.headers)}"

            raise Exception(f"Erreur lors de la recherche: {error_msg}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la recherche: {e}")

    def consult(self, id_: str, clean: bool = True) -> Any:
        """
        Récupère un article spécifique.

        Args:
            id_: Identifiant de l'article
            clean: Nettoyer les résultats

        Returns:
            Données de l'article
        """
        if "_" in id_:
            id_ = id_.split('_')[0]

        if id_.startswith("LEGIARTI") or id_.startswith("LEGISCTA"):
            endpoint = f"{self.api_url}/consult/getArticle"
            params = {"id": id_}
        elif id_.startswith("LEGITEXT"):
            endpoint = f"{self.api_url}/consult/legiPart"
            params = {"textId": id_, "date": date.today().isoformat()}
        elif id_.startswith("JURITEXT"):
            endpoint = f"{self.api_url}/consult/juri"
            params = {"textId": id_}
        elif id_.startswith("CNILTEXT"):
            endpoint = f"{self.api_url}/consult/cnil"
            params = {"textId": id_}
        elif id_.startswith("KALITEXT"):
            endpoint = f"{self.api_url}/consult/kaliText"
            params = {"id": id_}
        elif id_.startswith("KALIARTI"):
            endpoint = f"{self.api_url}/consult/kaliArticle"
            params = {"id": id_}
        elif id_.startswith("ACCOTEXT"):
            endpoint = f"{self.api_url}/consult/acco"
            params = {"id": id_}
        else:
            endpoint = f"{self.api_url}/consult/jorf"
            params = {"textCid": id_}

        try:
            response = requests.post(endpoint, headers=self._get_api_headers(), json=params)
            response.raise_for_status()
            api_response = self.clean(response.json()) if clean else response.json()
            return api_response

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la récupération de l'article")

    def clean(self, x, depth=0, max_depth=8):
        """Nettoie un dictionnaire ou une liste en ne conservant que les clés autorisées."""
        allowed_keys = {
            "id", "title", "text", "values", "datePublication", "startDate",
            "origine", "nature", "natureJuridiction", "solution", "numeroAffaire",
            "president", "avocats", "titre", "texte", "juridiction", "content"
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
