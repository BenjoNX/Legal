#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour l'API JudiLibre.
Ces tests utilisent l'API sandbox et nécessitent des credentials valides dans .env

Pour exécuter les tests:
    pytest test_api_judilibre.py -v
    pytest test_api_judilibre.py -v -m integration
"""

import pytest

from api_judilibre import JudilibreAPI

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def api():
    """Crée une instance unique de JudilibreAPI pour tous les tests."""
    return JudilibreAPI(sandbox=True)


def test_init_sandbox(api):
    """Test l'initialisation du client en mode sandbox"""
    assert api.client_id is not None
    assert api.client_secret is not None
    assert "sandbox" in api.base_url


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
    """Test une recherche simple"""
    results = api.search(query="responsabilité", page_size=5)
    assert results is not None


def test_search_with_field_filter(api):
    """Test une recherche sur des champs spécifiques"""
    results = api.search(query="dommages", field=["motivations", "dispositif"], page_size=3)
    assert results is not None


def test_search_with_operator_and(api):
    """Test une recherche avec l'opérateur AND"""
    results = api.search(query="responsabilité contractuelle", operator="and", page_size=5)
    assert results is not None


def test_search_with_operator_exact(api):
    """Test une recherche exacte"""
    results = api.search(query="Cour de cassation", operator="exact", page_size=5)
    assert results is not None


def test_search_with_date_range(api):
    """Test une recherche avec intervalle de dates"""
    results = api.search(
        query="divorce", date_start="2020-01-01", date_end="2023-12-31", page_size=5
    )
    assert results is not None


def test_search_with_type_filter(api):
    """Test une recherche filtrée par type de décision"""
    results = api.search(query="contrat", type=["arret"], page_size=5)
    assert results is not None


def test_search_with_chamber_civ1(api):
    """Test une recherche dans la première chambre civile"""
    results = api.search(
        query="responsabilité contractuelle",
        chamber=["civ1"],
        page_size=5,
    )
    assert results is not None


def test_search_with_chamber_soc(api):
    """Test une recherche dans la chambre sociale"""
    results = api.search(query="licenciement", chamber=["soc"], page_size=5)
    assert results is not None


def test_search_with_jurisdiction_filter(api):
    """Test une recherche filtrée par juridiction"""
    results = api.search(query="prescription", jurisdiction=["cc"], page_size=5)
    assert results is not None


def test_search_with_publication_filter(api):
    """Test une recherche filtrée par niveau de publication"""
    results = api.search(query="cassation", publication=["b"], page_size=3)
    assert results is not None


def test_search_with_solution_filter(api):
    """Test une recherche filtrée par solution"""
    results = api.search(query="recours", solution=["rejet"], page_size=5)
    assert results is not None


def test_search_with_sort_date(api):
    """Test une recherche triée par date"""
    results = api.search(query="propriété", sort="date", order="desc", page_size=5)
    assert results is not None


def test_search_with_sort_score(api):
    """Test une recherche triée par pertinence"""
    results = api.search(query="préjudice", sort="score", order="desc", page_size=5)
    assert results is not None


def test_search_pagination(api):
    """Test la pagination des résultats"""
    results_page1 = api.search(query="contrat", page=0, page_size=3)
    results_page2 = api.search(query="contrat", page=1, page_size=3)
    assert results_page1 is not None
    assert results_page2 is not None


def test_search_with_resolve_references(api):
    """Test une recherche avec résolution des références"""
    results = api.search(query="divorce", resolve_references=True, page_size=3)
    assert results is not None


def test_search_particular_interest(api):
    """Test une recherche filtrée par intérêt particulier"""
    results = api.search(query="jurisprudence", particularInterest=True, page_size=5)
    assert results is not None


def test_search_with_multiple_filters(api):
    """Test une recherche avec plusieurs filtres combinés"""
    results = api.search(
        query="responsabilité",
        type=["arret"],
        chamber=["allciv"],
        date_start="2020-01-01",
        date_end="2023-12-31",
        sort="date",
        order="desc",
        page_size=5,
    )
    assert results is not None


def test_search_empty_query(api):
    """Test une recherche sans query"""
    results = api.search(page_size=5)
    assert results is not None


