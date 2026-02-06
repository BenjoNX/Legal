#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour l'API Légifrance.
Ces tests utilisent l'API sandbox et nécessitent des credentials valides dans .env

Pour exécuter les tests:
    pytest test_api_legifrance.py -v
    pytest test_api_legifrance.py -v -m integration
"""

import pytest

from api_legifrance import LegifranceAPI

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def api():
    """Crée une instance unique de LegifranceAPI pour tous les tests."""
    return LegifranceAPI(sandbox=True)


def test_init_sandbox(api):
    """Test l'initialisation du client en mode sandbox"""
    assert api.client_id is not None
    assert api.client_secret is not None
    assert "sandbox" in api.base_url
    assert api.access_token is None


def test_get_access_token(api):
    """Test l'obtention du token d'accès OAuth"""
    token = api.get_access_token()
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    assert api.access_token == token
    assert api.token_expires_at is not None


def test_token_caching(api):
    """Test que le token est mis en cache et réutilisé"""
    token1 = api.get_access_token()
    token2 = api.get_access_token()
    assert token1 == token2


def test_search_simple(api):
    """Test une recherche simple dans le Code civil"""
    results = api.search(query="mariage", fond="CODE_ETAT", code="Code civil", page_size=5)
    assert results is not None
    assert len(results) > 0


def test_search_with_filters(api):
    """Test une recherche avec filtres par valeurs"""
    results = api.search(
        query="travail",
        fond="JORF",
        search_type="UN_DES_MOTS",
        filters={"NATURE": ["LOI"]},
        page_size=3,
    )
    assert results is not None


def test_search_with_date_filters(api):
    """Test une recherche avec filtres par dates"""
    results = api.search(
        query="environnement",
        fond="JORF",
        date_start="2020-01-01",
        page_size=5,
    )
    assert results is not None


def test_search_pagination(api):
    """Test la pagination des résultats"""
    results_page1 = api.search(query="contrat", fond="CODE_ETAT", page_number=1, page_size=3)
    results_page2 = api.search(query="contrat", fond="CODE_ETAT", page_number=2, page_size=3)
    assert results_page1 is not None
    assert results_page2 is not None


def test_search_exact_match(api):
    """Test la recherche exacte"""
    results = api.search(query="Code civil", fond="CODE_ETAT", search_type="EXACTE", page_size=5)
    assert results is not None


def test_search_in_title(api):
    """Test la recherche dans les titres uniquement"""
    results = api.search(query="pénal", fond="CODE_ETAT", field_type="TITLE", page_size=5)
    assert results is not None


def test_search_with_date(api):
    """Test la recherche avec filtre de dates"""
    results = api.search(query="environnement", fond="JORF", page_size=5, date_end="2022-01-01")
    assert results is not None


def test_article_legitext(api):
    """Test la récupération d'un texte légal (LEGITEXT)"""
    result = api.consult("LEGITEXT000006070721")
    assert result is not None


def test_article_legiarticle(api):
    """Test la récupération d'un article de loi (LEGIARTI)"""
    result = api.consult("LEGIARTI000006307920")
    assert result is not None


def test_article_juritext(api):
    """Test la récupération d'une jurisprudence (JURITEXT)"""
    result = api.consult("JURITEXT000037999394")
    assert result is not None


def test_article_CNILTEXT(api):
    """Test la récupération d'un texte CNIL"""
    result = api.consult("CNILTEXT000017652361")
    assert result is not None


def test_article_KALITEXT(api):
    """Test la récupération d'une convention collective"""
    result = api.consult("KALITEXT000005677408")
    assert result is not None


def test_article_KALIARTI(api):
    """Test la récupération d'un article de convention collective"""
    result = api.consult("KALIARTI000005833238")
    assert result is not None


def test_article_ACCOTEXT(api):
    """Test la récupération d'un accord d'entreprise"""
    result = api.consult("ACCOTEXT000037731479")
    assert result is not None


def test_article_JORF(api):
    """Test la récupération d'un texte JORF"""
    result = api.consult("JORFTEXT000033736934")
    assert result is not None


def test_search_invalid_fond(api):
    """Test qu'une erreur est levée pour un fond invalide"""
    with pytest.raises(ValueError, match="Fond invalide"):
        api.search(query="test", fond="INVALID_FOND")


def test_search_invalid_search_type(api):
    """Test qu'une erreur est levée pour un type de recherche invalide"""
    with pytest.raises(ValueError, match="Type de recherche invalide"):
        api.search(query="test", search_type="INVALID_TYPE")


def test_search_invalid_field_type(api):
    """Test qu'une erreur est levée pour un type de champ invalide"""
    with pytest.raises(ValueError, match="Type de champ invalide"):
        api.search(query="test", field_type="INVALID_CHAMP")


def test_search_no_query(api):
    """Test qu'une erreur est levée si aucune query n'est fournie"""
    with pytest.raises(ValueError, match="Le paramètre 'recherche' doit être fourni"):
        api.search()


def test_search_invalid_operator(api):
    """Test qu'une erreur est levée pour un opérateur invalide"""
    with pytest.raises(ValueError, match="L'opérateur doit être"):
        api.search(query="test", operator="INVALID")


def test_search_with_sort(api):
    """Test la recherche avec tri personnalisé"""
    results = api.search(query="loi", fond="JORF", sort="SIGNATURE_DATE_DESC", page_size=5)
    assert results is not None


def test_search_kali_conventions(api):
    """Test la recherche dans les conventions collectives"""
    results = api.search(query="télétravail", fond="KALI", page_size=3)
    assert results is not None


def test_search_jurisprudence(api):
    """Test la recherche dans la jurisprudence"""
    results = api.search(query="responsabilité", fond="JURI", page_size=3)
    assert results is not None


if __name__ == "__main__":
    print("Exécution des tests...")
    api_instance = LegifranceAPI(sandbox=True)
    print("\nTest 1: Initialisation")
    test_init_sandbox(api_instance)
    print("✓ Réussi")
    print("\nTest 2: Obtention du token")
    test_get_access_token(api_instance)
    print("✓ Réussi")
    print("\nTest 3: Recherche simple")
    test_search_simple(api_instance)
    print("✓ Réussi")
    print("\n✓ Tous les tests de base sont réussis!")
