def test_simple_search(client):
    """Test search."""
    response = client.search("Object.User.Emerald.Administrator", "")
    results = response[0]["References"]
    assert len(results) > 4


def test_search_max_results(client):
    """Test search with a max_results."""
    response = client.search("Object.User.Emerald.Administrator", "", max_results=3)
    results = response[0]["References"]
    assert len(results) < 4
