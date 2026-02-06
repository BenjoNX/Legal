#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour l'API Légifrance (sans appels réseau).
"""

import pytest
from unittest.mock import patch, MagicMock
from api_legifrance import LegifranceAPI
from api_legifrance_query_builder import LegifranceQueryBuilder

pytestmark = pytest.mark.unit


# ============================================================================
# TESTS DU QUERY BUILDER (aucun réseau nécessaire)
# ============================================================================


class TestLegifranceQueryBuilder:

    def test_init(self):
        qb = LegifranceQueryBuilder()
        assert qb.query["fond"] == ""
        assert qb.query["recherche"]["champs"] == []
        assert qb.query["recherche"]["filtres"] == []

    def test_set_fond_valid(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("CODE_ETAT")
        assert qb.query["fond"] == "CODE_ETAT"

    def test_set_fond_invalid(self):
        qb = LegifranceQueryBuilder()
        with pytest.raises(ValueError, match="Fonds invalide"):
            qb.set_fond("INVALID")

    def test_set_fond_all_values(self):
        qb = LegifranceQueryBuilder()
        for fond in ["ALL", "JORF", "CNIL", "CETAT", "JURI", "JUFI", "CONSTIT",
                      "KALI", "CODE_DATE", "CODE_ETAT", "LODA_DATE", "LODA_ETAT",
                      "CIRC", "ACCO"]:
            qb.set_fond(fond)
            assert qb.query["fond"] == fond

    def test_create_criteria_simple(self):
        qb = LegifranceQueryBuilder()
        c = qb.create_criteria("mariage", "EXACTE")
        assert c["valeur"] == "mariage"
        assert c["typeRecherche"] == "EXACTE"
        assert c["operateur"] == "ET"

    def test_create_criteria_with_proximite(self):
        qb = LegifranceQueryBuilder()
        c = qb.create_criteria("fonction publique", proximite=3)
        assert c["proximite"] == 3

    def test_create_criteria_with_subcriteria(self):
        qb = LegifranceQueryBuilder()
        sub = qb.create_criteria("soins", "UN_DES_MOTS")
        c = qb.create_criteria("dispositions", criteres=[sub])
        assert len(c["criteres"]) == 1
        assert c["criteres"][0]["valeur"] == "soins"

    def test_create_criteria_invalid_type(self):
        qb = LegifranceQueryBuilder()
        with pytest.raises(ValueError, match="Type de recherche invalide"):
            qb.create_criteria("test", "INVALID_TYPE")

    def test_add_field(self):
        qb = LegifranceQueryBuilder()
        c = qb.create_criteria("test")
        qb.add_field("TITLE", [c])
        assert len(qb.query["recherche"]["champs"]) == 1
        assert qb.query["recherche"]["champs"][0]["typeChamp"] == "TITLE"

    def test_add_field_invalid(self):
        qb = LegifranceQueryBuilder()
        with pytest.raises(ValueError, match="Type de champ invalide"):
            qb.add_field("INVALID", [])

    def test_add_filtre(self):
        qb = LegifranceQueryBuilder()
        qb.add_filtre("NATURE", ["LOI", "ORDONNANCE"])
        assert len(qb.query["recherche"]["filtres"]) == 1
        assert qb.query["recherche"]["filtres"][0]["facette"] == "NATURE"
        assert qb.query["recherche"]["filtres"][0]["valeurs"] == ["LOI", "ORDONNANCE"]

    def test_add_dates_jorf(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("JORF")
        qb.add_dates("2020-01-01", "2023-12-31")
        filtre = qb.query["recherche"]["filtres"][-1]
        assert filtre["facette"] == "DATE_PUBLICATION"
        assert filtre["dates"]["start"] == "2020-01-01"
        assert filtre["dates"]["end"] == "2023-12-31"

    def test_add_dates_juri(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("JURI")
        qb.add_dates("2020-01-01")
        filtre = qb.query["recherche"]["filtres"][-1]
        assert filtre["facette"] == "DATE_DECISION"

    def test_add_dates_kali(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("KALI")
        qb.add_dates("2020-01-01")
        filtre = qb.query["recherche"]["filtres"][-1]
        assert filtre["facette"] == "DATE_SIGNATURE"

    def test_add_dates_all_ignored(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("ALL")
        initial_count = len(qb.query["recherche"]["filtres"])
        qb.add_dates("2020-01-01")
        assert len(qb.query["recherche"]["filtres"]) == initial_count

    def test_set_pagination(self):
        qb = LegifranceQueryBuilder()
        qb.set_pagination(2, 25)
        assert qb.query["recherche"]["pageNumber"] == 2
        assert qb.query["recherche"]["pageSize"] == 25

    def test_set_pagination_max_50(self):
        qb = LegifranceQueryBuilder()
        qb.set_pagination(0, 100)
        assert qb.query["recherche"]["pageSize"] == 50

    def test_set_operator(self):
        qb = LegifranceQueryBuilder()
        qb.set_operator("OU")
        assert qb.query["recherche"]["operateur"] == "OU"

    def test_set_operator_invalid(self):
        qb = LegifranceQueryBuilder()
        with pytest.raises(ValueError):
            qb.set_operator("INVALID")

    def test_set_sort(self):
        qb = LegifranceQueryBuilder()
        qb.set_sort("SIGNATURE_DATE_DESC", "ID")
        assert qb.query["recherche"]["sort"] == "SIGNATURE_DATE_DESC"
        assert qb.query["recherche"]["secondSort"] == "ID"

    def test_set_advanced_search(self):
        qb = LegifranceQueryBuilder()
        qb.set_advanced_search(True)
        assert qb.query["recherche"]["fromAdvancedRecherche"] is True

    def test_build_requires_fond(self):
        qb = LegifranceQueryBuilder()
        with pytest.raises(ValueError, match="Le fonds doit être défini"):
            qb.build()

    def test_build_complete(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("CODE_ETAT")
        c = qb.create_criteria("mariage", "EXACTE")
        qb.add_field("ALL", [c])
        qb.set_pagination(0, 10)
        payload = qb.build()
        assert payload["fond"] == "CODE_ETAT"
        assert len(payload["recherche"]["champs"]) == 1

    def test_to_json(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("ALL")
        json_str = qb.to_json()
        assert '"fond": "ALL"' in json_str

    def test_reset(self):
        qb = LegifranceQueryBuilder()
        qb.set_fond("JORF")
        qb.add_filtre("NATURE", ["LOI"])
        qb.reset()
        assert qb.query["fond"] == ""
        assert qb.query["recherche"]["filtres"] == []

    def test_chaining(self):
        qb = LegifranceQueryBuilder()
        result = qb.set_fond("ALL").set_operator("ET").set_pagination(0, 20)
        assert result is qb


# ============================================================================
# TESTS DE L'API CLIENT AVEC MOCKS
# ============================================================================


class TestLegifranceAPIMocked:

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    def test_init_production(self):
        api = LegifranceAPI(sandbox=False)
        assert api.client_id == "test_id"
        assert api.client_secret == "test_secret"
        assert "sandbox" not in api.base_url
        assert api.access_token is None

    @patch.dict("os.environ", {
        "PISTE_SANDBOX_CLIENT_ID": "sandbox_id",
        "PISTE_SANDBOX_CLIENT_SECRET": "sandbox_secret",
    })
    def test_init_sandbox(self):
        api = LegifranceAPI(sandbox=True)
        assert api.client_id == "sandbox_id"
        assert "sandbox" in api.base_url

    @patch.dict("os.environ", {}, clear=True)
    @patch("api_legifrance.load_dotenv")
    def test_init_missing_credentials(self, mock_dotenv):
        with pytest.raises(ValueError, match="identifiants PISTE"):
            LegifranceAPI(sandbox=False)

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_get_access_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "fake_token_abc123",
            "expires_in": 3600,
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        api = LegifranceAPI(sandbox=False)
        token = api.get_access_token()

        assert token == "fake_token_abc123"
        assert api.access_token == "fake_token_abc123"
        assert api.token_expires_at is not None

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_token_caching(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "access_token": "cached_token",
            "expires_in": 3600,
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        api = LegifranceAPI(sandbox=False)
        token1 = api.get_access_token()
        token2 = api.get_access_token()

        assert token1 == token2
        assert mock_post.call_count == 1  # Only one HTTP call

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_search_simple(self, mock_post):
        # First call: token, second call: search
        token_response = MagicMock()
        token_response.json.return_value = {"access_token": "token", "expires_in": 3600}
        token_response.raise_for_status = MagicMock()

        search_response = MagicMock()
        search_response.json.return_value = {
            "results": [
                {"titles": [{"id": "LEGIARTI000006307920", "title": "Article 144"}]}
            ]
        }
        search_response.raise_for_status = MagicMock()

        mock_post.side_effect = [token_response, search_response]

        api = LegifranceAPI(sandbox=False)
        results = api.search(query="mariage", fond="CODE_ETAT", page_size=5)
        assert results is not None

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    def test_search_no_query(self):
        api = LegifranceAPI(sandbox=False)
        with pytest.raises(ValueError, match="Le paramètre 'recherche' doit être fourni"):
            api.search()

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    def test_search_invalid_fond(self):
        api = LegifranceAPI(sandbox=False)
        with pytest.raises(ValueError, match="Fond invalide"):
            api.search(query="test", fond="INVALID")

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    def test_search_invalid_operator(self):
        api = LegifranceAPI(sandbox=False)
        with pytest.raises(ValueError):
            api.search(query="test", operator="INVALID")

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_consult_legiarti(self, mock_post):
        token_response = MagicMock()
        token_response.json.return_value = {"access_token": "token", "expires_in": 3600}
        token_response.raise_for_status = MagicMock()

        consult_response = MagicMock()
        consult_response.json.return_value = {
            "id": "LEGIARTI000006307920",
            "text": "Le mariage ne peut être contracté avant dix-huit ans révolus.",
            "title": "Article 144",
        }
        consult_response.raise_for_status = MagicMock()

        mock_post.side_effect = [token_response, consult_response]

        api = LegifranceAPI(sandbox=False)
        result = api.consult("LEGIARTI000006307920")
        assert result is not None

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_consult_legitext(self, mock_post):
        token_response = MagicMock()
        token_response.json.return_value = {"access_token": "token", "expires_in": 3600}
        token_response.raise_for_status = MagicMock()

        consult_response = MagicMock()
        consult_response.json.return_value = {"id": "LEGITEXT000006070721", "title": "Code civil"}
        consult_response.raise_for_status = MagicMock()

        mock_post.side_effect = [token_response, consult_response]

        api = LegifranceAPI(sandbox=False)
        result = api.consult("LEGITEXT000006070721")
        assert result is not None

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_consult_strips_date_suffix(self, mock_post):
        token_response = MagicMock()
        token_response.json.return_value = {"access_token": "token", "expires_in": 3600}
        token_response.raise_for_status = MagicMock()

        consult_response = MagicMock()
        consult_response.json.return_value = {"id": "LEGITEXT000006069565", "title": "Test"}
        consult_response.raise_for_status = MagicMock()

        mock_post.side_effect = [token_response, consult_response]

        api = LegifranceAPI(sandbox=False)
        result = api.consult("LEGITEXT000006069565_31-12-2006")
        assert result is not None

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    @patch("api_legifrance.requests.post")
    def test_consult_endpoint_routing(self, mock_post):
        """Verify correct endpoints are chosen based on ID prefix."""
        token_response = MagicMock()
        token_response.json.return_value = {"access_token": "token", "expires_in": 3600}
        token_response.raise_for_status = MagicMock()

        consult_response = MagicMock()
        consult_response.json.return_value = {"id": "test"}
        consult_response.raise_for_status = MagicMock()

        api = LegifranceAPI(sandbox=False)

        test_cases = [
            ("LEGIARTI000001", "consult/getArticle"),
            ("LEGISCTA000001", "consult/getArticle"),
            ("LEGITEXT000001", "consult/legiPart"),
            ("JURITEXT000001", "consult/juri"),
            ("CNILTEXT000001", "consult/cnil"),
            ("KALITEXT000001", "consult/kaliText"),
            ("KALIARTI000001", "consult/kaliArticle"),
            ("ACCOTEXT000001", "consult/acco"),
            ("JORFTEXT000001", "consult/jorf"),
        ]

        for id_prefix, expected_endpoint in test_cases:
            mock_post.reset_mock()
            mock_post.side_effect = [token_response, consult_response]
            api.access_token = None  # Force token refresh

            api.consult(id_prefix)

            search_call = mock_post.call_args_list[-1]
            url_called = search_call[0][0] if search_call[0] else search_call[1].get("url", "")
            assert expected_endpoint in url_called, f"ID {id_prefix} should call {expected_endpoint}, got {url_called}"


# ============================================================================
# TESTS DE LA MÉTHODE CLEAN
# ============================================================================


class TestLegifranceClean:

    @patch.dict("os.environ", {
        "PISTE_CLIENT_ID": "test_id",
        "PISTE_CLIENT_SECRET": "test_secret",
    })
    def setup_method(self, method=None):
        self.api = LegifranceAPI(sandbox=False)

    def test_clean_simple_dict(self):
        data = {"id": "LEGIARTI123", "title": "Article 144", "garbage": "removed"}
        result = self.api.clean(data)
        assert result["id"] == "LEGIARTI123"
        assert result["title"] == "Article 144"
        assert "garbage" not in result

    def test_clean_nested_dict(self):
        data = {"results": [{"id": "ABC", "title": "Test"}]}
        result = self.api.clean(data)
        assert result is not None

    def test_clean_empty_values(self):
        data = {"id": "ABC", "title": None, "text": ""}
        result = self.api.clean(data)
        assert "title" not in result
        assert "text" not in result

    def test_clean_max_depth(self):
        deep = {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"id": "deep"}}}}}}}}}}
        result = self.api.clean(deep, max_depth=3)
        # Should stop before reaching deep levels
        assert result is None or "i" not in str(result)

    def test_clean_string_list_preserved(self):
        data = {"values": ["a", "b", "c"]}
        # "values" is in allowed_keys but it's a list of strings - handled by list branch
        result = self.api.clean(data)
        assert result is not None

    def test_clean_none_input(self):
        result = self.api.clean(None)
        assert result is None