def test_search_invalid_operator(api):
    """Test qu'une erreur est levée pour un opérateur invalide"""
    with pytest.raises(ValueError, match="operator doit être"):
        api.search(query="test", operator="invalid")


def test_search_invalid_sort(api):
    """Test qu'une erreur est levée pour un tri invalide"""
    with pytest.raises(ValueError, match="sort doit être"):
        api.search(query="test", sort="invalid")


def test_search_invalid_order(api):
    """Test qu'une erreur est levée pour un ordre invalide"""
    with pytest.raises(ValueError, match="order doit être"):
        api.search(query="test", order="invalid")


def test_decision_with_resolve_references(api):
    """Test la récupération d'une décision avec références résolues"""
    search_results = api.search(query="contrat", page_size=1)
    if search_results and "results" in search_results and len(search_results["results"]) > 0:
        decision_id = search_results["results"][0].get("id")
        if decision_id:
            decision = api.consult(decision_id, resolve_references=True)
            assert decision is not None


def test_decision_with_query_highlight(api):
    """Test la récupération d'une décision avec surlignage de termes"""
    search_results = api.search(query="divorce", page_size=1)
    if search_results and "results" in search_results and len(search_results["results"]) > 0:
        decision_id = search_results["results"][0].get("id")
        if decision_id:
            decision = api.consult(decision_id, query="divorce", operator="or")
            assert decision is not None


def test_decision_empty_id(api):
    """Test qu'une erreur est levée si l'ID est vide"""
    with pytest.raises(ValueError, match="L'identifiant de la décision est obligatoire"):
        api.consult("")


def test_decision_invalid_operator(api):
    """Test qu'une erreur est levée pour un opérateur invalide dans consult"""
    with pytest.raises(ValueError, match="operator doit être"):
        api.consult("test_id", query="test", operator="invalid")


def test_taxonomy_jurisdiction(api):
    """Test la récupération de la taxonomie des juridictions"""
    jurisdictions = api.taxonomy("jurisdiction")
    assert jurisdictions is not None
    assert isinstance(jurisdictions, (dict, list))


def test_taxonomy_chamber(api):
    """Test la récupération de la taxonomie des chambres"""
    chambers = api.taxonomy("chamber")
    assert chambers is not None


def test_taxonomy_type(api):
    """Test la récupération de la taxonomie des types de décision"""
    types = api.taxonomy("type")
    assert types is not None


def test_taxonomy_publication(api):
    """Test la récupération de la taxonomie des niveaux de publication"""
    publications = api.taxonomy("publication")
    assert publications is not None


def test_taxonomy_solution(api):
    """Test la récupération de la taxonomie des solutions"""
    solutions = api.taxonomy("solution")
    assert solutions is not None


def test_taxonomy_field(api):
    """Test la récupération de la taxonomie des champs"""
    fields = api.taxonomy("field")
    assert fields is not None


def test_taxonomy_with_key(api):
    """Test la récupération d'un intitulé par clé"""
    result = api.taxonomy("jurisdiction", key="cc")
    assert result is not None


def test_taxonomy_with_value(api):
    """Test la récupération d'une clé par intitulé"""
    result = api.taxonomy("jurisdiction", value="cour de cassation")
    assert result is not None


def test_taxonomy_with_context(api):
    """Test la récupération d'une taxonomie avec contexte"""
    chambers_cc = api.taxonomy("chamber", context_value="cc")
    assert chambers_cc is not None


def test_taxonomy_key_and_value_mutually_exclusive(api):
    """Test que key et value sont mutuellement exclusifs"""
    with pytest.raises(ValueError, match="mutuellement exclusifs"):
        api.taxonomy("jurisdiction", key="cc", value="cour de cassation")


def test_taxonomy_key_requires_id(api):
    """Test que key nécessite taxonomy_id"""
    with pytest.raises(ValueError, match="taxonomy_id' est requis"):
        api.taxonomy(key="cc")


def test_taxonomy_value_requires_id(api):
    """Test que value nécessite taxonomy_id"""
    with pytest.raises(ValueError, match="taxonomy_id' est requis"):
        api.taxonomy(value="cour de cassation")


if __name__ == "__main__":
    print("Exécution des tests JudiLibre...")
    api_instance = JudilibreAPI(sandbox=True)
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
